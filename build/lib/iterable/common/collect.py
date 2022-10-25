import logging
import os
import shutil
import tempfile
from urllib import parse

import requests
from bs4 import BeautifulSoup

REQUEST_HEADER = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Mobile Safari/537.36'}
DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'
DEFAULT_CHUNK_SIZE = 4096
DEFAULT_TIMEOUT = 300


def get_file(url, filename, aria2=False, aria2path=None, timeout=DEFAULT_TIMEOUT):
    logging.info('Retrieving %s from %s' % (filename, url))
    page = requests.get(url, headers=REQUEST_HEADER, stream=True, verify=False, timeout=timeout)
    if not aria2:
        f = open(filename, 'wb')
        total = 0
        chunk = 0
        for line in page.iter_content(chunk_size=DEFAULT_CHUNK_SIZE):
            chunk += 1
            if line:
                f.write(line)
            total += len(line)
            if chunk % 1000 == 0:
                logging.debug('File %s to size %d' % (filename, total))
        f.close()
    else:
        dirpath = os.path.dirname(filename)
        basename = os.path.basename(filename)
        if len(dirpath) > 0:
            s = "%s --retry-wait=10 -d %s --out=%s %s" % (aria2path, dirpath, basename, url)
        else:
            s = "%s --retry-wait=10 --out=%s %s" % (aria2path, basename, url)
        logging.info('Aria2 command line: %s' % (s))
        os.system(s)
    return filename


def is_absolute_url(url):
    return bool(parse.urlparse(url).netloc)


def get_file_by_pattern(current_path, temp_path, url, url_data_prefix, filename, file_type=None, aria2=False,
                        aria2path=None, force=True, timeout=DEFAULT_TIMEOUT):
    """Collects specific file by it's url pattern and saves it as filename"""
    shift = len(file_type) + 1
    user_agent = DEFAULT_USER_AGENT
    session = requests.Session()
    session.headers.update(
        {'User-Agent': user_agent})
    html_data = session.get(url, verify=False, timeout=timeout).content
    soup = BeautifulSoup(html_data, features='lxml')
    data_url = None
    for u in soup.find_all('a'):
        href = u.get('href')
        if href and href.find(url_data_prefix) > -1:
            if file_type is not None and href[-shift:] == '.%s' % (file_type):
                data_url = u.get('href')
                if not is_absolute_url(data_url):
                    data_url = parse.urljoin(url, data_url)
                break
    if not data_url:
        logging.info('Dataset url not found')
        return None
    else:
        if not os.path.exists(filename) or force:
            get_file(data_url, filename, aria2=aria2, aria2path=aria2path, timeout=timeout)
            logging.info('Downloaded %s to %s' % (data_url, filename))
        else:
            logging.info('File %s already downloaded' % (filename))

        return filename


def get_file_by_name(current_path, temp_path, url, name=None, prefix=None, file_prefix=None, file_type=None,
                     aria2=False, aria2path=None, force=True):
    """Collects specific file by it's name"""
    user_agent = DEFAULT_USER_AGENT
    session = requests.Session()
    session.headers.update(
        {'User-Agent': user_agent})
    html_data = session.get(url, verify=False).content
    soup = BeautifulSoup(html_data, features='lxml')
    data_url = None
    for u in soup.find_all('a'):
        if name:
            if u.text == name:
                data_url = u.get('href')
                break
        elif prefix:
            if u.text.find(prefix) > -1:
                data_url = u.get('href')
                break
    if not data_url:
        logging.info('Dataset url not found')
    else:
        if not is_absolute_url(data_url):
            data_url = parse.urljoin(url, data_url)
        filename = data_url.rsplit('/', 1)[-1]
        logging.info('Downloading %s to %s' % (data_url, filename))
        fd, temp_filepath = tempfile.mkstemp()
        os.close(fd)
        #        temp_filepath = os.path.join(temp_path, filename)
        current_filepath = os.path.join(current_path, "%s_current.%s" % (file_prefix, file_type))
        logging.info('Temp %s' % (temp_filepath))
        if not os.path.exists(temp_filepath) or force:
            get_file(data_url, temp_filepath, aria2=aria2, aria2path=aria2path)
            logging.info('Downloaded %s to %s' % (data_url, filename))
        else:
            logging.info('File %s already downloaded' % (filename))
        #            if not os.path.exists(current_filepath):
        shutil.move(temp_filepath, current_filepath)
        logging.debug('File %s moved to current' % (filename))
