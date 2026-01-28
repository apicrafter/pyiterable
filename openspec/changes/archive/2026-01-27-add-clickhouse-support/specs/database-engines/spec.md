## MODIFIED Requirements

### Requirement: Database Engine Support
The system SHALL support reading data from SQL and NoSQL databases as iterable data sources, treating database query results exactly like files: an iterator of `dict` rows, with the same error handling, metrics, pipelines, and DataFrame bridges.

#### Scenario: PostgreSQL query as iterable source
- **WHEN** a user calls `open_iterable("postgresql://user:pass@host:5432/dbname", engine="postgres", query="SELECT id, name, created_at FROM users WHERE active = TRUE")`
- **THEN** the system connects to PostgreSQL, executes the query, and returns an iterable that yields dict rows with keys `id`, `name`, `created_at`

#### Scenario: PostgreSQL table name auto-query
- **WHEN** a user calls `open_iterable("postgresql://user:pass@host:5432/dbname", engine="postgres", query="users")` with a table name instead of SQL query
- **THEN** the system automatically builds and executes `SELECT * FROM users`, returning an iterable of all rows from the table

#### Scenario: PostgreSQL streaming with batch size
- **WHEN** a user calls `open_iterable("postgresql://...", engine="postgres", query="SELECT * FROM large_table", batch_size=5000)`
- **THEN** the system uses server-side cursors to stream results in batches of 5000 rows, maintaining memory efficiency for large result sets

#### Scenario: PostgreSQL read-only transaction
- **WHEN** a user calls `open_iterable("postgresql://...", engine="postgres", query="SELECT * FROM users")` with default `read_only=True`
- **THEN** the system wraps the query in a read-only transaction, preventing accidental data modification

#### Scenario: ClickHouse query execution
- **WHEN** a user calls `open_iterable("clickhouse://user:pass@host:9000/dbname", engine="clickhouse", query="SELECT id, name, created_at FROM users WHERE active = 1")`
- **THEN** the system connects to ClickHouse, executes the query, and returns an iterable that yields dict rows with keys `id`, `name`, `created_at`

#### Scenario: ClickHouse table name auto-query
- **WHEN** a user calls `open_iterable("clickhouse://user:pass@host:9000/dbname", engine="clickhouse", query="events")` with a table name instead of SQL query
- **THEN** the system automatically builds and executes `SELECT * FROM events`, returning an iterable of all rows from the table

#### Scenario: ClickHouse streaming with batch size
- **WHEN** a user calls `open_iterable("clickhouse://...", engine="clickhouse", query="SELECT * FROM large_table", batch_size=10000)`
- **THEN** the system streams results in batches of 10000 rows using ClickHouse's native format or JSONEachRow, maintaining memory efficiency for large result sets

#### Scenario: ClickHouse database parameter
- **WHEN** a user calls `open_iterable("clickhouse://user:pass@host:9000", engine="clickhouse", database="analytics", query="SELECT * FROM events")`
- **THEN** the system connects to the specified database and executes the query, returning an iterable of dict rows

#### Scenario: ClickHouse query settings
- **WHEN** a user calls `open_iterable("clickhouse://...", engine="clickhouse", query="SELECT * FROM table", settings={"max_threads": 4, "max_memory_usage": 10000000000})`
- **THEN** the system executes the query with the specified ClickHouse settings, enabling query-level configuration

#### Scenario: ClickHouse list_tables helper
- **WHEN** a user calls `list_tables(engine="clickhouse", connection_string="clickhouse://...")`
- **THEN** the system returns a list of dicts with database, table name, and row count estimates for all tables accessible to the user

#### Scenario: MySQL query execution
- **WHEN** a user calls `open_iterable("mysql://user:pass@host:3306/dbname", engine="mysql", query="SELECT * FROM orders")`
- **THEN** the system connects to MySQL, executes the query using server-side cursors, and returns an iterable of dict rows

#### Scenario: MongoDB collection query
- **WHEN** a user calls `open_iterable("mongodb://user:pass@host:27017", engine="mongo", database="analytics", collection="events", filter={"status": "ok"})`
- **THEN** the system connects to MongoDB, queries the specified collection with the filter, and returns an iterable of dict documents

#### Scenario: MongoDB aggregation pipeline
- **WHEN** a user calls `open_iterable("mongodb://...", engine="mongo", database="analytics", collection="events", pipeline=[{"$match": {"status": "ok"}}, {"$group": {"_id": "$category"}}])`
- **THEN** the system executes the aggregation pipeline and returns an iterable of result documents

