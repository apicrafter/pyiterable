# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]

### Added
- **Database Engine Support**: Read-only access to SQL and NoSQL databases as iterable data sources
  - **PostgreSQL Support**: Full support for PostgreSQL databases via `psycopg2-binary`
    - Connection via connection strings or existing connection objects
    - Streaming queries using server-side cursors for memory efficiency
    - Table name auto-query: automatically builds `SELECT * FROM table` queries
    - Query parameters: `query`, `schema`, `columns`, `filter`, `batch_size`
    - Read-only transactions by default for safety
    - `list_tables()` helper function for database introspection
  - **Database Driver Architecture**: Extensible driver registry system
    - `DBDriver` abstract base class for database-specific implementations
    - Driver registry with `register_driver()`, `get_driver()`, `list_drivers()`
    - `DatabaseIterable` wrapper providing `BaseIterable` interface for database sources
  - **Integration with Existing Features**:
    - Database sources work with `open_iterable()` via `engine` parameter
    - Database → file conversion via `convert()` function
    - Database sources in data pipelines via `pipeline()` function
    - DataFrame bridges (`.to_pandas()`, `.to_polars()`, `.to_dask()`) work with database sources
  - **Optional Dependencies**: New dependency groups for database support
    - `db`: All database engines (`psycopg2-binary`, `pymongo`, `elasticsearch`, `pymysql`, `pyodbc`)
    - `db-sql`: SQL databases only (`psycopg2-binary`, `pymysql`, `pyodbc`)
    - `db-nosql`: NoSQL databases only (`pymongo`, `elasticsearch`)
  - **Usage Examples**:
    ```python
    from iterable.helpers.detect import open_iterable
    
    # Read from PostgreSQL database
    with open_iterable(
        'postgresql://user:password@localhost:5432/mydb',
        engine='postgres',
        iterableargs={'query': 'users'}
    ) as source:
        for row in source:
            print(row)
    
    # Convert database to file
    from iterable.convert import convert
    convert(
        fromfile='postgresql://localhost/mydb',
        tofile='users.parquet',
        iterableargs={'engine': 'postgres', 'query': 'users'}
    )
    ```
  - **Planned Database Support**: MySQL/MariaDB, Microsoft SQL Server, SQLite, MongoDB, Elasticsearch/OpenSearch
  - **Documentation**: Comprehensive database engine documentation in `docs/docs/api/database-engines.md`

### Changed
- `open_iterable()` now accepts database engines via `engine` parameter (e.g., `'postgres'`, `'mysql'`, `'mongo'`)
- `convert()` now supports database sources (database → file conversion)
- `pipeline()` now supports database sources as input

## [1.0.11] - 2026-01-25

### Added
- **Atomic Writes for Safer File Operations**: Production-safe file writing with temporary files and atomic renames
  - **New `atomic` Parameter**: Added to `convert()`, `bulk_convert()`, and `pipeline()` functions
    - When `atomic=True`, writes to temporary file (`.tmp` suffix) and atomically renames to final destination
    - Ensures output files are never left in partially written state
    - Original files preserved on failure or interruption
    - Temporary files automatically cleaned up on both success and failure
  - **Production Safety**: Prevents data corruption from crashes, interruptions, or mid-process failures
  - **Backward Compatible**: Defaults to `atomic=False` for existing code compatibility
  - **Usage Examples**:
    ```python
    from iterable.convert.core import convert
    
    # Convert with atomic writes for production safety
    convert('input.csv', 'output.parquet', atomic=True)
    
    # Atomic writes in pipelines
    from iterable.pipeline import pipeline
    pipeline(source=source, destination=dest, process_func=func, atomic=True)
    ```
  - **Limitations**: Atomic writes only work on same filesystem (uses `os.replace()`)
