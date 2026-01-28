# Bulk Operations Optimization Design

## Executive Summary

This document designs further optimizations for bulk operations (`read_bulk()` and `write_bulk()`) in IterableData. While many formats already have efficient implementations, there are opportunities to optimize columnar formats (Parquet, Arrow, ORC) and in-memory formats (ARFF, TOML, HTML, etc.) by leveraging format-specific batch capabilities and slicing operations.

## Current State

### Efficient Implementations (Already Optimized)

1. **CSV Format** (`iterable/datatypes/csv.py`)
   - Uses `next(self.reader)` directly in `read_bulk()`
   - Avoids method call overhead
   - Status: ✅ Efficient

2. **JSONL Format** (`iterable/datatypes/jsonl.py`)
   - Uses `readline()` directly, then parses JSON
   - Avoids method call overhead
   - Status: ✅ Efficient

3. **JSON Format** (`iterable/datatypes/json.py`)
   - **Non-streaming mode**: Uses efficient slicing `self.data[self.pos : self.pos + read_count]`
   - **Streaming mode**: Direct parser access with buffer management
   - Status: ✅ Efficient

### Partially Optimized (Can Be Improved)

1. **Parquet Format** (`iterable/datatypes/parquet.py`)
   - **Current**: `__iterator()` uses `iter_batches(batch_size=self.batch_size)` internally
   - **Problem**: `read_bulk()` calls `read()` in a loop, which consumes from iterator one-by-one
   - **Opportunity**: Directly consume batches from `iter_batches()` instead of one-by-one
   - **Status**: ⚠️ Partially optimized - can improve

2. **Arrow Format** (`iterable/datatypes/arrow.py`)
   - **Current**: `__iterator()` uses `to_batches(max_chunksize=self.batch_size)` internally
   - **Problem**: `read_bulk()` calls `read()` in a loop, which consumes from iterator one-by-one
   - **Opportunity**: Directly consume batches from `to_batches()` instead of one-by-one
   - **Status**: ⚠️ Partially optimized - can improve

3. **ORC Format** (`iterable/datatypes/orc.py`)
   - **Current**: Uses `pyorc.Reader` which is an iterator
   - **Problem**: `read_bulk()` calls `read()` in a loop
   - **Opportunity**: Check if pyorc supports batch reading; if not, current approach is acceptable
   - **Status**: ⚠️ Needs investigation

### In-Memory Formats (Can Be Optimized)

Many formats load entire file into memory and use simple loop pattern:

1. **ARFF Format** (`iterable/datatypes/arff.py`)
   - **Current**: Loads data into `self.rows` list, `read_bulk()` calls `read()` in a loop
   - **Opportunity**: Use slicing like JSON: `self.rows[self.pos : self.pos + num]`
   - **Status**: ⚠️ Can be optimized

2. **TOML Format** (`iterable/datatypes/toml.py`)
   - **Current**: Loads data into `self.items` list, `read_bulk()` calls `read()` in a loop
   - **Opportunity**: Use slicing: `self.items[self.pos : self.pos + num]`
   - **Status**: ⚠️ Can be optimized

3. **Other In-Memory Formats**
   - HTML, Feed, RDS, RData, PX, etc.
   - All load entire file into `self.data` or similar list
   - **Opportunity**: Use slicing instead of calling `read()` in a loop
   - **Status**: ⚠️ Can be optimized

### Acceptable Pattern (No Optimization Needed)

Many formats use the simple loop pattern, which is acceptable because:
- They're already streaming (line-by-line or record-by-record)
- The overhead of calling `read()` is minimal
- The format doesn't support batch operations natively

**Examples**: XML, CDX, TXT, LTSV, Apache Log, WARC, etc.

## Optimization Opportunities

### 1. Columnar Formats: Direct Batch Consumption

#### Parquet Format

