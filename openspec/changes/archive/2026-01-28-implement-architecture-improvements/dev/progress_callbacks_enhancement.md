# Progress Callbacks Enhancement for Long-Running Operations

## Current State

IterableData already has progress callbacks implemented for the main long-running operations:

### ✅ Existing Progress Callback Support

1. **`convert()`** - Single file conversion
   - Progress callback parameter: `progress: Callable[[dict[str, Any]], None] | None`
   - Callback receives: `rows_read`, `rows_written`, `elapsed`, `estimated_total`
   - Invoked every `DEFAULT_PROGRESS_INTERVAL` (1000 rows)

2. **`pipeline()`** - Data pipeline processing
   - Progress callback parameter: `progress: Callable[[dict[str, Any]], None] | None`
   - Callback receives: `rows_processed`, `elapsed`, `throughput`, `rec_count`, `exceptions`, `nulls`
   - Invoked every `DEFAULT_PROGRESS_INTERVAL` (1000 rows)

3. **`bulk_convert()`** - Multiple file conversion
   - Progress callback parameter: `progress: Callable[[dict[str, Any]], None] | None`
   - Callback receives: `file_index`, `total_files`, `current_file`, `file_rows_read`, `file_rows_written`, plus all `convert()` stats
   - Invoked for each file conversion

### Current Implementation Details

- **Progress Interval**: `DEFAULT_PROGRESS_INTERVAL = 1000` rows
- **Error Handling**: Callbacks wrapped in try/except to prevent crashes
- **Metrics**: Comprehensive stats dictionaries with timing, throughput, and counts
- **Integration**: Works with `show_progress` for tqdm integration

## Enhancement Opportunities

### 1. Configurable Progress Interval

**Current**: Fixed interval of 1000 rows  
**Enhancement**: Allow users to configure the interval

```python
# Proposed API
convert(
    'input.csv',
    'output.parquet',
    progress=callback,
    progress_interval=500  # Call callback every 500 rows
)
```

**Benefits**:
- Fine-grained control for fast operations
- Coarser intervals for very slow operations (reduce overhead)
- Better performance tuning

### 2. Progress Callbacks for Direct Iteration

**Current**: No progress tracking for direct iteration  
**Enhancement**: Helper function or wrapper for progress tracking

```python
# Proposed API
from iterable.helpers.progress import with_progress

def progress_callback(stats):
    print(f"Processed {stats['rows_read']} rows")

with open_iterable('large_file.csv') as source:
    for row in with_progress(source, callback=progress_callback):
        process(row)
```

**Alternative**: Context manager wrapper

```python
from iterable.helpers.progress import ProgressTracker

with open_iterable('large_file.csv') as source:
    with ProgressTracker(source, callback=progress_callback) as tracked:
        for row in tracked:
            process(row)
```

**Benefits**:
- Progress tracking for any iteration
- No changes to existing code required
- Optional - users opt-in when needed

### 3. Enhanced Progress Callback Information

**Current**: Basic stats (rows, elapsed, throughput)  
**Enhancement**: Additional metrics

```python
# Enhanced callback stats
{
    # Existing
    'rows_read': int,
    'rows_written': int,
    'elapsed': float,
    'estimated_total': int | None,
    'throughput': float | None,
    
    # New additions
    'bytes_read': int,           # Bytes read so far
    'bytes_written': int,         # Bytes written so far
    'memory_usage_mb': float,     # Current memory usage
    'percent_complete': float,    # Percentage (0-100) if total known
    'estimated_time_remaining': float | None,  # ETA in seconds
    'current_file': str | None,   # For bulk operations
    'file_index': int | None,     # For bulk operations
    'total_files': int | None,    # For bulk operations
}
```

**Benefits**:
- More comprehensive monitoring
- Better integration with monitoring systems
- ETA calculations for better UX

### 4. Progress Callbacks for `read_bulk()` Operations

**Current**: No progress tracking for bulk reads  
**Enhancement**: Optional progress callback for bulk operations

```python
# Proposed API
with open_iterable('large_file.csv') as source:
    def progress_callback(stats):
        print(f"Read {stats['chunks_read']} chunks, {stats['total_rows']} rows")
    
    for chunk in source.read_bulk(10000, progress=progress_callback):
        process_chunk(chunk)
```

**Benefits**:
- Progress tracking for bulk operations
- Useful for very large files processed in chunks

### 5. Progress Callbacks for Format Detection

**Current**: No progress tracking for format detection  
**Enhancement**: Progress callback for content-based detection (large files)

```python
# Proposed API (for large files)
def progress_callback(stats):
    print(f"Scanned {stats['bytes_scanned']} bytes for format detection")

result = detect_file_type(
    'large_file',
    progress=progress_callback
)
```

**Benefits**:
- Visibility into format detection progress
- Useful for very large files where detection takes time

### 6. Progress Callback Frequency Control

**Current**: Fixed row-based interval  
**Enhancement**: Multiple frequency options

```python
# Proposed API
convert(
    'input.csv',
    'output.parquet',
    progress=callback,
    progress_interval=1000,        # Every N rows
    progress_interval_seconds=5.0,  # Or every N seconds (whichever comes first)
    progress_on_start=True,         # Call at start
    progress_on_complete=True,      # Call at completion
)
```

**Benefits**:
- Time-based intervals for slow operations
- Guaranteed start/complete callbacks
- More flexible progress reporting

### 7. Progress Callback Chaining

**Current**: Single callback function  
**Enhancement**: Support multiple callbacks

```python
# Proposed API
def log_callback(stats):
    logger.info(f"Progress: {stats['rows_read']} rows")

def metrics_callback(stats):
    metrics.gauge('rows_processed', stats['rows_read'])

convert(
    'input.csv',
    'output.parquet',
    progress=[log_callback, metrics_callback]  # Multiple callbacks
)
```