- **Bulk File Conversion**: Convert multiple files at once using glob patterns, directories, or file lists
  - **New `bulk_convert()` Function**: Batch conversion of multiple files with aggregated results
    - Supports glob patterns (e.g., `'data/raw/*.csv.gz'`)
    - Supports directory paths (converts all files in directory)
    - Supports single file paths
    - Reuses existing `convert()` function internally for each file
  - **Flexible Output Naming**: 
    - Filename patterns with placeholders: `{name}`, `{stem}`, `{ext}`
    - Extension replacement via `to_ext` parameter
    - Example: `pattern='{name}.parquet'` or `to_ext='parquet'`
  - **Aggregated Results**: `BulkConversionResult` object with:
    - Total files processed, successful, and failed
    - Total rows converted across all files
    - Per-file conversion results
    - Aggregated errors and throughput metrics
  - **Error Resilience**: Continues processing remaining files if one fails
  - **All `convert()` Parameters Supported**: All parameters (batch_size, iterableargs, is_flatten, etc.) are passed through
  - **Usage Examples**:
    ```python
    from iterable.convert.core import bulk_convert
    
    # Convert all CSV files matching glob pattern
    result = bulk_convert('data/raw/*.csv.gz', 'data/processed/', to_ext='parquet')
    
    # Convert with custom filename pattern
    result = bulk_convert('data/*.csv', 'output/', pattern='{name}.parquet')
    
    # Convert entire directory
    result = bulk_convert('data/raw/', 'data/processed/', to_ext='parquet')
    
    # Access results
    print(f"Converted {result.successful_files}/{result.total_files} files")
    print(f"Total rows: {result.total_rows_out}")
    for file_result in result.file_results:
        if file_result.success:
            print(f"✓ {file_result.source_file}")
        else:
            print(f"✗ {file_result.source_file}: {file_result.error}")
    ```
- **Observability Features**: Progress tracking, metrics, and logging for conversions and pipelines
  - **Progress Callbacks**: Custom callbacks for real-time progress tracking
    - `convert()` now accepts `progress` parameter for periodic progress updates
    - `pipeline()` now accepts `progress` parameter for periodic progress updates
    - Callbacks receive stats dictionary with rows processed, elapsed time, and throughput
  - **Built-in Progress Bars**: Visual progress indicators using `tqdm`
    - `convert()` now supports `show_progress` parameter for automatic progress bars
    - Progress bars respect `silent` parameter and gracefully handle missing `tqdm`
  - **Standardized Metrics Objects**: Structured metrics for programmatic access
    - `convert()` now returns `ConversionResult` object with:
      - `rows_in`, `rows_out`, `elapsed_seconds`, `bytes_read`, `bytes_written`, `errors`
    - `pipeline()` now returns `PipelineResult` object with:
      - `rows_processed`, `elapsed_seconds`, `throughput`, `exceptions`, `nulls`
      - Supports both attribute access and dictionary-style access for backward compatibility
  - **Usage Examples**:
    ```python
    # Progress callback
    def cb(stats):
        print(f"Progress: {stats['rows_read']} rows read")
    
    result = convert('input.csv', 'output.parquet', progress=cb)
    print(f"Converted {result.rows_out} rows in {result.elapsed_seconds:.2f}s")
    
    # Progress bar
    result = convert('input.jsonl', 'output.parquet', show_progress=True)
    
    # Pipeline metrics
    result = pipeline(source, destination, process_func=transform, progress=cb)
    print(f"Throughput: {result.throughput:.0f} rows/second")
    ```
  - **Backward Compatibility**: All changes are additive and backward compatible
    - Existing code using `convert()` without return value handling continues to work
    - Existing code using `pipeline()` with dictionary-style stats access continues to work
- **Cloud Storage Support**: Direct access to cloud object storage (S3, GCS, Azure) via URI schemes
  - **Supported Providers**:
    - Amazon S3: `s3://` and `s3a://` schemes
    - Google Cloud Storage: `gs://` and `gcs://` schemes
    - Azure Blob Storage: `az://`, `abfs://`, and `abfss://` schemes
  - **Features**:
    - Transparent integration with existing format detection and codec logic
    - Works with all compression codecs (gzip, zstd, bz2, etc.)
    - Streaming support for memory-efficient processing
    - Authentication via environment variables or `storage_options` parameter
  - **Optional Dependencies**: New `cloud` extra group in `pyproject.toml`
    - Install with: `pip install iterabledata[cloud]`
    - Includes: `fsspec`, `s3fs`, `gcsfs`, `adlfs`
  - **Usage Examples**:
    ```python
    # Read from S3
    with open_iterable('s3://bucket/data.csv') as source:
        for row in source:
            print(row)
    
    # Read compressed file from GCS
    with open_iterable('gs://bucket/data.jsonl.gz') as source:
        for row in source:
            print(row)
    
    # Write to Azure with authentication
    with open_iterable(
        'az://container/output.jsonl',
        mode='w',
        iterableargs={'storage_options': {'connection_string': '...'}}
    ) as dest:
        dest.write({'name': 'Alice', 'age': 30})
    ```
  - **Note**: DuckDB engine does not support cloud storage URIs; use `engine='internal'` (default)
  - All existing functionality works identically for cloud storage as for local files
