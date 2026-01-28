## Context
Production data conversion and pipeline operations need guarantees that output files are either complete or don't exist. Current implementation writes directly to target files, which can leave partial/corrupted files if operations fail mid-process.

## Goals / Non-Goals

### Goals
- Ensure output files are only visible when fully written
- Prevent partial file corruption from crashes or interruptions
- Maintain backward compatibility (opt-in feature)
- Support both `convert()` and `pipeline()` functions

### Non-Goals
- Append mode implementation (deferred for future consideration)
- Atomic writes for in-memory or stream destinations
- Cross-filesystem atomic operations (will raise clear errors)

## Decisions

### Decision: Use `os.replace()` for atomic rename
- **Rationale**: `os.replace()` (Python 3.3+) provides atomic rename on same filesystem, which is the standard approach for atomic file operations
- **Alternatives considered**:
  - `shutil.move()`: Not atomic on all platforms
  - `os.rename()`: May fail on Windows if destination exists
- **Limitation**: Only works on same filesystem; will raise clear error if attempted across filesystems

### Decision: Temporary file naming strategy
- **Approach**: Append `.tmp` suffix to target filename (e.g., `output.csv` → `output.csv.tmp`)
- **Rationale**: Simple, predictable, easy to identify and clean up
- **Alternatives considered**:
  - `tempfile` module: More robust but less predictable filenames
  - UUID-based names: More complex, harder to debug
- **Implementation**: Use `os.path.join(os.path.dirname(target), os.path.basename(target) + '.tmp')` for cross-platform safety

### Decision: Atomic write at function level, not BaseFileIterable
- **Rationale**: Atomic writes are a high-level concern (complete file operations), not per-write operation
- **Implementation**: Handle atomic logic in `convert()` and `pipeline()` functions, not in individual `write()`/`write_bulk()` calls
- **Benefits**: Simpler implementation, works with existing codec wrappers, doesn't require changes to all format implementations

### Decision: Cleanup on both success and failure
- **Approach**: Always clean up temporary files, whether operation succeeds or fails
- **Implementation**: Use try/finally blocks to ensure cleanup
- **Edge case**: If rename succeeds but cleanup fails, log warning but don't fail (temp file will be overwritten on next run)

### Decision: Default to `atomic=False` for backward compatibility
- **Rationale**: Existing code should continue working without changes
- **Migration path**: Users can opt-in to atomic writes by setting `atomic=True`
- **Future consideration**: Could make default `True` in major version bump

## Risks / Trade-offs

### Risk: Cross-filesystem rename failures
- **Mitigation**: Detect and raise clear error message explaining limitation
- **Trade-off**: Atomic writes only work on same filesystem (acceptable limitation)

### Risk: Temporary file conflicts
- **Mitigation**: Check if temp file exists and handle appropriately (overwrite or raise error)
- **Trade-off**: Very low probability in practice

### Risk: Performance overhead
- **Mitigation**: Minimal overhead (one extra rename operation at end)
- **Trade-off**: Acceptable for production safety guarantees

### Risk: Codec wrapper complexity
- **Mitigation**: Atomic logic happens at file level, after codec closes and flushes
- **Trade-off**: Works transparently with existing codec implementations

## Migration Plan

### Phase 1: Implementation
1. Add `atomic` parameter to `convert()` and `pipeline()`
2. Implement temporary file + rename logic
3. Add comprehensive tests
4. Update documentation

### Phase 2: Rollout
- Feature is opt-in, no breaking changes
- Users can gradually adopt atomic writes in production
- Monitor for edge cases or issues

### Rollback
- If issues arise, users can set `atomic=False` to revert to previous behavior
- No code changes required for rollback

## Open Questions

- Should we support append mode in this change or defer to future proposal?
  - **Decision**: Defer to future consideration (out of scope for atomic writes)
- Should atomic writes be default in future major version?
  - **Decision**: Consider for v2.0, but not in this change
- How to handle atomic writes with cloud storage (S3, GCS)?
  - **Decision**: Out of scope (cloud storage has different atomicity guarantees)
