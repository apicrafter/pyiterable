# Change: Add Atomic Writes for Safer File Operations

## Why
When converting or processing data in production environments, file write operations can fail mid-process, leaving corrupted or incomplete output files. This creates several problems:

- **Data Loss Risk**: If a conversion fails halfway through, the output file may be partially written and unusable
- **Race Conditions**: Other processes may read incomplete files while they're being written
- **Recovery Complexity**: Partial files require cleanup and can cause downstream processing errors
- **Production Reliability**: Production ETL pipelines need guarantees that output files are either complete or don't exist

Currently, `convert()` and `pipeline()` write directly to the target file. If the process crashes, is interrupted, or encounters an error, the output file may be left in an incomplete state.

Adding atomic write support will:
- Ensure output files are only visible when fully written (using temporary files + rename)
- Prevent partial file corruption from crashes or interruptions
- Improve production reliability for critical data pipelines
- Optionally support append mode for continuous log writing scenarios

## What Changes
- **Atomic Write Option**:
  - Add `atomic=True` parameter to `convert()` and `pipeline()` functions
  - When enabled, write to a temporary file (e.g., `output.tmp`) and use `os.replace()` to atomically rename to final destination
  - Temporary files are cleaned up on failure (output file remains unchanged)
  - Default to `atomic=False` for backward compatibility
- **Temporary File Handling**:
  - Generate temporary filename by appending `.tmp` to target filename (or use `tempfile` for cross-platform safety)
  - Use `os.replace()` for atomic rename (works on same filesystem)
  - Clean up temporary files on both success and failure
  - Handle edge cases: existing temp files, permission issues, disk space
- **Append Mode Support** (optional, future consideration):
  - Consider append mode (`mode='a'`) for formats that support it (e.g., JSONL, CSV, text logs)
  - Enable continuous writing to log files without atomic rename overhead
  - Document which formats support append mode
- **Error Handling**:
  - Preserve original file if atomic write fails
  - Clear error messages when atomic operations fail (e.g., cross-filesystem rename)
  - Log temporary file cleanup operations

## Impact
- **Affected Specs**:
  - `convert` - MODIFIED to support atomic writes
  - `pipeline` - MODIFIED to support atomic writes
- **Affected Files**:
  - `iterable/convert/core.py` - Add `atomic` parameter and temporary file logic
  - `iterable/pipeline/core.py` - Add `atomic` parameter for destination writes
  - `iterable/base.py` - Potentially add atomic write support to `BaseFileIterable` (if needed)
  - `tests/test_convert.py` - Add tests for atomic write scenarios
  - `tests/test_pipeline.py` - Add tests for atomic write scenarios
  - `CHANGELOG.md` - Document new atomic write feature
  - `docs/docs/api/convert.md` - Document `atomic` parameter
  - `docs/docs/api/pipeline.md` - Document `atomic` parameter
- **Dependencies**:
  - No new dependencies required (uses standard library `os`, `tempfile`)
- **Backward Compatibility**:
  - All changes are backward compatible (default `atomic=False`)
  - Existing code continues to work without modification
  - New functionality is opt-in via `atomic=True` parameter
