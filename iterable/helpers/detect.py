from __future__ import annotations
import chardet
from typing import TypedDict, Optional, Literal, Union, Type
from ..base import BaseIterable, BaseCodec
from ..datatypes.avro import AVROIterable
from ..datatypes.bsonf import BSONIterable
from ..datatypes.csv import CSVIterable
from ..datatypes.dbf import DBFIterable
from ..datatypes.orc import ORCIterable
from ..datatypes.parquet import ParquetIterable
from ..datatypes.picklef import PickleIterable
from ..datatypes.json import JSONIterable
from ..datatypes.jsonl import JSONLinesIterable
from ..datatypes.jsonld import JSONLDIterable
from ..datatypes.xls import XLSIterable
from ..datatypes.xlsx import XLSXIterable
from ..datatypes.xml import XMLIterable
from ..datatypes.arrow import ArrowIterable
from ..datatypes.msgpack import MessagePackIterable
from ..datatypes.fwf import FixedWidthIterable
from ..datatypes.yaml import YAMLIterable
from ..datatypes.sas import SASIterable
from ..datatypes.stata import StataIterable
from ..datatypes.spss import SPSSIterable
from ..datatypes.protobuf import ProtobufIterable
from ..datatypes.ion import IonIterable
from ..datatypes.hdf5 import HDF5Iterable
from ..datatypes.geojson import GeoJSONIterable
from ..datatypes.toml import TOMLIterable
from ..datatypes.delta import DeltaIterable
from ..datatypes.cbor import CBORIterable
from ..datatypes.ods import ODSIterable
from ..datatypes.sqlite import SQLiteIterable
from ..datatypes.duckdb import DuckDBIterable as DuckDBDatatypeIterable
from ..datatypes.psv import PSVIterable, SSVIterable
from ..datatypes.ubjson import UBJSONIterable
from ..datatypes.capnp import CapnpIterable
from ..datatypes.iceberg import IcebergIterable
from ..datatypes.turtle import TurtleIterable
from ..datatypes.flatbuffers import FlatBuffersIterable
from ..datatypes.thrift import ThriftIterable
from ..datatypes.txt import TxtIterable
from ..datatypes.hudi import HudiIterable
from ..datatypes.apachelog import ApacheLogIterable
from ..datatypes.tfrecord import TFRecordIterable
from ..datatypes.sequencefile import SequenceFileIterable
from ..datatypes.gelf import GELIterable
from ..datatypes.cef import CEFIterable
from ..datatypes.ntriples import NTriplesIterable
from ..datatypes.nquads import NQuadsIterable
from ..datatypes.kafka import KafkaIterable
from ..datatypes.pulsar import PulsarIterable
from ..datatypes.flink import FlinkIterable
from ..datatypes.beam import BeamIterable
from ..datatypes.recordio import RecordIOIterable
from ..datatypes.rdfxml import RDFXMLIterable
from ..datatypes.ilp import ILPIterable
from ..datatypes.annotatedcsv import AnnotatedCSVIterable
from ..datatypes.cdx import CDXIterable
from ..datatypes.warc import WARCIterable
from ..datatypes.ldif import LDIFIterable
from ..datatypes.mbox import MBOXIterable
from ..datatypes.ini import INIIterable
from ..datatypes.edn import EDNIterable
from ..datatypes.smile import SMILEIterable
from ..datatypes.bencode import BencodeIterable
from ..datatypes.vcf import VCFIterable
from ..datatypes.ical import ICALIterable
from ..datatypes.eml import EMLIterable
from ..datatypes.mysqldump import MySQLDumpIterable
from ..datatypes.pgcopy import PGCopyIterable
from ..datatypes.hocon import HOCONIterable
from ..datatypes.flexbuffers import FlexBuffersIterable
from ..datatypes.asn1 import ASN1Iterable
from ..datatypes.mhtml import MHTMLIterable
from ..datatypes.ltsv import LTSVIterable
from ..datatypes.px import PXIterable
from ..datatypes.kml import KMLIterable
from ..datatypes.gml import GMLIterable
from ..datatypes.shapefile import ShapefileIterable
from ..datatypes.geopackage import GeoPackageIterable
from ..datatypes.csvw import CSVWIterable
from ..datatypes.rdata import RDataIterable
from ..datatypes.rds import RDSIterable
from ..datatypes.lance import LanceIterable
from ..engines.duckdb import DuckDBIterable

