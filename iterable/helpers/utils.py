from __future__ import annotations
import typing
from itertools import takewhile, repeat
from collections import defaultdict
from collections import OrderedDict
import chardet
from statistics import mean

from ..base import BaseIterable

DEFAULT_DELIMITERS = [',', ';', '\t', '|']

def rowincount(filename:str=None, fileobj=None):
    """Count number of rows by filename or file object"""
    totals = 0
    if filename is not None:
        f = open(filename, 'rb')
        bufgen = takewhile(lambda x: x, (f.read(1024*1024) for _ in repeat(None)))
        totals = sum(buf.count(b'\n') for buf in bufgen)
        f.close()        
    elif fileobj is not None:
        f = fileobj
        bufgen = takewhile(lambda x: x, (f.read(1024*1024) for _ in repeat(None)))
        totals = sum(buf.count(b'\n') for buf in bufgen)                
    else:
        raise ValueError('Filename or fileobj should not be None')
    return totals


def detect_encoding_raw(filename:str = None, stream:typing.IO=None, limit:int=1000000) -> str:
    """Detect file or file object encoding reading 1MB data by default and using chardet"""    
    if filename is not None:
        f = open(filename, 'rb')
        chunk = f.read(limit)
        f.close()
        return chardet.detect(chunk)
    else:
        return chardet.detect(stream.read(limit))

def detect_delimiter(filename:str = None, stream:typing.IO=None, encoding:str ='utf8', limit:int=20, threshold=0.6) -> str:
    """Detect CSV file or file object delimiter with known encoding and limit with number of lines"""
    lines = []
    char_map = {}
    if filename:
        f = open(filename, 'r', encoding=encoding)
        for n in range(0, limit):
            line = f.readline().strip()
            if len(line) > 0:
                lines.append(line)
        f.close()
    else:
        for n in range(0, limit):
            lines.append(stream.readline())

    for char in DEFAULT_DELIMITERS:
        char_map[char] = []
    
    for line in lines:
        for char in DEFAULT_DELIMITERS:
            char_map[char].append(line.count(char))
    
    candidates = {}
    for char in char_map:        
        if min(char_map[char]) != 0 and mean(char_map[char]) / max(char_map[char]) > threshold:
            candidates[char] = max(char_map[char])
            
    delimiter = max(candidates, key=candidates.get)
    return delimiter

def get_dict_value(d:dict, keys: list[str]):
    """Return value of selected dict key"""
    out = []
    if d is None:
        return out
#    keys = key.split('.')
    if len(keys) == 1:
        if type(d) == type({}) or isinstance(d, OrderedDict):
            if keys[0] in d.keys():
                out.append(d[keys[0]])
        else:
            for r in d:
                if r and keys[0] in r.keys():
                    out.append(r[keys[0]])
#        return out
    else:
        if type(d) == type({}) or isinstance(d, OrderedDict):
            if keys[0] in d.keys():
                out.extend(get_dict_value(d[keys[0]], keys[1:]))
        else:
            for r in d:
                if keys[0] in r.keys():
                    out.extend(get_dict_value(r[keys[0]], keys[1:]))
    return out


def strip_dict_fields(record, fields, startkey=0):
    """Remove selected dict fields"""
    keys = record.keys()
    localf = []
    for field in fields:
        if len(field) > startkey:
            localf.append(field[startkey])
    for k in list(keys):
        if k not in localf:
            del record[k]

    if len(k) > 0:
        for k in record.keys():
            if type(record[k]) == type({}):
                record[k] = strip_dict_fields(record[k], fields, startkey + 1)
    return record


def dict_generator(indict:dict, pre:list=None):
    """Processes python dictionary and return list of key values
    :param indict
    :param pre
    :return generator"""
    pre = pre[:] if pre else []
    if isinstance(indict, dict):
        for key, value in list(indict.items()):
            if key == "_id":
                continue
            if isinstance(value, dict):
                #                print 'dgen', value, key, pre
                for d in dict_generator(value, pre + [key]):
                    yield d
            elif isinstance(value, list) or isinstance(value, tuple):
                for v in value:
                    if isinstance(v, dict):
                        #                print 'dgen', value, key, pre
                        for d in dict_generator(v, pre + [key]):
                            yield d
#                    for d in dict_generator(v, [key] + pre):
#                        yield d
            else:
                yield pre + [key, value]
    else:
        yield indict


def guess_int_size(value:int):
    """Guess integer size"""
    if value < 255:
        return 'uint8'
    if value < 65535:
        return 'uint16'
    return 'uint32'

