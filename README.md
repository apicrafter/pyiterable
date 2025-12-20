# Iterable Data

Iterable Data is a Python library for reading and writing data files row by row in a consistent, iterator-based interface. It provides a unified API for working with various data formats (CSV, JSON, Parquet, XML, etc.) similar to `csv.DictReader` but supporting many more formats.

This library simplifies data processing and conversion between formats while preserving complex nested data structures (unlike pandas DataFrames which require flattening).

## Features

- **Unified API**: Single interface for reading/writing multiple data formats
- **Automatic Format Detection**: Detects file type and compression from filename
- **Support for Compression**: Works seamlessly with compressed files
- **Preserves Nested Data**: Handles complex nested structures as Python dictionaries
- **DuckDB Integration**: Optional DuckDB engine for high-performance queries
- **Pipeline Processing**: Built-in pipeline support for data transformation
- **Encoding Detection**: Automatic encoding and delimiter detection for text files
- **Bulk Operations**: Efficient batch reading and writing
- **Context Manager Support**: Use `with` statements for automatic resource cleanup

## Supported File Types

### Core Formats
- **JSON** - Standard JSON files
- **JSONL/NDJSON** - JSON Lines format (one JSON object per line)
- **JSON-LD** - JSON for Linking Data (RDF format)
- **CSV/TSV** - Comma and tab-separated values
- **Annotated CSV** - CSV with type annotations and metadata
- **CSVW** - CSV on the Web (with metadata)
- **PSV/SSV** - Pipe and semicolon-separated values
- **LTSV** - Labeled Tab-Separated Values
- **FWF** - Fixed Width Format
- **XML** - XML files with configurable tag parsing
- **ZIP XML** - XML files within ZIP archives

### Binary Formats
- **BSON** - Binary JSON format
- **MessagePack** - Efficient binary serialization
- **CBOR** - Concise Binary Object Representation
- **UBJSON** - Universal Binary JSON
- **SMILE** - Binary JSON variant
- **Bencode** - BitTorrent encoding format
- **Avro** - Apache Avro binary format
- **Pickle** - Python pickle format

### Columnar & Analytics Formats
- **Parquet** - Apache Parquet columnar format
- **ORC** - Optimized Row Columnar format
- **Arrow/Feather** - Apache Arrow columnar format
- **Lance** - Modern columnar format optimized for ML and vector search
- **Delta Lake** - Delta Lake format
- **Iceberg** - Apache Iceberg format
- **Hudi** - Apache Hudi format

### Database Formats
- **SQLite** - SQLite database files
- **DBF** - dBase/FoxPro database files
- **MySQL Dump** - MySQL dump files
- **PostgreSQL Copy** - PostgreSQL COPY format
- **DuckDB** - DuckDB database files

### Statistical Formats
- **SAS** - SAS data files
- **Stata** - Stata data files
- **SPSS** - SPSS data files
- **R Data** - R RDS and RData files
- **PX** - PC-Axis format

### Geospatial Formats
- **GeoJSON** - Geographic JSON format
- **GeoPackage** - OGC GeoPackage format
- **GML** - Geography Markup Language
- **KML** - Keyhole Markup Language
- **Shapefile** - ESRI Shapefile format

### RDF & Semantic Formats
- **JSON-LD** - JSON for Linking Data
- **RDF/XML** - RDF in XML format
- **Turtle** - Terse RDF Triple Language
- **N-Triples** - Line-based RDF format
- **N-Quads** - N-Triples with context

### Log & Event Formats
- **Apache Log** - Apache access/error logs
- **CEF** - Common Event Format
- **GELF** - Graylog Extended Log Format
- **WARC** - Web ARChive format
- **CDX** - Web archive index format
- **ILP** - InfluxDB Line Protocol

### Email Formats
- **EML** - Email message format
- **MBOX** - Mailbox format
- **MHTML** - MIME HTML format

### Configuration Formats
- **INI** - INI configuration files
- **TOML** - Tom's Obvious Minimal Language
- **YAML** - YAML Ain't Markup Language
- **HOCON** - Human-Optimized Config Object Notation
- **EDN** - Extensible Data Notation