from ..codecs.bz2codec import BZIP2Codec
from ..codecs.gzipcodec import GZIPCodec
from ..codecs.lzmacodec import LZMACodec
from ..codecs.lz4codec import LZ4Codec
from ..codecs.zipcodec import ZIPCodec
from ..codecs.brotlicodec import BrotliCodec
from ..codecs.zstdcodec import ZSTDCodec
from ..codecs.snappycodec import SnappyCodec
from ..codecs.lzocodec import LZOCodec


class FileTypeResult(TypedDict):
    """Result of file type detection"""
    filename: str
    success: bool
    codec: Optional[Type[BaseCodec]]
    datatype: Optional[Type[BaseIterable]]


class CompressionResult(TypedDict):
    """Result of compression detection"""
    filename: str
    success: bool
    compression: Optional[Type[BaseCodec]]
    codec: Optional[Type[BaseCodec]]
    datatype: Optional[Type[BaseIterable]]


DATATYPES = [AVROIterable, BSONIterable, CSVIterable, DBFIterable, ORCIterable, 
             ParquetIterable, PickleIterable, JSONIterable, JSONLinesIterable, JSONLDIterable,
             XLSIterable, XLSXIterable, XMLIterable, ArrowIterable, 
             MessagePackIterable, FixedWidthIterable, YAMLIterable,
             SASIterable, StataIterable, SPSSIterable, ProtobufIterable,
             IonIterable, HDF5Iterable, GeoJSONIterable, TOMLIterable, DeltaIterable,
             CBORIterable, ODSIterable, SQLiteIterable, DuckDBDatatypeIterable, PSVIterable, SSVIterable,
             UBJSONIterable, CapnpIterable, IcebergIterable, TurtleIterable,
             FlatBuffersIterable, ThriftIterable, TxtIterable, HudiIterable, ApacheLogIterable,
             TFRecordIterable, SequenceFileIterable, GELIterable, CEFIterable,
             NTriplesIterable, NQuadsIterable, KafkaIterable, PulsarIterable,
             FlinkIterable, BeamIterable, RecordIOIterable, RDFXMLIterable,
             ILPIterable, AnnotatedCSVIterable, CDXIterable, WARCIterable,
             LDIFIterable, MBOXIterable, INIIterable, EDNIterable, SMILEIterable,
             BencodeIterable, VCFIterable, ICALIterable, EMLIterable, MySQLDumpIterable,
             PGCopyIterable, HOCONIterable, FlexBuffersIterable, ASN1Iterable, MHTMLIterable,
             LTSVIterable, PXIterable, KMLIterable, GMLIterable, ShapefileIterable,
             GeoPackageIterable, CSVWIterable, RDataIterable, RDSIterable, LanceIterable]
CODECS = [BZIP2Codec, LZMACodec, GZIPCodec, LZ4Codec, ZIPCodec, BrotliCodec, ZSTDCodec, SnappyCodec, LZOCodec]

TEXT_DATA_TYPES = ['xml', 'csv', 'tsv', 'jsonl', 'ndjson', 'json', 'jsonld', 'yaml', 'yml', 'fwf', 'fixed', 'geojson', 'toml', 'psv', 'ssv', 'turtle', 'ttl', 'apachelog', 'log', 'access.log', 'gelf', 'cef', 'nt', 'nq', 'ntriples', 'nquads', 'rdf', 'rdf.xml', 'ilp', 'annotatedcsv', 'cdx', 'ldif', 'mbox', 'ini', 'properties', 'conf', 'edn', 'vcf', 'ical', 'ics', 'eml', 'sql', 'mysqldump', 'pgcopy', 'copy', 'hocon', 'mhtml', 'mht', 'txt', 'text', 'ltsv', 'px', 'kml', 'gml', 'csvw']

