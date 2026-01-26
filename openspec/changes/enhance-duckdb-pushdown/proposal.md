# Change: Enhance DuckDB Engine with Pushdown and SQL Query Support

## Why
The current DuckDB engine provides basic file reading capabilities but lacks the advanced query optimization features that make DuckDB powerful. Users working with large columnar datasets (CSV, JSONL, Parquet) need:

1. **Projection Pushdown**: When users only need specific columns, reading all columns wastes I/O and memory. DuckDB can push column selection down to the file reader, dramatically reducing data transfer.

2. **Filter Pushdown**: Filtering rows in Python after reading all data is inefficient. DuckDB can push WHERE clauses down to the file reader, skipping irrelevant rows entirely.

3. **Direct SQL Queries**: Some users want full SQL power (JOINs, aggregations, etc.) without leaving the iterabledata interface. This enables complex analytics while maintaining the familiar iterator pattern.

These enhancements will make iterabledata significantly more efficient for analytical workloads on large datasets, reducing memory usage and improving performance by orders of magnitude for filtered/projected queries.

## What Changes
- **Column Projection Pushdown**:
  - Add `columns` parameter to `iterableargs` (list of column names)
  - When DuckDB engine is used, translate `columns=['col1', 'col2']` into SQL `SELECT col1, col2 FROM ...`
  - Only selected columns are read from disk, reducing I/O and memory usage
  - Falls back gracefully when non-DuckDB engine is used (reads all columns, then filters in Python)

- **Filter Pushdown**:
  - Add `filter` parameter to `iterableargs` accepting:
    - SQL WHERE clause string: `filter="col1 > 10 AND col2 = 'x'"`
    - Python callable: `filter=lambda row: row['col1'] > 10 and row['col2'] == 'x'`
  - When DuckDB engine is used with SQL string filter, translate into SQL `WHERE` clause
  - When Python callable is provided, attempt to translate simple predicates to SQL (e.g., `row['col'] > 10` → `col > 10`)
  - Complex callables fall back to Python-side filtering
  - Falls back gracefully when non-DuckDB engine is used (filters in Python after reading)

- **Direct SQL Query Support**:
  - Add `query` parameter to `iterableargs` accepting raw SQL query string
  - When `query` is provided, use it directly as the SQL query (user must reference table/data source correctly)
  - For CSV/JSONL/Parquet files, table name is inferred from filename or can be aliased
  - Example: `query='SELECT a, b FROM data WHERE a > 10 ORDER BY b LIMIT 100'`
  - When `query` is provided, `columns` and `filter` parameters are ignored (query takes precedence)
  - Validates that query is safe (read-only, no DDL/DML operations)

- **Format Detection for DuckDB Functions**:
  - Enhance DuckDB engine to detect file format and use appropriate DuckDB function:
    - CSV files → `read_csv_auto()`
    - JSONL/NDJSON files → `read_json_auto()` or `read_ndjson_auto()`
    - JSON files → `read_json_auto()`
    - Parquet files → `read_parquet()`
  - Currently only uses `read_csv_auto()` for all files, which is incorrect

- **Combined Pushdown Support**:
  - Support combining `columns` and `filter` parameters
  - Example: `columns=['name', 'age']` + `filter="age > 18"` → `SELECT name, age FROM ... WHERE age > 18`

## Impact
- **Affected Specs**:
  - `duckdb-engine` - ADDED (new capability specification)
- **Affected Files**:
  - `iterable/engines/duckdb.py` - Enhance `DuckDBEngineIterable` to support pushdown parameters and SQL queries
  - `iterable/helpers/detect.py` - Pass pushdown parameters through `open_iterable()` to engine
  - `iterable/base.py` - Potentially add interface methods for pushdown (if needed for consistency)
  - `tests/test_duckdb.py` (new or enhance existing) - Comprehensive tests for pushdown features
  - `docs/docs/api/engines.md` - Document new pushdown parameters
  - `docs/docs/use-cases/duckdb-integration.md` - Add examples of pushdown usage
  - `CHANGELOG.md` - Document new features
- **Dependencies**:
  - No new required dependencies (DuckDB already optional)
  - May need to enhance DuckDB version requirement if newer features are used
- **Backward Compatibility**:
  - All changes are additive and backward compatible
  - Default behavior (no `columns`, `filter`, or `query`) remains unchanged
  - Existing code continues to work without modifications
  - Non-DuckDB engines ignore pushdown parameters (graceful fallback)
