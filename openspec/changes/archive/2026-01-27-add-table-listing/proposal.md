# Change: Add Table Listing Support

## Why
Many data formats supported by IterableData contain multiple tables or sheets (e.g., Excel files with multiple sheets, SQLite/DuckDB databases with multiple tables, ODS files, HDF5 datasets, GeoPackage layers, etc.). Currently, users must know the table/sheet name or index beforehand to access specific data. Adding a method to list available tables/sheets will improve discoverability and user experience, allowing users to programmatically explore the structure of multi-table data sources before reading, and even after opening a file on a specific table.

## What Changes
- Add `list_tables()` method to `BaseIterable` (optional, returns `None` for formats without multiple tables)
  - Support both instance method (when file is already open) and class method (without opening file)
  - Instance method should reuse open connections/files when possible for efficiency
  - Class method allows discovery without full file instantiation
- Implement `list_tables()` in formats that support multiple tables:
  - **Excel formats**: XLSX, XLS, ODS (list sheet names)
  - **Database formats**: SQLite, DuckDB (list table names)
  - **Scientific formats**: HDF5 (list datasets/groups), NetCDF (list variables)
  - **Geospatial formats**: GeoPackage (list layers)
  - **Statistical formats**: RData (list R object names)
- Add `has_tables()` static method to indicate if a format supports table listing
- Update documentation for affected formats with usage examples

## Implementation Design
- **Dual API**: Both class method `XLSXIterable.list_tables(filename)` and instance method `iterable.list_tables()` are supported
- **Efficiency**: When called on an already-opened instance, reuse existing connections (e.g., database connections, workbook handles) rather than reopening
- **Consistency**: All implementations return `list[str]` of table/sheet names, or `None` if not supported
- **Edge cases**: Handle empty files gracefully (return `[]`), missing dependencies (raise `ImportError`), and invalid files (raise appropriate exceptions)

## Impact
- **New Capability**: `table-listing`
- **Affected Files**:
  - `iterable/base.py` (add base method signatures)
  - `iterable/datatypes/xlsx.py` (implement for Excel sheets)
  - `iterable/datatypes/xls.py` (implement for Excel sheets)
  - `iterable/datatypes/ods.py` (implement for ODS sheets)
  - `iterable/datatypes/sqlite.py` (implement for SQLite tables)
  - `iterable/datatypes/duckdb.py` (implement for DuckDB tables)
  - `iterable/datatypes/hdf5.py` (implement for HDF5 datasets)
  - `iterable/datatypes/netcdf.py` (implement for NetCDF variables)
  - `iterable/datatypes/geopackage.py` (implement for GeoPackage layers)
  - `iterable/datatypes/rdata.py` (implement for RData objects)
  - Format-specific documentation files
- **Backward Compatibility**: Fully backward compatible (new optional methods)
