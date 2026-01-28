## ADDED Requirements

### Requirement: Table Listing Support
The system SHALL provide methods to list available tables, sheets, datasets, layers, or other named collections in data formats that support multiple such entities.

#### Scenario: List Excel sheets via class method
- **WHEN** calling `XLSXIterable.list_tables('data.xlsx')` on a file with multiple sheets
- **THEN** it returns a list of sheet names (e.g., `['Sheet1', 'Sheet2', 'Data']`) without requiring file instantiation

#### Scenario: List Excel sheets via instance method
- **WHEN** calling `list_tables()` on an already-opened XLSXIterable instance (even if opened with `page=1`)
- **THEN** it returns all available sheet names, reusing the open workbook handle for efficiency

#### Scenario: List SQLite tables
- **WHEN** calling `list_tables()` on a SQLite database with multiple tables
- **THEN** it returns a list of table names (e.g., `['users', 'orders', 'products']`)

#### Scenario: List DuckDB tables
- **WHEN** calling `list_tables()` on a DuckDB database with multiple tables
- **THEN** it returns a list of table names (e.g., `['customers', 'transactions']`)

#### Scenario: List HDF5 datasets
- **WHEN** calling `list_tables()` on an HDF5 file
- **THEN** it returns a list of dataset paths (e.g., `['/data', '/group/dataset1', '/group/dataset2']`)

#### Scenario: List GeoPackage layers
- **WHEN** calling `list_tables()` on a GeoPackage file
- **THEN** it returns a list of layer names (e.g., `['roads', 'buildings', 'parcels']`)

#### Scenario: List RData objects
- **WHEN** calling `list_tables()` on an RData file containing multiple R objects
- **THEN** it returns a list of object names (e.g., `['df1', 'df2', 'vector1']`)

#### Scenario: Format without multiple tables
- **WHEN** calling `list_tables()` on a format that doesn't support multiple tables (e.g., CSV, JSONL)
- **THEN** it returns `None` to indicate the feature is not supported

#### Scenario: Empty database or file
- **WHEN** calling `list_tables()` on a database with no tables or an Excel file with no sheets
- **THEN** it returns an empty list `[]`

#### Scenario: Check if format supports tables
- **WHEN** calling `has_tables()` static method on a format class
- **THEN** it returns `True` for formats that support multiple tables (XLSX, XLS, ODS, SQLite, DuckDB, HDF5, NetCDF, GeoPackage, RData) and `False` otherwise

#### Scenario: Use table listing to iterate over sheets
- **WHEN** a user calls `list_tables()` to get available sheets
- **THEN** they can use the returned names/indices to open specific tables using existing `page` or `table` parameters

#### Scenario: List tables on already-opened file
- **WHEN** a file is opened with a specific table selected (e.g., `open_iterable('data.xlsx', iterableargs={'page': 1})`)
- **THEN** calling `list_tables()` on the instance still returns all available tables, not just the current one

#### Scenario: Efficient reuse of connections
- **WHEN** calling `list_tables()` on an already-opened database instance
- **THEN** it reuses the existing database connection rather than opening a new one
