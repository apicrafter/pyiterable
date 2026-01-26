# Change: Add Observability (Progress, Metrics, and Logging)

## Why
For long-running conversions and data pipelines, users need visibility into progress and performance metrics. Currently, the `convert()` function returns `None` and only provides basic progress bars via `tqdm` when `silent=False`. The `pipeline()` function returns a stats dictionary, but there's no standardized way to track progress during execution or get structured metrics from conversions.

Without proper observability:
- Users cannot programmatically track conversion progress (e.g., for CI/CD, monitoring systems)
- No standardized metrics object makes it difficult to integrate with monitoring tools
- Progress callbacks are not available for custom progress reporting
- Metrics are not easily accessible for programmatic workflows

Adding observability features will:
- Enable progress tracking via callbacks for both `convert()` and `pipeline()`
- Provide standardized metrics objects for programmatic access
- Support built-in progress bars with optional `tqdm` integration
- Make it easier to integrate IterableData into monitoring and automation workflows

## What Changes
- **Progress Callbacks**:
  - Add `progress` parameter to `convert()` function accepting a callback function
  - Add `progress` parameter to `pipeline()` function accepting a callback function
  - Callback receives stats dictionary with fields like `rows_read`, `rows_written`, `elapsed`, `estimated_total`
  - Callbacks are invoked periodically during processing (configurable frequency)
- **Built-in Progress Bars**:
  - Add `show_progress` parameter to `convert()` function (boolean, uses `tqdm` if installed)
  - Enhance existing `silent` parameter behavior to work with new progress system
  - Provide helper function that uses `tqdm` when available, graceful fallback when not
- **Standardized Metrics Objects**:
  - Create `ConversionResult` class with fields: `rows_in`, `rows_out`, `elapsed_seconds`, `bytes_read`, `bytes_written`, `errors`
  - Modify `convert()` to return `ConversionResult` instead of `None`
  - Create `PipelineResult` class extending the existing stats dictionary pattern with structured fields
  - Ensure metrics are available both during execution (via callbacks) and after completion (via return value)
- **Backward Compatibility**:
  - Existing code using `convert()` without return value handling continues to work
  - `silent` parameter behavior preserved (defaults to `True`)
  - `pipeline()` stats dictionary structure maintained for existing code

## Impact
- **Affected Specs**:
  - `observability` - NEW capability for progress tracking and metrics
- **Affected Files**:
  - `iterable/convert/core.py` - Add progress callback support, return `ConversionResult`
  - `iterable/pipeline/core.py` - Add progress callback support, enhance return value
  - `iterable/types.py` (new or existing) - Define `ConversionResult` and `PipelineResult` classes
  - `pyproject.toml` - Ensure `tqdm` remains in dependencies (already present)
  - `tests/test_convert.py` - Add tests for progress callbacks and metrics
  - `tests/test_pipeline.py` - Add tests for progress callbacks
  - `tests/test_observability.py` (new) - Comprehensive tests for observability features
  - `CHANGELOG.md` - Document new observability features
  - `docs/docs/api/convert.md` - Update documentation with progress and metrics examples
  - `docs/docs/api/pipeline.md` - Update documentation with progress and metrics examples
  - `docs/docs/api/observability.md` (new) - Documentation for observability features
- **Dependencies**:
  - `tqdm` is already a core dependency (no new dependencies required)
  - Optional: Consider making `tqdm` optional in future, but not required for this change
- **Backward Compatibility**:
  - All changes are additive and backward compatible
  - `convert()` can still be called without handling return value
  - `silent` parameter defaults to `True` (existing behavior)
  - `pipeline()` stats dictionary structure maintained
  - Progress callbacks are optional parameters