### Office Formats
- **XLS/XLSX** - Microsoft Excel files
- **ODS** - OpenDocument Spreadsheet

### Streaming & Big Data Formats
- **Kafka** - Apache Kafka format
- **Pulsar** - Apache Pulsar format
- **Flink** - Apache Flink format
- **Beam** - Apache Beam format
- **RecordIO** - RecordIO format
- **SequenceFile** - Hadoop SequenceFile
- **TFRecord** - TensorFlow Record format

### Protocol & Serialization Formats
- **Protocol Buffers** - Google Protocol Buffers
- **Cap'n Proto** - Cap'n Proto serialization
- **FlatBuffers** - FlatBuffers serialization
- **FlexBuffers** - FlexBuffers format
- **Thrift** - Apache Thrift format
- **ASN.1** - ASN.1 encoding format
- **Ion** - Amazon Ion format

### Other Formats
- **VCF** - Variant Call Format (genomics)
- **iCal** - iCalendar format
- **LDIF** - LDAP Data Interchange Format
- **TXT** - Plain text files

## Supported Compression Codecs

- **GZip** (.gz)
- **BZip2** (.bz2)
- **LZMA** (.xz, .lzma)
- **LZ4** (.lz4)
- **ZIP** (.zip)
- **Brotli** (.br)
- **ZStandard** (.zst, .zstd)
- **Snappy** (.snappy, .sz)
- **LZO** (.lzo, .lzop)
- **SZIP** (.sz)
- **7z** (.7z)

## Requirements

Python 3.10+

## Installation

```bash
pip install iterabledata
```

Or install from source:

```bash
git clone https://github.com/apicrafter/pyiterable.git
cd pyiterable
pip install .
```

## Quick Start

### Basic Reading

```python
from iterable.helpers.detect import open_iterable

# Automatically detects format and compression
# Using context manager (recommended)
with open_iterable('data.csv.gz') as source:
    for row in source:
        print(row)
        # Process your data here
# File is automatically closed

# Or manually (still supported)
source = open_iterable('data.csv.gz')
for row in source:
    print(row)
source.close()
```

### Writing Data

```python
from iterable.helpers.detect import open_iterable

# Write compressed JSONL file
# Using context manager (recommended)
with open_iterable('output.jsonl.zst', mode='w') as dest:
    for item in my_data:
        dest.write(item)
# File is automatically closed

# Or manually (still supported)
dest = open_iterable('output.jsonl.zst', mode='w')
for item in my_data:
    dest.write(item)
dest.close()
```

## Usage Examples

### Reading Compressed CSV Files

```python
from iterable.helpers.detect import open_iterable

# Read compressed CSV file (supports .gz, .bz2, .xz, .zst, .lz4, .br, .snappy, .lzo)
source = open_iterable('data.csv.xz')
n = 0
for row in source:
    n += 1
    # Process row data
    if n % 1000 == 0:
        print(f'Processed {n} rows')
source.close()
```

### Reading Different Formats

```python
from iterable.helpers.detect import open_iterable

# Read JSONL file
jsonl_file = open_iterable('data.jsonl')
for row in jsonl_file:
    print(row)
jsonl_file.close()

# Read Parquet file
parquet_file = open_iterable('data.parquet')
for row in parquet_file:
    print(row)
parquet_file.close()

# Read XML file (specify tag name)
xml_file = open_iterable('data.xml', iterableargs={'tagname': 'item'})
for row in xml_file:
    print(row)
xml_file.close()

# Read Excel file
xlsx_file = open_iterable('data.xlsx')
for row in xlsx_file:
    print(row)
xlsx_file.close()
```

### Format Detection and Encoding