def guess_datatype(s:str, qd:Object) -> dict:
    """Guesses type of data by string provided
    :param s
    :param qd
    :return datatype"""
    attrs = {'base' : 'str'}
#    s = unicode(s)
    if s is None:
       return {'base' : 'empty'}
    if type(s) == type(1):
        return {'base' : 'int'}
    if type(s) == type(1.0):
        return {'base' : 'float'}
    elif type(s) != type(''):
#        print((type(s)))
        return {'base' : 'typed'}
#    s = s.decode('utf8', 'ignore')
    if s.isdigit():
        if s[0] == 0:
            attrs = {'base' : 'numstr'}
        else:
            attrs = {'base' : 'int', 'subtype' : guess_int_size(int(s))}
    else:
        try:
            i = float(s)
            attrs = {'base' : 'float'}
            return attrs
        except ValueError:
            pass
        if qd:
            is_date = False
            res = qd.match(s)
            if res:
                attrs = {'base': 'date', 'pat': res['pattern']}
                is_date = True
            if not is_date:
                if len(s.strip()) == 0:
                    attrs = {'base' : 'empty'}
    return attrs


def count_file_newlines(filename:str = None, stream:typing.IO = None):
    """Counts number of lines in file"""
    def _make_gen(reader):
        while True:
            b = reader(2 ** 16)
            if not b: break
            yield b

    if fname:
        with open(fname, "rb") as f:
            count = sum(buf.count(b"\n") for buf in _make_gen(f.raw.read))
    else:
        sum(stream.count(b"\n") for buf in _make_gen(f.raw.read))
    return count


def get_dict_keys(iterable:list[dict], limit:int=1000) -> list[str]:
    """Returns dictionary keys"""
    n = 0
    keys = []
    for item in iterable:
        if limit and n > limit:
            break
        n += 1
        dk = dict_generator(item)
        for i in dk:
            k = ".".join(i[:-1])
            if k not in keys:
                keys.append(k)
    return keys

def get_iterable_keys(iterable:BaseIterable, limit:int=1000) -> list[str]:
    """Returns BaseIterable object keys"""
    n = 0
    keys = []
    for item in iterable:
        if limit and n > limit:
            break
        n += 1
        dk = dict_generator(item)
        for i in dk:
            k = ".".join(i[:-1])
            if k not in keys:
                keys.append(k)
    return keys

def is_flat_object(item:object) -> bool:
    """Measures if object is flat"""
    for k, v in item.items():
        if isinstance(v, tuple) or isinstance(v, list):
            return False
        elif isinstance(v, dict):
            if not _is_flat(v): return False
    return True

# -*- coding: utf-8 -*-

def get_dict_value(adict:dict, key:str, prefix:list=None):
    if prefix is None:
        prefix = key.split('.')
    if len(prefix) == 1:
        return adict[prefix[0]]
    else:
        return get_dict_value(adict[prefix[0]], key, prefix=prefix[1:])

def get_dict_value_deep(adict:dict, key:str, prefix:list = None, as_array:bool = False, splitter:str = '.'):
    """Used to get value from hierarhic dicts in python with params with dots as splitter"""
    if prefix is None:
        prefix = key.split(splitter)
    if len(prefix) == 1:
        if type(adict) == type({}):
            if not prefix[0] in adict.keys():
                return None
            if as_array:
                return [adict[prefix[0]], ]
            return adict[prefix[0]]
        elif type(adict) == type([]):
            if as_array:
                result = []
                for v in adict:
                    if prefix[0] in v.keys():
                        result.append(v[prefix[0]])
                return result
            else:
                if len(adict) > 0 and prefix[0] in adict[0].keys():
                    return adict[0][prefix[0]]
        return None
    else:
        if type(adict) == type({}):
            if prefix[0] in adict.keys():
                return get_dict_value_deep(adict[prefix[0]], key, prefix=prefix[1:], as_array=as_array)
        elif type(adict) == type([]):
            if as_array:
                result = []
                for v in adict:
                    res = get_dict_value_deep(v[prefix[0]], key, prefix=prefix[1:], as_array=as_array)
                    if res:
                        result.extend(res)
                return result
            else:
                return get_dict_value_deep(adict[0][prefix[0]], key, prefix=prefix[1:], as_array=as_array)
        return None


def make_flat(item):
    result = {}
    for k, v in item.items():
        if isinstance(v, tuple) or isinstance(v, list) or isinstance(v, dict):
            result[k] = str(v)
        result[k] = v
    return result