**Current Implementation**:
```python
def read_bulk(self, num: int = DEFAULT_BULK_NUMBER) -> list[dict]:
    chunk = []
    for _n in range(0, num):
        try:
            chunk.append(self.read())  # Calls next(self.iterator)
        except StopIteration:
            break
    return chunk
```

**Problem**: Even though `__iterator()` uses `iter_batches()`, consuming one row at a time loses batch efficiency.

**Optimized Implementation**:
```python
def read_bulk(self, num: int = DEFAULT_BULK_NUMBER) -> list[dict]:
    """Read bulk Parquet records efficiently using batch reading."""
    chunk = []
    
    # If we have a cached batch, use it first
    if hasattr(self, '_cached_batch') and self._cached_batch:
        while len(chunk) < num and self._cached_batch:
            chunk.append(self._cached_batch.pop(0))
            self.pos += 1
    
    # If we need more, read from batches directly
    while len(chunk) < num:
        try:
            # Get next batch from reader
            batch = next(self._batch_iterator)
            batch_rows = batch.to_pylist()
            
            # Add rows from batch to chunk
            remaining = num - len(chunk)
            chunk.extend(batch_rows[:remaining])
            self.pos += len(batch_rows[:remaining])
            
            # Cache remaining rows from batch
            if len(batch_rows) > remaining:
                self._cached_batch = batch_rows[remaining:]
            else:
                self._cached_batch = []
                
        except StopIteration:
            break
    
    return chunk
```

**Benefits**:
- Reads entire batches at once (more efficient I/O)
- Reduces function call overhead
- Better cache locality
- Leverages columnar format efficiency

#### Arrow Format

**Current Implementation**:
```python
def read_bulk(self, num: int = DEFAULT_BULK_NUMBER) -> list[dict]:
    chunk = []
    for _n in range(0, num):
        chunk.append(self.read())
    return chunk
```

**Optimized Implementation**:
```python
def read_bulk(self, num: int = DEFAULT_BULK_NUMBER) -> list[dict]:
    """Read bulk Arrow records efficiently using batch reading."""
    chunk = []
    
    # If we have a cached batch, use it first
    if hasattr(self, '_cached_batch') and self._cached_batch:
        while len(chunk) < num and self._cached_batch:
            chunk.append(self._cached_batch.pop(0))
            self.pos += 1
    
    # If we need more, read from batches directly
    while len(chunk) < num:
        try:
            # Get next batch from table
            batch = next(self._batch_iterator)
            batch_rows = batch.to_pylist()
            
            # Add rows from batch to chunk
            remaining = num - len(chunk)
            chunk.extend(batch_rows[:remaining])
            self.pos += len(batch_rows[:remaining])
            
            # Cache remaining rows from batch
            if len(batch_rows) > remaining:
                self._cached_batch = batch_rows[remaining:]
            else:
                self._cached_batch = []
                
        except StopIteration:
            break
    
    return chunk
```

**Benefits**: Similar to Parquet - leverages batch reading efficiency.

#### ORC Format

**Current Implementation**:
```python
def read_bulk(self, num: int = DEFAULT_BULK_NUMBER) -> list[dict]:
    chunk = []
    for _n in range(0, num):
        chunk.append(self.read())
    return chunk
```

**Investigation Needed**: Check if `pyorc.Reader` supports batch reading methods.

**Potential Optimization**:
- If pyorc supports batch reading, use it directly
- If not, current approach is acceptable (ORC reader is already efficient)

### 2. In-Memory Formats: Use Slicing

#### ARFF Format

**Current Implementation**:
```python
def read_bulk(self, num: int = DEFAULT_BULK_NUMBER) -> list[dict]:
    chunk = []
    for _n in range(0, num):
        try:
            chunk.append(self.read())
        except StopIteration:
            break
    return chunk
```

