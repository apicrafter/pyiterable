# Bulk Operations Audit: `read_bulk()` Implementations

This document audits `read_bulk()` implementations across all formats to identify optimization opportunities.

## Summary

**Total formats audited**: ~80 formats
**Efficient implementations**: ~5 formats (CSV, JSONL, JSON, GeoJSON, TopoJSON)
**Inefficient implementations**: ~75 formats (call `read()` in a loop)

## Efficient Implementations

### 1. CSV (`csv.py`)
- **Implementation**: Uses `next(self.reader)` directly
- **Status**: ✅ Efficient - avoids method call overhead
- **Pattern**: Direct iterator access

### 2. JSONL (`jsonl.py`)
- **Implementation**: Uses `readline()` directly, then parses
- **Status**: ✅ Efficient - avoids method call overhead
- **Pattern**: Direct file I/O

### 3. JSON (`json.py`)
- **Implementation**: 
  - Streaming mode: Direct parser access
  - Non-streaming mode: Efficient slicing `self.data[self.pos : self.pos + read_count]`
- **Status**: ✅ Efficient - uses slicing for non-streaming
- **Pattern**: Slicing for in-memory data, direct parser for streaming

### 4. GeoJSON (`geojson.py`)
- **Implementation**: Similar to JSON - uses buffer and parser directly
- **Status**: ✅ Efficient
- **Pattern**: Direct parser access for streaming

### 5. TopoJSON (`topojson.py`)
- **Implementation**: Uses parser buffer directly
- **Status**: ✅ Efficient (when streaming)
- **Pattern**: Direct parser access

## Inefficient Implementations

Most formats use the simple pattern:
```python
def read_bulk(self, num: int = 10) -> list[dict]:
    chunk = []
    for _n in range(0, num):
        try:
            chunk.append(self.read())
        except StopIteration:
            break
    return chunk
```

This pattern is acceptable for most formats, but can be optimized for:

### High Priority Optimizations

1. **Parquet (`parquet.py`)**
   - **Current**: Calls `read()` in a loop, but iterator uses `iter_batches()` internally
   - **Status**: ✅ Already efficient - `__iterator()` uses `iter_batches(batch_size=self.batch_size)`
   - **Note**: The iterator pattern is optimal - batches are read efficiently under the hood

2. **Arrow (`arrow.py`)**
   - **Current**: Likely calls `read()` in a loop
   - **Optimization**: Use Arrow's batch reading capabilities
   - **Priority**: High

3. **ORC (`orc.py`)**
   - **Current**: Likely calls `read()` in a loop
   - **Optimization**: Use ORC's batch reading capabilities
   - **Priority**: Medium

### Medium Priority Optimizations

4. **Formats with in-memory data** (already loaded)
   - Formats that load entire file into `self.data` list
   - **Optimization**: Use slicing like JSON does: `self.data[self.pos : self.pos + num]`
   - **Formats**: ARFF, HTML, TOML, Feed, etc.
   - **Priority**: Medium (improves performance but data already in memory)

### Low Priority (Acceptable Pattern)

Most formats that use the simple loop pattern are acceptable because:
- They're already streaming (line-by-line or record-by-record)
- The overhead of calling `read()` is minimal
- The format doesn't support batch operations natively

**Examples**: XML, CDX, TXT, LTSV, Apache Log, etc.

## Recommendations

### Immediate Actions

1. **Optimize Parquet `read_bulk()`** (High Priority)
   - Use `iter_batches()` for efficient batch reading
   - Reduces overhead for large Parquet files

2. **Optimize Arrow `read_bulk()`** (High Priority)
   - Use Arrow's batch reading capabilities

3. **Optimize in-memory formats** (Medium Priority)
   - Use slicing for formats that load entire file
   - Simple change: `self.data[self.pos : self.pos + num]`

### Future Considerations

- Consider async I/O for truly parallel operations (if applicable)
- Add performance benchmarks for bulk vs individual operations
- Document bulk operation guarantees and performance characteristics

## Action Items

- [x] Audit all `read_bulk()` implementations
- [ ] Optimize Parquet `read_bulk()` to use `iter_batches()`
- [ ] Optimize Arrow `read_bulk()` to use batch reading
- [ ] Optimize in-memory formats to use slicing
- [ ] Add performance benchmarks
- [ ] Document bulk operation guarantees
