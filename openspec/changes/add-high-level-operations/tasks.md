## 1. Phase 1: Core Operations (Stats & Simple Transforms)

### 1.1 Module Structure
- [ ] 1.1.1 Create `iterable/ops/` directory structure
- [ ] 1.1.2 Create `iterable/ops/__init__.py` with module exports
- [ ] 1.1.3 Set up module-level documentation

### 1.2 Inspection Operations (`ops.inspect`)
- [ ] 1.2.1 Implement `inspect.count()` - Fast row counting with DuckDB support
- [ ] 1.2.2 Implement `inspect.head()` - Get first N rows
- [ ] 1.2.3 Implement `inspect.tail()` - Get last N rows
- [ ] 1.2.4 Implement `inspect.headers()` - Get column names
- [ ] 1.2.5 Implement `inspect.sniff()` - File format detection and metadata
- [ ] 1.2.6 Implement `inspect.analyze()` - Dataset structure analysis
- [ ] 1.2.7 Add tests in `tests/test_ops_inspect.py`
- [ ] 1.2.8 Add documentation in `docs/docs/api/ops-inspect.md`

### 1.3 Statistics Operations (`ops.stats`)
- [ ] 1.3.1 Implement `stats.compute()` - Comprehensive statistics with DuckDB pushdown
- [ ] 1.3.2 Implement `stats.frequency()` - Value frequency analysis
- [ ] 1.3.3 Implement `stats.uniq()` - Unique value detection
- [ ] 1.3.4 Add type inference and date detection
- [ ] 1.3.5 Add tests in `tests/test_ops_stats.py`
- [ ] 1.3.6 Add documentation in `docs/docs/api/ops-stats.md`

### 1.4 Basic Transform Operations (`ops.transform`)
- [ ] 1.4.1 Implement `transform.head()` - Slice first N rows
- [ ] 1.4.2 Implement `transform.tail()` - Slice last N rows
- [ ] 1.4.3 Implement `transform.sample()` - Random sampling
- [ ] 1.4.4 Implement `transform.deduplicate()` - Remove duplicates
- [ ] 1.4.5 Implement `transform.select()` - Column selection
- [ ] 1.4.6 Implement `transform.slice_rows()` - Row slicing
- [ ] 1.4.7 Add tests in `tests/test_ops_transform.py`
- [ ] 1.4.8 Add documentation in `docs/docs/api/ops-transform.md`

## 2. Phase 2: Filtering & Search

### 2.1 Filter Operations (`ops.filter`)
- [ ] 2.1.1 Implement expression parser for filter expressions
- [ ] 2.1.2 Implement `filter.filter_expr()` - Boolean expression filtering
- [ ] 2.1.3 Implement `filter.search()` - Regex search across fields
- [ ] 2.1.4 Add DuckDB pushdown support for filter operations
- [ ] 2.1.5 Add basic query support (MistQL-like)
- [ ] 2.1.6 Add tests in `tests/test_ops_filter.py`
- [ ] 2.1.7 Add documentation in `docs/docs/api/ops-filter.md`

## 3. Phase 3: Validation & Schema

### 3.1 Validation Framework (`validate`)
- [ ] 3.1.1 Create `iterable/validate/` directory structure
- [ ] 3.1.2 Implement `validate/core.py` - Validation engine
- [ ] 3.1.3 Implement `validate/rules.py` - Built-in validation rules
  - [ ] 3.1.3.1 Email validation rule
  - [ ] 3.1.3.2 URL validation rule
  - [ ] 3.1.3.3 Russian identifier rules (INN, OGRN)
  - [ ] 3.1.3.4 Custom validator registration system
- [ ] 3.1.4 Implement `validate.iterable()` - Validation pipeline
- [ ] 3.1.5 Add validation modes (stats, invalid, valid)
- [ ] 3.1.6 Add tests in `tests/test_validate.py`
- [ ] 3.1.7 Add documentation in `docs/docs/api/validate.md`

### 3.2 Schema Generation (`ops.schema`)
- [ ] 3.2.1 Implement `schema.infer()` - Schema inference from data
- [ ] 3.2.2 Implement `schema.to_jsonschema()` - JSON Schema output
- [ ] 3.2.3 Implement `schema.to_yaml()` - YAML output
- [ ] 3.2.4 Implement `schema.to_cerberus()` - Cerberus spec output
- [ ] 3.2.5 Implement `schema.to_avro()` - Avro schema output
- [ ] 3.2.6 Implement `schema.to_parquet_metadata()` - Parquet schema output
- [ ] 3.2.7 Add tests in `tests/test_ops_schema.py`
- [ ] 3.2.8 Add documentation in `docs/docs/api/ops-schema.md`

## 4. Phase 4: Advanced Transforms & Ingestion

### 4.1 Advanced Transform Operations (`ops.transform`)
- [ ] 4.1.1 Implement `transform.enum_field()` - Add sequence/enumeration
- [ ] 4.1.2 Implement `transform.reverse()` - Reverse row order
- [ ] 4.1.3 Implement `transform.fill_missing()` - Fill missing values
- [ ] 4.1.4 Implement `transform.rename_fields()` - Rename columns
- [ ] 4.1.5 Implement `transform.explode()` - Explode array/string fields
- [ ] 4.1.6 Implement `transform.replace_values()` - Value replacement
- [ ] 4.1.7 Implement `transform.sort_rows()` - Row sorting (with materialization)
- [ ] 4.1.8 Implement `transform.transpose()` - Transpose rows/columns
- [ ] 4.1.9 Implement `transform.split()` - Split fields
- [ ] 4.1.10 Implement `transform.fixlengths()` - Fix field lengths
- [ ] 4.1.11 Implement `transform.cat()` - Concatenate iterables
- [ ] 4.1.12 Update tests in `tests/test_ops_transform.py`
- [ ] 4.1.13 Update documentation in `docs/docs/api/ops-transform.md`