**Optimized Implementation**:
```python
def read_bulk(self, num: int = DEFAULT_BULK_NUMBER) -> list[dict]:
    """Read bulk ARFF records efficiently using slicing."""
    remaining = len(self.rows) - self.pos
    if remaining == 0:
        return []
    
    read_count = min(num, remaining)
    row_slice = self.rows[self.pos : self.pos + read_count]
    
    # Convert rows to dicts
    chunk = []
    for row_values in row_slice:
        result = dict(zip(self.keys, row_values, strict=False))
        if self.relation_name:
            result["_relation"] = self.relation_name
        chunk.append(result)
    
    self.pos += read_count
    return chunk
```

**Benefits**:
- Single slice operation instead of N function calls
- Better performance for large batch sizes
- Simpler code

#### TOML Format

**Current Implementation**:
```python
def read_bulk(self, num: int = DEFAULT_BULK_NUMBER) -> list[dict]:
    chunk = []
    for _n in range(0, num):
        try:
            chunk.append(self.read())
        except StopIteration:
            break
    return chunk
```

**Optimized Implementation**:
```python
def read_bulk(self, num: int = DEFAULT_BULK_NUMBER) -> list[dict]:
    """Read bulk TOML records efficiently using slicing."""
    remaining = len(self.items) - self.pos
    if remaining == 0:
        return []
    
    read_count = min(num, remaining)
    chunk = self.items[self.pos : self.pos + read_count]
    self.pos += read_count
    return chunk
```

**Benefits**: Same as ARFF - single slice operation, better performance.

### 3. Generic Optimization Pattern for In-Memory Formats

For formats that load entire file into a list (e.g., `self.data`, `self.items`, `self.rows`):

**Pattern**:
```python
def read_bulk(self, num: int = DEFAULT_BULK_NUMBER) -> list[dict]:
    """Read bulk records efficiently using slicing."""
    # Get the data list (format-specific attribute name)
    data_list = self.data  # or self.items, self.rows, etc.
    
    remaining = len(data_list) - self.pos
    if remaining == 0:
        return []
    
    read_count = min(num, remaining)
    chunk = data_list[self.pos : self.pos + read_count]
    self.pos += read_count
    return chunk
```

**Formats That Can Use This Pattern**:
- ARFF: `self.rows`
- TOML: `self.items`
- HTML: `self.data` (if list)
- Feed: `self.data` (if list)
- RDS: `self.data`
- RData: `self.data`
- PX: `self.records`
- And others that load entire file into memory

## Implementation Strategy

### Phase 1: Columnar Formats (High Priority)

1. **Optimize Parquet `read_bulk()`**
   - Implement batch caching mechanism
   - Directly consume from `iter_batches()`
   - Maintain backward compatibility

2. **Optimize Arrow `read_bulk()`**
   - Implement batch caching mechanism
   - Directly consume from `to_batches()`
   - Maintain backward compatibility

3. **Investigate ORC `read_bulk()`**
   - Check pyorc documentation for batch reading
   - Implement if supported, document if not

### Phase 2: In-Memory Formats (Medium Priority)

1. **Identify all in-memory formats**
   - Audit formats that load entire file into `self.data` or similar
   - Create list of formats to optimize

2. **Implement slicing optimization**
   - Apply slicing pattern to each format
   - Handle format-specific conversions (e.g., ARFF row conversion)
   - Test for correctness

3. **Verify performance improvements**
   - Benchmark before/after
   - Document performance characteristics

### Phase 3: Testing and Documentation

1. **Add performance benchmarks**
   - Compare bulk vs individual operations
   - Measure improvement for optimized formats
   - Include in test suite

2. **Document optimizations**
   - Update format-specific documentation
   - Document performance characteristics
   - Provide guidance on optimal batch sizes

## Performance Considerations

### Expected Improvements

1. **Columnar Formats (Parquet, Arrow)**
   - **Current**: ~100-1000 rows/second (one-by-one consumption)
   - **Optimized**: ~10,000-100,000 rows/second (batch consumption)
   - **Improvement**: 10-100x faster for bulk operations

2. **In-Memory Formats**
   - **Current**: O(N) function calls for N rows
   - **Optimized**: O(1) slice operation + O(N) conversion
   - **Improvement**: 2-5x faster for large batch sizes

