## 1. Implementation

### 1.1 Metrics Classes
- [ ] 1.1.1 Create or update `iterable/types.py` with metrics classes:
  - [ ] Define `ConversionResult` class with fields: `rows_in`, `rows_out`, `elapsed_seconds`, `bytes_read`, `bytes_written`, `errors`
  - [ ] Define `PipelineResult` class extending stats pattern with structured fields
  - [ ] Add type hints and docstrings
  - [ ] Make classes dataclasses or use `@dataclass` decorator for clean attribute access

### 1.2 Convert Function Enhancements
- [ ] 1.2.1 Update `iterable/convert/core.py`:
  - [ ] Add `progress` parameter (optional callback function)
  - [ ] Add `show_progress` parameter (boolean, uses tqdm if installed)
  - [ ] Implement progress callback invocation during conversion
  - [ ] Track metrics: rows_read, rows_written, elapsed time, bytes processed
  - [ ] Modify function to return `ConversionResult` instead of `None`
  - [ ] Ensure backward compatibility (existing code still works)
  - [ ] Integrate `show_progress` with existing `silent` parameter logic
  - [ ] Handle cases where `tqdm` is not available gracefully

### 1.3 Pipeline Function Enhancements
- [ ] 1.3.1 Update `iterable/pipeline/core.py`:
  - [ ] Add `progress` parameter (optional callback function)
  - [ ] Implement progress callback invocation during pipeline execution
  - [ ] Enhance return value to use `PipelineResult` class (maintain backward compatibility)
  - [ ] Track additional metrics: rows_processed, throughput, etc.
  - [ ] Ensure existing stats dictionary structure is preserved

### 1.4 Progress Helper Functions
- [ ] 1.4.1 Create progress helper utilities:
  - [ ] Create helper function that wraps `tqdm` with graceful fallback
  - [ ] Support custom progress bar formatting
  - [ ] Handle progress updates at configurable intervals

## 2. Testing

- [ ] 2.1 Create `tests/test_observability.py`:
  - [ ] Test `ConversionResult` class creation and attribute access
  - [ ] Test `PipelineResult` class creation and attribute access
  - [ ] Test progress callbacks in `convert()`:
    - [ ] Callback invoked with correct stats structure
    - [ ] Callback receives updates at appropriate intervals
    - [ ] Multiple callbacks can be registered (if supported)
  - [ ] Test progress callbacks in `pipeline()`:
    - [ ] Callback invoked with correct stats structure
    - [ ] Callback receives updates during execution
  - [ ] Test `show_progress` parameter in `convert()`:
    - [ ] Progress bar displayed when `show_progress=True`
    - [ ] No progress bar when `show_progress=False` or `silent=True`
    - [ ] Graceful handling when `tqdm` not available
  - [ ] Test metrics collection:
    - [ ] Verify `rows_in` and `rows_out` are accurate
    - [ ] Verify `elapsed_seconds` is calculated correctly
    - [ ] Verify `bytes_read` and `bytes_written` are tracked (if applicable)
  - [ ] Test backward compatibility:
    - [ ] Existing code using `convert()` without return value still works
    - [ ] Existing code using `pipeline()` with stats dict still works
    - [ ] `silent` parameter behavior unchanged

- [ ] 2.2 Update `tests/test_convert.py`:
  - [ ] Add tests for progress callbacks
  - [ ] Add tests for `show_progress` parameter
  - [ ] Add tests for `ConversionResult` return value
  - [ ] Ensure existing tests still pass

- [ ] 2.3 Update `tests/test_pipeline.py`:
  - [ ] Add tests for progress callbacks
  - [ ] Add tests for enhanced return value
  - [ ] Ensure existing tests still pass

- [ ] 2.4 Run all tests: `pytest tests/test_observability.py tests/test_convert.py tests/test_pipeline.py -v`

## 3. Documentation

- [ ] 3.1 Create `docs/docs/api/observability.md`:
  - [ ] Document progress callbacks with examples
  - [ ] Document `show_progress` parameter usage
  - [ ] Document `ConversionResult` class and its fields
  - [ ] Document `PipelineResult` class and its fields
  - [ ] Include examples for programmatic metrics access
  - [ ] Include examples for CI/CD and monitoring integration

- [ ] 3.2 Update `docs/docs/api/convert.md`:
  - [ ] Add `progress` parameter documentation
  - [ ] Add `show_progress` parameter documentation
  - [ ] Update return value documentation (now returns `ConversionResult`)
  - [ ] Add examples using progress callbacks
  - [ ] Add examples accessing conversion metrics

- [ ] 3.3 Update `docs/docs/api/pipeline.md`:
  - [ ] Add `progress` parameter documentation
  - [ ] Update return value documentation (enhanced with `PipelineResult`)
  - [ ] Add examples using progress callbacks
  - [ ] Add examples accessing pipeline metrics

- [ ] 3.4 Update `CHANGELOG.md`:
  - [ ] Add entry for observability features
  - [ ] Document new parameters and return values
  - [ ] Note backward compatibility

- [ ] 3.5 Update main README if needed:
  - [ ] Add observability to features list
  - [ ] Add quick example showing progress tracking

## 4. Validation

- [ ] 4.1 Run linter: `ruff check iterable tests`
- [ ] 4.2 Run formatter: `ruff format iterable tests`
- [ ] 4.3 Run type checker: `mypy iterable`
- [ ] 4.4 Run all tests: `pytest --verbose`
- [ ] 4.5 Validate OpenSpec: `openspec validate add-observability --strict`
