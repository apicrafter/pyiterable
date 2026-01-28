# Design: Database Engines Support

## Context

IterableData currently supports file-based data sources through a unified `open_iterable()` API with format detection and multiple processing engines (`internal`, `duckdb`). This design extends the engine architecture to support SQL and NoSQL databases as first-class iterable data sources, treating database query results exactly like files: an iterator of `dict` rows.

## Goals / Non-Goals

### Goals
- **Unified API**: Database sources use the same `open_iterable()` interface as files
- **Streaming**: Support memory-efficient streaming of large database result sets
- **Read-only by default**: Ensure safety in analytical/ETL workloads
- **Seamless integration**: Work with existing features (convert, pipeline, DataFrame bridges)
- **Extensibility**: Plugin architecture for adding new database engines
- **Optional dependencies**: Core library remains lightweight

### Non-Goals
- **Write support**: Initial implementation is read-only (write support is future work)
- **Full SQL/NoSQL feature parity**: Focus on common read patterns, not all database-specific features
- **Connection pooling**: Rely on database drivers' built-in pooling if needed
- **Transaction management**: Simple read-only transactions, not complex transaction orchestration
- **Query optimization**: Push query optimization to database engines, not IterableData

## Decisions

### Decision: DBDriver Base Class Abstraction

**What**: Create a `DBDriver` base class that all database drivers inherit from, with a simple interface (`connect()`, `iterate()`, `close()`).

**Why**: 
- Provides consistent interface across different database types
- Enables driver registry and plugin architecture
- Simplifies integration with `open_iterable()`
- Allows shared error handling and metrics tracking

**Alternatives considered**:
- Direct integration without abstraction: Rejected - too much code duplication
- SQLAlchemy as universal abstraction: Rejected - adds heavy dependency, doesn't cover NoSQL well
- Per-database classes without base: Rejected - harder to maintain and extend

### Decision: Engine-based Routing in open_iterable()

**What**: Extend `open_iterable()` to detect database engines via `engine` parameter (e.g., `engine="postgres"`), route to appropriate driver, and return a database iterable.

**Why**:
- Consistent with existing engine architecture (`internal`, `duckdb`)
- Minimal API changes - users specify engine explicitly
- Clear separation between file-based and database-based sources
- Easy to extend with new database engines

**Alternatives considered**:
- Auto-detect database from connection string: Rejected - ambiguous, explicit is better
- Separate `open_database()` function: Rejected - breaks unified API principle
- URL scheme detection (e.g., `postgresql://`): Rejected - conflicts with file paths, less explicit

### Decision: Streaming via Batch Processing

**What**: All database drivers use batch-based streaming (fetch N rows at a time) rather than row-by-row fetching or full result set loading.

**Why**:
- Memory efficient for large result sets
- Balances network round-trips with memory usage
- Works consistently across SQL and NoSQL databases
- Configurable via `batch_size` parameter

**Alternatives considered**:
- Row-by-row fetching: Rejected - too many network round-trips for large datasets
- Full result set loading: Rejected - defeats purpose of streaming, memory issues
- Database-specific optimizations: Considered - may add later, but start with consistent approach

### Decision: Read-only by Default

**What**: All database engines default to `read_only=True`, and SQL engines wrap queries in read-only transactions where supported.

**Why**:
- Safety: Prevents accidental data modification in analytical/ETL workflows
- Aligns with IterableData's read-focused design
- Can be relaxed in future versions if needed
- Clear intent: IterableData is for data extraction, not modification

**Alternatives considered**:
- Read-write by default: Rejected - too risky for analytical workloads
- No read-only enforcement: Rejected - safety concern
- Explicit read-only flag required: Rejected - default should be safe

### Decision: Connection String/URL as Source Parameter

**What**: Use database connection strings/URLs (e.g., `postgresql://user:pass@host:5432/dbname`) as the `source` parameter in `open_iterable()`, with database-specific parameters in `iterableargs`.

**Why**:
- Standard format across databases
- Familiar to users (same as SQLAlchemy, etc.)
- Flexible: can also accept existing connection objects
- Clear separation: connection info in `source`, query info in `iterableargs`

**Alternatives considered**:
- Separate connection parameters: Rejected - too verbose, connection strings are standard
- Only connection objects: Rejected - less convenient, requires users to manage connections
- Config file approach: Rejected - adds complexity, connection strings are simpler

### Decision: Driver Registry Pattern

**What**: Implement a driver registry that maps engine names to driver classes, allowing registration of new drivers without modifying core code.

**Why**:
- Enables plugin architecture for third-party database engines
- Keeps core code clean and extensible
- Allows runtime driver registration
- Makes testing easier (mock drivers)

