## 1. Implementation
- [ ] 1.1 Implement `bulk_convert()` function in `iterable/convert/core.py`
  - [ ] 1.1.1 Add function signature with parameters (source, dest, pattern, etc.)
  - [ ] 1.1.2 Implement glob pattern expansion using `pathlib` or `glob`
  - [ ] 1.1.3 Implement directory traversal for directory inputs
  - [ ] 1.1.4 Implement filename pattern generation (e.g., `{name}.parquet`)
  - [ ] 1.1.5 Create output directory if it doesn't exist
  - [ ] 1.1.6 Loop over input files and call `convert()` for each
  - [ ] 1.1.7 Aggregate results across all conversions
  - [ ] 1.1.8 Handle errors per-file and continue processing
  - [ ] 1.1.9 Support all `convert()` parameters (batch_size, iterableargs, etc.)
- [ ] 1.2 Create `BulkConversionResult` type in `iterable/types.py`
  - [ ] 1.2.1 Define result class with aggregated metrics
  - [ ] 1.2.2 Include per-file results list
  - [ ] 1.2.3 Include total statistics (files, rows, time, errors)
- [ ] 1.3 Add convenience export in `iterable/helpers/detect.py` (optional)
  - [ ] 1.3.1 Export `bulk_convert` from detect module for easier imports

## 2. Testing
- [ ] 2.1 Add tests for glob pattern matching
  - [ ] 2.1.1 Test `*.csv` pattern matching
  - [ ] 2.1.2 Test `*.csv.gz` pattern with compression
  - [ ] 2.1.3 Test nested glob patterns
- [ ] 2.2 Add tests for directory conversion
  - [ ] 2.2.1 Test converting entire directory
  - [ ] 2.2.2 Test preserving directory structure
  - [ ] 2.2.3 Test flat output mode
- [ ] 2.3 Add tests for filename pattern generation
  - [ ] 2.3.1 Test `{name}.parquet` pattern
  - [ ] 2.3.2 Test `{stem}.parquet` pattern
  - [ ] 2.3.3 Test extension replacement
  - [ ] 2.3.4 Test pattern with compression extensions
- [ ] 2.4 Add tests for error handling
  - [ ] 2.4.1 Test continuation after single file failure
  - [ ] 2.4.2 Test error collection in results
  - [ ] 2.4.3 Test partial success scenarios
- [ ] 2.5 Add tests for parameter passthrough
  - [ ] 2.5.1 Test batch_size parameter
  - [ ] 2.5.2 Test iterableargs parameter
  - [ ] 2.5.3 Test all convert() parameters
- [ ] 2.6 Add tests for aggregated results
  - [ ] 2.6.1 Test total file count
  - [ ] 2.6.2 Test total row counts
  - [ ] 2.6.3 Test total time aggregation
  - [ ] 2.6.4 Test per-file result access

## 3. Documentation
- [ ] 3.1 Update `docs/docs/api/convert.md`
  - [ ] 3.1.1 Add `bulk_convert()` function documentation
  - [ ] 3.1.2 Document parameters and usage examples
  - [ ] 3.1.3 Add examples for glob patterns
  - [ ] 3.1.4 Add examples for directory conversion
  - [ ] 3.1.5 Add examples for filename patterns
- [ ] 3.2 Update `CHANGELOG.md`
  - [ ] 3.2.1 Add entry for bulk conversion feature
  - [ ] 3.2.2 Include usage examples
- [ ] 3.3 Update `README.md` (if needed)
  - [ ] 3.3.1 Add bulk conversion example if appropriate

## 4. Validation
- [ ] 4.1 Run `openspec validate add-bulk-convert --strict`
- [ ] 4.2 Run linter: `ruff check iterable tests`
- [ ] 4.3 Run formatter: `ruff format iterable tests`
- [ ] 4.4 Run tests: `pytest tests/test_convert.py -v`
- [ ] 4.5 Verify all tests pass
