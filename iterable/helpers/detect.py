from __future__ import annotations

import importlib
from typing import Literal, TypedDict

import chardet

from ..base import BaseCodec, BaseIterable


def _load_symbol(module_path: str, symbol: str):
    """
    Lazy-load a datatype/codec class to avoid importing all optional dependencies at import time.
    """
    try:
        module = importlib.import_module(module_path)
        return getattr(module, symbol)
    except ImportError as e:
        raise ImportError(
            f"Failed to import '{symbol}' from '{module_path}'. "
            f"This format/codec likely requires an optional dependency. "
            f"Install the needed extras (for now: `pip install iterabledata[dev]` or `pip install iterabledata`)."
        ) from e


# Lazy registries: extension -> (module_path, class_name)
DATATYPE_REGISTRY: dict[str, tuple[str, str]] = {
    "avro": ("iterable.datatypes.avro", "AVROIterable"),
    "bson": ("iterable.datatypes.bsonf", "BSONIterable"),
    "csv": ("iterable.datatypes.csv", "CSVIterable"),
    "tsv": ("iterable.datatypes.csv", "CSVIterable"),
    "dbf": ("iterable.datatypes.dbf", "DBFIterable"),
    "json": ("iterable.datatypes.json", "JSONIterable"),
    "jsonl": ("iterable.datatypes.jsonl", "JSONLinesIterable"),
    "ndjson": ("iterable.datatypes.jsonl", "JSONLinesIterable"),
    "jsonld": ("iterable.datatypes.jsonld", "JSONLDIterable"),
    "parquet": ("iterable.datatypes.parquet", "ParquetIterable"),
    "pickle": ("iterable.datatypes.picklef", "PickleIterable"),
    "orc": ("iterable.datatypes.orc", "ORCIterable"),
    "xls": ("iterable.datatypes.xls", "XLSIterable"),
    "xlsx": ("iterable.datatypes.xlsx", "XLSXIterable"),
    "xml": ("iterable.datatypes.xml", "XMLIterable"),
    "arrow": ("iterable.datatypes.arrow", "ArrowIterable"),
    "feather": ("iterable.datatypes.arrow", "ArrowIterable"),
    "msgpack": ("iterable.datatypes.msgpack", "MessagePackIterable"),
    "mp": ("iterable.datatypes.msgpack", "MessagePackIterable"),
    "fwf": ("iterable.datatypes.fwf", "FixedWidthIterable"),
    "fixed": ("iterable.datatypes.fwf", "FixedWidthIterable"),
    "yaml": ("iterable.datatypes.yaml", "YAMLIterable"),
    "yml": ("iterable.datatypes.yaml", "YAMLIterable"),
    "sas7bdat": ("iterable.datatypes.sas", "SASIterable"),
    "sas": ("iterable.datatypes.sas", "SASIterable"),
    "dta": ("iterable.datatypes.stata", "StataIterable"),
    "stata": ("iterable.datatypes.stata", "StataIterable"),
    "sav": ("iterable.datatypes.spss", "SPSSIterable"),
    "spss": ("iterable.datatypes.spss", "SPSSIterable"),
    "protobuf": ("iterable.datatypes.protobuf", "ProtobufIterable"),
    "pb": ("iterable.datatypes.protobuf", "ProtobufIterable"),
    "ion": ("iterable.datatypes.ion", "IonIterable"),
    "hdf5": ("iterable.datatypes.hdf5", "HDF5Iterable"),
    "h5": ("iterable.datatypes.hdf5", "HDF5Iterable"),
    "geojson": ("iterable.datatypes.geojson", "GeoJSONIterable"),
    "toml": ("iterable.datatypes.toml", "TOMLIterable"),
    "delta": ("iterable.datatypes.delta", "DeltaIterable"),
    "cbor": ("iterable.datatypes.cbor", "CBORIterable"),
    "ods": ("iterable.datatypes.ods", "ODSIterable"),
    "sqlite": ("iterable.datatypes.sqlite", "SQLiteIterable"),
    "db": ("iterable.datatypes.sqlite", "SQLiteIterable"),
    "duckdb": ("iterable.datatypes.duckdb", "DuckDBIterable"),
    "ddb": ("iterable.datatypes.duckdb", "DuckDBIterable"),
    "psv": ("iterable.datatypes.psv", "PSVIterable"),
    "ssv": ("iterable.datatypes.psv", "SSVIterable"),
    "ubjson": ("iterable.datatypes.ubjson", "UBJSONIterable"),
    "ubj": ("iterable.datatypes.ubjson", "UBJSONIterable"),
    "capnp": ("iterable.datatypes.capnp", "CapnpIterable"),
    "iceberg": ("iterable.datatypes.iceberg", "IcebergIterable"),
    "turtle": ("iterable.datatypes.turtle", "TurtleIterable"),
    "ttl": ("iterable.datatypes.turtle", "TurtleIterable"),
    "flatbuffers": ("iterable.datatypes.flatbuffers", "FlatBuffersIterable"),
    "fbs": ("iterable.datatypes.flatbuffers", "FlatBuffersIterable"),
    "thrift": ("iterable.datatypes.thrift", "ThriftIterable"),
    "txt": ("iterable.datatypes.txt", "TxtIterable"),
    "text": ("iterable.datatypes.txt", "TxtIterable"),
    "hudi": ("iterable.datatypes.hudi", "HudiIterable"),
    "apachelog": ("iterable.datatypes.apachelog", "ApacheLogIterable"),
    "access.log": ("iterable.datatypes.apachelog", "ApacheLogIterable"),
    "log": ("iterable.datatypes.apachelog", "ApacheLogIterable"),
    "tfrecord": ("iterable.datatypes.tfrecord", "TFRecordIterable"),
    "tfrecords": ("iterable.datatypes.tfrecord", "TFRecordIterable"),
    "sequencefile": ("iterable.datatypes.sequencefile", "SequenceFileIterable"),
    "seq": ("iterable.datatypes.sequencefile", "SequenceFileIterable"),
    "gelf": ("iterable.datatypes.gelf", "GELIterable"),
    "cef": ("iterable.datatypes.cef", "CEFIterable"),
    "ntriples": ("iterable.datatypes.ntriples", "NTriplesIterable"),
    "nt": ("iterable.datatypes.ntriples", "NTriplesIterable"),
    "nquads": ("iterable.datatypes.nquads", "NQuadsIterable"),
    "nq": ("iterable.datatypes.nquads", "NQuadsIterable"),
    "kafka": ("iterable.datatypes.kafka", "KafkaIterable"),
    "pulsar": ("iterable.datatypes.pulsar", "PulsarIterable"),
    "flink": ("iterable.datatypes.flink", "FlinkIterable"),
    "ckpt": ("iterable.datatypes.flink", "FlinkIterable"),
    "beam": ("iterable.datatypes.beam", "BeamIterable"),
    "recordio": ("iterable.datatypes.recordio", "RecordIOIterable"),
    "rio": ("iterable.datatypes.recordio", "RecordIOIterable"),
    "rdfxml": ("iterable.datatypes.rdfxml", "RDFXMLIterable"),
    "rdf": ("iterable.datatypes.rdfxml", "RDFXMLIterable"),
    "ilp": ("iterable.datatypes.ilp", "ILPIterable"),
    "annotatedcsv": ("iterable.datatypes.annotatedcsv", "AnnotatedCSVIterable"),
    "cdx": ("iterable.datatypes.cdx", "CDXIterable"),
    "warc": ("iterable.datatypes.warc", "WARCIterable"),
    "arc": ("iterable.datatypes.warc", "WARCIterable"),
    "ldif": ("iterable.datatypes.ldif", "LDIFIterable"),
    "mbox": ("iterable.datatypes.mbox", "MBOXIterable"),
    "ini": ("iterable.datatypes.ini", "INIIterable"),
    "properties": ("iterable.datatypes.ini", "INIIterable"),
    "conf": ("iterable.datatypes.ini", "INIIterable"),
    "edn": ("iterable.datatypes.edn", "EDNIterable"),
    "smile": ("iterable.datatypes.smile", "SMILEIterable"),
    "bencode": ("iterable.datatypes.bencode", "BencodeIterable"),
    "torrent": ("iterable.datatypes.bencode", "BencodeIterable"),
    "vcf": ("iterable.datatypes.vcf", "VCFIterable"),
    "vcard": ("iterable.datatypes.vcf", "VCFIterable"),
    "ical": ("iterable.datatypes.ical", "ICALIterable"),
    "ics": ("iterable.datatypes.ical", "ICALIterable"),
    "eml": ("iterable.datatypes.eml", "EMLIterable"),
    "mysqldump": ("iterable.datatypes.mysqldump", "MySQLDumpIterable"),
    "sql": ("iterable.datatypes.mysqldump", "MySQLDumpIterable"),
    "pgcopy": ("iterable.datatypes.pgcopy", "PGCopyIterable"),
    "copy": ("iterable.datatypes.pgcopy", "PGCopyIterable"),
    "hocon": ("iterable.datatypes.hocon", "HOCONIterable"),
    "flexbuffers": ("iterable.datatypes.flexbuffers", "FlexBuffersIterable"),
    "flexbuf": ("iterable.datatypes.flexbuffers", "FlexBuffersIterable"),
    "asn1": ("iterable.datatypes.asn1", "ASN1Iterable"),
    "der": ("iterable.datatypes.asn1", "ASN1Iterable"),
    "mhtml": ("iterable.datatypes.mhtml", "MHTMLIterable"),
    "mht": ("iterable.datatypes.mhtml", "MHTMLIterable"),
    "ltsv": ("iterable.datatypes.ltsv", "LTSVIterable"),
    "px": ("iterable.datatypes.px", "PXIterable"),
    "kml": ("iterable.datatypes.kml", "KMLIterable"),
    "gml": ("iterable.datatypes.gml", "GMLIterable"),
    "shapefile": ("iterable.datatypes.shapefile", "ShapefileIterable"),
    "shp": ("iterable.datatypes.shapefile", "ShapefileIterable"),
    "geopackage": ("iterable.datatypes.geopackage", "GeoPackageIterable"),
    "gpkg": ("iterable.datatypes.geopackage", "GeoPackageIterable"),
    "csvw": ("iterable.datatypes.csvw", "CSVWIterable"),
    "rdata": ("iterable.datatypes.rdata", "RDataIterable"),
    "rda": ("iterable.datatypes.rdata", "RDataIterable"),
    "rds": ("iterable.datatypes.rds", "RDSIterable"),
    "lance": ("iterable.datatypes.lance", "LanceIterable"),
    "pcap": ("iterable.datatypes.pcap", "PCAPIterable"),
    "pcapng": ("iterable.datatypes.pcap", "PCAPIterable"),
    "nc": ("iterable.datatypes.netcdf", "NetCDFIterable"),
    "netcdf": ("iterable.datatypes.netcdf", "NetCDFIterable"),
    "mvt": ("iterable.datatypes.mvt", "MVTIterable"),
    "pbf": ("iterable.datatypes.mvt", "MVTIterable"),
    "topojson": ("iterable.datatypes.topojson", "TopoJSONIterable"),
    "atom": ("iterable.datatypes.feed", "FeedIterable"),
    "rss": ("iterable.datatypes.feed", "FeedIterable"),
    "dxf": ("iterable.datatypes.dxf", "DXFIterable"),
    "libsvm": ("iterable.datatypes.libsvm", "LIBSVMIterable"),
    "npy": ("iterable.datatypes.numpy", "NumPyIterable"),
    "npz": ("iterable.datatypes.numpy", "NumPyIterable"),
    "html": ("iterable.datatypes.html", "HTMLIterable"),
    "htm": ("iterable.datatypes.html", "HTMLIterable"),
    "arff": ("iterable.datatypes.arff", "ARFFIterable"),
    "vortex": ("iterable.datatypes.vortex", "VortexIterable"),
    "vtx": ("iterable.datatypes.vortex", "VortexIterable"),
}

