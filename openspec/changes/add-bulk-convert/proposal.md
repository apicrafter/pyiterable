# Change: Add Bulk File Conversion

## Why
Users frequently need to convert multiple files at once, such as:
- Converting entire directories of data files between formats
- Processing glob patterns (e.g., `data/raw/*.csv.gz`)
- Batch ETL operations on multiple source files
- Format migration projects

Currently, users must manually loop over files and call `convert()` for each one, which:
- Requires boilerplate code for file discovery and iteration
- Makes it difficult to handle output filename generation
- Lacks unified progress tracking across multiple conversions
- Doesn't provide aggregated results for batch operations

Adding `bulk_convert()` will:
- Simplify multi-file conversion workflows
- Support glob patterns and directory processing
- Provide flexible output filename generation via patterns
- Aggregate conversion results across all files
- Maintain the same conversion quality as single-file `convert()`

## What Changes
- **New `bulk_convert()` Function**:
  - Accept glob patterns, directory paths, or lists of file paths
  - Support output directory specification with filename pattern generation
  - Reuse existing `convert()` function internally for each file
  - Aggregate results across all conversions
  - Support all existing `convert()` parameters (batch_size, iterableargs, etc.)
- **Filename Pattern Generation**:
  - Support pattern strings like `{name}.parquet` to derive output filenames
  - Extract base name from input files and apply pattern
  - Handle extension replacement (e.g., `.csv.gz` → `.parquet`)
  - Support `{name}`, `{stem}`, `{ext}` placeholders in patterns
- **Output Directory Handling**:
  - Create output directory if it doesn't exist
  - Preserve relative directory structure when converting directories
  - Support flat output (all files in single directory) or structure preservation
- **Progress Tracking**:
  - Track progress across all files in batch
  - Provide aggregated statistics (total files, total rows, total time)
  - Support per-file progress callbacks
- **Error Handling**:
  - Continue processing remaining files if one fails
  - Collect errors per file
  - Return aggregated results with per-file success/failure status

## Impact
- **Affected Specs**:
  - `convert` - ADDED capability for bulk/multi-file conversion
- **Affected Files**:
  - `iterable/convert/core.py` - Add `bulk_convert()` function
  - `iterable/helpers/detect.py` - Export `bulk_convert` from detect module (optional convenience)
  - `tests/test_convert.py` - Add tests for bulk conversion scenarios
  - `CHANGELOG.md` - Document new bulk conversion feature
  - `docs/docs/api/convert.md` - Add bulk conversion documentation
- **Dependencies**:
  - No new dependencies required (uses standard library `glob`, `pathlib`)
- **Backward Compatibility**:
  - All changes are additive and backward compatible
  - Existing `convert()` function remains unchanged
  - New functionality is opt-in via `bulk_convert()` function