- **DataFrame Bridges**: Convenient methods to convert iterable data to Pandas, Polars, and Dask DataFrames
  - **Pandas Bridge** (`to_pandas()` method):
    - Convert iterable to pandas DataFrame: `df = source.to_pandas()`
    - Chunked processing: `for df in source.to_pandas(chunksize=100_000): ...`
    - Preserves nested data structures as dict/list columns
  - **Polars Bridge** (`to_polars()` method):
    - Convert iterable to Polars DataFrame: `df = source.to_polars()`
    - Chunked processing: `for df in source.to_polars(chunksize=100_000): ...`
    - Efficient memory usage and modern API
  - **Dask Bridge** (`to_dask()` method and helper function):
    - Single file: `ddf = source.to_dask()`
    - Multi-file support: `ddf = to_dask(['file1.csv', 'file2.jsonl'])` - automatically detects formats
    - Builds Dask computation graph from multiple files
    - Supports out-of-core and distributed processing
  - **Optional Dependencies**: New `dataframes` extra group in `pyproject.toml`
    - Install with: `pip install iterabledata[dataframes]`
    - Includes: `pandas`, `polars`, `dask[dataframe]`
  - All methods raise helpful `ImportError` messages if dependencies are missing
  - Works with all supported formats (CSV, JSONL, Parquet, etc.)
  - Example usage:
    ```python
    # Pandas
    with open_iterable('data.csv.gz') as src:
        df = src.to_pandas()
    
    # Polars with chunking
    with open_iterable('large.csv') as src:
        for df in src.to_polars(chunksize=100_000):
            process(df)
    
    # Dask multi-file
    from iterable.helpers.bridges import to_dask
    ddf = to_dask(['file1.csv', 'file2.jsonl', 'file3.parquet'])
    result = ddf.groupby('category').sum().compute()
    ```
- **DuckDB Engine Pushdown Optimizations**: Advanced query optimizations for DuckDB engine
  - **Column Projection Pushdown** (`columns` parameter in `iterableargs`):
    - Only read specified columns from disk, reducing I/O and memory usage
    - Example: `iterableargs={'columns': ['name', 'age']}`
    - Works with CSV, JSONL, JSON, and Parquet formats
  - **Filter Pushdown** (`filter` parameter in `iterableargs`):
    - Filter rows at the database level before reading into Python
    - Supports SQL string filters: `iterableargs={'filter': "age > 18 AND status = 'active'"}`
    - Supports Python callable filters: `iterableargs={'filter': lambda row: row['age'] > 18}`
    - Python callables fall back to Python-side filtering if not translatable to SQL
  - **Direct SQL Query Support** (`query` parameter in `iterableargs`):
    - Execute full SQL queries while maintaining iterator interface
    - Example: `iterableargs={'query': 'SELECT name, age FROM read_csv_auto(\'file.csv\') WHERE age > 18 ORDER BY age DESC LIMIT 100'}`
    - Validates queries are read-only (rejects DDL/DML operations)
    - When `query` is provided, `columns` and `filter` parameters are ignored
  - **Format Detection Improvements**:
    - DuckDB engine now correctly detects file format and uses appropriate DuckDB function
    - CSV files use `read_csv_auto()`
    - JSONL/NDJSON files use `read_json_auto()`
    - JSON files use `read_json_auto()`
    - Parquet files use `read_parquet()`
  - **Combined Pushdown**: Support combining `columns` and `filter` for maximum efficiency
  - **Backward Compatible**: All changes are additive; existing code continues to work
  - Example usage:
    ```python
    # Column projection + filter pushdown
    with open_iterable(
        'data.csv',
        engine='duckdb',
        iterableargs={
            'columns': ['name', 'age'],
            'filter': 'age > 18'
        }
    ) as src:
        for row in src:
            process(row)
    
    # Direct SQL query
    with open_iterable(
        'data.parquet',
        engine='duckdb',
        iterableargs={
            'query': 'SELECT name FROM read_parquet(\'data.parquet\') WHERE age > 18'
        }
    ) as src:
        for row in src:
            process(row)
    ```
