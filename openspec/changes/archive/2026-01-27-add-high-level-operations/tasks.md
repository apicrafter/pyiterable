## 1. Phase 1: Core Operations (Stats & Simple Transforms)

### 1.1 Module Structure
- [x] 1.1.1 Create `iterable/ops/` directory structure
- [x] 1.1.2 Create `iterable/ops/__init__.py` with module exports
- [x] 1.1.3 Set up module-level documentation

### 1.2 Inspection Operations (`ops.inspect`)
- [x] 1.2.1 Implement `inspect.count()` - Fast row counting with DuckDB support
- [x] 1.2.2 Implement `inspect.head()` - Get first N rows
- [x] 1.2.3 Implement `inspect.tail()` - Get last N rows
- [x] 1.2.4 Implement `inspect.headers()` - Get column names
- [x] 1.2.5 Implement `inspect.sniff()` - File format detection and metadata
- [x] 1.2.6 Implement `inspect.analyze()` - Dataset structure analysis
- [x] 1.2.7 Add tests in `tests/test_ops_inspect.py`
- [x] 1.2.8 Add documentation in `docs/docs/api/ops-inspect.md`

### 1.3 Statistics Operations (`ops.stats`)
- [x] 1.3.1 Implement `stats.compute()` - Comprehensive statistics with DuckDB pushdown
- [x] 1.3.2 Implement `stats.frequency()` - Value frequency analysis
- [x] 1.3.3 Implement `stats.uniq()` - Unique value detection
- [x] 1.3.4 Add type inference and date detection
- [x] 1.3.5 Add tests in `tests/test_ops_stats.py`
- [x] 1.3.6 Add documentation in `docs/docs/api/ops-stats.md`

### 1.4 Basic Transform Operations (`ops.transform`)
- [x] 1.4.1 Implement `transform.head()` - Slice first N rows
- [x] 1.4.2 Implement `transform.tail()` - Slice last N rows
- [x] 1.4.3 Implement `transform.sample()` - Random sampling
- [x] 1.4.4 Implement `transform.deduplicate()` - Remove duplicates
- [x] 1.4.5 Implement `transform.select()` - Column selection
- [x] 1.4.6 Implement `transform.slice_rows()` - Row slicing
- [x] 1.4.7 Add tests in `tests/test_ops_transform.py`
- [x] 1.4.8 Add documentation in `docs/docs/api/ops-transform.md`

## 2. Phase 2: Filtering & Search

### 2.1 Filter Operations (`ops.filter`)
- [x] 2.1.1 Implement expression parser for filter expressions
- [x] 2.1.2 Implement `filter.filter_expr()` - Boolean expression filtering
- [x] 2.1.3 Implement `filter.search()` - Regex search across fields
- [x] 2.1.4 Add DuckDB pushdown support for filter operations
- [x] 2.1.5 Add basic query support (MistQL-like)
- [x] 2.1.6 Add tests in `tests/test_ops_filter.py`
- [x] 2.1.7 Add documentation in `docs/docs/api/ops-filter.md`

## 3. Phase 3: Validation & Schema

### 3.1 Validation Framework (`validate`)
- [x] 3.1.1 Create `iterable/validate/` directory structure
- [x] 3.1.2 Implement `validate/core.py` - Validation engine
- [x] 3.1.3 Implement `validate/rules.py` - Built-in validation rules
  - [x] 3.1.3.1 Email validation rule
  - [x] 3.1.3.2 URL validation rule
  - [x] 3.1.3.3 Russian identifier rules (INN, OGRN)
  - [x] 3.1.3.4 Custom validator registration system
- [x] 3.1.4 Implement `validate.iterable()` - Validation pipeline
- [x] 3.1.5 Add validation modes (stats, invalid, valid)
- [x] 3.1.6 Add tests in `tests/test_validate.py`
- [x] 3.1.7 Add documentation in `docs/docs/api/validate.md`

