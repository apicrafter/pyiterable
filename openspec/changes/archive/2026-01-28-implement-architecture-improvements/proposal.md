# Change: Implement Architecture Improvements

## Why
The IterableData library has a solid foundation but contains **47 critical issues** across **12 categories** that limit production readiness, scalability, and maintainability. Comprehensive analysis reveals:

- **Memory anti-patterns**: Formats like JSON load entire files into memory, contradicting the streaming design philosophy
- **Inefficient bulk operations**: `read_bulk()` implementations provide no performance benefit
- **Poor error handling**: Generic exceptions make error handling impossible for users
- **Limited format detection**: Relies solely on filename extensions, failing for streams and files without extensions
- **Incomplete implementations**: Missing write support, base class design issues, resource management problems

These issues impact core functionality, usability, and the library's ability to handle production-scale workloads. The architecture improvement plan provides a prioritized roadmap to address these systematically.

## What Changes

### Phase 1: Critical Fixes (P0)
- **Memory Anti-Pattern Fixes**: Implement streaming parsers for JSON, GeoJSON, TopoJSON and audit all formats for memory-loading patterns
- **Bulk Operation Optimization**: Refactor `read_bulk()` implementations across all formats to use true bulk I/O operations
- **Exception Hierarchy**: Create proper exception hierarchy (`IterableDataError`, `FormatError`, `CodecError`, etc.) replacing generic exceptions
- **Content-Based Detection**: Implement magic number detection and content-based heuristics for format detection

### Phase 2: High Priority (P1)
- **DuckDB Engine Refactoring**: Simplify caching logic, use parameterized queries, optimize DataFrame conversions
- **Base Class Design**: Convert to ABC with proper abstract methods, fix method signatures, add default implementations
- **Resource Management**: Improve exception handling in `reset()`, add seekable stream validation, prevent resource leaks
- **Write Implementation Documentation**: Mark read-only formats, add capability metadata, provide clear error messages

### Phase 3: Medium Priority (P2)
- **Type Hint Coverage**: Add complete type hints to all public methods, enable strict mypy checking
- **Codec Integration Simplification**: Refactor complex initialization logic using builder pattern or factory methods
- **Testing Expansion**: Add performance benchmarks, memory profiling tests, stress tests for large files
- **Documentation Improvements**: Standardize examples, add error handling sections, complete parameter documentation

### Phase 4: Lower Priority (P3)
- **API Design Improvements**: Async/await support, progress callbacks, validation hooks, plugin system
- **Performance Optimizations**: Connection pooling, read-ahead caching, parallel processing
- **Developer Experience**: Debug mode, improved error messages, logging framework

**BREAKING**: Exception hierarchy changes may break existing error handling code that catches generic exceptions. Migration guide will be provided.

## Impact
- **Affected Specs**: 
  - `format-detection` (content-based detection)
  - `streaming-processing` (memory-efficient streaming)
  - `error-handling` (exception hierarchy)
  - `bulk-operations` (optimized bulk I/O)
  - `format-capabilities` (updated capability reporting)
- **Affected Code**: 
  - All format implementations in `iterable/datatypes/` (90+ files)
  - Base classes: `iterable/base.py`
  - Detection: `iterable/helpers/detect.py`
  - Engines: `iterable/engines/duckdb.py`
  - New: `iterable/exceptions.py`
- **User Impact**:
  - Improved memory efficiency for large files
  - Better error messages and exception handling
  - Faster bulk operations
  - More reliable format detection
  - Breaking changes in exception handling (migration guide provided)
- **Timeline**: 16 weeks total (4 weeks for critical fixes, 4 weeks for high priority, 4 weeks for medium priority, 4 weeks for polish)
- **Estimated Effort**: 320-435 hours total