```python
from iterable.helpers.detect import open_iterable, detect_file_type
from iterable.helpers.utils import detect_encoding, detect_delimiter

# Detect file type and compression
result = detect_file_type('data.csv.gz')
print(f"Type: {result['datatype']}, Codec: {result['codec']}")

# Detect encoding for CSV files
encoding_info = detect_encoding('data.csv')
print(f"Encoding: {encoding_info['encoding']}, Confidence: {encoding_info['confidence']}")

# Detect delimiter for CSV files
delimiter = detect_delimiter('data.csv', encoding=encoding_info['encoding'])

# Open with detected settings
source = open_iterable('data.csv', iterableargs={
    'encoding': encoding_info['encoding'],
    'delimiter': delimiter
})
```

### Format Conversion

```python
from iterable.helpers.detect import open_iterable
from iterable.convert.core import convert

# Simple format conversion
convert('input.jsonl.gz', 'output.parquet')

# Convert with options
convert(
    'input.csv.xz',
    'output.jsonl.zst',
    iterableargs={'delimiter': ';', 'encoding': 'utf-8'},
    batch_size=10000
)

# Convert and flatten nested structures
convert(
    'input.jsonl',
    'output.csv',
    is_flatten=True,
    batch_size=50000
)
```

### Using Pipeline for Data Processing

```python
from iterable.helpers.detect import open_iterable
from iterable.pipeline.core import pipeline

source = open_iterable('input.parquet')
destination = open_iterable('output.jsonl.xz', mode='w')

def transform_record(record, state):
    """Transform each record"""
    # Add processing logic
    out = {}
    for key in ['name', 'email', 'age']:
        if key in record:
            out[key] = record[key]
    return out

def progress_callback(stats, state):
    """Called every trigger_on records"""
    print(f"Processed {stats['rec_count']} records, "
          f"Duration: {stats.get('duration', 0):.2f}s")

def final_callback(stats, state):
    """Called when processing completes"""
    print(f"Total records: {stats['rec_count']}")
    print(f"Total time: {stats['duration']:.2f}s")

pipeline(
    source=source,
    destination=destination,
    process_func=transform_record,
    trigger_func=progress_callback,
    trigger_on=1000,
    final_func=final_callback,
    start_state={}
)

source.close()
destination.close()
```

### Manual Format and Codec Usage

```python
from iterable.datatypes.jsonl import JSONLinesIterable
from iterable.datatypes.bsonf import BSONIterable
from iterable.codecs.gzipcodec import GZIPCodec
from iterable.codecs.lzmacodec import LZMACodec

# Read gzipped JSONL
read_codec = GZIPCodec('input.jsonl.gz', mode='r', open_it=True)
reader = JSONLinesIterable(codec=read_codec)

# Write LZMA compressed BSON
write_codec = LZMACodec('output.bson.xz', mode='wb', open_it=False)
writer = BSONIterable(codec=write_codec, mode='w')

for row in reader:
    writer.write(row)

reader.close()
writer.close()
```

### Using DuckDB Engine

```python
from iterable.helpers.detect import open_iterable

# Use DuckDB engine for CSV, JSON, JSONL files
# Supported formats: csv, jsonl, ndjson, json
# Supported codecs: gz, zstd, zst
source = open_iterable(
    'data.csv.gz',
    engine='duckdb'
)

# DuckDB engine supports totals
total = source.totals()
print(f"Total records: {total}")

for row in source:
    print(row)
source.close()
```

### Bulk Operations

```python
from iterable.helpers.detect import open_iterable

source = open_iterable('input.jsonl')
destination = open_iterable('output.parquet', mode='w')

# Read and write in batches for better performance
batch = []
for row in source:
    batch.append(row)
    if len(batch) >= 10000:
        destination.write_bulk(batch)
        batch = []

# Write remaining records
if batch:
    destination.write_bulk(batch)

source.close()
destination.close()
```

### Working with Excel Files

```python
from iterable.helpers.detect import open_iterable

# Read Excel file (specify sheet or page)
xls_file = open_iterable('data.xlsx', iterableargs={'page': 0})

for row in xls_file:
    print(row)
xls_file.close()

# Read specific sheet in XLSX
xlsx_file = open_iterable('data.xlsx', iterableargs={'page': 'Sheet2'})
```

### XML Processing