### 3.2 Schema Generation (`ops.schema`)
- [x] 3.2.1 Implement `schema.infer()` - Schema inference from data
- [x] 3.2.2 Implement `schema.to_jsonschema()` - JSON Schema output
- [x] 3.2.3 Implement `schema.to_yaml()` - YAML output
- [x] 3.2.4 Implement `schema.to_cerberus()` - Cerberus spec output
- [x] 3.2.5 Implement `schema.to_avro()` - Avro schema output
- [x] 3.2.6 Implement `schema.to_parquet_metadata()` - Parquet schema output
- [x] 3.2.7 Add tests in `tests/test_ops_schema.py`
- [x] 3.2.8 Add documentation in `docs/docs/api/ops-schema.md`

## 4. Phase 4: Advanced Transforms & Ingestion

### 4.1 Advanced Transform Operations (`ops.transform`)
- [x] 4.1.1 Implement `transform.enum_field()` - Add sequence/enumeration
- [x] 4.1.2 Implement `transform.reverse()` - Reverse row order
- [x] 4.1.3 Implement `transform.fill_missing()` - Fill missing values
- [x] 4.1.4 Implement `transform.rename_fields()` - Rename columns
- [x] 4.1.5 Implement `transform.explode()` - Explode array/string fields
- [x] 4.1.6 Implement `transform.replace_values()` - Value replacement
- [x] 4.1.7 Implement `transform.sort_rows()` - Row sorting (with materialization)
- [x] 4.1.8 Implement `transform.transpose()` - Transpose rows/columns
- [x] 4.1.9 Implement `transform.split()` - Split fields
- [x] 4.1.10 Implement `transform.fixlengths()` - Fix field lengths
- [x] 4.1.11 Implement `transform.cat()` - Concatenate iterables
- [x] 4.1.12 Update tests in `tests/test_ops_transform.py`
- [x] 4.1.13 Update documentation in `docs/docs/api/ops-transform.md`

### 4.2 Relational Operations (`ops.transform`)
- [x] 4.2.1 Implement `transform.join()` - Join two iterables
- [x] 4.2.2 Implement `transform.diff()` - Set difference
- [x] 4.2.3 Implement `transform.exclude()` - Exclude rows
- [x] 4.2.4 Add DuckDB support for relational operations when possible
- [x] 4.2.5 Update tests in `tests/test_ops_transform.py`
- [x] 4.2.6 Update documentation in `docs/docs/api/ops-transform.md`

### 4.3 Database Ingestion (`ingest`)
- [x] 4.3.1 Create `iterable/ingest/` directory structure
- [x] 4.3.2 Implement `ingest/core.py` - Base ingestor interface
- [x] 4.3.3 Implement `ingest/postgresql.py` - PostgreSQL ingestor
  - [x] 4.3.3.1 Batch processing
  - [x] 4.3.3.2 Upsert support
  - [x] 4.3.3.3 Auto-create table
  - [x] 4.3.3.4 Retry with backoff
  - [x] 4.3.3.5 Progress reporting
- [x] 4.3.4 Implement `ingest/sqlite.py` - SQLite ingestor
- [x] 4.3.5 Implement `ingest/duckdb.py` - DuckDB ingestor
- [x] 4.3.6 Implement `ingest/mongodb.py` - MongoDB ingestor
- [x] 4.3.7 Implement `ingest/mysql.py` - MySQL ingestor
- [x] 4.3.8 Implement `ingest/elasticsearch.py` - Elasticsearch ingestor
- [x] 4.3.9 Implement `ingest.to_db()` - Unified ingestion API
- [x] 4.3.10 Add tests in `tests/test_ingest.py`
- [x] 4.3.11 Add documentation in `docs/docs/api/ingest.md`

## 5. Phase 5: AI-Powered Documentation

### 5.1 AI Documentation (`ai`)
- [x] 5.1.1 Create `iterable/ai/` directory structure
- [x] 5.1.2 Implement provider abstraction (OpenAI, OpenRouter, Ollama, LMStudio, Perplexity)
- [x] 5.1.3 Implement `ai.doc.generate()` - AI-powered documentation generation
- [x] 5.1.4 Integrate with schema inference for context
- [x] 5.1.5 Add format support (markdown, JSON, etc.)
- [x] 5.1.6 Add tests in `tests/test_ai.py` (with mocks for API calls)
- [x] 5.1.7 Add documentation in `docs/docs/api/ai.md`

## 6. Integration & Polish

### 6.1 Module Exports
- [x] 6.1.1 Update `iterable/__init__.py` to export new modules
- [x] 6.1.2 Ensure consistent import patterns
- [x] 6.1.3 Add module-level docstrings

