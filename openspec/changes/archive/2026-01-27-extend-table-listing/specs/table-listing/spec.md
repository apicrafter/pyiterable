## MODIFIED Requirements

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

#### Scenario: List HTML tables
- **WHEN** calling `list_tables()` on an HTML file containing multiple `<table>` elements
- **THEN** it returns a list of table identifiers (e.g., `['0', '1', 'table1']` or indices `['0', '1', '2']`), preferring IDs or names from `<table id="...">` or `<caption>` elements when available

#### Scenario: List HTML tables via instance method
- **WHEN** calling `list_tables()` on an already-opened HTMLIterable instance (even if opened with `table_index=0`)
- **THEN** it returns all available table identifiers, reusing the parsed HTML document for efficiency

#### Scenario: List XML tag names
- **WHEN** calling `list_tables()` on an XML file containing multiple elements
- **THEN** it returns a list of unique tag names that can be iterated (e.g., `['item', 'product', 'record']`)

#### Scenario: List XML tag names via instance method
- **WHEN** calling `list_tables()` on an already-opened XMLIterable instance (even if opened with `tagname='item'`)
- **THEN** it returns all available tag names, reusing the parsed XML document for efficiency

#### Scenario: List ZIPXML files
- **WHEN** calling `list_tables()` on a ZIPXML file containing multiple XML files
- **THEN** it returns a list of XML filenames within the ZIP archive (e.g., `['data1.xml', 'data2.xml', 'records.xml']`)

#### Scenario: List ZIPXML files via instance method
- **WHEN** calling `list_tables()` on an already-opened ZIPXMLSource instance
- **THEN** it returns all XML filenames in the ZIP archive, reusing the open ZIP handle for efficiency

#### Scenario: List Iceberg tables
- **WHEN** calling `list_tables()` on an Iceberg catalog with multiple tables
- **THEN** it returns a list of table names (e.g., `['customers', 'orders', 'products']`)

#### Scenario: List Hudi tables
- **WHEN** calling `list_tables()` on a Hudi catalog or directory with multiple tables
- **THEN** it returns a list of table names (e.g., `['events', 'users', 'transactions']`)

#### Scenario: List Delta tables
- **WHEN** calling `list_tables()` on a Delta Lake catalog or directory with multiple tables
- **THEN** it returns a list of table names (e.g., `['sales', 'inventory', 'customers']`)

#### Scenario: Delta single table directory
- **WHEN** calling `list_tables()` on a Delta table that is a single table directory (not a catalog)
- **THEN** it returns `None` or `[]` to indicate table listing is not applicable for single-table directories

#### Scenario: Format without multiple tables
- **WHEN** calling `list_tables()` on a format that doesn't support multiple tables (e.g., CSV, JSONL)
- **THEN** it returns `None` to indicate the feature is not supported

#### Scenario: Empty database or file
- **WHEN** calling `list_tables()` on a database with no tables, an Excel file with no sheets, or an HTML file with no tables
- **THEN** it returns an empty list `[]` to indicate no tables are available

#### Scenario: HTML table with ID
- **WHEN** calling `list_tables()` on an HTML file where tables have `id` attributes (e.g., `<table id="summary">`)
- **THEN** it returns a list including the ID values (e.g., `['summary', 'details']`) when available, falling back to indices for tables without IDs

#### Scenario: HTML table with caption
- **WHEN** calling `list_tables()` on an HTML file where tables have `<caption>` elements
- **THEN** it returns a list including caption text (e.g., `['Sales Summary', 'Product Details']`) when available, falling back to IDs or indices