```python
from iterable.helpers.detect import open_iterable

# Parse XML with specific tag name
xml_file = open_iterable(
    'data.xml',
    iterableargs={
        'tagname': 'book',
        'prefix_strip': True  # Strip XML namespace prefixes
    }
)

for item in xml_file:
    print(item)
xml_file.close()
```

### Advanced: Converting Compressed XML to Parquet

```python
from iterable.datatypes.xml import XMLIterable
from iterable.datatypes.parquet import ParquetIterable
from iterable.codecs.bz2codec import BZIP2Codec

# Read compressed XML
read_codec = BZIP2Codec('data.xml.bz2', mode='r')
reader = XMLIterable(codec=read_codec, tagname='page')

# Write to Parquet with schema adaptation
writer = ParquetIterable(
    'output.parquet',
    mode='w',
    use_pandas=False,
    adapt_schema=True,
    batch_size=10000
)

batch = []
for row in reader:
    batch.append(row)
    if len(batch) >= 10000:
        writer.write_bulk(batch)
        batch = []

if batch:
    writer.write_bulk(batch)

reader.close()
writer.close()
```

## API Reference

### Main Functions

#### `open_iterable(filename, mode='r', engine='internal', codecargs={}, iterableargs={})`

Opens a file and returns an iterable object.

**Parameters:**
- `filename` (str): Path to the file
- `mode` (str): File mode ('r' for read, 'w' for write)
- `engine` (str): Processing engine ('internal' or 'duckdb')
- `codecargs` (dict): Arguments for codec initialization
- `iterableargs` (dict): Arguments for iterable initialization

**Returns:** Iterable object for the detected file type

#### `detect_file_type(filename)`

Detects file type and compression codec from filename.

**Returns:** Dictionary with `success`, `datatype`, and `codec` keys

#### `convert(fromfile, tofile, iterableargs={}, scan_limit=1000, batch_size=50000, silent=True, is_flatten=False)`

Converts data between formats.

**Parameters:**
- `fromfile` (str): Source file path
- `tofile` (str): Destination file path
- `iterableargs` (dict): Options for iterable
- `scan_limit` (int): Number of records to scan for schema detection
- `batch_size` (int): Batch size for bulk operations
- `silent` (bool): Suppress progress output
- `is_flatten` (bool): Flatten nested structures

### Iterable Methods

All iterable objects support:

- `read()` - Read single record
- `read_bulk(num)` - Read multiple records
- `write(record)` - Write single record
- `write_bulk(records)` - Write multiple records
- `reset()` - Reset iterator to beginning
- `close()` - Close file handles

## Engines

### Internal Engine (Default)

The internal engine uses pure Python implementations for all formats. It supports all file types and compression codecs.

### DuckDB Engine

The DuckDB engine provides high-performance querying capabilities for supported formats:
- **Formats**: CSV, JSONL, NDJSON, JSON
- **Codecs**: GZIP, ZStandard (.zst)
- **Features**: Fast querying, totals counting, SQL-like operations

Use `engine='duckdb'` when opening files:

```python
source = open_iterable('data.csv.gz', engine='duckdb')
```

## Examples Directory

See the [examples](examples/) directory for more complete examples:

- `simplewiki/` - Processing Wikipedia XML dumps

## More Examples and Tests

See the [tests](tests/) directory for comprehensive usage examples and test cases.

## Related Projects

This library is used in:
- [undatum](https://github.com/datacoon/undatum) - Command line data processing tool
- [datacrafter](https://github.com/apicrafter/datacrafter) - Data processing ETL engine

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

### Version 1.0.7 (2024-12-20)
- **Major Format Expansion**: Added support for 50+ new data formats across multiple categories
- **Enhanced Compression**: Added LZO, Snappy, and SZIP codec support
- **CI/CD**: Added GitHub Actions workflows for automated testing and deployment
- **Documentation**: Complete documentation site with Docusaurus
- **Testing**: Comprehensive test suite for all formats

### Version 1.0.6
- Comprehensive documentation enhancements
- GitHub Actions release workflow
- Improved examples and use cases

### Version 1.0.5
- DuckDB engine support
- Enhanced format detection
- Pipeline processing framework
- Bulk operations support