### Trade-offs

1. **Memory Usage**
   - Batch caching increases memory usage slightly
   - Acceptable trade-off for performance gain

2. **Code Complexity**
   - Batch caching adds complexity
   - Worth it for significant performance improvement

3. **Backward Compatibility**
   - All optimizations maintain API compatibility
   - No breaking changes

## Testing Strategy

### Unit Tests

1. **Correctness Tests**
   - Verify `read_bulk()` returns correct number of rows
   - Verify rows match individual `read()` calls
   - Test edge cases (empty files, end of file, etc.)

2. **Batch Caching Tests**
   - Verify batch caching works correctly
   - Test partial batch consumption
   - Test batch boundary conditions

3. **Slicing Tests**
   - Verify slicing returns correct data
   - Test position tracking
   - Test format-specific conversions

### Performance Tests

1. **Benchmark Bulk Operations**
   - Compare optimized vs unoptimized implementations
   - Measure throughput (rows/second)
   - Measure memory usage

2. **Benchmark Different Batch Sizes**
   - Test various batch sizes (10, 100, 1000, 10000)
   - Identify optimal batch sizes
   - Document recommendations

### Integration Tests

1. **End-to-End Tests**
   - Test bulk operations in real-world scenarios
   - Test with large files
   - Test with various formats

## Usage Examples

### Parquet Bulk Reading (Optimized)

```python
# Before optimization: Reads one row at a time
with open_iterable("data.parquet") as source:
    batch = source.read_bulk(1000)  # Slow - one-by-one consumption

# After optimization: Reads entire batches
with open_iterable("data.parquet") as source:
    batch = source.read_bulk(1000)  # Fast - batch consumption
```

### Arrow Bulk Reading (Optimized)

```python
# Optimized batch reading
with open_iterable("data.arrow") as source:
    batch = source.read_bulk(1000)  # Uses batch reading
```

### In-Memory Format Bulk Reading (Optimized)

```python
# ARFF format - uses slicing
with open_iterable("data.arff") as source:
    batch = source.read_bulk(1000)  # Fast - single slice operation

# TOML format - uses slicing
with open_iterable("data.toml") as source:
    batch = source.read_bulk(1000)  # Fast - single slice operation
```

## Migration Path

### Backward Compatibility

- **No API Changes**: All optimizations are internal
- **Same Behavior**: Results are identical to current implementation
- **Performance Only**: Improvements are transparent to users

### Gradual Rollout

1. **Phase 1**: Optimize columnar formats (Parquet, Arrow)
2. **Phase 2**: Optimize in-memory formats (ARFF, TOML, etc.)
3. **Phase 3**: Document and benchmark improvements

## Recommendations

### Immediate Actions (Phase 1)

1. **Optimize Parquet `read_bulk()`**
   - Implement batch caching
   - Directly consume from `iter_batches()`
   - Test thoroughly

2. **Optimize Arrow `read_bulk()`**
   - Implement batch caching
   - Directly consume from `to_batches()`
   - Test thoroughly

3. **Investigate ORC**
   - Check pyorc batch reading capabilities
   - Implement if supported

### Future Enhancements (Phase 2)

1. **Optimize in-memory formats**
   - Apply slicing pattern systematically
   - Handle format-specific conversions
   - Benchmark improvements

2. **Add performance benchmarks**
   - Include in test suite
   - Document performance characteristics
   - Provide guidance on optimal batch sizes

## Conclusion

Bulk operations can be significantly optimized for columnar formats (Parquet, Arrow) and in-memory formats (ARFF, TOML, etc.) by leveraging format-specific batch capabilities and slicing operations. The recommended approach is to:

1. **Phase 1**: Optimize columnar formats first (highest impact)
2. **Phase 2**: Optimize in-memory formats (good impact, easier implementation)
3. **Phase 3**: Document and benchmark improvements

All optimizations maintain backward compatibility and provide transparent performance improvements to users.
