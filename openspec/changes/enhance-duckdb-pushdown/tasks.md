## 1. Implementation

- [ ] 1.1 Enhance DuckDB engine format detection
  - [ ] 1.1.1 Detect file format (CSV, JSONL, JSON, Parquet) from filename/extension
  - [ ] 1.1.2 Use appropriate DuckDB function (`read_csv_auto`, `read_json_auto`, `read_parquet`) based on format
  - [ ] 1.1.3 Update `_load_batch()`, `read_bulk()`, and `totals()` methods to use correct function
  - [ ] 1.1.4 Add tests for format detection and correct function selection

- [ ] 1.2 Implement column projection pushdown
  - [ ] 1.2.1 Add `columns` parameter handling in `DuckDBEngineIterable.__init__()`
  - [ ] 1.2.2 Modify SQL generation to include column selection when `columns` is provided
  - [ ] 1.2.3 Update `_load_batch()`, `read_bulk()`, and `totals()` to use column projection
  - [ ] 1.2.4 Add validation for column names (check they exist in file)
  - [ ] 1.2.5 Add tests for column projection with various formats

- [ ] 1.3 Implement filter pushdown
  - [ ] 1.3.1 Add `filter` parameter handling in `DuckDBEngineIterable.__init__()`
  - [ ] 1.3.2 Support SQL string filters: translate directly to SQL WHERE clause
  - [ ] 1.3.3 Support Python callable filters: attempt to translate simple predicates to SQL
  - [ ] 1.3.4 Implement predicate translator for common patterns (comparisons, AND/OR, etc.)
  - [ ] 1.3.5 Fall back to Python-side filtering for complex callables
  - [ ] 1.3.6 Update `_load_batch()`, `read_bulk()`, and `totals()` to use filter pushdown
  - [ ] 1.3.7 Add tests for SQL string filters
  - [ ] 1.3.8 Add tests for Python callable filters (both translatable and non-translatable)

- [ ] 1.4 Implement direct SQL query support
  - [ ] 1.4.1 Add `query` parameter handling in `DuckDBEngineIterable.__init__()`
  - [ ] 1.4.2 Validate query is read-only (no DDL/DML operations)
  - [ ] 1.4.3 Handle table name inference/aliasing for file-based queries
  - [ ] 1.4.4 When `query` is provided, ignore `columns` and `filter` parameters
  - [ ] 1.4.5 Update `_load_batch()`, `read_bulk()`, and `totals()` to use custom query
  - [ ] 1.4.6 Add tests for direct SQL queries with various formats
  - [ ] 1.4.7 Add tests for query validation (reject DDL/DML)

- [ ] 1.5 Support combined pushdown (columns + filter)
  - [ ] 1.5.1 Ensure `columns` and `filter` can be used together
  - [ ] 1.5.2 Generate combined SQL: `SELECT col1, col2 FROM ... WHERE condition`
  - [ ] 1.5.3 Add tests for combined pushdown scenarios

- [ ] 1.6 Pass parameters through `open_iterable()`
  - [ ] 1.6.1 Update `open_iterable()` to accept `columns`, `filter`, `query` in `iterableargs`
  - [ ] 1.6.2 Pass parameters to `DuckDBEngineIterable` when engine is 'duckdb'
  - [ ] 1.6.3 Add validation that parameters are only used with DuckDB engine (warn/error for other engines)
  - [ ] 1.6.4 Add tests for parameter passing through `open_iterable()`

## 2. Testing

- [ ] 2.1 Unit tests for format detection
  - [ ] 2.1.1 Test CSV format detection and `read_csv_auto()` usage
  - [ ] 2.1.2 Test JSONL format detection and `read_json_auto()` usage
  - [ ] 2.1.3 Test JSON format detection and `read_json_auto()` usage
  - [ ] 2.1.4 Test Parquet format detection and `read_parquet()` usage

- [ ] 2.2 Unit tests for column projection
  - [ ] 2.2.1 Test single column projection
  - [ ] 2.2.2 Test multiple column projection
  - [ ] 2.2.3 Test column projection with different formats
  - [ ] 2.2.4 Test invalid column names (should raise error)
  - [ ] 2.2.5 Test column projection performance (verify I/O reduction)

- [ ] 2.3 Unit tests for filter pushdown
  - [ ] 2.3.1 Test SQL string filters with simple conditions
  - [ ] 2.3.2 Test SQL string filters with complex conditions (AND/OR)
  - [ ] 2.3.3 Test Python callable filters (translatable patterns)
  - [ ] 2.3.4 Test Python callable filters (non-translatable, fallback to Python)
  - [ ] 2.3.5 Test filter pushdown with different formats
  - [ ] 2.3.6 Test filter pushdown performance (verify row skipping)

- [ ] 2.4 Unit tests for direct SQL queries
  - [ ] 2.4.1 Test simple SELECT queries
  - [ ] 2.4.2 Test queries with WHERE, ORDER BY, LIMIT
  - [ ] 2.4.3 Test queries with aggregations (if supported)
  - [ ] 2.4.4 Test query validation (reject INSERT/UPDATE/DELETE)
  - [ ] 2.4.5 Test query validation (reject CREATE/DROP/ALTER)

- [ ] 2.5 Integration tests
  - [ ] 2.5.1 Test combined columns + filter pushdown
  - [ ] 2.5.2 Test query parameter precedence over columns/filter
  - [ ] 2.5.3 Test with compressed files (GZIP, ZStandard)
  - [ ] 2.5.4 Test with large files (performance validation)
  - [ ] 2.5.5 Test error handling (invalid SQL, missing columns, etc.)

- [ ] 2.6 Backward compatibility tests
  - [ ] 2.6.1 Test existing code works without new parameters
  - [ ] 2.6.2 Test non-DuckDB engines ignore pushdown parameters gracefully

## 3. Documentation

- [ ] 3.1 Update API documentation
  - [ ] 3.1.1 Document `columns` parameter in `docs/docs/api/engines.md`
  - [ ] 3.1.2 Document `filter` parameter in `docs/docs/api/engines.md`
  - [ ] 3.1.3 Document `query` parameter in `docs/docs/api/engines.md`
  - [ ] 3.1.4 Update `open_iterable()` documentation with new parameters

- [ ] 3.2 Add usage examples
  - [ ] 3.2.1 Add column projection examples to `docs/docs/use-cases/duckdb-integration.md`
  - [ ] 3.2.2 Add filter pushdown examples
  - [ ] 3.2.3 Add direct SQL query examples
  - [ ] 3.2.4 Add combined pushdown examples
  - [ ] 3.2.5 Add performance comparison examples

- [ ] 3.3 Update CHANGELOG
  - [ ] 3.3.1 Document new pushdown features
  - [ ] 3.3.2 Document SQL query support
  - [ ] 3.3.3 Document format detection improvements

## 4. Validation

- [ ] 4.1 Run full test suite
- [ ] 4.2 Run linter: `ruff check iterable tests`
- [ ] 4.3 Run formatter: `ruff format iterable tests`
- [ ] 4.4 Run type checker: `mypy iterable`
- [ ] 4.5 Validate OpenSpec proposal: `openspec validate enhance-duckdb-pushdown --strict`
