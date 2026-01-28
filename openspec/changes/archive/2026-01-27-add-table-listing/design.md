## Context
Many data formats contain multiple tables, sheets, datasets, or other named collections. Users need to discover these before or after opening a file. The implementation should be efficient, developer-friendly, and consistent across formats.

## Goals / Non-Goals

### Goals
- Provide both class method and instance method APIs for maximum flexibility
- Reuse open connections/files when possible for efficiency
- Consistent behavior across all supported formats
- Clear indication when a format doesn't support table listing
- Handle edge cases gracefully (empty files, missing dependencies)

### Non-Goals
- Listing files within ZIP archives (different use case, already handled by ZIP codec)
- Listing nested structures in formats like JSON (not "tables" in the same sense)
- Modifying existing table selection parameters (`page`, `table`, etc.)

## Decisions

### Decision: Dual API (Class Method + Instance Method)
**What**: Support both `XLSXIterable.list_tables(filename)` (class method) and `iterable.list_tables()` (instance method)

**Why**: 
- Class method allows discovery without instantiating the full iterable (useful for exploration)
- Instance method allows discovery after opening, reusing existing connections
- Both patterns are common in Python libraries (e.g., `pandas.read_excel` vs `df.columns`)

**Alternatives considered**:
- Only instance method: Less flexible, requires full file opening
- Only class method: Can't reuse open connections, less efficient

### Decision: Return Type Consistency
**What**: All implementations return `list[str]` of names, or `None` if not supported

**Why**:
- Consistent API across formats
- `None` clearly indicates "not supported" vs empty list `[]` which means "no tables"
- List of strings is simple and Pythonic

**Alternatives considered**:
- Return dict with metadata: More complex, not needed for basic discovery
- Return tuples with indices: Less intuitive, indices can be derived from list position

### Decision: Reuse Open Connections
**What**: When `list_tables()` is called on an already-opened instance, reuse existing connections (database connections, workbook handles, etc.)

**Why**:
- More efficient (no need to reopen files)
- Better resource management
- Expected behavior when file is already open

**Implementation pattern**:
```python
def list_tables(self):
    # If file is already open, reuse connection
    if hasattr(self, 'workbook') and self.workbook is not None:
        return self.workbook.sheetnames
    # Otherwise, open temporarily
    workbook = load_workbook(self.filename)
    try:
        return workbook.sheetnames
    finally:
        workbook.close()
```

### Decision: Class Method Implementation Pattern
**What**: Class methods open files temporarily, read table names, then close

**Why**:
- No need to keep file open for just listing
- Cleaner resource management
- Matches user expectation for "discovery" operation

**Implementation pattern**:
```python
@classmethod
def list_tables(cls, filename: str) -> list[str] | None:
    if not cls.has_tables():
        return None
    workbook = load_workbook(filename)
    try:
        return workbook.sheetnames
    finally:
        workbook.close()
```

### Decision: Format-Specific Naming
**What**: Use format-appropriate terminology (sheets for Excel, tables for databases, datasets for HDF5, layers for GeoPackage)

**Why**:
- More intuitive for users familiar with each format
- Matches existing parameter names (`page` for sheets, `table` for databases)

**Mapping**:
- Excel formats (XLSX, XLS, ODS): "sheets" → return sheet names
- Database formats (SQLite, DuckDB): "tables" → return table names
- HDF5: "datasets" → return dataset paths
- NetCDF: "variables" → return variable names (or dimensions, TBD)
- GeoPackage: "layers" → return layer names
- RData: "objects" → return R object names

## Risks / Trade-offs

### Risk: Performance Impact
**Risk**: Opening files just to list tables might be slow for large files

**Mitigation**: 
- Reuse open connections when possible
- For class methods, only read metadata (not full file)
- Document that listing is a lightweight operation

### Risk: Inconsistent Behavior
**Risk**: Different formats might implement differently, confusing users

**Mitigation**:
- Clear base class interface
- Comprehensive tests
- Documentation with examples for each format

### Risk: Resource Leaks
**Risk**: Opening files for listing might not close properly

**Mitigation**:
- Always use context managers or try/finally
- Reuse existing connections when available
- Test resource cleanup

### Trade-off: NetCDF Complexity
**Trade-off**: NetCDF has variables, dimensions, and groups - what should we list?

**Decision**: List variables (most similar to "tables"), but document that dimensions/groups exist

## Migration Plan
No migration needed - this is a new feature with full backward compatibility.

## Open Questions
1. **NetCDF variables vs dimensions**: Should we list variables (data) or dimensions (structure)? Decision: Variables, as they're more like "tables"
2. **HDF5 hierarchical paths**: Should we list all datasets recursively or just top-level? Decision: List all datasets with full paths (e.g., `/group/dataset`)
3. **RData object types**: Should we filter to only data frames, or list all objects? Decision: List all objects, let users filter if needed
