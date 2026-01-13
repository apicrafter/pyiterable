# Design: Architecture Improvements Implementation

## Context
The IterableData library serves as a unified interface for reading and writing data files in various formats. It emphasizes streaming, memory-efficient processing for large datasets. However, analysis reveals critical architectural flaws that prevent it from meeting production requirements at scale.

**Stakeholders**: 
- Library users processing large datasets
- Developers maintaining and extending the library
- Organizations using the library in production ETL pipelines

**Constraints**:
- Must maintain backward compatibility where possible
- Cannot break existing user code unnecessarily
- Must support Python 3.10+
- Must keep core dependencies lightweight

## Goals / Non-Goals

### Goals
- Fix memory anti-patterns to enable true streaming for all formats
- Optimize bulk operations to provide actual performance benefits
- Provide actionable error handling through proper exception hierarchy
- Enable format detection for streams and files without extensions
- Improve code quality and maintainability
- Maintain backward compatibility where feasible

### Non-Goals
- Complete rewrite of the library (incremental improvements)
- Adding new format support (focus on improving existing)
- Changing the core API design (improve implementation, not interface)
- Performance optimizations that sacrifice code clarity

## Decisions

### Decision 1: Streaming JSON Implementation
**What**: Use `ijson` library for streaming JSON parsing instead of `json.load()`

**Why**: 
- `json.load()` loads entire file into memory, breaking streaming design
- `ijson` provides incremental parsing suitable for large files
- Maintains compatibility with existing JSON structure

**Alternatives Considered**:
- Custom streaming parser: Too complex, reinventing the wheel
- Keep `json.load()` with size warnings: Doesn't solve the problem
- Require JSONL format: Too restrictive for users

**Trade-offs**:
- Adds optional dependency (`ijson`)
- Slightly more complex code
- May have different error messages than standard `json`

### Decision 2: Exception Hierarchy Design
**What**: Create comprehensive exception hierarchy in `iterable/exceptions.py`

**Why**:
- Generic exceptions make error handling impossible
- Users need to catch specific errors programmatically
- Enables better error messages and debugging

**Alternatives Considered**:
- Keep generic exceptions: Doesn't solve the problem
- Minimal hierarchy: Not sufficient for all use cases
- Exception codes only: Less Pythonic, harder to use

**Trade-offs**:
- **BREAKING CHANGE**: Existing error handling code will need updates
- More exception classes to maintain
- Migration guide required

### Decision 3: Content-Based Detection Strategy
**What**: Implement magic number detection combined with heuristics

**Why**:
- Filename-only detection fails for streams and files without extensions
- Magic numbers are reliable for binary formats
- Heuristics work for text formats

**Alternatives Considered**:
- Filename-only: Doesn't solve the problem
- Content-only: May be slower, less reliable for some formats
- User-specified format: Too manual, poor UX

**Trade-offs**:
- More complex detection logic
- May have false positives for ambiguous content
- Requires reading file headers (minimal I/O cost)

### Decision 4: Bulk Operation Optimization Approach
**What**: Refactor `read_bulk()` to use format-specific bulk I/O operations

**Why**:
- Current implementations provide no performance benefit
- Users expect bulk operations to be faster
- Format-specific optimizations are possible

**Alternatives Considered**:
- Keep current implementation: Doesn't solve performance issue
- Generic buffering: Less efficient than format-specific
- Remove bulk operations: Breaks API, users rely on it

**Trade-offs**:
- More code to maintain per format
- May require format-specific knowledge
- Performance gains vary by format

### Decision 5: Base Class ABC Conversion
**What**: Convert `BaseIterable` to use `abc.ABC` with `@abstractmethod`

**Why**:
- Current design allows incomplete implementations
- Abstract methods enforce contract compliance
- Better IDE support and type checking

**Alternatives Considered**:
- Keep current design: Allows incomplete implementations
- Interface protocols: Less Pythonic, more complex
- Documentation-only: Not enforced, easy to miss

**Trade-offs**:
- All subclasses must implement abstract methods
- May require updates to existing formats
- More strict, but better design

## Risks / Trade-offs

### Risk 1: Breaking Changes from Exception Hierarchy
**Impact**: High - Users catching generic exceptions will need updates
**Mitigation**: 
- Provide comprehensive migration guide
- Maintain backward compatibility shims where possible
- Clear deprecation warnings before removal

### Risk 2: Performance Regressions from Refactoring
**Impact**: Medium - Bulk operations or detection may be slower
**Mitigation**:
- Comprehensive benchmarking before/after
- Performance regression tests
- Gradual rollout with feature flags

### Risk 3: Memory Issues in Production
**Impact**: High - Large files may still cause memory issues
**Mitigation**:
- Extensive testing with large files (10GB+)
- Memory profiling in CI
- Clear documentation of memory requirements

### Risk 4: Incomplete Implementation
**Impact**: Medium - Some formats may not be fully optimized
**Mitigation**:
- Prioritize most-used formats first
- Clear documentation of format-specific limitations
- Incremental improvements over time

## Migration Plan

### Phase 1: Critical Fixes (Non-Breaking)
- Streaming JSON implementation (adds functionality, doesn't break)
- Bulk operation optimization (improves performance, maintains API)
- Content-based detection (enhances detection, maintains backward compatibility)

### Phase 2: Exception Hierarchy (Breaking)
- Create new exception classes
- Add deprecation warnings for old exception patterns
- Provide migration guide
- Update all internal code
- Release with clear breaking change notice

### Phase 3: Base Class Changes (Potentially Breaking)
- Convert to ABC
- Update all format implementations
- Test thoroughly
- May require user code updates if they subclass

### Rollback Strategy
- Each phase can be rolled back independently
- Git tags for each phase
- Feature flags for new detection logic
- Maintain old exception classes as deprecated aliases

## Open Questions

1. **Streaming JSON Performance**: Will `ijson` be fast enough for production use? May need benchmarking.
2. **Exception Migration**: How many users will be affected? May need user survey.
3. **Bulk Operation API**: Should we change the API signature or keep it the same?
4. **Content Detection Confidence**: What confidence threshold should we use for auto-detection?
5. **ABC Migration**: Should we make all methods abstract or provide defaults?

## Success Criteria

- Memory usage <100MB for 10GB files (streaming)
- Bulk operations 10x faster than individual operations
- 100% specific exceptions, no generic `Exception`
- 95%+ type hint coverage
- 90%+ test coverage
- All critical issues (P0) resolved