DATATYPE_MAP = {'avro' : AVROIterable, 
                'bson' : BSONIterable, 
                'csv' : CSVIterable,
                'tsv' : CSVIterable,
                'dbf' : DBFIterable,
                'json' : JSONIterable,
                'jsonl' : JSONLinesIterable,
                'ndjson' : JSONLinesIterable,
                'jsonld' : JSONLDIterable,
                'parquet' : ParquetIterable,
                'pickle' : PickleIterable,
                'orc' : ORCIterable,
                'xls' : XLSIterable,
                'xlsx' : XLSXIterable,
                'xml' : XMLIterable,
                'arrow' : ArrowIterable,
                'feather' : ArrowIterable,
                'msgpack' : MessagePackIterable,
                'mp' : MessagePackIterable,
                'fwf' : FixedWidthIterable,
                'fixed' : FixedWidthIterable,
                'yaml' : YAMLIterable,
                'yml' : YAMLIterable,
                'sas7bdat' : SASIterable,
                'sas' : SASIterable,
                'dta' : StataIterable,
                'stata' : StataIterable,
                'sav' : SPSSIterable,
                'spss' : SPSSIterable,
                'protobuf' : ProtobufIterable,
                'pb' : ProtobufIterable,
                'ion' : IonIterable,
                'hdf5' : HDF5Iterable,
                'h5' : HDF5Iterable,
                'geojson' : GeoJSONIterable,
                'toml' : TOMLIterable,
                'delta' : DeltaIterable,
                'cbor' : CBORIterable,
                'ods' : ODSIterable,
                'sqlite' : SQLiteIterable,
                'db' : SQLiteIterable,
                'duckdb' : DuckDBDatatypeIterable,
                'ddb' : DuckDBDatatypeIterable,
                'psv' : PSVIterable,
                'ssv' : SSVIterable,
                'ubjson' : UBJSONIterable,
                'ubj' : UBJSONIterable,
                'capnp' : CapnpIterable,
                'iceberg' : IcebergIterable,
                'turtle' : TurtleIterable,
                'ttl' : TurtleIterable,
                'flatbuffers' : FlatBuffersIterable,
                'fbs' : FlatBuffersIterable,
                'thrift' : ThriftIterable,
                'txt' : TxtIterable,
                'text' : TxtIterable,
                'hudi' : HudiIterable,
                'apachelog' : ApacheLogIterable,
                'access.log' : ApacheLogIterable,
                'log' : ApacheLogIterable,
                'tfrecord' : TFRecordIterable,
                'tfrecords' : TFRecordIterable,
                'sequencefile' : SequenceFileIterable,
                'seq' : SequenceFileIterable,
                'gelf' : GELIterable,
                'cef' : CEFIterable,
                'ntriples' : NTriplesIterable,
                'nt' : NTriplesIterable,
                'nquads' : NQuadsIterable,
                'nq' : NQuadsIterable,
                'kafka' : KafkaIterable,
                'pulsar' : PulsarIterable,
                'flink' : FlinkIterable,
                'ckpt' : FlinkIterable,
                'beam' : BeamIterable,
                'recordio' : RecordIOIterable,
                'rio' : RecordIOIterable,
                'rdfxml' : RDFXMLIterable,
                'rdf' : RDFXMLIterable,
                'ilp' : ILPIterable,
                'annotatedcsv' : AnnotatedCSVIterable,
                'cdx' : CDXIterable,
                'warc' : WARCIterable,
                'arc' : WARCIterable,
                'ldif' : LDIFIterable,
                'mbox' : MBOXIterable,
                'ini' : INIIterable,
                'properties' : INIIterable,
                'conf' : INIIterable,
                'edn' : EDNIterable,
                'smile' : SMILEIterable,
                'bencode' : BencodeIterable,
                'torrent' : BencodeIterable,
                'vcf' : VCFIterable,
                'vcard' : VCFIterable,
                'ical' : ICALIterable,
                'ics' : ICALIterable,
                'eml' : EMLIterable,
                'mysqldump' : MySQLDumpIterable,
                'sql' : MySQLDumpIterable,
                'pgcopy' : PGCopyIterable,
                'copy' : PGCopyIterable,
                'hocon' : HOCONIterable,
                'flexbuffers' : FlexBuffersIterable,
                'flexbuf' : FlexBuffersIterable,
                'asn1' : ASN1Iterable,
                'der' : ASN1Iterable,
                'mhtml' : MHTMLIterable,
                'mht' : MHTMLIterable,
                'ltsv' : LTSVIterable,
                'px' : PXIterable,
                'kml' : KMLIterable,
                'gml' : GMLIterable,
                'shapefile' : ShapefileIterable,
                'shp' : ShapefileIterable,
                'geopackage' : GeoPackageIterable,
                'gpkg' : GeoPackageIterable,
                'csvw' : CSVWIterable,
                'rdata' : RDataIterable,
                'rda' : RDataIterable,
                'rds' : RDSIterable,
                'lance' : LanceIterable
                }

CODECS_MAP = {'bz2' : BZIP2Codec, 
              'gz' : GZIPCodec,
              'lz4' : LZ4Codec,
              'xz' : LZMACodec,
              'lzma' : LZMACodec,
              'zip' : ZIPCodec,
              'br' : BrotliCodec,
              'zstd' : ZSTDCodec,
              'zst' : ZSTDCodec,
              'snappy' : SnappyCodec,
              'sz' : SnappyCodec,
              'lzo' : LZOCodec,
              'lzop' : LZOCodec
              }


