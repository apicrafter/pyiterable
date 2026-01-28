# Design: High-Level Operations Integration

## Context
This change integrates high-level data operations from Undatum's CLI into iterabledata as reusable library functions. The goal is to make iterabledata a complete data processing foundation while keeping Undatum as a thin CLI wrapper.

## Goals / Non-Goals

### Goals
- Provide all Undatum operations as library functions
- Maintain streaming-friendly, iterator-based design
- Leverage DuckDB for performance when available
- Keep core install lightweight with optional dependencies
- Ensure seamless integration with existing iterabledata APIs
- Support both programmatic and CLI use cases

### Non-Goals
- Replacing existing iterabledata APIs (all changes are additive)
- Requiring all dependencies for core functionality
- Breaking backward compatibility
- Implementing Undatum CLI refactoring (separate effort)

## Decisions

### Decision: Iterator-Based API Design
**What**: All operations accept and return iterators of dict-like rows.

**Why**: 
- Consistent with existing iterabledata design (`open_iterable()` returns iterators)
- Memory-efficient for large datasets
- Composable with `pipeline()` framework
- Natural fit for streaming processing

**Alternatives Considered**:
- DataFrame-based API: Rejected - conflicts with streaming design, requires materialization
- Separate batch API: Rejected - adds complexity, streaming covers most use cases

### Decision: Module Organization by Operation Type
**What**: Organize operations into `ops.transform`, `ops.stats`, `ops.filter`, etc.

**Why**:
- Clear separation of concerns
- Easy to discover related operations
- Allows selective imports
- Matches user mental model (transformations vs statistics vs filtering)

**Alternatives Considered**:
- Single `ops` module: Rejected - would become too large, harder to navigate
- Flat structure: Rejected - namespace pollution, harder to organize

### Decision: DuckDB Pushdown for Performance
**What**: Use DuckDB engine for operations when source format and engine support it.

**Why**:
- Significant performance improvement for large files
- DuckDB already integrated in iterabledata
- Transparent to users (automatic optimization)
- Falls back gracefully when DuckDB unavailable

**Alternatives Considered**:
- Always use Python streaming: Rejected - too slow for large datasets
- Require DuckDB: Rejected - adds required dependency, breaks lightweight core

### Decision: Optional Dependencies for Heavy Features
**What**: AI and database features in separate optional dependency groups.

**Why**:
- Keeps core install lightweight
- Users only install what they need
- Matches existing iterabledata pattern (duckdb, dataframes extras)
- Allows gradual adoption

**Alternatives Considered**:
- Include everything in core: Rejected - bloats install, many users don't need AI/DB
- Separate packages: Rejected - adds complexity, harder to maintain

### Decision: Validation Rules as Pluggable System
**What**: Built-in rules (email, URL, etc.) plus custom validator registration.

**Why**:
- Extensible for user-specific validation needs
- Reusable validation logic
- Consistent API for all validators
- Supports complex validation pipelines

**Alternatives Considered**:
- Hardcoded rules only: Rejected - too limiting, users need custom validation
- External validation library: Rejected - adds dependency, want integrated solution

### Decision: Schema Generation with Multiple Output Formats
**What**: Infer schema from data, support multiple output formats (JSON Schema, Avro, Parquet, etc.).

**Why**:
- Different tools require different schema formats
- Single inference, multiple outputs reduces duplication
- Matches Undatum's approach
- Useful for documentation and validation

**Alternatives Considered**:
- Single format only: Rejected - too limiting, users need different formats
- Format-specific inference: Rejected - duplicates logic, harder to maintain

### Decision: Database Ingestion with Abstract Base Class
**What**: `BaseIngestor` interface with concrete implementations per database.

**Why**:
- Consistent API across databases
- Easy to add new database support
- Shared logic (batching, retry, progress) in base class
- Testable with mock ingestors

**Alternatives Considered**:
- Database-specific APIs: Rejected - inconsistent, harder to learn
- Single generic ingestor: Rejected - too complex, database-specific optimizations needed

## Risks / Trade-offs

### Risk: Performance for Large Datasets
**Mitigation**: 
- Use DuckDB pushdown when available
- Streaming design prevents memory issues
- Document performance characteristics
- Provide benchmarks

### Risk: API Surface Area Growth
**Mitigation**:
- Clear module organization
- Comprehensive documentation
- Consistent naming conventions
- Type hints for discoverability

### Risk: Dependency Bloat
**Mitigation**:
- Optional dependencies for heavy features
- Core remains lightweight
- Clear documentation of what requires what
- Gradual adoption path

### Risk: Breaking Changes During Undatum Integration
**Mitigation**:
- All changes are additive
- Backward compatibility maintained
- Undatum refactoring is separate effort
- Shared tests ensure consistency

### Trade-off: Streaming vs Materialization
**Decision**: Prefer streaming, materialize only when necessary (e.g., full sort).

**Rationale**: Memory efficiency is core to iterabledata's value proposition. Operations that require materialization (like full sort) will document this clearly.

## Migration Plan

### Phase 1: Core Operations (Stats & Simple Transforms)
- Implement `ops.stats` (count, stats, frequency, uniq)
- Implement basic transforms (head, tail, sample, dedup, select, slice)
- Add tests and documentation
- **Deliverable**: Users can compute statistics and perform basic transforms

### Phase 2: Filtering & Search
- Add `filter_expr` and `search` (regex)
- Wire DuckDB engine for pushdown
- Add tests and documentation
- **Deliverable**: Users can filter and search data efficiently

### Phase 3: Validation & Schema
- Implement `validate.iterable()` with core rules
- Implement `schema.infer()` + JSON/YAML/JSONSchema output
- Add tests and documentation
- **Deliverable**: Users can validate data and generate schemas

### Phase 4: Relational Ops & Ingestion
- Add `join`, `diff`, `exclude`, and `cat` operations
- Implement `ingest.to_db` for PostgreSQL, SQLite, DuckDB
- Extend to MongoDB/MySQL/Elasticsearch
- Add tests and documentation
- **Deliverable**: Users can perform relational operations and ingest to databases

### Phase 5: AI-Powered Documentation
- Add `ai.doc.generate()` with provider selection
- Add tests and documentation
- **Deliverable**: Users can generate AI-powered documentation

### Rollback Strategy
- Each phase is independently deployable
- No breaking changes, so rollback is simply not using new features
- Optional dependencies mean removal doesn't affect core

## Open Questions

1. **MistQL Integration**: Should we include MistQL-like query support in `ops.filter`, or keep it separate?
   - **Decision**: Include basic query support, full MistQL as future enhancement

2. **Progress Reporting**: Should operations support progress callbacks like `convert()` and `pipeline()`?
   - **Decision**: Yes, use existing observability patterns for consistency

3. **Error Handling**: How should operations handle malformed data?
   - **Decision**: Use existing error handling controls, allow per-operation configuration

4. **Type Inference**: How detailed should type inference be in `ops.stats`?
   - **Decision**: Start with basic types (str, int, float, bool, date), extend based on feedback

5. **Schema Evolution**: Should schema generation handle schema evolution scenarios?
   - **Decision**: Initial version focuses on single-snapshot schemas, evolution as future enhancement
