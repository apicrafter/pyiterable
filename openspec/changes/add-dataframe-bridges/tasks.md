## 1. Implementation

### 1.1 Core Bridge Methods
- [x] 1.1.1 Add `to_pandas(chunksize=None)` method to `BaseIterable` in `iterable/base.py`
  - [x] Handle `chunksize=None` case: collect all rows and return single DataFrame
  - [x] Handle `chunksize` specified: return iterator of DataFrames
  - [x] Add proper ImportError handling with helpful message
  - [x] Handle nested data structures (flatten or preserve as dict/list columns)
- [x] 1.1.2 Add `to_polars(chunksize=None)` method to `BaseIterable` in `iterable/base.py`
  - [x] Handle `chunksize=None` case: collect all rows and return single DataFrame
  - [x] Handle `chunksize` specified: return iterator of DataFrames
  - [x] Add proper ImportError handling with helpful message
  - [x] Leverage Polars lazy evaluation when appropriate
- [x] 1.1.3 Add `to_dask()` method to `BaseIterable` in `iterable/base.py`
  - [x] Support single file conversion
  - [x] Add proper ImportError handling with helpful message
  - [x] Build Dask DataFrame from iterable

### 1.2 Dask Multi-File Support
- [x] 1.2.1 Create `iterable/helpers/bridges.py` module
- [x] 1.2.2 Implement `to_dask(files)` helper function for multiple files
  - [x] Accept list of file paths or patterns
  - [x] Use `open_iterable()` to detect formats for each file
  - [x] Build Dask computation graph from multiple files
  - [x] Return unified Dask DataFrame

### 1.3 Dependencies
- [x] 1.3.1 Add optional dependencies to `pyproject.toml`:
  - [x] Add `pandas` to optional dependencies
  - [x] Add `polars` to optional dependencies
  - [x] Add `dask[dataframe]` to optional dependencies
  - [x] Update `all` convenience group to include new dependencies

## 2. Testing

- [x] 2.1 Create `tests/test_dataframe_bridges.py`
- [x] 2.2 Test `to_pandas()` method:
  - [x] Test with `chunksize=None` (single DataFrame)
  - [x] Test with `chunksize` specified (iterator of DataFrames)
  - [x] Test with nested data structures
  - [x] Test ImportError when pandas not installed (mock)
  - [x] Test with various formats (CSV, JSONL, etc.)
  - [x] Test with empty files
  - [x] Test with large files (chunked processing)
- [x] 2.3 Test `to_polars()` method:
  - [x] Test with `chunksize=None` (single DataFrame)
  - [x] Test with `chunksize` specified (iterator of DataFrames)
  - [x] Test with nested data structures
  - [x] Test ImportError when polars not installed (mock)
  - [x] Test with various formats (CSV, JSONL, etc.)
  - [x] Test with empty files
  - [x] Test with large files (chunked processing)
- [x] 2.4 Test `to_dask()` method:
  - [x] Test single file conversion
  - [x] Test multi-file conversion via helper function
  - [x] Test ImportError when dask not installed (mock)
  - [x] Test with various formats
  - [x] Test Dask computation graph correctness
- [ ] 2.5 Run all tests: `pytest tests/test_dataframe_bridges.py -v`

## 3. Documentation

- [x] 3.1 Create `docs/docs/api/dataframe-bridges.md`:
  - [x] Document `to_pandas()` method with examples
  - [x] Document `to_polars()` method with examples
  - [x] Document `to_dask()` method and multi-file helper
  - [x] Include chunked processing examples
  - [x] Include installation instructions for optional dependencies
  - [x] Include performance considerations
- [x] 3.2 Update `CHANGELOG.md`:
  - [x] Add entry for DataFrame bridges feature
  - [x] Document new methods and optional dependencies
- [x] 3.3 Update main README if needed:
  - [x] Add DataFrame bridges to features list
  - [x] Add quick example in usage section

## 4. Validation

- [x] 4.1 Run linter: `ruff check iterable tests`
- [x] 4.2 Run formatter: `ruff format iterable tests`
- [x] 4.3 Run type checker: `mypy iterable` (with --ignore-missing-imports for optional deps)
- [ ] 4.4 Run all tests: `pytest --verbose` (requires optional dependencies: pandas, polars, dask)
- [x] 4.5 Validate OpenSpec: `openspec validate add-dataframe-bridges --strict`