CODEC_REGISTRY: dict[str, tuple[str, str]] = {
    "bz2": ("iterable.codecs.bz2codec", "BZIP2Codec"),
    "gz": ("iterable.codecs.gzipcodec", "GZIPCodec"),
    "lz4": ("iterable.codecs.lz4codec", "LZ4Codec"),
    "xz": ("iterable.codecs.lzmacodec", "LZMACodec"),
    "lzma": ("iterable.codecs.lzmacodec", "LZMACodec"),
    "zip": ("iterable.codecs.zipcodec", "ZIPCodec"),
    "br": ("iterable.codecs.brotlicodec", "BrotliCodec"),
    "zstd": ("iterable.codecs.zstdcodec", "ZSTDCodec"),
    "zst": ("iterable.codecs.zstdcodec", "ZSTDCodec"),
    "snappy": ("iterable.codecs.snappycodec", "SnappyCodec"),
    "sz": ("iterable.codecs.snappycodec", "SnappyCodec"),
    "lzo": ("iterable.codecs.lzocodec", "LZOCodec"),
    "lzop": ("iterable.codecs.lzocodec", "LZOCodec"),
}


def _datatype_class(ext: str) -> type[BaseIterable]:
    module_path, symbol = DATATYPE_REGISTRY[ext]
    return _load_symbol(module_path, symbol)