**Alternatives considered**:
- Hard-coded driver mapping: Rejected - less extensible
- Import-based discovery: Considered - may add later, but explicit registration is clearer

### Decision: Common Parameter Convention

**What**: Define a shared set of `iterableargs` that work across most databases (`query`, `batch_size`, `read_only`, `on_error`, `metrics`, `timeout`, etc.), with database-specific extensions.

**Why**:
- Consistent user experience across databases
- Easier to learn and use
- Enables generic code that works with multiple databases
- Still allows database-specific features via additional parameters

**Alternatives considered**:
- Database-specific parameters only: Rejected - too much variation, harder to use
- Fully generic parameters only: Rejected - loses database-specific capabilities

## Risks / Trade-offs

### Risk: Connection Management
**Risk**: Database connections need proper lifecycle management (open, use, close). If users forget to close or exceptions occur, connections may leak.

**Mitigation**: 
- Use context managers (`with` statement) consistently
- Ensure `close()` is called in `__exit__` and `__del__`
- Document best practices
- Consider connection pooling in future if needed

### Risk: Memory Usage with Large Result Sets
**Risk**: Even with batching, very large result sets could consume significant memory if not properly streamed.

**Mitigation**:
- Use database-specific streaming mechanisms (server-side cursors, scroll APIs)
- Default to reasonable `batch_size` values
- Document memory considerations
- Test with large datasets

### Risk: Database Driver Compatibility
**Risk**: Different database drivers have different APIs and capabilities, making unified interface challenging.

**Mitigation**:
- Start with well-established drivers (psycopg2, pymongo, etc.)
- Abstract differences in `DBDriver` base class
- Test across driver versions
- Document driver-specific behaviors

### Risk: Performance Overhead
**Risk**: Abstraction layer adds overhead compared to direct database access.

**Mitigation**:
- Keep abstraction thin
- Use database drivers' native streaming capabilities
- Benchmark and optimize hot paths
- Document performance characteristics

### Trade-off: Feature Completeness vs Simplicity
**Trade-off**: Supporting all database-specific features would make the API complex, but limiting features reduces utility.

**Decision**: Start with common read patterns, allow database-specific parameters for advanced use cases. Can extend later based on user feedback.

### Trade-off: Optional Dependencies vs Convenience
**Trade-off**: Making all database drivers optional keeps core lightweight but requires users to install dependencies.

**Decision**: Optional dependencies with helpful error messages. This aligns with IterableData's philosophy of keeping core lightweight while supporting many formats.

## Migration Plan

### Phase 1: Core Infrastructure (Week 1-2)
1. Implement `DBDriver` base class and registry
2. Implement `PostgresDriver` as reference implementation
3. Integrate with `open_iterable()`
4. Add basic tests

### Phase 2: Additional SQL Databases (Week 3-4)
1. Implement MySQL, MSSQL, SQLite drivers
2. Add `list_tables()` helpers
3. Expand test coverage

### Phase 3: NoSQL Databases (Week 5-6)
1. Implement MongoDB driver
2. Implement Elasticsearch/OpenSearch driver
3. Add `list_collections()` and `list_indices()` helpers
4. Expand test coverage

### Phase 4: Integration & Polish (Week 7-8)
1. Integrate with `convert()` and `pipeline()`
2. Verify DataFrame bridges work
3. Complete documentation
4. Performance testing and optimization

### Rollback Plan
- If critical issues arise, database engine support can be disabled by removing driver registrations
- No breaking changes to existing file-based functionality
- Optional dependencies mean removal doesn't affect core library

## Open Questions

1. **Write Support**: Should we plan write support architecture now, or defer entirely?
   - **Decision**: Defer for now, but ensure architecture doesn't prevent future write support

2. **Connection Pooling**: Should IterableData manage connection pools, or rely on drivers?
   - **Decision**: Rely on drivers for now, consider pooling in future if needed

3. **Query Validation**: Should we validate SQL queries for safety (e.g., prevent DROP TABLE)?
   - **Decision**: Read-only transactions provide safety, but may add explicit query validation later

4. **Schema Inference**: Should we infer schemas from database queries automatically?
   - **Decision**: Defer - can add later, not critical for initial implementation

5. **Async Support**: Should we support async/await for database operations?
   - **Decision**: Defer - sync interface first, async can be added later if needed

6. **SQLAlchemy Integration**: Should we support SQLAlchemy engines/connections directly?
   - **Decision**: Consider as optional convenience - users can pass SQLAlchemy connections if they want

7. **Error Recovery**: How should we handle transient database errors (retries, backoff)?
   - **Decision**: Basic retry support via `retries` parameter, rely on database drivers for advanced retry logic
