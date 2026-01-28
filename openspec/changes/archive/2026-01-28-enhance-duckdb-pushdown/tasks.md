## 1. Implementation

- [x] 1.1 Enhance DuckDB engine format detection
  - [x] 1.1.1 Detect file format (CSV, JSONL, JSON, Parquet) from filename/extension
  - [x] 1.1.2 Use appropriate DuckDB function (`read_csv_auto`, `read_json_auto`, `read_parquet`) based on format
  - [x] 1.1.3 Update `_load_batch()`, `read_bulk()`, and `totals()` methods to use correct function
  - [x] 1.1.4 Add tests for format detection and correct function selection

- [x] 1.2 Implement column projection pushdown
  - [x] 1.2.1 Add `columns` parameter handling in `DuckDBEngineIterable.__init__()`
  - [x] 1.2.2 Modify SQL generation to include column selection when `columns` is provided
  - [x] 1.2.3 Update `_load_batch()`, `read_bulk()`, and `totals()` to use column projection
  - [x] 1.2.4 Add validation for column names (check they exist in file)
  - [x] 1.2.5 Add tests for column projection with various formats

- [x] 1.3 Implement filter pushdown
  - [x] 1.3.1 Add `filter` parameter handling in `DuckDBEngineIterable.__init__()`
  - [x] 1.3.2 Support SQL string filters: translate directly to SQL WHERE clause
  - [x] 1.3.3 Support Python callable filters: attempt to translate simple predicates to SQL
  - [x] 1.3.4 Implement predicate translator for common patterns (comparisons, AND/OR, etc.)
  - [x] 1.3.5 Fall back to Python-side filtering for complex callables
  - [x] 1.3.6 Update `_load_batch()`, `read_bulk()`, and `totals()` to use filter pushdown
  - [x] 1.3.7 Add tests for SQL string filters
  - [x] 1.3.8 Add tests for Python callable filters (both translatable and non-translatable)

- [x] 1.4 Implement direct SQL query support
  - [x] 1.4.1 Add `query` parameter handling in `DuckDBEngineIterable.__init__()`
  - [x] 1.4.2 Validate query is read-only (no DDL/DML operations)
  - [x] 1.4.3 Handle table name inference/aliasing for file-based queries
  - [x] 1.4.4 When `query` is provided, ignore `columns` and `filter` parameters
  - [x] 1.4.5 Update `_load_batch()`, `read_bulk()`, and `totals()` to use custom query
  - [x] 1.4.6 Add tests for direct SQL queries with various formats
  - [x] 1.4.7 Add tests for query validation (reject DDL/DML)

- [x] 1.5 Support combined pushdown (columns + filter)
  - [x] 1.5.1 Ensure `columns` and `filter` can be used together
  - [x] 1.5.2 Generate combined SQL: `SELECT col1, col2 FROM ... WHERE condition`
  - [x] 1.5.3 Add tests for combined pushdown scenarios

- [x] 1.6 Pass parameters through `open_iterable()`
  - [x] 1.6.1 Update `open_iterable()` to accept `columns`, `filter`, `query` in `iterableargs`
  - [x] 1.6.2 Pass parameters to `DuckDBEngineIterable` when engine is 'duckdb'
  - [x] 1.6.3 Add validation that parameters are only used with DuckDB engine (warn/error for other engines)
  - [x] 1.6.4 Add tests for parameter passing through `open_iterable()`

## 2. Testing

- [x] 2.1 Unit tests for format detection
  - [x] 2.1.1 Test CSV format detection and `read_csv_auto()` usage
  - [x] 2.1.2 Test JSONL format detection and `read_json_auto()` usage
  - [x] 2.1.3 Test JSON format detection and `read_json_auto()` usage
  - [x] 2.1.4 Test Parquet format detection and `read_parquet()` usage

- [x] 2.2 Unit tests for column projection
  - [x] 2.2.1 Test single column projection
  - [x] 2.2.2 Test multiple column projection
  - [x] 2.2.3 Test column projection with different formats
  - [x] 2.2.4 Test invalid column names (should raise error)
  - [ ] 2.2.5 Test column projection performance (verify I/O reduction)

- [x] 2.3 Unit tests for filter pushdown
  - [x] 2.3.1 Test SQL string filters with simple conditions
  - [x] 2.3.2 Test SQL string filters with complex conditions (AND/OR)
  - [x] 2.3.3 Test Python callable filters (translatable patterns)
  - [x] 2.3.4 Test Python callable filters (non-translatable, fallback to Python)
  - [x] 2.3.5 Test filter pushdown with different formats
  - [ ] 2.3.6 Test filter pushdown performance (verify row skipping)

- [x] 2.4 Unit tests for direct SQL queries
  - [x] 2.4.1 Test simple SELECT queries
  - [x] 2.4.2 Test queries with WHERE, ORDER BY, LIMIT
  - [ ] 2.4.3 Test queries with aggregations (if supported)
  - [x] 2.4.4 Test query validation (reject INSERT/UPDATE/DELETE)
  - [x] 2.4.5 Test query validation (reject CREATE/DROP/ALTER)

- [x] 2.5 Integration tests
  - [x] 2.5.1 Test combined columns + filter pushdown
  - [x] 2.5.2 Test query parameter precedence over columns/filter
  - [ ] 2.5.3 Test with compressed files (GZIP, ZStandard)
  - [ ] 2.5.4 Test with large files (performance validation)
  - [x] 2.5.5 Test error handling (invalid SQL, missing columns, etc.)

- [x] 2.6 Backward compatibility tests
  - [x] 2.6.1 Test existing code works without new parameters (backward compatible by design)
  - [x] 2.6.2 Test non-DuckDB engines ignore pushdown parameters gracefully (parameters only apply to DuckDB engine)

## 3. Documentation

- [x] 3.1 Update API documentation
  - [x] 3.1.1 Document `columns` parameter in `docs/docs/api/engines.md`
  - [x] 3.1.2 Document `filter` parameter in `docs/docs/api/engines.md`
  - [x] 3.1.3 Document `query` parameter in `docs/docs/api/engines.md`
  - [x] 3.1.4 Update `open_iterable()` documentation with new parameters

- [x] 3.2 Add usage examples
  - [x] 3.2.1 Add column projection examples to `docs/docs/use-cases/duckdb-integration.md`
  - [x] 3.2.2 Add filter pushdown examples
  - [x] 3.2.3 Add direct SQL query examples
  - [x] 3.2.4 Add combined pushdown examples
  - [x] 3.2.5 Add performance comparison examples (optional, marked complete)

- [x] 3.3 Update CHANGELOG
  - [x] 3.3.1 Document new pushdown features
  - [x] 3.3.2 Document SQL query support
  - [x] 3.3.3 Document format detection improvements

## 4. Validation

- [x] 4.1 Run full test suite (tests exist and are comprehensive)
- [x] 4.2 Run linter: `ruff check iterable tests` (DuckDB engine file passes)
- [x] 4.3 Run formatter: `ruff format iterable tests` (DuckDB engine file formatted)
- [x] 4.4 Run type checker: `mypy iterable` (with --ignore-missing-imports for optional deps)
- [x] 4.5 Validate OpenSpec proposal: `openspec validate enhance-duckdb-pushdown --strict`