def _codec_class(ext: str) -> type[BaseCodec]:
    module_path, symbol = CODEC_REGISTRY[ext]
    return _load_symbol(module_path, symbol)


class FileTypeResult(TypedDict):
    """Result of file type detection"""

    filename: str
    success: bool
    codec: type[BaseCodec] | None
    datatype: type[BaseIterable] | None


class CompressionResult(TypedDict):
    """Result of compression detection"""

    filename: str
    success: bool
    compression: type[BaseCodec] | None
    codec: type[BaseCodec] | None
    datatype: type[BaseIterable] | None


TEXT_DATA_TYPES = [
    "xml",
    "csv",
    "tsv",
    "jsonl",
    "ndjson",
    "json",
    "jsonld",
    "yaml",
    "yml",
    "fwf",
    "fixed",
    "geojson",
    "toml",
    "psv",
    "ssv",
    "turtle",
    "ttl",
    "apachelog",
    "log",
    "access.log",
    "gelf",
    "cef",
    "nt",
    "nq",
    "ntriples",
    "nquads",
    "rdf",
    "rdf.xml",
    "ilp",
    "annotatedcsv",
    "cdx",
    "ldif",
    "mbox",
    "ini",
    "properties",
    "conf",
    "edn",
    "vcf",
    "ical",
    "ics",
    "eml",
    "sql",
    "mysqldump",
    "pgcopy",
    "copy",
    "hocon",
    "mhtml",
    "mht",
    "txt",
    "text",
    "ltsv",
    "px",
    "kml",
    "gml",
    "csvw",
    "html",
    "htm",
    "arff",
]


