# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [1.0.8] - 2025-12-20

### Added
- **Extensive Format Support**: Added support for 50+ new data formats including:
  - **Geospatial Formats**: GeoJSON, GeoPackage, GML, KML, Shapefile
  - **RDF Formats**: JSON-LD, RDF/XML, Turtle, N-Triples, N-Quads
  - **Log Formats**: Apache Log, CEF, GELF, WARC, CDX
  - **Email Formats**: EML, MBOX, MHTML
  - **Binary Formats**: MessagePack, CBOR, UBJSON, SMILE, Bencode, FlatBuffers, FlexBuffers, Thrift, Cap'n Proto, Protocol Buffers, ASN.1
  - **Columnar Formats**: Delta Lake, Iceberg, Hudi, Lance
  - **Database Formats**: SQLite, MySQL Dump, PostgreSQL Copy, R Data (RDS, RData)
  - **Statistical Formats**: SPSS, Stata, SAS, PX
  - **Web Formats**: CSVW (CSV on the Web), INI, HOCON, TOML, YAML, EDN
  - **Streaming Formats**: Kafka, Pulsar, Flink, Beam, RecordIO, SequenceFile, TFRecord
  - **Other Formats**: VCF, iCal, LDIF, ILP (InfluxDB Line Protocol), Fixed Width (FWF), PSV/SSV, LTSV, TXT, ODS
- **Annotated CSV Support**: Added support for CSV files with type annotations and metadata
- **Compression Codecs**: Added support for LZO, Snappy, and SZIP compression formats
- **GitHub Actions Workflows**: Added CI/CD workflows for linting, testing, and documentation deployment
- **Comprehensive Test Suite**: Added test coverage for all new formats with fixtures and test data
- **Documentation**: Complete Docusaurus-based documentation site with format-specific guides, API reference, and use cases
- **Performance Optimization Analysis**: Comprehensive performance analysis document identifying critical bottlenecks and optimization opportunities
- **Development Documentation**: Added performance optimization guide in `dev/docs/PERFORMANCE_OPTIMIZATIONS.md`

### Improved
- **Format Detection**: Enhanced automatic format detection to support all new formats
- **Documentation**: Complete documentation restructure with Docusaurus, format templates, and comprehensive guides
- **Code Organization**: Better structured codebase with consistent patterns across all datatypes
- **Test Infrastructure**: Improved test fixtures and utilities for format testing

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

