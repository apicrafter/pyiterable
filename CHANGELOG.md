# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


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