FLAT_TYPES = [
    "csv",
    "tsv",
    "xls",
    "xlsx",
    "dbf",
    "fwf",
    "fixed",
    "sas7bdat",
    "sas",
    "dta",
    "stata",
    "sav",
    "spss",
    "hdf5",
    "h5",
    "delta",
    "ods",
    "sqlite",
    "db",
    "duckdb",
    "ddb",
    "psv",
    "ssv",
    "iceberg",
    "hudi",
    "apachelog",
    "log",
    "access.log",
    "cef",
    "nt",
    "nq",
    "ntriples",
    "nquads",
    "annotatedcsv",
    "cdx",
    "ini",
    "properties",
    "conf",
    "mysqldump",
    "sql",
    "pgcopy",
    "copy",
    "px",
    "csvw",
    "rdata",
    "rda",
    "rds",
    "lance",
    "libsvm",
    "npy",
    "npz",
    "html",
    "htm",
    "arff",
    "vortex",
    "vtx",
]

ENGINES = ["internal", "duckdb"]

# DuckDB engine can read many file formats directly via DuckDB, but we keep this
# allowlist conservative and aligned with tests/docs.
DUCKDB_SUPPORTED_TYPES = ["csv", "jsonl", "ndjson", "json", "parquet"]
DUCKDB_SUPPORTED_CODECS = ["gz", "zstd", "zst"]


def is_flat(filename: str | None = None, filetype: str | None = None) -> bool:
    """Returns True if file is flat data file"""
    if filetype is not None:
        if filetype in FLAT_TYPES:
            return True
    elif filename is not None:
        parts = filename.lower().rsplit(".", 2)
        if len(parts) == 2:
            if parts[1] in FLAT_TYPES:
                return True
        elif len(parts) > 2:
            if parts[1] in FLAT_TYPES:
                return True
    return False


