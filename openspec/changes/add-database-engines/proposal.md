# Change: Add Database Engines Support

## Why
Many real-world data workflows require reading data from SQL and NoSQL databases. Currently, IterableData only supports file-based data sources, which limits its utility for modern data pipelines that need to extract data from databases for ETL, analytics, and data migration tasks.

Users must currently:
- Export database data to files before processing, adding unnecessary steps
- Write custom database connection code that duplicates IterableData's iterator abstraction
- Miss out on IterableData's unified interface, error handling, metrics, and pipeline features when working with databases
- Use different APIs for file-based vs database-based data sources

Adding database engines as first-class iterable sources will:
- Enable direct database queries as iterable data sources using the same `open_iterable()` API
- Treat database query results exactly like files: an iterator of `dict` rows
- Integrate seamlessly with existing features (pipelines, conversion, DataFrame bridges)
- Provide consistent error handling, metrics, and observability across all data sources
- Support read-only operations by default for safety in analytical/ETL workloads
- Extend the existing engine architecture (`internal`, `duckdb`) with database-specific engines

## What Changes
- **Database Engine Architecture**:
  - Introduce `DBDriver` base class abstraction for database connections
  - Register database engines (`engine="postgres"`, `"mysql"`, `"mssql"`, `"sqlite"`, `"mongo"`, `"elasticsearch"`, `"opensearch"`)
  - Extend `open_iterable()` to accept database connection strings/URLs as the `source` parameter
  - Support database-specific `iterableargs` (query, filter, projection, batch_size, etc.)
- **SQL Database Support**:
  - Add `PostgresDriver` with streaming via server-side cursors
  - Add `MySQLDriver`/`MariaDBDriver` with streaming support
  - Add `MSSQLDriver` for Microsoft SQL Server
  - Add `SQLiteDriver` for SQLite databases
  - Support SQL queries via `query` parameter or table name (auto-builds `SELECT * FROM table`)
  - Default to read-only transactions for safety
- **NoSQL Database Support**:
  - Add `MongoDriver` with database/collection, filter, projection, and aggregation pipeline support
  - Add `ElasticsearchDriver`/`OpenSearchDriver` with scroll-based iteration
  - Support query DSL and filtering via `iterableargs`
- **Common Database Parameters**:
  - `query`: SQL query string or table name (SQL engines)
  - `batch_size`: Number of rows/documents fetched per round-trip (streaming)
  - `read_only`: Default `True` for all DB engines (safety)
  - `on_error`: Error handling strategy (`'raise'`, `'skip'`, `'warn'`)
  - `metrics`: Same metrics structure as file reading (rows, bytes, elapsed)
  - `timeout`, `retries`, `ssl_mode`: Connection and reliability settings
- **Integration with Existing Features**:
  - Extend `convert()` to support database sources/destinations
  - Enable `pipeline()` to work with database sources
  - Support DataFrame bridges (`.to_pandas()`, `.to_polars()`, `.to_dask()`) for database results
- **Discovery Helpers**:
  - Add `list_tables()` for SQL databases (schema, table name, row estimates)
  - Add `list_collections()` for MongoDB (collection names)
  - Add `list_indices()` for Elasticsearch/OpenSearch (index names)
- **Optional Dependencies**:
  - Add database drivers as optional dependencies (`psycopg2`, `pymongo`, `elasticsearch`, `pymysql`, `pyodbc`, etc.)
  - Raise helpful `ImportError` messages when dependencies are missing
  - Core library remains lightweight without database dependencies

## Impact
- **Affected Specs**:
  - `database-engines` - NEW capability for database engine support
  - `convert` - MODIFIED to support database sources/destinations
  - `pipeline` - MODIFIED to support database sources
- **Affected Files**:
  - `iterable/db/` (new directory) - Database driver implementations
    - `iterable/db/base.py` - `DBDriver` base class
    - `iterable/db/postgres.py` - Postgres driver
    - `iterable/db/mysql.py` - MySQL/MariaDB driver
    - `iterable/db/mssql.py` - MSSQL driver
    - `iterable/db/sqlite.py` - SQLite driver
    - `iterable/db/mongo.py` - MongoDB driver
    - `iterable/db/elasticsearch.py` - Elasticsearch/OpenSearch driver
    - `iterable/db/__init__.py` - Driver registry
  - `iterable/helpers/detect.py` - Modify `open_iterable()` to detect and route database engines
  - `iterable/convert/core.py` - Extend `convert()` to support database sources/destinations
  - `iterable/pipeline/core.py` - Ensure `pipeline()` works with database sources
  - `pyproject.toml` - Add optional dependencies for database drivers
  - `tests/test_db_engines.py` (new) - Comprehensive tests for database engines
  - `CHANGELOG.md` - Document new database engine feature
  - `docs/docs/api/database-engines.md` (new) - Documentation for database engine usage
- **Dependencies**:
  - New optional dependencies: `psycopg2-binary`, `pymongo`, `elasticsearch`, `pymysql`, `pyodbc`, `sqlalchemy` (optional)
  - All dependencies are optional - core library remains lightweight
  - Users only install database drivers they need
- **Backward Compatibility**:
  - All changes are additive and backward compatible
  - Existing file-based sources continue to work unchanged
  - Database engine support is opt-in via `engine` parameter
  - No breaking changes to existing APIs
