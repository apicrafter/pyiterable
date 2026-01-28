# Change: Extend Table Listing Support to Additional Formats

## Why
The initial table listing feature (`add-table-listing`) was implemented for core multi-table formats (Excel, databases, HDF5, etc.). However, several other formats in IterableData also support multiple tables, elements, or collections that users need to discover:

- **HTML files** can contain multiple `<table>` elements (currently requires `table_index` parameter)
- **XML files** can contain multiple elements of the same tag name (currently requires `tagname` parameter)
- **ZIPXML files** can contain multiple XML files within a ZIP archive, each potentially with multiple elements
- **Data lake formats** (Iceberg, Hudi, Delta) can have multiple tables in catalogs or directories
- **Other formats** may benefit from table listing for consistency and discoverability

Extending table listing to these formats will provide a consistent discovery experience across all multi-table formats and eliminate the need for users to manually inspect files or know table/element names beforehand.

## What Changes
- Extend `list_tables()` and `has_tables()` implementations to additional formats:
  - **HTML format**: List all `<table>` elements (by index or ID if available)
  - **XML format**: List all unique tag names that can be iterated (when `tagname` is used)
  - **ZIPXML format**: List all XML files within the ZIP archive
  - **Iceberg format**: List all tables in the catalog (when catalog-based)
  - **Hudi format**: List all tables in the catalog or directory
  - **Delta format**: List all tables in a Delta Lake catalog or directory (if supported)
- Update format-specific documentation with table listing examples
- Add tests for each new format's table listing functionality

## Implementation Design
- **Consistency**: Follow the same dual API pattern (class method + instance method) as existing implementations
- **HTML**: Return list of table indices (0, 1, 2, ...) or table IDs/names if available from `<table id="...">` or `<caption>` elements
- **XML**: Return list of unique tag names found in the document (when tagname-based iteration is applicable)
- **ZIPXML**: Return list of XML filenames within the ZIP archive
- **Data lake formats**: Return list of table names from catalogs/directories
- **Efficiency**: Reuse open file handles, parsers, or connections when possible
- **Edge cases**: Handle empty files gracefully (return `[]`), missing dependencies (raise `ImportError`), and invalid files (raise appropriate exceptions)

## Impact
- **Modified Capability**: `table-listing` (extending existing capability)
- **Affected Files**:
  - `iterable/datatypes/html.py` (implement `has_tables()` and `list_tables()`)
  - `iterable/datatypes/xml.py` (implement `has_tables()` and `list_tables()`)
  - `iterable/datatypes/zipxml.py` (implement `has_tables()` and `list_tables()`)
  - `iterable/datatypes/iceberg.py` (implement `has_tables()` and `list_tables()`)
  - `iterable/datatypes/hudi.py` (implement `has_tables()` and `list_tables()`)
  - `iterable/datatypes/delta.py` (implement `has_tables()` and `list_tables()`)
  - Format-specific documentation files
  - Test files for each format
- **Backward Compatibility**: Fully backward compatible (new optional methods, existing behavior unchanged)
