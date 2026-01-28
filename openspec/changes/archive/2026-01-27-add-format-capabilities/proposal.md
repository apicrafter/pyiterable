# Change: Add Format Capability Reporting

## Why
Users of IterableData need to understand what capabilities each data format supports before choosing a format or attempting operations. Currently, capabilities are scattered across:
- Individual format classes (methods like `has_totals()`, `has_tables()`, `is_flatonly()`, `is_streaming()`)
- Documentation (capability matrix in docs)
- Trial and error (attempting operations and catching exceptions)

This makes it difficult for users to:
- Discover which formats support specific features (e.g., "which formats can I write to?", "which formats support totals?")
- Make informed decisions about format selection
- Understand format limitations programmatically
- Build format-agnostic code that adapts to available capabilities

A centralized capability reporting system will provide a unified way to query format capabilities, improving developer experience and enabling better tooling and documentation generation.

## What Changes
- **New Capability Reporting API**: Add functions to query format capabilities:
  - `get_format_capabilities(format_id: str) -> dict` - Returns capability dict for a specific format
  - `list_all_capabilities() -> dict[str, dict]` - Returns capabilities for all registered formats
  - `get_capability(format_id: str, capability: str) -> bool | None` - Query a specific capability
- **Capability Model**: Define a standardized set of capabilities to track:
  - `readable` - Format supports reading data (`read()` method)
  - `writable` - Format supports writing data (`write()` method)
  - `bulk_read` - Format supports bulk reading (`read_bulk()` method)
  - `bulk_write` - Format supports bulk writing (`write_bulk()` method)
  - `totals` - Format supports row count totals (`has_totals()` returns True)
  - `streaming` - Format supports streaming (doesn't load entire file into memory)
  - `flat_only` - Format only supports flat (non-nested) data structures
  - `tables` - Format supports multiple tables/sheets/datasets (`has_tables()` returns True)
  - `compression` - Format supports compression codecs (GZIP, BZIP2, etc.)
  - `nested` - Format can preserve nested data structures (opposite of flat_only)
- **Implementation**: 
  - Add capability detection logic that introspects format classes
  - Implement capability reporting functions in `iterable/helpers/capabilities.py` (new module)
  - Use static method calls and method existence checks to determine capabilities
  - Handle optional dependencies gracefully (return None or False when dependencies missing)
- **Documentation**: Update documentation with capability reporting examples
- **Tests**: Add comprehensive tests for capability detection across all formats

## Implementation Design
- **Location**: New module `iterable/helpers/capabilities.py` to keep capability logic separate from detection
- **Detection Strategy**: 
  - Use introspection to check for method existence (`hasattr()`, `callable()`)
  - Call static methods like `has_totals()`, `has_tables()`, `is_flatonly()` when available
  - Check for `read()`, `write()`, `read_bulk()`, `write_bulk()` methods
  - For streaming: check `is_streaming()` method or infer from format characteristics
  - For compression: check if format works with codecs via `detect.py` logic
- **Return Format**: Dictionary with boolean values (True/False) or None for unknown/unsupported
  ```python
  {
    "readable": True,
    "writable": True,
    "bulk_read": True,
    "bulk_write": True,
    "totals": True,
    "streaming": True,
    "flat_only": False,
    "tables": False,
    "compression": True,
    "nested": True
  }
  ```
- **Error Handling**: 
  - Return None for capabilities that cannot be determined (e.g., missing dependencies)
  - Raise `ValueError` for unknown format IDs
  - Handle ImportError gracefully when optional dependencies are missing
- **Performance**: Cache capability results per format class to avoid repeated introspection
- **Integration**: Can be used by documentation generators, CLI tools, and user code

## Impact
- **New Capability**: `format-capabilities` (new capability for reporting format features)
- **Affected Files**:
  - `iterable/helpers/capabilities.py` (new file)
  - `iterable/helpers/__init__.py` (export capability functions)
  - `iterable/helpers/detect.py` (may need integration for format registry access)
  - Documentation files (add capability reporting examples)
  - `tests/test_capabilities.py` (new test file)
- **Backward Compatibility**: Fully backward compatible (new functionality, no breaking changes)
- **User Impact**: 
  - Users can programmatically query format capabilities
  - Documentation can be auto-generated from capability data
  - Better developer experience for format selection
