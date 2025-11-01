import chardet
from ..datatypes.avro import AVROIterable
from ..datatypes.bsonf import BSONIterable
from ..datatypes.csv import CSVIterable
from ..datatypes.orc import ORCIterable
from ..datatypes.parquet import ParquetIterable
from ..datatypes.picklef import PickleIterable
from ..datatypes.json import JSONIterable
from ..datatypes.jsonl import JSONLinesIterable
from ..datatypes.xls import XLSIterable
from ..datatypes.xlsx import XLSXIterable
from ..datatypes.xml import XMLIterable
from ..engines.duckdb import DuckDBIterable

from ..codecs.bz2codec import BZIP2Codec
from ..codecs.gzipcodec import GZIPCodec
from ..codecs.lzmacodec import LZMACodec
from ..codecs.lz4codec import LZ4Codec
from ..codecs.zipcodec import ZIPCodec
from ..codecs.brotlicodec import BrotliCodec
from ..codecs.zstdcodec import ZSTDCodec


DATATYPES = [AVROIterable, BSONIterable, CSVIterable, ORCIterable, 
             ParquetIterable, PickleIterable, JSONIterable, JSONLinesIterable, 
             XLSIterable, XLSXIterable, XMLIterable]
CODECS = [BZIP2Codec, LZMACodec, GZIPCodec, LZ4Codec, ZIPCodec, BrotliCodec, ZSTDCodec]

TEXT_DATA_TYPES = ['xml', 'csv', 'tsv', 'jsonl', 'ndjson', 'json']

DATATYPE_MAP = {'avro' : AVROIterable, 
                'bson' : BSONIterable, 
                'csv' : CSVIterable,
                'tsv' : CSVIterable,
                'json' : JSONIterable,
                'jsonl' : JSONLinesIterable,
                'ndjson' : JSONLinesIterable,
                'parquet' : ParquetIterable,
                'pickle' : PickleIterable,
                'orc' : ORCIterable,
                'xls' : XLSIterable,
                'xlsx' : XLSXIterable,
                'xml' : XMLIterable
                }

CODECS_MAP = {'bz2' : BZIP2Codec, 
              'gz' : GZIPCodec,
              'lz4' : LZ4Codec,
              'xz' : LZMACodec,
              'lzma' : LZMACodec,
              'zip' : ZIPCodec,
              'br' : BrotliCodec,
              'zstd' : ZSTDCodec,
              'zst' : ZSTDCodec
              }


FLAT_TYPES = ['csv', 'tsv', 'xls', 'xlsx']

ENGINES = ['internal', 'duckdb']

DUCKDB_SUPPORTED_TYPES = ['csv', 'jsonl', 'ndjson', 'json']
DUCKDB_SUPPORTED_CODECS = ['gz', 'zstd', 'zst']

def is_flat(filename:str=None, filetype:str=None):
    """Returns True if file is flat data file"""
    if filetype is not None:
        if filetype in FLAT_TYPES: 
            return True
    elif filename is not None:
        parts = filename.lower().rsplit('.', 2)
        if len(parts) == 2:
             if parts[1] in FLAT_TYPES: return True
        elif len(parts) > 2:
             if parts[1] in FLAT_TYPES: return True
    return False


def detect_file_type(filename:str) -> dict:
    """Detects file type and compression codec from filename"""
    result = {'filename' : filename, 'success' : False, 'codec' : None, 'datatype' : None}
    parts = filename.lower().rsplit('.', 2)
    if len(parts) == 2:
        if parts[-1] in DATATYPE_MAP.keys():
            result['datatype'] = DATATYPE_MAP[parts[-1]]
            result['success'] = True
    elif len(parts) > 2:
        if parts[-2] in DATATYPE_MAP.keys() and CODECS_MAP.keys():
            result['datatype'] = DATATYPE_MAP[parts[-2]]
            result['success'] = True
            result['codec'] = CODECS_MAP[parts[-1]]
        elif parts[-1] in DATATYPE_MAP.keys():
            result['datatype'] = DATATYPE_MAP[parts[-1]]
            result['success'] = True                
    return result

def detect_compression(filename:str) -> dict:
    """Detects file type and compression codec from filename"""
    result = {'filename' : filename, 'success' : False, 'codec' : None, 'datatype' : None}
    parts = filename.lower().rsplit('.', 2)
    if len(parts) == 2:
        if parts[-1] in CODECS_MAP.keys():
            result['compression'] = CODECS_MAP[parts[-1]]
            result['success'] = True
    elif len(parts) > 2:
        if parts[-1] in CODECS_MAP.keys():
            result['compression'] = CODECS_MAP[parts[-1]]
            result['success'] = True                
    return result


def detect_encoding_any(filename:str, limit:int=1000000):
    """Detects encodung of any data file including compressed"""
    result = detect_file_type(filename)
    fileobj = None
    codec = None
    if result['success']:        
        if result['codec'] is not None:
            codec = result['codec'](filename, open_it=True)
            fileobj = codec.fileobj()
    if fileobj is None:
        fileobj = open(filename, 'rb')
    
    chunk = fileobj.read(limit)
    if codec is not None:
        codec.close()
    else:
        fileobj.close()
    detected = chardet.detect(chunk)
    return detected

        


def open_iterable(filename:str, mode:str = 'r', engine:str='internal', codecargs:dict={}, iterableargs:dict={}):
    """Opens file and returns iterable object. Codecargs and iterable args are dicts with arguments to codec and iterable class"""
    result = detect_file_type(filename)
    iterable = None
    if engine not in ['internal', 'duckdb']: raise ValueError(f'Engine could be only: internal or duckdb. Not {engine}')
    if result['success']:
        if result['codec'] is not None and engine != 'duckdb':
            codec = result['codec'](filename=filename, mode=mode, options=codecargs)
            iterable = result['datatype'](codec=codec, mode=mode, options=iterableargs)
        elif engine == 'duckdb':
            iterable = DuckDBIterable(filename=filename, mode=mode, options=iterableargs)
        else:
            iterable = result['datatype'](filename=filename, mode=mode, options=iterableargs)
        
    return iterable
