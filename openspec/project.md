# Project Context

## Purpose
Iterable Data is a Python library for reading and writing data files row by row in a consistent, iterator-based interface. It abstracts away the differences between various data formats (CSV, JSON, Parquet, XML, etc.) and compression codecs, providing a unified API akin to `csv.DictReader` but with much broader support. It focuses on memory-efficient streaming processing, making it suitable for ETL pipelines and data conversion tasks where loading entire datasets into memory (like pandas) is not feasible or necessary.

## Tech Stack
-   **Language**: Python 3.10+
-   **Core Dependencies**: `chardet`, `tqdm`
-   **Optional Engines**: DuckDB (`duckdb` package)
-   **Testing**: `pytest`, `pytest-cov`, `pytest-benchmark`, `pytest-xdist`
-   **Linting & Formatting**: `ruff`
-   **Type Checking**: `mypy`
-   **Security**: `bandit`, `pip-audit`
-   **Build System**: `setuptools`

## Project Conventions

### Code Style
-   **Formatter**: `ruff` is used for both linting and formatting.
-   **Line Length**: 120 characters.
-   **Strings**: Double quotes (`"`) are preferred.
-   **Docstrings**: Google style docstrings.
-   **Imports**: Organized into standard library, third-party, and local imports.
-   **Type Hints**: Encouraged for all function signatures.

### Architecture Patterns
-   **Iterator Pattern**: The core abstraction is an iterable that yields rows (dictionaries).
-   **Factory Pattern**: `open_iterable()` is the main entry point, abstracting concrete class instantiation based on file extension or arguments.
-   **Component Structure**:
    -   `iterable/datatypes/`: implementations for specific formats (e.g., `CSVIterable`).
    -   `iterable/codecs/`: implementations for compression (e.g., `GZIPCodec`).
    -   `iterable/engines/`: alternate processing backends (e.g., DuckDB).

### Testing Strategy
-   **Framework**: `pytest`.
-   **Structure**: One test file per format/feature in `tests/` (e.g., `test_csv.py`).
-   **Coverage**: tracked via `pytest-cov`, report in `htmlcov/`.
-   **Requirements**: Tests must pass on Python 3.10, 3.11, and 3.12.

### Git Workflow
-   **Pre-commit**: Hooks configured for `ruff`, `bandit`, `pydocstyle`, `check-yaml`, etc.
-   **Commits**: Clear, descriptive messages.
-   **PRs**: Must pass CI checks (lint, format, test).

## Domain Context
-   **Streaming vs Batch**: Emphasize row-by-row processing over full in-memory loading.
-   **Format Diversity**: The library handles a vast array of formats (50+), from simple CSV to binary Avro/Parquet and nested XML.
-   **Compression**: Transparent handling of compression is a key feature.

## Important Constraints
-   **Memory Usage**: Core components must remain memory-efficient (streaming).
-   **Dependency usage**: Keep core dependencies light; use `project.optional-dependencies` for heavy format support (e.g., `pandas`, `pyarrow`).

## External Dependencies
-   **DuckDB**: Used for high-performance SQL-like querying on supported files.
-   **Format Libraries**: Relies on `lxml`, `openpyxl`, `pyarrow`, etc., for specific format parsing.