FLAT_TYPES = ['csv', 'tsv', 'xls', 'xlsx', 'dbf', 'fwf', 'fixed', 'sas7bdat', 'sas', 'dta', 'stata', 'sav', 'spss', 'hdf5', 'h5', 'delta', 'ods', 'sqlite', 'db', 'duckdb', 'ddb', 'psv', 'ssv', 'iceberg', 'hudi', 'apachelog', 'log', 'access.log', 'cef', 'nt', 'nq', 'ntriples', 'nquads', 'annotatedcsv', 'cdx', 'ini', 'properties', 'conf', 'mysqldump', 'sql', 'pgcopy', 'copy', 'px', 'csvw', 'rdata', 'rda', 'rds', 'lance']

ENGINES = ['internal', 'duckdb']

DUCKDB_SUPPORTED_TYPES = ['csv', 'jsonl', 'ndjson', 'json']
DUCKDB_SUPPORTED_CODECS = ['gz', 'zstd', 'zst']

def is_flat(filename: Optional[str] = None, filetype: Optional[str] = None) -> bool:
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


def detect_file_type(filename: str) -> FileTypeResult:
    """Detects file type and compression codec from filename
    
    Args:
        filename: Path to the file to detect
        
    Returns:
        FileTypeResult dictionary with detection results
        
    Raises:
        ValueError: If filename is empty or invalid
    """
    if not filename:
        raise ValueError("Filename cannot be empty")
    
    result: FileTypeResult = {
        'filename': filename,
        'success': False,
        'codec': None,
        'datatype': None
    }
    parts = filename.lower().rsplit('.', 2)
    if len(parts) == 2:
        if parts[-1] in DATATYPE_MAP.keys():
            result['datatype'] = DATATYPE_MAP[parts[-1]]
            result['success'] = True
    elif len(parts) > 2:
        if parts[-2] in DATATYPE_MAP.keys() and parts[-1] in CODECS_MAP.keys():
            result['datatype'] = DATATYPE_MAP[parts[-2]]
            result['success'] = True
            result['codec'] = CODECS_MAP[parts[-1]]
        elif parts[-1] in DATATYPE_MAP.keys():
            result['datatype'] = DATATYPE_MAP[parts[-1]]
            result['success'] = True                
    return result

def detect_compression(filename: str) -> CompressionResult:
    """Detects compression codec from filename
    
    Args:
        filename: Path to the file to detect compression for
        
    Returns:
        CompressionResult dictionary with detection results
        
    Raises:
        ValueError: If filename is empty or invalid
    """
    if not filename:
        raise ValueError("Filename cannot be empty")
    
    result: CompressionResult = {
        'filename': filename,
        'success': False,
        'compression': None,
        'codec': None,
        'datatype': None
    }
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


def detect_encoding_any(filename: str, limit: int = 1000000) -> dict:
    """Detects encoding of any data file including compressed
    
    Args:
        filename: Path to the file to detect encoding for
        limit: Maximum bytes to read for detection (default: 1000000)
        
    Returns:
        Dictionary with encoding detection results from chardet containing:
        - 'encoding': Detected encoding name
        - 'confidence': Confidence score (0.0 to 1.0)
        - 'language': Detected language (if available)
        
    Raises:
        FileNotFoundError: If file does not exist
        ValueError: If filename is empty
        IOError: If file cannot be read
    """
    if not filename:
        raise ValueError("Filename cannot be empty")
    
    import os
    if not os.path.exists(filename):
        raise FileNotFoundError(
            f"File not found: '{filename}'. "
            f"Please check that the file exists and the path is correct."
        )
    
    result = detect_file_type(filename)
    fileobj = None
    codec = None
    
    try:
        if result['success']:        
            if result['codec'] is not None:
                try:
                    codec = result['codec'](filename, open_it=True)
                    fileobj = codec.fileobj()
                except Exception as e:
                    raise IOError(
                        f"Failed to open compressed file '{filename}' with codec '{result['codec']}'. "
                        f"Error: {str(e)}"
                    ) from e
        if fileobj is None:
            try:
                fileobj = open(filename, 'rb')
            except IOError as e:
                raise IOError(
                    f"Cannot read file '{filename}'. "
                    f"Please check file permissions and that the file is not corrupted. "
                    f"Error: {str(e)}"
                ) from e
        
        chunk = fileobj.read(limit)
        if not chunk:
            raise ValueError(f"File '{filename}' appears to be empty")
        
        detected = chardet.detect(chunk)
        if not detected or detected.get('encoding') is None:
            raise ValueError(
                f"Could not detect encoding for file '{filename}'. "
                f"The file may be binary or use an unsupported encoding."
            )
        
        return detected
    finally:
        if codec is not None:
            try:
                codec.close()
            except Exception:
                pass
        elif fileobj is not None:
            try:
                fileobj.close()
            except Exception:
                pass

        


