---
sidebar_position: 5
title: Migration Guide
description: Guide for upgrading between versions of Iterable Data
---

# Migration Guide

This guide helps you migrate your code when upgrading between versions of Iterable Data.

## Version 1.0.7 and Later

### Context Manager Support

**What Changed**: Iterable Data now supports Python's context manager protocol (`with` statements).

**Before (Still Supported)**:
```python
from iterable.helpers.detect import open_iterable

source = open_iterable('data.csv')
try:
    for row in source:
        process(row)
finally:
    source.close()
```

**After (Recommended)**:
```python
from iterable.helpers.detect import open_iterable

# Recommended: Using context manager
with open_iterable('data.csv') as source:
    for row in source:
        process(row)
# File automatically closed
```

**Migration Steps**:
1. Replace `try/finally` blocks with `with` statements
2. Remove manual `close()` calls when using context managers
3. Old code still works - migration is optional but recommended

**Benefits**:
- Cleaner, more Pythonic code
- Automatic resource cleanup
- Better error handling

## Version 1.0.6

### Enhanced Documentation

**What Changed**: Comprehensive documentation improvements with better examples and API reference.

**Action Required**: Review updated documentation for best practices and new patterns.

### Improved Examples

**What Changed**: All examples updated to show best practices.

**Action Required**: Update your code to follow new patterns shown in documentation.

## Version 1.0.5

### DuckDB Engine Support

**What Changed**: Added optional DuckDB engine for high-performance querying.

**Before**:
```python
from iterable.helpers.detect import open_iterable

source = open_iterable('data.csv.gz')
for row in source:
    process(row)
source.close()
```

**After (Optional Enhancement)**:
```python
from iterable.helpers.detect import open_iterable

# Use DuckDB engine for better performance on large files
with open_iterable('data.csv.gz', engine='duckdb') as source:
    total = source.totals()  # Fast row counting
    for row in source:
        process(row)
```

**Migration Steps**:
1. Install DuckDB: `pip install duckdb`
2. Add `engine='duckdb'` parameter when opening supported formats
3. Old code continues to work with internal engine

**Benefits**:
- Faster queries on large CSV/JSONL files
- Fast row counting
- SQL-like operations

### Pipeline Processing Framework

**What Changed**: Added `pipeline()` function for data transformation workflows.

**Before**:
```python
from iterable.helpers.detect import open_iterable

source = open_iterable('input.csv')
destination = open_iterable('output.jsonl', mode='w')

for row in source:
    transformed = transform(row)
    destination.write(transformed)

source.close()
destination.close()
```

**After (Optional Enhancement)**:
```python
from iterable.helpers.detect import open_iterable
from iterable.pipeline.core import pipeline

with open_iterable('input.csv') as source:
    with open_iterable('output.jsonl', mode='w') as destination:
        def transform_record(record, state):
            return transform(record)
        
        pipeline(
            source=source,
            destination=destination,
            process_func=transform_record
        )
```

**Migration Steps**:
1. Import `pipeline` from `iterable.pipeline.core`
2. Refactor transformation logic into `process_func`
3. Use pipeline for progress tracking and error handling

**Benefits**:
- Built-in progress tracking
- Error handling framework
- State management
- Cleaner code structure

### Bulk Operations Support

**What Changed**: Enhanced support for bulk read/write operations.

**Before**:
```python
from iterable.helpers.detect import open_iterable

dest = open_iterable('output.jsonl', mode='w')
for record in records:
    dest.write(record)
dest.close()
```

**After (Recommended)**:
```python
from iterable.helpers.detect import open_iterable

with open_iterable('output.jsonl', mode='w') as dest:
    dest.write_bulk(records)  # Much faster
```

**Migration Steps**:
1. Collect records into batches
2. Use `write_bulk()` instead of individual `write()` calls
3. Use `read_bulk()` for reading multiple records

**Benefits**:
- Significantly better performance
- Reduced I/O operations
- Better memory efficiency

## General Migration Tips

### Testing Your Migration

1. **Test with small files first**: Verify migration works with small test files
2. **Compare outputs**: Ensure migrated code produces same results
3. **Check performance**: Verify performance improvements (if applicable)
4. **Test error handling**: Ensure error handling still works correctly

### Backward Compatibility

- **Old code still works**: Most changes are additive, not breaking
- **Gradual migration**: You can migrate incrementally
- **No forced changes**: Old patterns remain supported

### Common Migration Patterns

#### Pattern 1: Adding Context Managers

```python
# Old
source = open_iterable('data.csv')
try:
    for row in source:
        process(row)
finally:
    source.close()

# New
with open_iterable('data.csv') as source:
    for row in source:
        process(row)
```

#### Pattern 2: Using Bulk Operations

```python
# Old
dest = open_iterable('output.jsonl', mode='w')
for record in records:
    dest.write(record)
dest.close()

# New
with open_iterable('output.jsonl', mode='w') as dest:
    dest.write_bulk(records)
```

#### Pattern 3: Adding DuckDB Engine

```python
# Old
source = open_iterable('large_data.csv.gz')
for row in source:
    process(row)
source.close()

# New (optional, for better performance)
with open_iterable('large_data.csv.gz', engine='duckdb') as source:
    total = source.totals()  # Fast counting
    for row in source:
        process(row)
```

## Breaking Changes

### None in Recent Versions

All recent versions maintain backward compatibility. If you encounter any issues:

1. Check the [CHANGELOG](../CHANGELOG.md) for detailed changes
2. Review [Troubleshooting Guide](troubleshooting.md) for solutions
3. Report issues on GitHub

## Getting Help

If you need help with migration:

1. **Check documentation**: Review updated guides and examples
2. **Review examples**: Check use case examples for patterns
3. **Test incrementally**: Migrate one feature at a time
4. **Ask for help**: Open an issue on GitHub if you encounter problems

## Related Topics

- [Troubleshooting Guide](troubleshooting.md) - Common issues and solutions
- [Best Practices](best-practices.md) - Recommended patterns
- [API Reference](/api/open-iterable) - Full API documentation
- [CHANGELOG](../../CHANGELOG.md) - Detailed version history

