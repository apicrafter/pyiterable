# Change: Add High-Level Operations (Integrate Undatum Concepts)

## Why
Currently, iterabledata provides powerful low-level functionality (unified iterable API, format detection, compression, DuckDB integration, pipelines, DataFrame bridges) but lacks high-level operations that are available in Undatum's CLI. This creates a gap where:

- Users must implement common data operations (stats, filtering, validation, transforms) themselves
- Undatum's CLI contains valuable logic that isn't accessible to library users
- Code duplication exists between Undatum and potential library users
- The library cannot serve as a complete foundation for data processing workflows

By "pulling up" Undatum's best ideas into iterabledata as reusable library functions:
- Undatum's CLI becomes a thin wrapper over iterabledata
- Python users can access all high-level operations programmatically
- New features can be added in one place (iterabledata) and surface in CLI "for free"
- The library becomes a complete, production-ready data processing foundation

## What Changes
- **New Operation Modules**:
  - `iterabledata.ops.transform` - Row/column transformations (enum, reverse, fill, rename, explode, replace, dedup, sort, slice, sample, select, transpose, etc.)
  - `iterabledata.ops.stats` - Statistics, frequency analysis, unique value detection, type inference
  - `iterabledata.ops.filter` - Boolean expression filtering, regex search, query support
  - `iterabledata.ops.schema` - Schema generation (YAML, JSON, Cerberus, JSON Schema, Avro, Parquet)
  - `iterabledata.ops.inspect` - Dataset inspection (count, head, tail, headers, sniff, analyze)
  - `iterabledata.validate` - Validation rules and validation pipeline (email, URL, custom rules)
  - `iterabledata.ingest` - Database ingestion (PostgreSQL, MongoDB, DuckDB, MySQL, SQLite, Elasticsearch)
  - `iterabledata.ai` - Optional AI-powered documentation and field descriptions

- **Optional Dependencies**:
  - Add `ai` extra for AI features (openai, openrouter, ollama, lmstudio, perplexity)
  - Add `db` extra for database ingestion (psycopg, pymongo, mysqlclient, elasticsearch)
  - Keep existing `duckdb` and `dataframes` extras

- **Integration with Existing Features**:
  - All operations work with iterators of dict-like rows (compatible with `open_iterable()`)
  - Operations integrate seamlessly with `pipeline()` framework
  - DuckDB engine used for pushdown optimization when available
  - Operations are streaming-friendly where possible

- **Backward Compatibility**:
  - All changes are additive (new modules, no breaking changes)
  - Existing code continues to work unchanged
  - Optional dependencies mean core install remains lightweight

## Impact
- **Affected Specs**:
  - `ops-transform` - NEW capability for row/column transformations
  - `ops-stats` - NEW capability for statistics and frequency analysis
  - `ops-filter` - NEW capability for filtering and search
  - `ops-schema` - NEW capability for schema generation
  - `ops-inspect` - NEW capability for dataset inspection
  - `validate` - NEW capability for data validation
  - `ingest` - NEW capability for database ingestion
  - `ai` - NEW capability for AI-powered documentation

- **Affected Files**:
  - `iterable/ops/` (new directory) - Operation modules
    - `iterable/ops/__init__.py` - Module exports
    - `iterable/ops/transform.py` - Transformation operations
    - `iterable/ops/stats.py` - Statistics operations
    - `iterable/ops/filter.py` - Filtering operations
    - `iterable/ops/schema.py` - Schema generation
    - `iterable/ops/inspect.py` - Inspection operations
  - `iterable/validate/` (new directory) - Validation framework
    - `iterable/validate/__init__.py` - Module exports
    - `iterable/validate/core.py` - Validation engine
    - `iterable/validate/rules.py` - Built-in validation rules
  - `iterable/ingest/` (new directory) - Database ingestion
    - `iterable/ingest/__init__.py` - Module exports
    - `iterable/ingest/core.py` - Base ingestor interface
    - `iterable/ingest/postgresql.py` - PostgreSQL ingestor
    - `iterable/ingest/mongodb.py` - MongoDB ingestor
    - `iterable/ingest/duckdb.py` - DuckDB ingestor
    - `iterable/ingest/mysql.py` - MySQL ingestor
    - `iterable/ingest/sqlite.py` - SQLite ingestor
    - `iterable/ingest/elasticsearch.py` - Elasticsearch ingestor
  - `iterable/ai/` (new directory) - AI-powered features
    - `iterable/ai/__init__.py` - Module exports
    - `iterable/ai/doc.py` - Documentation generation
  - `iterable/__init__.py` - Export new modules
  - `pyproject.toml` - Add optional dependencies
  - `tests/test_ops_transform.py` (new) - Transform operation tests
  - `tests/test_ops_stats.py` (new) - Statistics operation tests
  - `tests/test_ops_filter.py` (new) - Filter operation tests
  - `tests/test_ops_schema.py` (new) - Schema generation tests
  - `tests/test_ops_inspect.py` (new) - Inspection operation tests
  - `tests/test_validate.py` (new) - Validation tests
  - `tests/test_ingest.py` (new) - Ingestion tests
  - `tests/test_ai.py` (new) - AI feature tests
  - `CHANGELOG.md` - Document new high-level operations
  - `docs/docs/api/ops-transform.md` (new) - Transform operations documentation
  - `docs/docs/api/ops-stats.md` (new) - Statistics operations documentation
  - `docs/docs/api/ops-filter.md` (new) - Filter operations documentation
  - `docs/docs/api/ops-schema.md` (new) - Schema generation documentation
  - `docs/docs/api/ops-inspect.md` (new) - Inspection operations documentation
  - `docs/docs/api/validate.md` (new) - Validation documentation
  - `docs/docs/api/ingest.md` (new) - Ingestion documentation
  - `docs/docs/api/ai.md` (new) - AI features documentation

- **Dependencies**:
  - Core: No new required dependencies
  - Optional `ai` extra: openai>=1.0, openrouter, ollama, lmstudio, perplexity
  - Optional `db` extra: psycopg[binary], pymongo, mysqlclient, elasticsearch>=8.0
  - Existing optional dependencies remain unchanged

- **Integration Points**:
  - Operations work with `open_iterable()` return values
  - Operations integrate with `pipeline()` framework
  - DuckDB engine used for optimization when available
  - Operations are compatible with DataFrame bridges

- **Future Undatum Integration**:
  - Undatum CLI will be refactored to use these library functions
  - Shared tests will ensure consistency
  - Documentation will cross-link between library and CLI