### 4.2 Relational Operations (`ops.transform`)
- [ ] 4.2.1 Implement `transform.join()` - Join two iterables
- [ ] 4.2.2 Implement `transform.diff()` - Set difference
- [ ] 4.2.3 Implement `transform.exclude()` - Exclude rows
- [ ] 4.2.4 Add DuckDB support for relational operations when possible
- [ ] 4.2.5 Update tests in `tests/test_ops_transform.py`
- [ ] 4.2.6 Update documentation in `docs/docs/api/ops-transform.md`

### 4.3 Database Ingestion (`ingest`)
- [ ] 4.3.1 Create `iterable/ingest/` directory structure
- [ ] 4.3.2 Implement `ingest/core.py` - Base ingestor interface
- [ ] 4.3.3 Implement `ingest/postgresql.py` - PostgreSQL ingestor
  - [ ] 4.3.3.1 Batch processing
  - [ ] 4.3.3.2 Upsert support
  - [ ] 4.3.3.3 Auto-create table
  - [ ] 4.3.3.4 Retry with backoff
  - [ ] 4.3.3.5 Progress reporting
- [ ] 4.3.4 Implement `ingest/sqlite.py` - SQLite ingestor
- [ ] 4.3.5 Implement `ingest/duckdb.py` - DuckDB ingestor
- [ ] 4.3.6 Implement `ingest/mongodb.py` - MongoDB ingestor
- [ ] 4.3.7 Implement `ingest/mysql.py` - MySQL ingestor
- [ ] 4.3.8 Implement `ingest/elasticsearch.py` - Elasticsearch ingestor
- [ ] 4.3.9 Implement `ingest.to_db()` - Unified ingestion API
- [ ] 4.3.10 Add tests in `tests/test_ingest.py`
- [ ] 4.3.11 Add documentation in `docs/docs/api/ingest.md`

## 5. Phase 5: AI-Powered Documentation

### 5.1 AI Documentation (`ai`)
- [ ] 5.1.1 Create `iterable/ai/` directory structure
- [ ] 5.1.2 Implement provider abstraction (OpenAI, OpenRouter, Ollama, LMStudio, Perplexity)
- [ ] 5.1.3 Implement `ai.doc.generate()` - AI-powered documentation generation
- [ ] 5.1.4 Integrate with schema inference for context
- [ ] 5.1.5 Add format support (markdown, JSON, etc.)
- [ ] 5.1.6 Add tests in `tests/test_ai.py` (with mocks for API calls)
- [ ] 5.1.7 Add documentation in `docs/docs/api/ai.md`

## 6. Integration & Polish

### 6.1 Module Exports
- [ ] 6.1.1 Update `iterable/__init__.py` to export new modules
- [ ] 6.1.2 Ensure consistent import patterns
- [ ] 6.1.3 Add module-level docstrings

### 6.2 Optional Dependencies
- [ ] 6.2.1 Update `pyproject.toml` with `ai` extra
- [ ] 6.2.2 Update `pyproject.toml` with `db` extra
- [ ] 6.2.3 Update `pyproject.toml` with `full` extra (all optional deps)
- [ ] 6.2.4 Document dependency requirements in README

### 6.3 Integration with Existing Features
- [ ] 6.3.1 Ensure operations work with `open_iterable()` return values
- [ ] 6.3.2 Ensure operations integrate with `pipeline()` framework
- [ ] 6.3.3 Test DuckDB pushdown integration
- [ ] 6.3.4 Test DataFrame bridge compatibility

### 6.4 Progress & Observability
- [ ] 6.4.1 Add progress callback support to operations (where applicable)
- [ ] 6.4.2 Integrate with existing observability patterns
- [ ] 6.4.3 Add metrics collection for operations

## 7. Testing

### 7.1 Unit Tests
- [ ] 7.1.1 All operations have comprehensive unit tests
- [ ] 7.1.2 Test edge cases (empty data, malformed data, etc.)
- [ ] 7.1.3 Test DuckDB pushdown when available
- [ ] 7.1.4 Test fallback behavior when DuckDB unavailable
- [ ] 7.1.5 Test optional dependency behavior (graceful degradation)

### 7.2 Integration Tests
- [ ] 7.2.1 Test operations with various file formats
- [ ] 7.2.2 Test operations with compressed files
- [ ] 7.2.3 Test operations with cloud storage
- [ ] 7.2.4 Test operations in pipeline context
- [ ] 7.2.5 Test database ingestion with real databases (test containers)

### 7.3 Performance Tests
- [ ] 7.3.1 Benchmark operations on large datasets
- [ ] 7.3.2 Compare DuckDB vs Python streaming performance
- [ ] 7.3.3 Document performance characteristics

## 8. Documentation

### 8.1 API Documentation
- [ ] 8.1.1 Complete all API documentation files
- [ ] 8.1.2 Add code examples for each operation
- [ ] 8.1.3 Document performance characteristics
- [ ] 8.1.4 Document optional dependency requirements

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