#### Scenario: Elasticsearch scroll-based iteration
- **WHEN** a user calls `open_iterable("https://user:pass@es-host:9200", engine="elasticsearch", index="logs-2024-01", body={"query": {"match_all": {}}}, scroll="5m", size=10000)`
- **THEN** the system uses Elasticsearch scroll API to iterate through results in pages of 10000 hits, maintaining the scroll context for the specified timeout

#### Scenario: Elasticsearch source-only results
- **WHEN** a user calls `open_iterable("https://...", engine="elasticsearch", index="logs", source_only=True)`
- **THEN** the system yields only `hit["_source"]` for each document, excluding Elasticsearch metadata

#### Scenario: Database iterable with context manager
- **WHEN** a user uses `with open_iterable("postgresql://...", engine="postgres", query="SELECT * FROM users") as rows:`
- **THEN** the database connection is automatically closed when exiting the context manager, ensuring proper resource cleanup

#### Scenario: Database iterable metrics
- **WHEN** a user iterates over a database result set
- **THEN** the iterable tracks metrics (rows processed, bytes transferred, elapsed time) consistent with file-based iterables

#### Scenario: Database error handling
- **WHEN** a database query fails (e.g., invalid SQL, connection error)
- **THEN** the system raises an appropriate exception with a clear error message, consistent with file-based error handling

#### Scenario: Missing database driver dependency
- **WHEN** a user calls `open_iterable("postgresql://...", engine="postgres")` without `psycopg2-binary` installed
- **THEN** the system raises an ImportError with a helpful message indicating that `psycopg2-binary` must be installed for PostgreSQL support

#### Scenario: Missing ClickHouse driver dependency
- **WHEN** a user calls `open_iterable("clickhouse://...", engine="clickhouse")` without ClickHouse driver installed
- **THEN** the system raises an ImportError with a helpful message indicating that `clickhouse-connect` must be installed for ClickHouse support

#### Scenario: Database source in convert()
- **WHEN** a user calls `convert(fromfile="postgresql://...", tofile="output.parquet", iterableargs={"engine": "postgres", "query": "SELECT * FROM orders"})`
- **THEN** the system reads from PostgreSQL and writes to Parquet, handling connection lifecycle automatically

#### Scenario: ClickHouse source in convert()
- **WHEN** a user calls `convert(fromfile="clickhouse://...", tofile="output.parquet", iterableargs={"engine": "clickhouse", "query": "SELECT * FROM events"})`
- **THEN** the system reads from ClickHouse and writes to Parquet, handling connection lifecycle automatically

#### Scenario: Database source in pipeline()
- **WHEN** a user calls `pipeline(source="postgresql://...", destination="s3://bucket/output.parquet", process_func=enrich, iterableargs={"engine": "postgres", "query": "SELECT * FROM orders"})`
- **THEN** the system processes rows from PostgreSQL through the pipeline function and writes to the destination, streaming efficiently

#### Scenario: ClickHouse source in pipeline()
- **WHEN** a user calls `pipeline(source="clickhouse://...", destination="s3://bucket/output.parquet", process_func=enrich, iterableargs={"engine": "clickhouse", "query": "SELECT * FROM events"})`
- **THEN** the system processes rows from ClickHouse through the pipeline function and writes to the destination, streaming efficiently

#### Scenario: Database source DataFrame bridge
- **WHEN** a user calls `open_iterable("postgresql://...", engine="postgres", query="SELECT * FROM events").to_pandas()`
- **THEN** the system streams database rows into a pandas DataFrame, maintaining memory efficiency

#### Scenario: ClickHouse source DataFrame bridge
- **WHEN** a user calls `open_iterable("clickhouse://...", engine="clickhouse", query="SELECT * FROM events").to_pandas()`
- **THEN** the system streams ClickHouse rows into a pandas DataFrame, maintaining memory efficiency

#### Scenario: Database source chunked DataFrame bridge
- **WHEN** a user calls `for chunk in open_iterable("postgresql://...", engine="postgres", query="SELECT * FROM large_table").to_pandas(chunksize=100000):`
- **THEN** the system yields pandas DataFrames in chunks of 100000 rows, enabling processing of very large result sets