- **Error Handling Controls**: Configurable error policies and enhanced error context for robust data processing
  - **Configurable Error Policy** (`on_error` parameter in `iterableargs`):
    - `'raise'` (default) - Raise exceptions immediately (current behavior)
    - `'skip'` - Silently skip malformed records and continue processing
    - `'warn'` - Log warnings and continue processing (uses Python's `warnings` module)
  - **Error Logging** (`error_log` parameter in `iterableargs`):
    - Supports file path (string) or file-like object
    - Structured JSON log format with timestamp, filename, row number, byte offset, error message, and original line
    - Errors are logged regardless of error policy (useful for later analysis)
  - **Enhanced Error Context**:
    - `FormatParseError` and `ReadError` now include contextual attributes:
      - `filename` - File where error occurred
      - `row_number` - Row number (1-indexed, header excluded)
      - `byte_offset` - Byte offset in file where error occurred
      - `original_line` - Original line content that failed to parse (for text formats)
    - Error messages automatically include all available context
  - **Format Support**: Error handling implemented for CSV and JSONL formats
    - Other formats will benefit from base error handling infrastructure
  - **Backward Compatible**: Default behavior (`on_error='raise'`) maintains existing functionality
  - Example usage:
    ```python
    with open_iterable(
        'data.csv',
        iterableargs={'on_error': 'skip', 'error_log': 'errors.log'}
    ) as src:
        for row in src:
            process(row)
    ```
- **Type Hints and Typed Helpers**: Comprehensive type annotations and type-safe helper functions for modern Python projects
  - **Type Aliases** (`iterable/types.py`): Common type aliases for better code readability
    - `Row = dict[str, Any]` - Type alias for data rows
    - `IterableArgs = dict[str, Any]` - Type alias for iterable configuration arguments
    - `CodecArgs = dict[str, Any]` - Type alias for codec configuration arguments
  - **Complete Type Hints**: Full type annotations across the public API
    - `open_iterable()` - All parameters and return type annotated
    - `BaseIterable` methods - `read()`, `write()`, `read_bulk()`, `write_bulk()`, and all other methods
    - `convert()` - All parameters annotated with proper types
    - `pipeline()` - Complete type annotations for all parameters and return values
  - **Type Marker File**: Added `py.typed` marker file to indicate package supports type checking
    - Enables mypy, pyright, and other type checkers to use the provided type hints
  - **Typed Helper Functions** (`iterable/helpers/typed.py`):
    - `as_dataclasses(iterable, dataclass_type)` - Converts dict-based rows to dataclass instances
      - Provides type safety and IDE autocomplete for dataclass fields
      - Automatically filters extra fields not in the dataclass definition
    - `as_pydantic(iterable, model_type, validate=True)` - Converts rows to Pydantic model instances
      - Optional validation against Pydantic schemas
      - Catches schema issues early with helpful error messages
      - Requires `pydantic>=2.0.0` (install with `pip install iterabledata[pydantic]`)
  - **Improved IDE Support**: Type hints enable better autocomplete, type checking, and documentation in modern IDEs
  - All type hints are backward compatible and don't affect runtime behavior
- **Vortex Format Support**: Added support for reading and writing Vortex columnar data files
  - **Vortex Format** (`iterable/datatypes/vortex.py`) - Modern columnar format with fast random access
    - Supports reading and writing Vortex files (`.vortex`, `.vtx` extensions)
    - Automatic format detection by extension and magic number (`VTXF`)
    - Uses `vortex-data` library for core operations
    - Integrates with PyArrow for data conversion (dict ↔ Vortex arrays)
    - Supports bulk operations and totals counting
    - Requires `vortex-data>=0.56.0` package (install with `pip install iterabledata[vortex]`)
    - **Note**: `vortex-data` requires Python ≥3.11, but the library gracefully handles this version constraint

## [1.0.10] - 2026-01-13

### Added
- **Enhanced Format Detection**: Added content-based format detection using magic numbers and heuristics
  - **Magic Number Detection**: Detects binary formats by reading file headers (magic numbers)
    - `PAR1` → Parquet format
    - `ORC` → ORC format
    - `PK\x03\x04` → ZIP-based formats (XLSX, DOCX, etc.)
    - `ARROW1` → Arrow/Feather format
  - **Content Heuristic Detection**: Detects text formats using content analysis
    - JSON detection: Files starting with `{` or `[`
    - CSV detection: Files with consistent delimiter patterns (commas, tabs, pipes)
    - JSONL detection: Files where each line is valid JSON
  - **Combined Detection Strategy**: Uses filename extension as primary method, content detection as fallback
    - Works for files without extensions
    - Works for streams without filenames
    - Handles files with incorrect extensions
  - **Stream Support**: Content-based detection works with non-seekable streams
  - See `iterable.helpers.detect.detect_file_type_from_content()` for details
- **Exception Hierarchy**: Added comprehensive exception hierarchy for better error handling
  - **Base Exceptions**: `IterableDataError` - Base exception for all library errors
  - **Format Exceptions**: `FormatError`, `FormatNotSupportedError`, `FormatDetectionError`, `FormatParseError`
  - **Codec Exceptions**: `CodecError`, `CodecNotSupportedError`, `CodecDecompressionError`, `CodecCompressionError`
  - **Read/Write Exceptions**: `ReadError`, `WriteError`, `StreamingNotSupportedError`
  - **Resource Exceptions**: `ResourceError`, `StreamNotSeekableError`, `ResourceLeakError`
  - All exceptions include error codes for programmatic handling
  - See `iterable.exceptions` module for details
- **Format Capability Reporting**: Added programmatic API to query format capabilities
  - `get_format_capabilities(format_id)` - Get all capabilities for a specific format
  - `list_all_capabilities()` - Get capabilities for all registered formats
  - `get_capability(format_id, capability)` - Query a specific capability for a format
  - Capabilities include: readable, writable, bulk_read, bulk_write, totals, streaming, flat_only, tables, compression, nested
  - Returns boolean values (True/False) or None for unknown/unsupported capabilities
  - Handles optional dependencies gracefully
  - See `iterable.helpers.capabilities` module for details
- **Table Listing Support**: Added `list_tables()` and `has_tables()` methods to discover available tables, sheets, datasets, and other named collections in multi-table formats
  - **Excel formats** (XLSX, XLS, ODS): List sheet names
  - **Database formats** (SQLite, DuckDB): List table names
  - **Scientific formats** (HDF5, NetCDF): List dataset/variable names
  - **Geospatial formats** (GeoPackage): List layer names
  - **Statistical formats** (RData): List R object names
  - **Markup formats** (HTML, XML): List table identifiers (HTML) or tag names (XML)
  - **Archive formats** (ZIPXML): List XML filenames within ZIP archives
  - **Data lake formats** (Iceberg, Hudi): List table names from catalogs
  - Methods can be called on instances (reuses open connections) or with filename parameter
  - Returns `list[str]` of names, empty list `[]` for empty files, or `None` for unsupported formats
  - See [BaseIterable Methods](/api/base-iterable#list_tables) documentation for details

### Improved
- **Format Detection**: Enhanced `detect_file_type()` and `open_iterable()` to use content-based detection when filename detection fails
  - Automatically falls back to magic number detection for binary formats
  - Automatically falls back to heuristic detection for text formats
  - Better error messages with `FormatDetectionError` exception
  - Improved support for files without extensions or with incorrect extensions

## [1.0.9] - 2026-01-12

### Added
- **New Data Format Support**: Added support for 6 new data formats across scientific, geospatial, web feed, CAD, and network analysis domains
  - **NetCDF** (`iterable/datatypes/netcdf.py`) - Network Common Data Form for scientific array data
    - Supports reading multi-dimensional scientific data
    - Automatic dimension detection with configurable iteration
    - Requires `netCDF4` package (install with `pip install iterabledata[netcdf]`)
  - **Mapbox Vector Tiles** (`iterable/datatypes/mvt.py`) - MVT/PBF format for geospatial vector tiles
    - Decodes Mapbox Vector Tiles with layer support
    - Extracts features with geometry and properties
    - Requires `mapbox-vector-tile` package (install with `pip install iterabledata[geospatial]`)
  - **TopoJSON** (`iterable/datatypes/topojson.py`) - Topology-preserving GeoJSON extension
    - Converts TopoJSON topology to GeoJSON features
    - Supports multiple objects within a topology
    - Requires `topojson` package (install with `pip install iterabledata[geospatial]`)
  - **Atom/RSS Feeds** (`iterable/datatypes/feed.py`) - Web feed formats
    - Unified support for both Atom and RSS feeds
    - Extracts entries with metadata, content, and tags
    - Requires `feedparser` package (install with `pip install iterabledata[feed]`)
  - **DXF** (`iterable/datatypes/dxf.py`) - AutoCAD Drawing Exchange Format
    - Reads CAD entities (lines, circles, polylines, text, etc.)
    - Extracts geometry and layer information
    - Requires `ezdxf` package (install with `pip install iterabledata[dxf]`)
  - **PCAP/PCAPNG** (`iterable/datatypes/pcap.py`) - Packet capture format for network analysis
    - Supports both PCAP and PCAPNG formats
    - Extracts packet timestamps and data
    - Requires `dpkt` package (install with `pip install iterabledata[pcap]`)
- **Format Detection**: Updated `iterable/helpers/detect.py` with new file extensions:
  - `.nc`, `.netcdf` for NetCDF files
  - `.mvt`, `.pbf` for Mapbox Vector Tiles
  - `.topojson` for TopoJSON files
  - `.atom`, `.rss` for web feeds
  - `.dxf` for AutoCAD files
  - `.pcap`, `.pcapng` for packet capture files

### Improved
- All new formats support the `totals()` method for counting records
- Enhanced format detection with better extension mapping
- Consistent error handling with helpful installation messages

## [1.0.8] - 2026-01-05

### Added
- **AI Agent Integration Guides**: 
  - `AGENTS.md` - Comprehensive guide for integrating IterableData with LangChain, CrewAI, and AutoGen agents
  - `GEMINI.md` - Complete guide for using IterableData with Google Gemini AI for data processing and analysis
- **Documentation Enhancements**:
  - Added `docs/docs/api/capabilities.md` - Capability matrix showing read/write/bulk/totals/streaming support by format
  - Updated Docusaurus configuration and sidebars
- **Development Tools**:
  - `dev/benchmarks/bench_import_open.py` - Benchmarking tool for import performance
  - `dev/scripts/inspect_zip.py` - Utility for inspecting ZIP file contents
  - `dev/scripts/verify_output.py` - Output verification script
  - Moved `find_missing_fixtures.py` to `dev/scripts/` directory
- **Examples**:
  - `examples/zipxml/` - New example demonstrating ZIP XML processing with README
  - Updated existing examples with improvements
- **Test Data**:
  - Added `testdata/test_zipxml.zip` - Test fixture for ZIP XML processing
  - Added `tests/test_property_roundtrip.py` - New test for property roundtrip functionality

### Improved
- **Format Detection**: Enhanced `iterable/helpers/detect.py` with improved detection logic and better error handling
- **Compression Codecs**: Updated all codec implementations (brotli, bz2, gzip, lz4, lzma, lzo, raw, snappy, szip, zip, zstd) with consistent patterns and improved error handling
- **Data Type Handlers**: Refactored all datatype modules for better consistency, error handling, and code organization
- **Conversion Core**: Improved `iterable/convert/core.py` with better format handling
- **Pipeline Processing**: Enhanced `iterable/pipeline/core.py` with improved state management and error handling
- **Helper Utilities**: Updated `iterable/helpers/utils.py` and `iterable/helpers/schema.py` with new functionality
- **Base Classes**: Improved `iterable/base.py` with better abstraction and error handling
- **Test Suite**: Comprehensive updates to all test files with improved fixtures and test coverage
- **Test Data**: Updated compression test fixtures (br, bz2, gz, lz4, xz, zst) with corrected data
- **Documentation**: Updated installation instructions and GitHub Pages setup documentation

### Fixed
- Removed obsolete test data files (`test_convert_csv_json.json`, `test_mysqldump_*.sql`, `test_warc_roundtrip.warc`)
- Fixed compression codec implementations for better consistency
- Improved error messages and handling across all modules

## [1.0.7] - 2024-12-15

### Added
- **Comprehensive Documentation**: Enhanced README.md with detailed usage examples, API reference, and comprehensive guides
- **GitHub Actions Release Workflow**: Automatic release generation with version verification, testing, and PyPI publishing support
- **Improved Examples**: Added examples for all major use cases including format conversion, pipeline processing, and DuckDB integration

### Improved
- **Documentation Structure**: Better organized README with clear sections for quick start, usage examples, and API reference
- **Release Process**: Automated CI/CD pipeline for building and publishing releases

### Fixed
- Documentation examples and code snippets updated for accuracy

## [1.0.5] - Previous Release

### Added
- DuckDB engine support
- Enhanced format detection
- Improved compression codec handling
- Pipeline processing framework
- Bulk operations support

