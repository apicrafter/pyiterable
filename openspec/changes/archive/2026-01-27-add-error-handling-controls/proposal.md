# Change: Add Error Handling Controls

## Why
Real-world data is often messy and contains malformed records. Currently, when a parse error occurs during iteration, the entire operation fails, forcing users to either:
- Manually wrap every iteration in try/except blocks
- Accept that one bad record stops the entire data processing pipeline
- Write custom error handling logic for each format

This makes the library less robust for production ETL pipelines where data quality issues are common. Users need configurable error policies that allow them to:
- Skip bad records and continue processing
- Log errors for later analysis while continuing
- Get detailed contextual information about where errors occurred (file, row, byte offset, original line)

Adding configurable error handling controls will make `iterabledata` more production-ready and user-friendly for handling dirty data.

## What Changes
- **Configurable Error Policy**:
  - Add `on_error` parameter to `iterableargs` with options: `'raise'` (default), `'skip'`, `'warn'`
  - When `'skip'`: silently skip malformed records and continue iteration
  - When `'warn'`: log warning and continue iteration (uses Python's `warnings` module)
  - When `'raise'`: current behavior - raise exception immediately
- **Error Logging**:
  - Add `error_log` parameter to `iterableargs` (file path or file-like object)
  - When provided, errors are logged to the specified file with contextual information
  - Log format includes: timestamp, file name, row/byte offset, error message, original line (if available)
- **Enhanced Parse Error Context**:
  - Extend `FormatParseError` and related exceptions to include:
    - File name (if available)
    - Row number/offset (approximate when possible)
    - Byte offset in file
    - Original line content (for text formats)
  - Make contextual information available even when error policy is 'skip' or 'warn'
- **Error Callback Support** (optional enhancement):
  - Add `on_error_callback` parameter for custom error handling functions
  - Callback receives error object and can return action: 'raise', 'skip', 'warn'

## Impact
- **Affected Specs**:
  - `error-handling` - MODIFIED to add configurable error policies and enhanced context
- **Affected Files**:
  - `iterable/exceptions.py` - Enhance `FormatParseError` and related exceptions with contextual attributes
  - `iterable/base.py` - Add error handling logic to `BaseIterable.read()` and iteration methods
  - `iterable/helpers/detect.py` - Pass error handling configuration through `open_iterable()`
  - `iterable/datatypes/*.py` - Update format-specific implementations to use error policy and capture context
  - `tests/test_error_handling.py` (new) - Comprehensive tests for error policies and logging
  - `CHANGELOG.md` - Document new error handling features
- **Dependencies**:
  - No new required dependencies (uses standard library `warnings` and `logging` modules)
- **Backward Compatibility**:
  - Default behavior (`on_error='raise'`) maintains current behavior
  - All changes are additive and backward compatible
  - Existing code continues to work without modifications
