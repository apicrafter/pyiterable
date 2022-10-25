# -*- coding: utf-8 -*-
import logging

from .bsonf import BSONSource
from .csv import CSVSource
from .json import JSONSource
from .jsonl import JSONLinesSource
from .xls import XLSSource
from .xlsx import XLSXSource
from .xml import XMLSource
from .zipped import ZIPSourceWrapper
from .zipxml import ZIPXMLSource


def validate_options(options, required=[]):
    for k in required:
        if k not in options.keys():
            raise ValueError
    return True


MAP_REQUIRED_OPTIONS = {'zipxml': ['tagname', ], 'xml': ['tagname', ], 'xls': ['keys', ],
                        'xlsx': ['keys', ], 'csv': ['delimiter', ]}

FILEEXT_TO_SOURCETYPE = {'xml': 'xml', 'xls': 'xls', 'xlsx': 'xlsx', 'csv': 'csv', 'jsonl': 'jsonl', 'bson': 'bson',
                         'json': 'json'}


def get_source_from_file(filename, stype=None, options=None):
    logging.info('Getting source from extractor results, filename: %s stype: %s, options: %s' % (
    str(filename), str(stype), str(options)))
    ext = filename.rsplit('.', 1)[-1].lower()
    if not stype:
        if ext in FILEEXT_TO_SOURCETYPE.keys():
            stype = FILEEXT_TO_SOURCETYPE[ext]
    if stype == 'zipxml':
        validate_options(options, ['tagname', ])
        logging.debug('Use ZIP XML source with filename %s, tag %s' % (filename, options['tagname']))
        return ZIPXMLSource(filename=filename, tagname=options['tagname'])
    elif stype == 'xml':
        validate_options(options, ['tagname', ])
        logging.debug('Use XML source with filename %s, tag %s' % (filename, options['tagname']))
        return XMLSource(filename=filename, tagname=options['tagname'])
    elif stype == 'json':
        #        validate_options(options, ['tagname', ])
        logging.debug('Use JSON source with filename %s, tag %s' % (
        filename, options['tagname'] if 'tagname' in options.keys() else 'None'))
        return JSONSource(filename=filename, tagname=options['tagname'] if 'tagname' in options.keys() else None)
    elif stype == 'xls':
        validate_options(options, ['keys', ])
        if 'keys' in options.keys() and options['keys']:
            keys = options['keys'].split(',')
        else:
            keys = None
        logging.debug('Use XLS source with filename %s, keys %s' % (filename, keys))
        return XLSSource(filename=filename, keys=keys,
                         start_line=options['start_line'] if 'start_line' in options.keys() else 0)
    elif stype == 'xlsx':
        validate_options(options, ['keys', ])
        if 'keys' in options.keys() and options['keys']:
            keys = options['keys'].split(',')
        else:
            keys = None
        logging.debug('Use XLSX source with filename %s, keys %s' % (filename, keys))
        return XLSXSource(filename=filename, keys=keys,
                          start_line=options['start_line'] if 'start_line' in options.keys() else 0)
    elif stype == 'csv':
        keys = options['keys'].split(',') if 'keys' in options.keys() else None
        delimiter = options['delimiter'] if 'delimiter' in options.keys() else None
        encoding = options['encoding'] if 'encoding' in options.keys() else None
        logging.debug('Use CSV source with filename %s, keys %s, delimiter "%s", encoding %s' % (
        filename, keys, delimiter, encoding))
        return CSVSource(filename=filename, keys=keys,
                         delimiter=delimiter,
                         encoding=encoding)
    elif stype == 'bson':
        logging.debug('Use BSON source with filename %s' % (filename))
        return BSONSource(filename=filename)
    elif stype == 'jsonl':
        logging.debug('Use JSON lines source with filename %s' % (filename))
        return JSONLinesSource(filename=filename)
    else:
        raise NotImplementedError