def open_iterable(
    filename: str,
    mode: Literal['r', 'w', 'rb', 'wb'] = 'r',
    engine: Literal['internal', 'duckdb'] = 'internal',
    codecargs: Optional[dict] = None,
    iterableargs: Optional[dict] = None
) -> BaseIterable:
    """Opens file and returns iterable object.
    
    Args:
        filename: Path to the file to open
        mode: File mode ('r' for read, 'w' for write, 'rb'/'wb' for binary)
        engine: Processing engine ('internal' or 'duckdb')
        codecargs: Dictionary with arguments for codec initialization
        iterableargs: Dictionary with arguments for iterable initialization
        
    Returns:
        Iterable object for the detected file type
        
    Raises:
        ValueError: If engine is invalid, filename is empty, or DuckDB engine doesn't support the format/codec
        FileNotFoundError: If file does not exist (in read mode)
        RuntimeError: If file type cannot be detected or format is not supported
        
    Example:
        >>> source = open_iterable('data.csv.gz')
        >>> with source:
        ...     for row in source:
        ...         print(row)
    """
    import os
    
    if not filename:
        raise ValueError("Filename cannot be empty")
    
    if engine not in ['internal', 'duckdb']:
        raise ValueError(f"Engine must be 'internal' or 'duckdb', got '{engine}'")
    
    # Normalize mode: 'rb' -> 'r', 'wb' -> 'w' for text-based formats
    normalized_mode = 'r' if mode in ['r', 'rb'] else 'w'
    
    # Check file existence for read mode
    if normalized_mode == 'r' and not os.path.exists(filename):
        raise FileNotFoundError(
            f"File not found: '{filename}'. "
            f"Please check that the file exists and the path is correct."
        )
    
    if codecargs is None:
        codecargs = {}
    if iterableargs is None:
        iterableargs = {}
    
    result = detect_file_type(filename)
    
    if not result['success']:
        raise RuntimeError(
            f"Could not detect file type for '{filename}'. "
            f"Supported formats: {', '.join(sorted(set(DATATYPE_MAP.keys())))}"
        )
    
    # Extract file type from filename for DuckDB validation
    parts = filename.lower().rsplit('.', 2)
    detected_filetype = None
    detected_codec = None
    
    if len(parts) == 2:
        detected_filetype = parts[-1]
    elif len(parts) > 2:
        detected_filetype = parts[-2] if parts[-1] in CODECS_MAP.keys() else parts[-1]
        detected_codec = parts[-1] if parts[-1] in CODECS_MAP.keys() else None
    
    # Validate DuckDB engine support
    if engine == 'duckdb':
        if detected_filetype not in DUCKDB_SUPPORTED_TYPES:
            raise ValueError(
                f"DuckDB engine does not support file type '{detected_filetype}'. "
                f"Supported types: {', '.join(DUCKDB_SUPPORTED_TYPES)}. "
                f"Use engine='internal' for this file type."
            )
        if detected_codec is not None and detected_codec not in DUCKDB_SUPPORTED_CODECS:
            raise ValueError(
                f"DuckDB engine does not support compression codec '{detected_codec}'. "
                f"Supported codecs: {', '.join(DUCKDB_SUPPORTED_CODECS)}. "
                f"Use engine='internal' for this compression codec."
            )
    
    # Get datatype class name for better error messages
    datatype_name = result['datatype'].__name__ if result['datatype'] else 'unknown'
    
    try:
        if result['codec'] is not None and engine != 'duckdb':
            codec = result['codec'](filename=filename, mode=mode, options=codecargs)
            iterable = result['datatype'](codec=codec, mode=normalized_mode, options=iterableargs)
        elif engine == 'duckdb':
            iterable = DuckDBIterable(filename=filename, mode=normalized_mode, options=iterableargs)
        else:
            iterable = result['datatype'](filename=filename, mode=normalized_mode, options=iterableargs)
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"File not found: '{filename}'. "
            f"Please check that the file exists and the path is correct."
        ) from e
    except Exception as e:
        raise RuntimeError(
            f"Failed to open file '{filename}' with format '{datatype_name}' "
            f"(detected type: '{detected_filetype}', codec: '{detected_codec or 'none'}'). "
            f"Error: {str(e)}"
        ) from e
        
    return iterable