### 6.2 Optional Dependencies
- [x] 6.2.1 Update `pyproject.toml` with `ai` extra
- [x] 6.2.2 Update `pyproject.toml` with `db` extra
- [x] 6.2.3 Update `pyproject.toml` with `full` extra (all optional deps)
- [ ] 6.2.4 Document dependency requirements in README

### 6.3 Integration with Existing Features
- [x] 6.3.1 Ensure operations work with `open_iterable()` return values
- [x] 6.3.2 Ensure operations integrate with `pipeline()` framework
- [x] 6.3.3 Test DuckDB pushdown integration
- [x] 6.3.4 Test DataFrame bridge compatibility

### 6.4 Progress & Observability
- [x] 6.4.1 Add progress callback support to operations (where applicable)
- [x] 6.4.2 Integrate with existing observability patterns
- [ ] 6.4.3 Add metrics collection for operations

## 7. Testing

### 7.1 Unit Tests
- [x] 7.1.1 All operations have comprehensive unit tests
- [x] 7.1.2 Test edge cases (empty data, malformed data, etc.)
- [x] 7.1.3 Test DuckDB pushdown when available
- [x] 7.1.4 Test fallback behavior when DuckDB unavailable
- [x] 7.1.5 Test optional dependency behavior (graceful degradation)

### 7.2 Integration Tests
- [x] 7.2.1 Test operations with various file formats
- [x] 7.2.2 Test operations with compressed files
- [x] 7.2.3 Test operations with cloud storage
- [x] 7.2.4 Test operations in pipeline context
- [ ] 7.2.5 Test database ingestion with real databases (test containers)

### 7.3 Performance Tests
- [ ] 7.3.1 Benchmark operations on large datasets
- [ ] 7.3.2 Compare DuckDB vs Python streaming performance
- [ ] 7.3.3 Document performance characteristics

## 8. Documentation

### 8.1 API Documentation
- [x] 8.1.1 Complete all API documentation files
- [x] 8.1.2 Add code examples for each operation
- [ ] 8.1.3 Document performance characteristics
- [x] 8.1.4 Document optional dependency requirements

### 8.2 User Guides
- [ ] 8.2.1 Create "Getting Started with Operations" guide
- [ ] 8.2.2 Create "Performance Optimization" guide
- [ ] 8.2.3 Create "Database Ingestion" guide
- [ ] 8.2.4 Create "AI Documentation" guide

### 8.3 CHANGELOG
- [ ] 8.3.1 Document all new operations
- [ ] 8.3.2 Document optional dependencies
- [ ] 8.3.3 Note backward compatibility

### 8.4 README Updates
- [ ] 8.4.1 Add high-level operations to features list
- [ ] 8.4.2 Add quick examples
- [ ] 8.4.3 Update installation instructions for optional dependencies

## 9. Validation

### 9.1 Code Quality
- [ ] 9.1.1 Run linter: `ruff check iterable tests`
- [ ] 9.1.2 Run formatter: `ruff format iterable tests`
- [ ] 9.1.3 Run type checker: `mypy iterable`
- [ ] 9.1.4 Fix all linting and type errors

### 9.2 Test Coverage
- [ ] 9.2.1 Run tests: `pytest --verbose --cov=iterable`
- [ ] 9.2.2 Ensure coverage meets project standards
- [ ] 9.2.3 Fix any failing tests

### 9.3 OpenSpec Validation
- [ ] 9.3.1 Validate proposal: `openspec validate add-high-level-operations --strict`
- [ ] 9.3.2 Fix any validation errors
- [ ] 9.3.3 Ensure all requirements have scenarios

## 10. Future: Undatum Integration (Separate Effort)

### 10.1 Undatum Refactoring
- [ ] 10.1.1 Refactor Undatum commands to use iterabledata operations
- [ ] 10.1.2 Update Undatum tests to verify CLI argument passing
- [ ] 10.1.3 Ensure Undatum CLI behavior unchanged

### 10.2 Documentation Cross-Links
- [ ] 10.2.1 Add "Command-line frontends" section to iterabledata docs
- [ ] 10.2.2 Update Undatum docs to reference iterabledata
- [ ] 10.2.3 Add code examples showing library vs CLI usage
