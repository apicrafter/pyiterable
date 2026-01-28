## 1. Implementation

### 1.1 Core Atomic Write Logic
- [x] 1.1.1 Create helper function `_atomic_write()` in `iterable/convert/core.py` to handle temporary file creation and atomic rename
- [x] 1.1.2 Implement temporary filename generation (append `.tmp` or use `tempfile` module)
- [x] 1.1.3 Add cleanup logic for temporary files on both success and failure
- [x] 1.1.4 Handle edge cases: existing temp files, permission errors, cross-filesystem renames

### 1.2 Convert Function Updates
- [x] 1.2.1 Add `atomic: bool = False` parameter to `convert()` function signature
- [x] 1.2.2 Modify `convert()` to use temporary file when `atomic=True`
- [x] 1.2.3 Implement atomic rename after successful conversion
- [x] 1.2.4 Ensure proper cleanup of temporary files in error cases
- [x] 1.2.5 Update function docstring with `atomic` parameter documentation

### 1.3 Pipeline Function Updates
- [x] 1.3.1 Add `atomic: bool = False` parameter to `pipeline()` function signature
- [x] 1.3.2 Modify `Pipeline` class to support atomic writes for destination
- [x] 1.3.3 Implement temporary file handling in `Pipeline.run()` when destination is a file
- [x] 1.3.4 Ensure atomic rename happens after all writes complete
- [x] 1.3.5 Update function/class docstrings with `atomic` parameter documentation

### 1.4 BaseFileIterable Support (if needed)
- [x] 1.4.1 Evaluate if atomic write logic should be in `BaseFileIterable` or higher-level functions
- [x] 1.4.2 If needed, add atomic write support to `BaseFileIterable.close()` or similar method
- [x] 1.4.3 Ensure compatibility with codec wrappers and compression

### 1.5 Testing
- [x] 1.5.1 Add test for successful atomic write (verify temp file created and renamed)
- [x] 1.5.2 Add test for atomic write failure (verify original file preserved)
- [x] 1.5.3 Add test for cleanup of temporary files on error
- [x] 1.5.4 Add test for cross-filesystem rename error handling
- [x] 1.5.5 Add test for atomic write with `convert()` function
- [x] 1.5.6 Add test for atomic write with `pipeline()` function
- [x] 1.5.7 Add test for backward compatibility (default `atomic=False`)

### 1.6 Documentation
- [x] 1.6.1 Update `CHANGELOG.md` with atomic write feature
- [x] 1.6.2 Update `docs/docs/api/convert.md` with `atomic` parameter documentation
- [x] 1.6.3 Update `docs/docs/api/pipeline.md` with `atomic` parameter documentation
- [x] 1.6.4 Add usage examples showing atomic write in production scenarios
- [x] 1.6.5 Document limitations (e.g., cross-filesystem renames, append mode support)

### 1.7 Error Handling and Edge Cases
- [x] 1.7.1 Handle case where temporary file already exists
- [x] 1.7.2 Handle permission errors when creating temporary files
- [x] 1.7.3 Handle disk space errors gracefully
- [x] 1.7.4 Provide clear error messages for atomic operation failures
- [x] 1.7.5 Ensure temporary files are cleaned up even on unexpected exceptions