#### Scenario: ClickHouse source chunked DataFrame bridge
- **WHEN** a user calls `for chunk in open_iterable("clickhouse://...", engine="clickhouse", query="SELECT * FROM large_table").to_pandas(chunksize=100000):`
- **THEN** the system yields pandas DataFrames in chunks of 100000 rows, enabling processing of very large result sets

#### Scenario: List tables helper for PostgreSQL
- **WHEN** a user calls `list_tables(engine="postgres", connection_string="postgresql://...")`
- **THEN** the system returns a list of dicts with schema, table name, and row count estimates for all tables in the database

#### Scenario: List collections helper for MongoDB
- **WHEN** a user calls `list_collections(engine="mongo", connection_string="mongodb://...", database="analytics")`
- **THEN** the system returns a list of collection names in the specified database

#### Scenario: List indices helper for Elasticsearch
- **WHEN** a user calls `list_indices(engine="elasticsearch", connection_string="https://...")`
- **THEN** the system returns a list of index names in the Elasticsearch cluster

#### Scenario: Database iterable reset (when supported)
- **WHEN** a user calls `.reset()` on a database iterable that supports reset (e.g., SQLite with in-memory database)
- **THEN** the system re-executes the query and allows re-iteration over the result set

#### Scenario: Database iterable reset (not supported)
- **WHEN** a user calls `.reset()` on a database iterable that doesn't support reset (e.g., PostgreSQL with server-side cursor)
- **THEN** the system raises an appropriate exception indicating that reset is not supported for this database engine

#### Scenario: Backward compatibility with file sources
- **WHEN** a user calls `open_iterable("data.csv")` with a file path and no engine parameter
- **THEN** the system continues to work exactly as before, detecting the file format and using the internal engine, with no changes to existing behavior

#### Scenario: Database connection string parsing
- **WHEN** a user provides a database connection string (e.g., `postgresql://user:pass@host:5432/dbname`)
- **THEN** the system parses the connection string and extracts connection parameters (host, port, database, credentials)

#### Scenario: ClickHouse connection string parsing
- **WHEN** a user provides a ClickHouse connection string (e.g., `clickhouse://user:pass@host:9000/dbname` or `clickhouse+native://user:pass@host:9000/dbname`)
- **THEN** the system parses the connection string and extracts connection parameters (host, port, database, credentials)

#### Scenario: Existing database connection object
- **WHEN** a user passes an existing database connection object (e.g., `psycopg2.connection`) as the source parameter
- **THEN** the system uses the existing connection instead of creating a new one, allowing integration with connection pooling

#### Scenario: Existing ClickHouse client object
- **WHEN** a user passes an existing ClickHouse client object (e.g., `clickhouse_connect.get_client()`) as the source parameter
- **THEN** the system uses the existing client instead of creating a new one, allowing integration with connection pooling

#### Scenario: Database-specific parameters
- **WHEN** a user provides database-specific parameters (e.g., `schema` for PostgreSQL, `projection` for MongoDB)
- **THEN** the system passes these parameters to the appropriate database driver, enabling database-specific features

#### Scenario: ClickHouse-specific parameters
- **WHEN** a user provides ClickHouse-specific parameters (e.g., `settings` dict, `format` string, `database` name)
- **THEN** the system passes these parameters to the ClickHouse driver, enabling ClickHouse-specific query configuration

#### Scenario: Batch size configuration
- **WHEN** a user specifies `batch_size=1000` in iterableargs
- **THEN** the database driver fetches results in batches of 1000 rows/documents, balancing memory usage and network round-trips

#### Scenario: Timeout configuration
- **WHEN** a user specifies `timeout=30` in iterableargs
- **THEN** the database driver uses a 30-second timeout for connection and query operations

#### Scenario: SSL/TLS configuration
- **WHEN** a user specifies `ssl_mode="require"` or `verify=True` in iterableargs
- **THEN** the database driver configures SSL/TLS appropriately for secure connections

#### Scenario: Error handling strategy
- **WHEN** a user specifies `on_error="skip"` in iterableargs and a row fails to parse
- **THEN** the system skips the problematic row and continues iteration, consistent with file-based error handling

#### Scenario: Multiple database engines in same workflow
- **WHEN** a user processes data from multiple databases (e.g., PostgreSQL → MongoDB → file)
- **THEN** each database connection is managed independently, with proper cleanup for each source

#### Scenario: ClickHouse in multi-database workflow
- **WHEN** a user processes data from multiple databases (e.g., ClickHouse → PostgreSQL → file)
- **THEN** each database connection is managed independently, with proper cleanup for each source