**Benefits**:
- Separation of concerns (logging vs metrics)
- Multiple monitoring systems
- More flexible architecture

## Implementation Recommendations

### Priority 1: High Value, Low Effort

1. **Configurable Progress Interval** ✅
   - Add `progress_interval` parameter to `convert()`, `pipeline()`, `bulk_convert()`
   - Simple parameter addition
   - High user value

2. **Enhanced Progress Stats** ✅
   - Add `bytes_read`, `bytes_written`, `percent_complete`, `estimated_time_remaining`
   - Calculate from existing data
   - Better monitoring integration

3. **Progress Callbacks for Direct Iteration** ✅
   - Create `with_progress()` helper function
   - Wrapper around existing iterators
   - No changes to core code

### Priority 2: Medium Value, Medium Effort

4. **Progress Callbacks for `read_bulk()`** ⚠️
   - Requires changes to `read_bulk()` signature
   - May break backward compatibility
   - Consider alternative: wrapper function

5. **Time-Based Progress Intervals** ⚠️
   - More complex logic
   - Requires timing management
   - Good for very slow operations

### Priority 3: Lower Priority

6. **Multiple Callbacks** ⚠️
   - Can be achieved with wrapper function
   - Lower priority than single callback improvements

7. **Format Detection Progress** ⚠️
   - Rarely needed (detection is usually fast)
   - Only useful for very large files

## Proposed Implementation Plan

### Phase 1: Enhancements to Existing Callbacks

1. **Add `progress_interval` parameter**
   ```python
   def convert(
       ...,
       progress: Callable[[dict[str, Any]], None] | None = None,
       progress_interval: int = DEFAULT_PROGRESS_INTERVAL,
   ):
   ```

2. **Enhance progress stats**
   - Add `bytes_read`, `bytes_written` (track file sizes)
   - Add `percent_complete` (calculate from `estimated_total`)
   - Add `estimated_time_remaining` (calculate from throughput)

3. **Add start/complete callbacks**
   - Call progress callback at start with initial stats
   - Call progress callback at completion with final stats

### Phase 2: New Progress Tracking Features

4. **Create `with_progress()` helper**
   ```python
   # iterable/helpers/progress.py
   def with_progress(
       iterable: BaseIterable,
       callback: Callable[[dict[str, Any]], None],
       interval: int = DEFAULT_PROGRESS_INTERVAL,
   ) -> Iterator[Row]:
       """Wrap an iterable with progress tracking"""
       ...
   ```

5. **Add time-based intervals**
   - Track last callback time
   - Call callback if interval seconds have passed
   - Combine with row-based interval (whichever comes first)

## Examples

### Example 1: Configurable Interval

```python
def progress_callback(stats):
    print(f"Progress: {stats['rows_read']} rows")

# Fine-grained progress (every 100 rows)
convert(
    'input.csv',
    'output.parquet',
    progress=progress_callback,
    progress_interval=100
)

# Coarse progress (every 10000 rows)
convert(
    'large_input.csv',
    'output.parquet',
    progress=progress_callback,
    progress_interval=10000
)
```

### Example 2: Enhanced Stats

```python
def progress_callback(stats):
    print(f"Rows: {stats['rows_read']}/{stats['estimated_total']}")
    print(f"Progress: {stats['percent_complete']:.1f}%")
    if stats['estimated_time_remaining']:
        print(f"ETA: {stats['estimated_time_remaining']:.1f}s")
    print(f"Throughput: {stats['throughput']:.0f} rows/sec")
    print(f"Memory: {stats['memory_usage_mb']:.1f} MB")

convert('input.csv', 'output.parquet', progress=progress_callback)
```

### Example 3: Direct Iteration Progress

```python
from iterable.helpers.progress import with_progress

def progress_callback(stats):
    print(f"Processed {stats['rows_read']} rows")

with open_iterable('large_file.csv') as source:
    for row in with_progress(source, callback=progress_callback, interval=5000):
        process(row)
```

### Example 4: Multiple Callbacks

```python
def log_progress(stats):
    logger.info(f"Conversion progress: {stats['rows_read']} rows")

def send_metrics(stats):
    metrics.gauge('conversion.rows_read', stats['rows_read'])
    metrics.gauge('conversion.throughput', stats['throughput'])

# Using wrapper for multiple callbacks
def combined_callback(stats):
    log_progress(stats)
    send_metrics(stats)

convert('input.csv', 'output.parquet', progress=combined_callback)
```

## Testing Considerations

1. **Test progress callback invocation frequency**
2. **Test progress callback error handling** (callback raises exception)
3. **Test progress stats accuracy** (rows, bytes, timing)
4. **Test progress interval configuration**
5. **Test with very large files** (ensure callbacks don't slow down processing)
6. **Test with empty files** (ensure callbacks still work)
7. **Test with files without totals** (ensure `estimated_total` is None)

## Documentation Updates

1. **Update API documentation** for `convert()`, `pipeline()`, `bulk_convert()`
2. **Add progress callback examples** to user guide
3. **Document progress stats dictionary** structure
4. **Add best practices** for progress callbacks
5. **Document performance considerations** (callback overhead)

## Conclusion

Progress callbacks are already well-implemented in IterableData. The main enhancements would be:

1. **Configurable intervals** - High value, easy to implement
2. **Enhanced stats** - Better monitoring integration
3. **Direct iteration progress** - New capability for users
4. **Time-based intervals** - Useful for very slow operations

These enhancements would make progress callbacks more flexible and powerful while maintaining backward compatibility.
