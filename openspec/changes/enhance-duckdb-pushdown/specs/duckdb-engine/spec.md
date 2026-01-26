## ADDED Requirements

### Requirement: DuckDB Engine Column Projection Pushdown
The DuckDB engine SHALL support column projection pushdown to reduce I/O and memory usage when only specific columns are needed.

#### Scenario: Project single column from CSV
- **WHEN** user opens a CSV file with DuckDB engine and specifies `columns=['name']` in `iterableargs`
- **THEN** only the 'name' column is read from disk
- **AND** each row dictionary contains only the 'name' key
- **AND** the SQL query generated uses `SELECT name FROM read_csv_auto(...)`

#### Scenario: Project multiple columns from JSONL
- **WHEN** user opens a JSONL file with DuckDB engine and specifies `columns=['id', 'email', 'age']` in `iterableargs`
- **THEN** only the specified columns are read from disk
- **AND** each row dictionary contains only the specified keys
- **AND** the SQL query generated uses `SELECT id, email, age FROM read_json_auto(...)`

#### Scenario: Invalid column name raises error
- **WHEN** user specifies a column name that does not exist in the file
- **THEN** a `ValueError` is raised with a descriptive message indicating the invalid column name
- **AND** the error message suggests valid column names if available

#### Scenario: Column projection with non-DuckDB engine
- **WHEN** user specifies `columns` parameter but uses `engine='internal'`
- **THEN** all columns are read from disk
- **AND** columns are filtered in Python after reading (graceful fallback)
- **AND** a warning may be issued that pushdown is not available

### Requirement: DuckDB Engine Filter Pushdown
The DuckDB engine SHALL support filter pushdown to skip irrelevant rows at the file reader level, improving performance for filtered queries.

#### Scenario: SQL string filter with simple condition
- **WHEN** user opens a file with DuckDB engine and specifies `filter="age > 18"` in `iterableargs`
- **THEN** the filter is translated to SQL `WHERE age > 18`
- **AND** only rows matching the condition are read from disk
- **AND** rows that don't match are skipped entirely (not transferred from disk)

#### Scenario: SQL string filter with complex condition
- **WHEN** user specifies `filter="age > 18 AND status = 'active' OR priority = 'high'"` in `iterableargs`
- **THEN** the filter is translated to SQL `WHERE age > 18 AND status = 'active' OR priority = 'high'`
- **AND** only rows matching the condition are returned

#### Scenario: Python callable filter with translatable pattern
- **WHEN** user specifies `filter=lambda row: row['age'] > 18` in `iterableargs`
- **THEN** the callable is analyzed to extract the predicate
- **AND** if translatable (simple comparison), it is converted to SQL `WHERE age > 18`
- **AND** filter pushdown is applied at the DuckDB level

#### Scenario: Python callable filter with non-translatable pattern
- **WHEN** user specifies a complex callable like `filter=lambda row: complex_function(row['col'])` in `iterableargs`
- **THEN** the callable cannot be translated to SQL
- **AND** all rows are read from disk
- **AND** filtering is performed in Python after reading (graceful fallback)

#### Scenario: Filter pushdown with non-DuckDB engine
- **WHEN** user specifies `filter` parameter but uses `engine='internal'`
- **THEN** all rows are read from disk
- **AND** filtering is performed in Python after reading (graceful fallback)

### Requirement: DuckDB Engine Direct SQL Query Support
The DuckDB engine SHALL support direct SQL queries to enable complex analytics while maintaining the iterator interface.

#### Scenario: Simple SQL query
- **WHEN** user opens a file with DuckDB engine and specifies `query='SELECT a, b FROM data WHERE a > 10'` in `iterableargs`
- **THEN** the query is executed directly by DuckDB
- **AND** results are returned as row dictionaries through the iterator interface
- **AND** the `columns` and `filter` parameters are ignored (query takes precedence)

#### Scenario: SQL query with ORDER BY and LIMIT
- **WHEN** user specifies `query='SELECT name, age FROM data WHERE age > 18 ORDER BY age DESC LIMIT 100'` in `iterableargs`
- **THEN** the query is executed with sorting and limiting
- **AND** results are returned in the specified order
- **AND** only the first 100 matching rows are returned

#### Scenario: SQL query validation rejects DDL
- **WHEN** user specifies a query containing `CREATE`, `DROP`, or `ALTER` statements
- **THEN** a `ValueError` is raised indicating that only SELECT queries are allowed
- **AND** the query is not executed

#### Scenario: SQL query validation rejects DML
- **WHEN** user specifies a query containing `INSERT`, `UPDATE`, or `DELETE` statements
- **THEN** a `ValueError` is raised indicating that only SELECT queries are allowed
- **AND** the query is not executed

#### Scenario: SQL query with table name inference
- **WHEN** user specifies `query='SELECT * FROM data WHERE col > 10'` for a file named `data.csv`
- **THEN** the table name 'data' is inferred from the filename or can be referenced directly
- **AND** DuckDB resolves the table reference to the file

### Requirement: DuckDB Engine Format Detection
The DuckDB engine SHALL detect file format and use the appropriate DuckDB function for reading.

#### Scenario: CSV file uses read_csv_auto
- **WHEN** user opens a `.csv` file with DuckDB engine
- **THEN** the engine uses `read_csv_auto()` function
- **AND** the file is read correctly as CSV

#### Scenario: JSONL file uses read_json_auto
- **WHEN** user opens a `.jsonl` or `.ndjson` file with DuckDB engine
- **THEN** the engine uses `read_json_auto()` or `read_ndjson_auto()` function
- **AND** the file is read correctly as JSONL

#### Scenario: JSON file uses read_json_auto
- **WHEN** user opens a `.json` file with DuckDB engine
- **THEN** the engine uses `read_json_auto()` function
- **AND** the file is read correctly as JSON

#### Scenario: Parquet file uses read_parquet
- **WHEN** user opens a `.parquet` file with DuckDB engine
- **THEN** the engine uses `read_parquet()` function
- **AND** the file is read correctly as Parquet

### Requirement: Combined Pushdown Operations
The DuckDB engine SHALL support combining column projection and filter pushdown for maximum efficiency.

#### Scenario: Columns and filter together
- **WHEN** user specifies both `columns=['name', 'age']` and `filter="age > 18"` in `iterableargs`
- **THEN** the SQL query generated is `SELECT name, age FROM ... WHERE age > 18`
- **AND** only the specified columns are read
- **AND** only rows matching the filter are read
- **AND** both optimizations are applied simultaneously

#### Scenario: Query parameter takes precedence
- **WHEN** user specifies `query`, `columns`, and `filter` parameters together
- **THEN** the `query` parameter is used
- **AND** `columns` and `filter` parameters are ignored
- **AND** a warning may be issued that other parameters are ignored
