# Change: Add ClickHouse Database Engine Support

## Why
ClickHouse is a high-performance columnar OLAP database that has achieved significant market traction, reaching a $15B valuation in 2025. It is widely used for real-time analytics, observability, data warehousing, and machine learning workloads - use cases that align perfectly with IterableData's focus on analytical and ETL workflows.

Currently, IterableData supports PostgreSQL as a database engine, with MySQL, MSSQL, SQLite, MongoDB, and Elasticsearch planned. ClickHouse represents a critical gap in analytics database support, as it is specifically designed for the analytical workloads that IterableData targets. Many users working with large-scale analytics data are likely to have ClickHouse in their stack, and the lack of ClickHouse support forces them to:

- Export ClickHouse data to files before processing, adding unnecessary steps
- Write custom ClickHouse connection code that duplicates IterableData's iterator abstraction
- Miss out on IterableData's unified interface, error handling, metrics, and pipeline features when working with ClickHouse
- Use different APIs for ClickHouse vs other database sources

Adding ClickHouse as a first-class database engine will:
- Enable direct ClickHouse queries as iterable data sources using the same `open_iterable()` API
- Treat ClickHouse query results exactly like files: an iterator of `dict` rows
- Integrate seamlessly with existing features (pipelines, conversion, DataFrame bridges)
- Provide consistent error handling, metrics, and observability for ClickHouse sources
- Support read-only operations by default for safety in analytical/ETL workloads
- Extend the existing database engine architecture with minimal additional complexity

## What Changes
- **ClickHouse Database Driver**:
  - Add `ClickHouseDriver` class in `iterable/db/clickhouse.py` following the `DBDriver` base class pattern
  - Support connection via ClickHouse connection string/URL (`clickhouse://` or `clickhouse+native://`)
  - Support existing connection objects (clickhouse-connect client objects)
  - Implement streaming queries using batch processing for memory efficiency
  - Support SQL queries via `query` parameter or table name (auto-builds `SELECT * FROM table`)
  - Default to read-only operations for safety
  - Support ClickHouse-specific parameters (database, table, format, settings)
- **Common Database Parameters** (consistent with other SQL engines):
  - `query`: SQL query string or table name
  - `batch_size`: Number of rows fetched per round-trip (streaming)
  - `read_only`: Default `True` (safety)
  - `on_error`: Error handling strategy (`'raise'`, `'skip'`, `'warn'`)
  - `metrics`: Same metrics structure as file reading (rows, bytes, elapsed)
  - `timeout`, `retries`, `ssl_mode`: Connection and reliability settings
- **ClickHouse-Specific Parameters**:
  - `database`: Database name (if not in connection string)
  - `table`: Table name (alternative to `query` parameter)
  - `format`: Result format (default: native or JSONEachRow for streaming)
  - `settings`: ClickHouse query settings (dictionary of key-value pairs)
  - `max_block_size`: ClickHouse-specific batch size control
- **Integration with Existing Features**:
  - Extend `convert()` to support ClickHouse sources
  - Enable `pipeline()` to work with ClickHouse sources
  - Support DataFrame bridges (`.to_pandas()`, `.to_polars()`, `.to_dask()`) for ClickHouse results
- **Discovery Helpers**:
  - Add `list_tables()` helper function for ClickHouse (database, table name, row estimates)
  - Query ClickHouse system tables (`system.tables`, `system.databases`)
- **Optional Dependencies**:
  - Add `clickhouse-connect` as optional dependency (official ClickHouse driver)
  - Raise helpful `ImportError` messages when dependencies are missing
  - Core library remains lightweight without ClickHouse dependency

## Impact
- **Affected Specs**:
  - `database-engines` - MODIFIED to include ClickHouse support
- **Affected Files**:
  - `iterable/db/clickhouse.py` (new) - ClickHouse driver implementation
  - `iterable/db/__init__.py` - Register ClickHouse driver in built-in drivers
  - `iterable/helpers/detect.py` - Already supports database engines via registry (no changes needed)
  - `iterable/convert/core.py` - Already supports database sources (no changes needed)
  - `iterable/pipeline/core.py` - Already supports database sources (no changes needed)
  - `pyproject.toml` - Add optional dependency for ClickHouse driver
  - `tests/test_db_engines.py` - Add ClickHouse test cases
  - `CHANGELOG.md` - Document new ClickHouse engine feature
  - `docs/docs/api/database-engines.md` - Add ClickHouse documentation
- **Dependencies**:
  - New optional dependency: `clickhouse-connect>=0.6.0` (official ClickHouse driver, see design.md for rationale)
  - Add to `db` convenience group in optional dependencies
  - Add to `db-sql` convenience group (ClickHouse is SQL-based)
  - Dependency is optional - core library remains lightweight
  - Users only install ClickHouse driver if needed
- **Backward Compatibility**:
  - All changes are additive and backward compatible
  - Existing file-based sources continue to work unchanged
  - Existing database engines (PostgreSQL) continue to work unchanged
  - ClickHouse engine support is opt-in via `engine` parameter
  - No breaking changes to existing APIs
