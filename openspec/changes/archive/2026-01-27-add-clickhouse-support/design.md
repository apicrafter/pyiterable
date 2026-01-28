# Design: ClickHouse Database Engine Support

## Context

IterableData already supports database engines through the `DBDriver` base class architecture, with PostgreSQL implemented and other SQL/NoSQL databases planned. ClickHouse is a high-performance columnar OLAP database that has achieved significant market traction ($15B valuation in 2025) and is widely used for real-time analytics, observability, and data warehousing - use cases that align perfectly with IterableData's focus on analytical and ETL workflows.

This design extends the existing database engine architecture to support ClickHouse as a first-class iterable data source, following the same patterns established by the PostgreSQL driver while accommodating ClickHouse-specific features and characteristics.

## Goals / Non-Goals

### Goals
- **Unified API**: ClickHouse sources use the same `open_iterable()` interface as other database engines
- **Streaming**: Support memory-efficient streaming of large ClickHouse result sets using batch processing
- **Read-only by default**: Ensure safety in analytical/ETL workloads (ClickHouse doesn't have explicit read-only transactions, but we validate queries)
- **Seamless integration**: Work with existing features (convert, pipeline, DataFrame bridges)
- **ClickHouse-specific features**: Support ClickHouse query settings, native format, and database selection
- **Optional dependency**: Core library remains lightweight without ClickHouse driver

### Non-Goals
- **Write support**: Initial implementation is read-only (write support is future work)
- **Full ClickHouse feature parity**: Focus on common read patterns (SELECT queries), not all ClickHouse-specific features
- **Connection pooling**: Rely on ClickHouse driver's built-in pooling if needed
- **Query optimization**: Push query optimization to ClickHouse engine, not IterableData
- **Materialized views**: Focus on table queries, not materialized view management
- **Distributed queries**: Support single-server queries; distributed query coordination is ClickHouse's responsibility

## Decisions

### Decision: ClickHouse Driver Selection

**What**: Use `clickhouse-connect` as the primary ClickHouse driver for IterableData.

**Why**:
- Official driver recommended by ClickHouse
- Better enterprise compatibility (HTTP protocol works through firewalls/proxies)
- Built-in Pandas and Polars integration aligns with IterableData's DataFrame bridges
- SQLAlchemy dialect support provides additional flexibility
- Pure Python with optional Cython optimizations for performance
- Active maintenance and official support

**Alternatives considered**:
- `clickhouse-driver` (community driver): Considered - offers native TCP protocol with better performance, but less enterprise-friendly and not officially recommended. May add as alternative in future if users request it.
- Direct HTTP API calls: Rejected - too low-level, loses driver benefits (connection management, type conversion, etc.)

**Implementation note**: Support both connection string formats (`clickhouse://` for HTTP and `clickhouse+native://` for native TCP if we add clickhouse-driver support later).

### Decision: Streaming via Batch Processing with Native Format

**What**: Use ClickHouse's native binary format or JSONEachRow format for streaming results in batches, controlled by `batch_size` parameter and ClickHouse's `max_block_size` setting.

**Why**:
- Native format is more efficient than text formats (JSON, CSV)
- JSONEachRow provides human-readable alternative when needed
- Batch processing balances memory usage with network round-trips
- ClickHouse's columnar architecture naturally supports batch processing
- Configurable via `batch_size` parameter (maps to ClickHouse `max_block_size`)

**Alternatives considered**:
- Row-by-row fetching: Rejected - too many network round-trips for large datasets
- Full result set loading: Rejected - defeats purpose of streaming, memory issues
- Always use native format: Considered - but JSONEachRow is useful for debugging and compatibility

**Implementation**: Default to native format for performance, allow `format="JSONEachRow"` parameter for text-based formats.

### Decision: Query Settings Support

**What**: Support ClickHouse query settings via `settings` parameter (dictionary of key-value pairs) passed to query execution.

**Why**:
- ClickHouse query settings are essential for performance tuning (max_threads, max_memory_usage, etc.)
- Enables users to optimize queries for their specific use cases
- Common pattern in ClickHouse workflows
- No equivalent in other SQL databases, so ClickHouse-specific parameter

**Alternatives considered**:
- Ignore query settings: Rejected - too limiting, users need this for performance
- Hard-code common settings: Rejected - too opinionated, users should control this
- Settings in connection string: Rejected - query-level settings should be per-query, not connection-level

**Implementation**: Accept `settings` dict in `iterableargs`, pass to ClickHouse query execution.

### Decision: Database Parameter Support

**What**: Support `database` parameter in `iterableargs` to specify database name, in addition to connection string database.

**Why**:
- ClickHouse connection strings may not always include database name
- Allows users to query different databases without changing connection string
- Consistent with other database engines (PostgreSQL has `schema` parameter)
- Common pattern in ClickHouse workflows

**Alternatives considered**:
- Require database in connection string only: Rejected - less flexible
- Auto-detect database: Rejected - ambiguous, explicit is better

**Implementation**: If `database` parameter provided, use it; otherwise use database from connection string or default database.

### Decision: Read-only Query Validation

**What**: Since ClickHouse doesn't support explicit read-only transactions, validate queries to prevent non-SELECT statements (INSERT, DELETE, DROP, etc.) when `read_only=True` (default).

**Why**:
- ClickHouse lacks PostgreSQL-style read-only transactions
- Safety: Prevents accidental data modification in analytical/ETL workflows
- Aligns with IterableData's read-focused design
- Simple keyword-based validation is sufficient for common cases

**Alternatives considered**:
- No validation: Rejected - too risky, users might accidentally modify data
- Full SQL parsing: Rejected - too complex, keyword check is sufficient
- Rely on ClickHouse permissions: Considered - but explicit validation provides clearer error messages

**Implementation**: Simple keyword check for non-SELECT statements (INSERT, UPDATE, DELETE, DROP, CREATE, ALTER, TRUNCATE) when `read_only=True`. Allow opt-out via `read_only=False` if needed.

### Decision: Connection String Format

**What**: Support `clickhouse://` connection strings following standard URL format: `clickhouse://[user[:password]@]host[:port][/database][?param1=value1&param2=value2]`

**Why**:
- Standard URL format familiar to users
- Consistent with other database engines (postgresql://, mysql://)
- Supports authentication, host, port, database, and query parameters
- clickhouse-connect supports this format

**Alternatives considered**:
- Separate connection parameters: Rejected - too verbose, connection strings are standard
- Only connection objects: Rejected - less convenient, requires users to manage connections
- ClickHouse-specific format: Rejected - standard URL format is better

**Implementation**: Parse connection string using `clickhouse-connect`'s built-in parsing, extract components for connection.

### Decision: Table Name Auto-Query

**What**: Support table name as `query` parameter (e.g., `query="events"`), automatically building `SELECT * FROM events` query.

**Why**:
- Consistent with PostgreSQL driver behavior
- Convenient for simple use cases
- Reduces boilerplate for common patterns
- Users can still provide full SQL for complex queries

**Alternatives considered**:
- Require full SQL always: Rejected - less convenient, breaks consistency with other engines
- Auto-detect table vs SQL: Considered - but explicit is clearer, keyword detection is sufficient

**Implementation**: If `query` doesn't start with SQL keywords (SELECT, WITH, etc.), treat as table name and build `SELECT * FROM table` query.

### Decision: list_tables() Implementation

**What**: Query ClickHouse system tables (`system.tables`, `system.databases`) to list available tables with metadata (database, table name, row estimates).

**Why**:
- Consistent with PostgreSQL `list_tables()` helper
- Useful for discovery and introspection
- ClickHouse system tables provide rich metadata
- Enables users to explore available data sources

**Alternatives considered**:
- No helper function: Rejected - useful feature, consistent with other engines
- Query SHOW TABLES: Considered - but system tables provide more metadata (row counts, etc.)

**Implementation**: Query `system.tables` joined with `system.databases` to get table list with row count estimates from `system.parts` or `system.tables`.

## Risks / Trade-offs

### Risk: ClickHouse Driver Compatibility

**Risk**: clickhouse-connect API may change between versions, or users may prefer clickhouse-driver for performance reasons.

**Mitigation**:
- Pin minimum version in optional dependencies
- Abstract driver differences in `ClickHouseDriver` class
- Test across driver versions
- Document driver-specific behaviors
- Consider supporting both drivers in future if there's demand

### Risk: Query Validation False Positives

**Risk**: Simple keyword-based query validation may incorrectly flag valid SELECT queries (e.g., `SELECT * FROM insert_log` where "insert" is in table name).

**Mitigation**:
- Use word boundary checks (regex `\bINSERT\b`, etc.) to avoid false positives
- Test with common table names
- Provide clear error messages
- Allow opt-out via `read_only=False` if needed
- Document limitations

### Risk: Native Format Type Conversion

**Risk**: ClickHouse native format may have type conversion issues or incompatibilities with Python types.

**Mitigation**:
- Use clickhouse-connect's built-in type conversion
- Test with various ClickHouse data types
- Fall back to JSONEachRow format if native format causes issues
- Document type mapping
- Handle edge cases gracefully

### Risk: Memory Usage with Large Result Sets

**Risk**: Even with batching, very large ClickHouse result sets could consume significant memory, especially with wide tables.

**Mitigation**:
- Use ClickHouse's `max_block_size` setting to control batch size
- Default to reasonable `batch_size` values (10000 rows)
- Document memory considerations
- Test with large datasets
- Support column projection via `columns` parameter to reduce data transfer

### Trade-off: Performance vs Compatibility

**Trade-off**: Native format is faster but less compatible; JSONEachRow is more compatible but slower.

**Decision**: Default to native format for performance, allow JSONEachRow via `format` parameter for compatibility. Users can choose based on their needs.

### Trade-off: Query Settings Complexity

**Trade-off**: Supporting all ClickHouse query settings would be complex, but limiting settings reduces utility.

**Decision**: Support arbitrary settings dictionary - users pass what they need, driver passes through to ClickHouse. This keeps API simple while allowing full flexibility.

## Implementation Details

### ClickHouseDriver Class Structure

```python
class ClickHouseDriver(DBDriver):
    def __init__(self, source: str | Any, **kwargs: Any):
        # Initialize with connection string or existing client
        # Extract database, settings, format from kwargs
        
    def connect(self) -> None:
        # Create clickhouse-connect client
        # Parse connection string
        # Handle existing client objects
        
    def _build_query(self) -> str:
        # Build SQL query from parameters
        # Handle table name auto-query
        # Apply columns, filter parameters
        
    def _validate_read_only(self, query: str) -> None:
        # Check for non-SELECT statements if read_only=True
        # Raise ValueError if unsafe query detected
        
    def iterate(self) -> Iterator[Row]:
        # Execute query with settings
        # Stream results in batches
        # Convert to dict rows
        # Handle native format or JSONEachRow
        
    @staticmethod
    def list_tables(connection_string: str, database: str | None = None, **kwargs) -> list[dict]:
        # Query system.tables and system.databases
        # Return list of dicts with metadata
```

### Connection String Parsing

- Support `clickhouse://user:pass@host:9000/database` format
- Extract: user, password, host, port (default 8123 for HTTP), database
- Pass query parameters to clickhouse-connect
- Handle SSL/TLS via connection parameters

### Query Building

- If `query` is table name (no SQL keywords), build `SELECT * FROM table`
- Apply `columns` parameter for projection: `SELECT col1, col2 FROM table`
- Apply `filter` parameter for WHERE clause: `SELECT * FROM table WHERE filter`
- Apply `database` parameter: `SELECT * FROM database.table`
- Apply `settings` parameter to query execution

### Streaming Implementation

- Use `clickhouse-connect` client's `query()` method with streaming
- Set `max_block_size` based on `batch_size` parameter
- Iterate over result blocks
- Convert each row to dict with column names as keys
- Handle both native format (default) and JSONEachRow format

### Error Handling

- Connection errors: Raise `ConnectionError` with helpful message
- Query errors: Raise `RuntimeError` or ClickHouse-specific exceptions
- Missing driver: Raise `ImportError` with installation instructions
- Invalid queries: Raise `ValueError` with validation error details

## Migration Plan

### Phase 1: Core Implementation (Week 1)
1. Implement `ClickHouseDriver` class following `PostgresDriver` pattern
2. Support basic connection and query execution
3. Implement streaming with batch processing
4. Add query validation for read-only safety

### Phase 2: ClickHouse-Specific Features (Week 1-2)
1. Add `settings` parameter support
2. Add `database` parameter support
3. Add `format` parameter support (native vs JSONEachRow)
4. Implement `list_tables()` helper

### Phase 3: Integration & Testing (Week 2)
1. Integrate with `open_iterable()` via driver registry
2. Test with `convert()` function
3. Test with `pipeline()` function
4. Verify DataFrame bridges work
5. Add comprehensive tests

### Phase 4: Documentation & Polish (Week 2)
1. Update documentation
2. Add examples
3. Update CHANGELOG
4. Performance testing
5. Validation and linting

### Rollback Plan
- If critical issues arise, ClickHouse driver can be disabled by removing registration
- No breaking changes to existing functionality
- Optional dependency means removal doesn't affect core library

## Open Questions

1. **clickhouse-driver support**: Should we support both clickhouse-connect and clickhouse-driver?
   - **Decision**: Start with clickhouse-connect only. Add clickhouse-driver support later if users request it or if performance requirements demand native TCP protocol.

2. **Query result format**: Should we always use native format, or make it configurable?
   - **Decision**: Default to native format for performance, allow JSONEachRow via `format` parameter for compatibility and debugging.

3. **Connection pooling**: Should IterableData manage ClickHouse connection pools?
   - **Decision**: Rely on clickhouse-connect's built-in connection management. Users can pass pooled connections if needed.

4. **Distributed queries**: Should we support distributed ClickHouse queries?
   - **Decision**: Defer - single-server queries first. Distributed query coordination is ClickHouse's responsibility via cluster configuration.

5. **Materialized views**: Should we support querying ClickHouse materialized views?
   - **Decision**: Yes - materialized views appear as tables in system.tables, so they work automatically with table name queries.

6. **ClickHouse-specific data types**: How should we handle ClickHouse-specific types (Array, Tuple, Map, etc.)?
   - **Decision**: Rely on clickhouse-connect's type conversion. Test with various types and document any limitations.

7. **Compression**: Should we enable compression for query results?
   - **Decision**: Use clickhouse-connect defaults. ClickHouse HTTP protocol supports compression automatically, native protocol uses LZ4 by default.