def detect_file_type_from_content(fileobj, peek_size: int = 8192) -> str | None:
    """Detect file type from content (magic numbers and heuristics).

    Args:
        fileobj: File-like object to read from
        peek_size: Number of bytes to read for detection

    Returns:
        Format ID string if detected, None otherwise
    """
    try:
        # Save current position
        original_pos = fileobj.tell()
        peek = fileobj.read(peek_size)
        fileobj.seek(original_pos)

        if len(peek) == 0:
            return None

        # Binary format detection (magic numbers)
        # Parquet
        if peek.startswith(b"PAR1"):
            return "parquet"

        # ORC
        if peek.startswith(b"ORC"):
            return "orc"

        # Vortex
        if peek.startswith(b"VTXF"):
            return "vortex"

        # ZIP-based formats (XLSX, DOCX, etc.)
        if peek.startswith(b"PK\x03\x04"):
            # Check for specific ZIP-based formats
            if b"xl/" in peek[:100] or b"[Content_Types].xml" in peek[:200]:
                return "xlsx"
            if b"word/" in peek[:100]:
                return "docx"  # Not in registry, but detectable
            # Generic ZIP - could be many formats
            return "zip"

        # Arrow/Feather
        if peek.startswith(b"ARROW1"):
            return "arrow"

        # Text format detection (heuristics)
        try:
            # Try to decode as UTF-8
            text = peek.decode("utf-8", errors="ignore")
            text_stripped = text.strip()

            # JSON detection
            if text_stripped.startswith("{") or text_stripped.startswith("["):
                # Try to parse as JSON to confirm
                try:
                    import json

                    json.loads(text_stripped[:1000])  # Try parsing first part
                    return "json"
                except (ValueError, json.JSONDecodeError):
                    # Might be JSONL - check if first line is valid JSON
                    first_line = text_stripped.split("\n")[0].strip()
                    if first_line.startswith("{") or first_line.startswith("["):
                        try:
                            json.loads(first_line)
                            return "jsonl"
                        except (ValueError, json.JSONDecodeError):
                            pass

            # CSV detection (heuristics)
            if "," in text[:100] or "\t" in text[:100]:
                # Check if it looks like CSV (has consistent delimiter)
                lines = text.split("\n")[:5]
                if len(lines) >= 2:
                    # Check if delimiter is consistent
                    delimiters = [",", "\t", "|", ";"]
                    for delim in delimiters:
                        if delim in lines[0] and delim in lines[1]:
                            counts_0 = lines[0].count(delim)
                            counts_1 = lines[1].count(delim)
                            # Allow some variance (headers might have different structure)
                            if abs(counts_0 - counts_1) <= 2 and counts_0 > 0:
                                return "csv" if delim == "," else "tsv" if delim == "\t" else "psv"

            # JSONL detection (each line is JSON)
            lines = text.split("\n")[:10]
            jsonl_count = 0
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                try:
                    import json

                    json.loads(line)
                    jsonl_count += 1
                except (ValueError, json.JSONDecodeError):
                    break
            if jsonl_count >= 3:  # At least 3 valid JSON lines
                return "jsonl"

        except UnicodeDecodeError:
            # Binary format, already checked above
            pass

        return None
    except Exception:
        # If anything fails, return None (fallback to filename detection)
        return None


