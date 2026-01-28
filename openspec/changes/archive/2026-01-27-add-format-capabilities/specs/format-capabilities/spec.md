# Format Capability Reporting

## ADDED Requirements

### Requirement: Format Capability Query API
The system SHALL provide functions to query format capabilities programmatically, allowing users to discover what operations and features are supported by each data format.

#### Scenario: Query capabilities for a specific format
- **WHEN** user calls `get_format_capabilities("csv")`
- **THEN** system returns a dictionary with all capability flags for CSV format
- **AND** dictionary includes keys: `readable`, `writable`, `bulk_read`, `bulk_write`, `totals`, `streaming`, `flat_only`, `tables`, `compression`, `nested`
- **AND** values are boolean (True/False) or None for unknown capabilities

#### Scenario: List capabilities for all formats
- **WHEN** user calls `list_all_capabilities()`
- **THEN** system returns a dictionary mapping format IDs to their capability dictionaries
- **AND** all registered formats in the system are included
- **AND** each format entry contains the same capability keys

#### Scenario: Query a specific capability
- **WHEN** user calls `get_capability("json", "writable")`
- **THEN** system returns True if JSON format supports writing, False otherwise
- **AND** returns None if capability cannot be determined

#### Scenario: Handle unknown format
- **WHEN** user calls `get_format_capabilities("unknown_format")`
- **THEN** system raises ValueError with descriptive error message

#### Scenario: Handle missing optional dependencies
- **WHEN** user queries capabilities for a format requiring optional dependencies that are not installed
- **THEN** system returns capability dictionary with None values for capabilities that cannot be determined
- **AND** does not raise ImportError or crash

### Requirement: Capability Detection Logic
The system SHALL detect format capabilities by introspecting format classes and their methods.

#### Scenario: Detect read/write capabilities
- **WHEN** capability detection inspects a format class
- **THEN** `readable` is True if class has `read()` method
- **AND** `writable` is True if class has `write()` method
- **AND** `bulk_read` is True if class has `read_bulk()` method
- **AND** `bulk_write` is True if class has `write_bulk()` method

#### Scenario: Detect totals support
- **WHEN** capability detection inspects a format class
- **THEN** `totals` is True if static method `has_totals()` exists and returns True
- **AND** `totals` is False if `has_totals()` returns False or does not exist

#### Scenario: Detect table support
- **WHEN** capability detection inspects a format class
- **THEN** `tables` is True if static method `has_tables()` exists and returns True
- **AND** `tables` is False if `has_tables()` returns False or does not exist

#### Scenario: Detect flat-only support
- **WHEN** capability detection inspects a format class
- **THEN** `flat_only` is True if static method `is_flatonly()` exists and returns True
- **AND** `nested` is False when `flat_only` is True
- **AND** `nested` is True when `flat_only` is False

#### Scenario: Detect streaming support
- **WHEN** capability detection inspects a format class
- **THEN** `streaming` is True if instance method `is_streaming()` exists and returns True
- **AND** `streaming` may be inferred from format characteristics if method does not exist

#### Scenario: Detect compression support
- **WHEN** capability detection checks format compatibility
- **THEN** `compression` is True if format works with compression codecs (GZIP, BZIP2, etc.)
- **AND** detection uses format registry and codec compatibility information

### Requirement: Capability Caching
The system SHALL cache capability detection results to avoid repeated introspection of format classes.

#### Scenario: Cache capability results
- **WHEN** user queries capabilities for the same format multiple times
- **THEN** system returns cached results after first detection
- **AND** detection logic is only executed once per format class

#### Scenario: Cache invalidation not required
- **WHEN** format classes are not modified at runtime
- **THEN** cached capability results remain valid
- **AND** no cache invalidation mechanism is required

### Requirement: Capability Dictionary Structure
The system SHALL return capability information in a standardized dictionary format.

#### Scenario: Standard capability keys
- **WHEN** capability dictionary is returned
- **THEN** dictionary contains all standard capability keys:
  - `readable` (bool | None)
  - `writable` (bool | None)
  - `bulk_read` (bool | None)
  - `bulk_write` (bool | None)
  - `totals` (bool | None)
  - `streaming` (bool | None)
  - `flat_only` (bool | None)
  - `tables` (bool | None)
  - `compression` (bool | None)
  - `nested` (bool | None)

#### Scenario: Boolean or None values
- **WHEN** capability value is determined
- **THEN** value is True or False
- **WHEN** capability cannot be determined (e.g., missing dependencies)
- **THEN** value is None

### Requirement: Integration with Format Registry
The system SHALL integrate with the existing format detection and registry system.

#### Scenario: Access format registry
- **WHEN** capability functions need to enumerate formats
- **THEN** system uses format registry from `iterable/helpers/detect.py`
- **AND** format registry provides format IDs and class information

#### Scenario: Format ID consistency
- **WHEN** user queries capabilities using format ID
- **THEN** format ID matches IDs used in format registry
- **AND** format ID can be file extension or format name (e.g., "csv", "json", "parquet")