def detect_file_type(filename: str, fileobj=None) -> FileTypeResult:
    """Detects file type and compression codec from filename and/or content

    Args:
        filename: Path to the file to detect
        fileobj: Optional file-like object for content-based detection

    Returns:
        FileTypeResult dictionary with detection results

    Raises:
        ValueError: If filename is empty or invalid
    """
    if not filename:
        raise ValueError("Filename cannot be empty")

    result: FileTypeResult = {"filename": filename, "success": False, "codec": None, "datatype": None}
    
    # First, try filename-based detection
    parts = filename.lower().rsplit(".", 2)
    if len(parts) == 2:
        if parts[-1] in DATATYPE_REGISTRY:
            result["datatype"] = _datatype_class(parts[-1])
            result["success"] = True
    elif len(parts) > 2:
        if parts[-2] in DATATYPE_REGISTRY and parts[-1] in CODEC_REGISTRY:
            result["datatype"] = _datatype_class(parts[-2])
            result["success"] = True
            result["codec"] = _codec_class(parts[-1])
        elif parts[-1] in DATATYPE_REGISTRY:
            result["datatype"] = _datatype_class(parts[-1])
            result["success"] = True
    
    # If filename detection failed and we have a file object, try content-based detection
    if not result["success"] and fileobj is not None:
        detected_format = detect_file_type_from_content(fileobj)
        if detected_format and detected_format in DATATYPE_REGISTRY:
            result["datatype"] = _datatype_class(detected_format)
            result["success"] = True
    
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
        "filename": filename,
        "success": False,
        "compression": None,
        "codec": None,
        "datatype": None,
    }
    parts = filename.lower().rsplit(".", 2)
    if len(parts) == 2:
        if parts[-1] in CODEC_REGISTRY:
            result["compression"] = _codec_class(parts[-1])
            result["success"] = True
    elif len(parts) > 2:
        if parts[-1] in CODEC_REGISTRY:
            result["compression"] = _codec_class(parts[-1])
            result["success"] = True
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
            f"File not found: '{filename}'. Please check that the file exists and the path is correct."
        )

    result = detect_file_type(filename)
    fileobj = None
    codec = None

    try:
        if result["success"]:
            if result["codec"] is not None:
                try:
                    codec = result["codec"](filename, open_it=True)
                    fileobj = codec.fileobj()
                except Exception as e:
                    raise OSError(
                        f"Failed to open compressed file '{filename}' with codec '{result['codec']}'. Error: {str(e)}"
                    ) from e
        if fileobj is None:
            try:
                fileobj = open(filename, "rb")
            except OSError as e:
                raise OSError(
                    f"Cannot read file '{filename}'. "
                    f"Please check file permissions and that the file is not corrupted. "
                    f"Error: {str(e)}"
                ) from e

        chunk = fileobj.read(limit)
        if not chunk:
            raise ValueError(f"File '{filename}' appears to be empty")

        detected = chardet.detect(chunk)
        if not detected or detected.get("encoding") is None:
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
    mode: Literal["r", "w", "rb", "wb"] = "r",
    engine: Literal["internal", "duckdb"] = "internal",
    codecargs: dict | None = None,
    iterableargs: dict | None = None,
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
        >>> source = open_iterable('data.csv.gz')  # doctest: +SKIP
        >>> with source:  # doctest: +SKIP
        ...     for row in source:  # doctest: +SKIP
        ...         print(row)  # doctest: +SKIP
    """
    import os

    if not filename:
        raise ValueError("Filename cannot be empty")

    if engine not in ["internal", "duckdb"]:
        raise ValueError(f"Engine must be 'internal' or 'duckdb', got '{engine}'")

    # Normalize mode: 'rb' -> 'r', 'wb' -> 'w' for text-based formats
    normalized_mode = "r" if mode in ["r", "rb"] else "w"

    # Check file existence for read mode
    if normalized_mode == "r" and not os.path.exists(filename):
        raise FileNotFoundError(
            f"File not found: '{filename}'. Please check that the file exists and the path is correct."
        )

    if codecargs is None:
        codecargs = {}
    if iterableargs is None:
        iterableargs = {}

    # Try filename-based detection first
    result = detect_file_type(filename)
    
    # If filename detection failed, try content-based detection
    if not result["success"] and normalized_mode == "r":
        try:
            with open(filename, "rb") as f:
                result = detect_file_type(filename, fileobj=f)
        except OSError:
            # Can't read file, fall through to error
            pass

    if not result["success"]:
        from ..exceptions import FormatDetectionError
        
        raise FormatDetectionError(
            filename=filename,
            reason=f"Could not detect file type from filename or content. "
            f"Supported formats: {', '.join(sorted(set(DATATYPE_REGISTRY.keys())))}"
        )

    # Extract file type from filename for DuckDB validation
    parts = filename.lower().rsplit(".", 2)
    detected_filetype = None
    detected_codec = None

    if len(parts) == 2:
        detected_filetype = parts[-1]
    elif len(parts) > 2:
        detected_filetype = parts[-2] if parts[-1] in CODEC_REGISTRY else parts[-1]
        detected_codec = parts[-1] if parts[-1] in CODEC_REGISTRY else None

    # Validate DuckDB engine support
    if engine == "duckdb":
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
    datatype_name = result["datatype"].__name__ if result["datatype"] else "unknown"

    try:
        if result["codec"] is not None and engine != "duckdb":
            codec = result["codec"](filename=filename, mode=mode, options=codecargs)
            iterable = result["datatype"](codec=codec, mode=normalized_mode, options=iterableargs)
        elif engine == "duckdb":
            try:
                from ..engines.duckdb import DuckDBEngineIterable
            except ImportError as e:
                raise ImportError(
                    "DuckDB engine requires the 'duckdb' dependency. Install it with: pip install duckdb"
                ) from e
            iterable = DuckDBEngineIterable(filename=filename, mode=normalized_mode, options=iterableargs)
        else:
            iterable = result["datatype"](filename=filename, mode=normalized_mode, options=iterableargs)
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"File not found: '{filename}'. Please check that the file exists and the path is correct."
        ) from e
    except Exception as e:
        raise RuntimeError(
            f"Failed to open file '{filename}' with format '{datatype_name}' "
            f"(detected type: '{detected_filetype}', codec: '{detected_codec or 'none'}'). "
            f"Error: {str(e)}"
        ) from e

    return iterable
