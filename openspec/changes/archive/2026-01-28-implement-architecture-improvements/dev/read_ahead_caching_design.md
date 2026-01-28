# Read-Ahead Caching Design

## Executive Summary

This document designs a read-ahead caching system for IterableData that prefetches data from file sources to reduce I/O wait time during sequential row processing. The system improves performance for network-based sources (S3, GCS, Azure), local files with slow I/O, and formats that read line-by-line (CSV, JSONL).

## Current State

### I/O Patterns

IterableData currently reads data sequentially, row-by-row:

1. **CSV Format** (`iterable/datatypes/csv.py`)
   - Uses `csv.DictReader` which reads line-by-line sequentially
   - Each `read()` call triggers a file read operation
   - No prefetching or buffering beyond Python's default file buffering (typically 8KB)

2. **JSONL Format** (`iterable/datatypes/jsonl.py`)
   - Reads line-by-line using `next(self.fobj)`
   - Each `read()` call reads one line from the file object
   - No prefetching beyond default file buffering

3. **JSON Format** (`iterable/datatypes/json.py`)
   - Uses `ijson` for streaming large files (>10MB)
   - Has a small `_items_buffer` that pre-fetches one item
   - Still reads incrementally from the underlying file object

4. **Other Formats**
   - Most formats read sequentially, row-by-row or in small batches
   - No systematic read-ahead caching across formats

### Existing Buffering

1. **Python File Object Buffering**
   - Default buffering: 8KB for text files, 4KB for binary files
   - Operates at the OS level, transparent to application code
   - Helps with small reads but doesn't prefetch ahead of consumption

2. **Format-Specific Buffering**
   - JSON format has `_items_buffer` that pre-fetches one item
   - Some formats use internal buffers for parsing (e.g., XML, Parquet)
   - No unified read-ahead caching system

### Limitations

1. **I/O Wait Time**: Each `read()` call may wait for disk/network I/O
2. **Network Sources**: S3, GCS, Azure have higher latency - each read waits for network round-trip
3. **Sequential Processing**: CPU waits for I/O during row processing
4. **No Prefetching**: Data is only read when explicitly requested

## Use Cases

### 1. Network-Based Sources (S3, GCS, Azure)

**Problem**: Network latency causes each read operation to wait for data transfer.

**Benefit**: Prefetching multiple rows ahead reduces perceived latency.

**Example**:
```python
# Without read-ahead: Each read() waits for network round-trip
with open_iterable("s3://bucket/data.csv") as source:
    for row in source:  # Each iteration waits for network I/O
        process(row)

# With read-ahead: Prefetched rows available immediately
with open_iterable("s3://bucket/data.csv", iterableargs={'read_ahead': 100}) as source:
    for row in source:  # Prefetched rows available, minimal wait
        process(row)
```

### 2. Slow Local I/O

**Problem**: Slow disks (HDD, network-mounted filesystems) cause I/O wait time.

**Benefit**: Prefetching hides I/O latency behind CPU processing.

**Example**:
```python
# Processing large CSV on slow disk
with open_iterable("large_file.csv", iterableargs={'read_ahead': 50}) as source:
    for row in source:
        # CPU processes row while next batch prefetches
        complex_processing(row)
```

### 3. Sequential Processing with Variable Row Processing Time

**Problem**: Some rows take longer to process, creating opportunities for prefetching.

**Benefit**: While processing slow rows, next rows are prefetched.

**Example**:
```python
with open_iterable("data.jsonl", iterableargs={'read_ahead': 20}) as source:
    for row in source:
        if is_complex_row(row):
            # Takes 100ms to process
            process_complex(row)
        else:
            # Takes 1ms to process
            process_simple(row)
        # Next 20 rows prefetched during processing
```

### 4. Bulk Operations

**Problem**: `read_bulk()` may benefit from prefetching additional batches.

**Benefit**: Prefetching next batch while processing current batch.

**Example**:
```python
with open_iterable("data.csv", iterableargs={'read_ahead': 2}) as source:
    while True:
        batch = source.read_bulk(1000)  # Read 1000 rows
        if not batch:
            break
        # Next 2000 rows prefetched while processing batch
        process_batch(batch)
```

## Design Options

### Option 1: Simple Buffer-Based Read-Ahead (Recommended)

**Approach**: Maintain a buffer of prefetched rows, refill when buffer is low.

**Pros**:
- Simple implementation
- Low overhead
- Works with existing iterator protocol
- No threading complexity

**Cons**:
- Synchronous I/O (doesn't hide I/O latency completely)
- Limited benefit for very slow I/O

**Implementation**:
- Buffer stores N prefetched rows
- When buffer drops below threshold, read more rows synchronously
- Consumer reads from buffer

### Option 2: Thread-Based Prefetching

**Approach**: Background thread prefetches rows while main thread processes current rows.

**Pros**:
- Truly asynchronous - hides I/O latency
- Significant benefit for network sources
- CPU and I/O can overlap

**Cons**:
- Threading complexity
- Thread synchronization overhead
- Memory overhead (prefetched rows)
- Potential for race conditions

**Implementation**:
- Background thread reads ahead
- Queue stores prefetched rows
- Main thread consumes from queue
- Thread synchronization required

### Option 3: Async/Await-Based Prefetching

**Approach**: Use async I/O with `asyncio` for prefetching.

**Pros**:
- True async I/O
- Efficient for network sources
- Modern Python pattern

**Cons**:
- Requires async/await support (see Task 13.1)
- More complex implementation
- Not compatible with synchronous API without wrappers

**Implementation**:
- Async iterator with prefetching
- `asyncio` tasks for concurrent I/O
- Requires async API (future work)

### Recommendation: Hybrid Approach

**Phase 1**: Simple buffer-based read-ahead (Option 1)
- Easy to implement
- Immediate benefits
- Backward compatible
- No threading complexity

**Phase 2**: Thread-based prefetching (Option 2) for network sources
- Significant benefit for S3/GCS/Azure
- Optional feature (opt-in)
- More complex but higher performance

**Phase 3**: Async/await support (Option 3) - see Task 13.1
- Modern async API
- Best for async applications

## Implementation Design

### Core Components

#### 1. ReadAheadBuffer Class

```python
class ReadAheadBuffer:
    """Buffer for prefetched rows with automatic refilling."""
    
    def __init__(self, source: Iterator[Row], buffer_size: int = 10, refill_threshold: float = 0.3):
        """
        Args:
            source: Source iterator to prefetch from
            buffer_size: Maximum number of rows to prefetch
            refill_threshold: Refill when buffer drops below this fraction (0.0-1.0)
        """
        self.source = source
        self.buffer_size = buffer_size
        self.refill_threshold = int(buffer_size * refill_threshold)
        self.buffer: list[Row] = []
        self.exhausted = False
    
    def __iter__(self) -> Iterator[Row]:
        return self
    
    def __next__(self) -> Row:
        # Refill buffer if needed
        if len(self.buffer) <= self.refill_threshold and not self.exhausted:
            self._refill()
        
        # Return from buffer
        if self.buffer:
            return self.buffer.pop(0)
        
        # Buffer empty and source exhausted
        raise StopIteration
    
    def _refill(self) -> None:
        """Refill buffer from source."""
        target_size = self.buffer_size - len(self.buffer)
        for _ in range(target_size):
            try:
                row = next(self.source)
                self.buffer.append(row)
            except StopIteration:
                self.exhausted = True
                break
    
    def peek(self, n: int = 1) -> list[Row]:
        """Peek at next N rows without consuming them."""
        # Refill if needed
        if len(self.buffer) < n and not self.exhausted:
            self._refill()
        return self.buffer[:n]
    
    def clear(self) -> None:
        """Clear buffer (for reset operations)."""
        self.buffer.clear()
        self.exhausted = False
```

#### 2. Thread-Based Prefetching (Phase 2)

```python
import threading
import queue
from typing import Iterator, Optional

class ThreadedReadAheadBuffer:
    """Thread-based read-ahead buffer for asynchronous prefetching."""
    
    def __init__(self, source: Iterator[Row], buffer_size: int = 10):
        """
        Args:
            source: Source iterator to prefetch from
            buffer_size: Maximum number of rows in queue
        """
        self.source = source
        self.queue: queue.Queue[Optional[Row]] = queue.Queue(maxsize=buffer_size)
        self.thread: Optional[threading.Thread] = None
        self.stop_event = threading.Event()
        self.exhausted = False
        self.error: Optional[Exception] = None
    
    def __iter__(self) -> Iterator[Row]:
        return self
    
    def __next__(self) -> Row:
        # Start prefetching thread if not started
        if self.thread is None:
            self._start_prefetching()
        
        # Get row from queue
        row = self.queue.get()
        
        # Check for errors
        if isinstance(row, Exception):
            raise row
        
        # Check for exhaustion
        if row is None:
            raise StopIteration
        
        return row
    
    def _start_prefetching(self) -> None:
        """Start background thread for prefetching."""
        self.thread = threading.Thread(target=self._prefetch_worker, daemon=True)
        self.thread.start()
    
    def _prefetch_worker(self) -> None:
        """Worker thread that prefetches rows."""
        try:
            for row in self.source:
                if self.stop_event.is_set():
                    break
                self.queue.put(row)
            # Signal exhaustion
            self.queue.put(None)
        except Exception as e:
            # Signal error
            self.queue.put(e)
        finally:
            self.exhausted = True
    
    def close(self) -> None:
        """Stop prefetching thread."""
        self.stop_event.set()
        if self.thread is not None:
            self.thread.join(timeout=1.0)
```

### Integration Points

#### 1. BaseFileIterable Integration

```python
class BaseFileIterable(BaseIterable):
    def __init__(self, ..., options: dict[str, Any] | None = None):
        # ... existing initialization ...
        
        # Read-ahead configuration
        self._read_ahead_enabled = options.get("read_ahead", False)
        self._read_ahead_size = options.get("read_ahead_size", 10)
        self._read_ahead_threaded = options.get("read_ahead_threaded", False)
        self._read_ahead_buffer = None
    
    def __iter__(self) -> Iterator[Row]:
        """Iterator with optional read-ahead caching."""
        if self._read_ahead_enabled:
            if self._read_ahead_threaded:
                self._read_ahead_buffer = ThreadedReadAheadBuffer(
                    super().__iter__(),
                    buffer_size=self._read_ahead_size
                )
            else:
                self._read_ahead_buffer = ReadAheadBuffer(
                    super().__iter__(),
                    buffer_size=self._read_ahead_size
                )
            return iter(self._read_ahead_buffer)
        else:
            return super().__iter__()
    
    def reset(self) -> None:
        """Reset iterator and clear read-ahead buffer."""
        super().reset()
        if self._read_ahead_buffer is not None:
            self._read_ahead_buffer.clear()
```

#### 2. Format-Specific Integration

Some formats may benefit from format-specific read-ahead:

```python
class CSVIterable(BaseFileIterable):
    def read(self, skip_empty: bool = True) -> Row:
        """Read with read-ahead support."""
        if self._read_ahead_enabled and self._read_ahead_buffer:
            return next(self._read_ahead_buffer)
        else:
            # Standard read
            return super().read(skip_empty)
```

### Configuration Options

#### Via `iterableargs` Parameter

```python
open_iterable(
    "data.csv",
    iterableargs={
        "read_ahead": True,              # Enable read-ahead (default: False)
        "read_ahead_size": 50,           # Buffer size (default: 10)
        "read_ahead_threaded": False,    # Use thread-based prefetching (default: False)
        "read_ahead_refill_threshold": 0.3  # Refill threshold (default: 0.3)
    }
)
```

#### Global Configuration

```python
# In iterable/config.py or similar
DEFAULT_READ_AHEAD_SIZE = 10
DEFAULT_READ_AHEAD_THREADED = False
DEFAULT_READ_AHEAD_REFILL_THRESHOLD = 0.3
```

### Format-Specific Considerations

#### 1. CSV Format

- **Benefit**: High - reads line-by-line
- **Implementation**: Wrap `csv.DictReader` iterator with read-ahead buffer
- **Considerations**: Buffer stores parsed rows (dicts), not raw lines

#### 2. JSONL Format

- **Benefit**: High - reads line-by-line
- **Implementation**: Wrap file iterator with read-ahead buffer
- **Considerations**: Buffer stores parsed JSON objects

#### 3. JSON Format

- **Benefit**: Medium - already has `_items_buffer`
- **Implementation**: Enhance existing buffer or add read-ahead on top
- **Considerations**: May conflict with existing buffering

#### 4. Parquet Format

- **Benefit**: Low - already reads in batches
- **Implementation**: Read-ahead at batch level, not row level
- **Considerations**: May not provide significant benefit

#### 5. Network Sources (S3, GCS, Azure)

- **Benefit**: Very High - network latency
- **Implementation**: Thread-based prefetching recommended
- **Considerations**: Significant performance improvement expected

## Performance Considerations

### Benefits

1. **Reduced I/O Wait Time**
   - Prefetched rows available immediately
   - CPU can process while I/O happens in background (threaded mode)

2. **Better Resource Utilization**
   - Overlap I/O and CPU work
   - Especially beneficial for network sources

3. **Smoother Processing**
   - Reduces variability in processing time
   - More consistent throughput

### Overhead

1. **Memory Overhead**
   - Buffer stores N rows in memory
   - Typical: 10-100 rows × row size
   - Usually negligible (<1MB for most use cases)

2. **CPU Overhead**
   - Buffer management (minimal)
   - Thread synchronization (threaded mode only)
   - Usually negligible compared to I/O savings

3. **Complexity**
   - Additional code to maintain
   - Potential for bugs (threading)
   - Testing complexity

### When Read-Ahead Helps

1. **High I/O Latency**: Network sources, slow disks
2. **Sequential Processing**: Reading rows one-by-one
3. **Variable Processing Time**: Some rows take longer to process
4. **CPU-Bound Processing**: CPU can process while I/O happens

### When Read-Ahead Doesn't Help

1. **Low I/O Latency**: Fast local SSDs
2. **Bulk Operations**: Already reading in batches
3. **I/O-Bound Processing**: Processing is faster than I/O
4. **Random Access**: Not reading sequentially

## Implementation Strategy

### Phase 1: Simple Buffer-Based Read-Ahead (Recommended First Step)

1. **Implement `ReadAheadBuffer` class**
   - Simple buffer with automatic refilling
   - No threading complexity
   - Works with existing iterator protocol

2. **Integrate into `BaseFileIterable`**
   - Add configuration options
   - Wrap iterator with read-ahead buffer when enabled
   - Maintain backward compatibility

3. **Test with CSV and JSONL formats**
   - Verify correctness
   - Measure performance improvements
   - Test edge cases (empty files, errors, reset)

4. **Documentation**
   - Usage examples
   - Performance guidance
   - When to use read-ahead

### Phase 2: Thread-Based Prefetching (Optional Enhancement)

1. **Implement `ThreadedReadAheadBuffer` class**
   - Background thread for prefetching
   - Queue-based communication
   - Error handling and cleanup

2. **Add configuration option**
   - `read_ahead_threaded` parameter
   - Opt-in feature

3. **Test with network sources**
   - S3, GCS, Azure
   - Measure performance improvements
   - Verify thread safety

4. **Documentation**
   - When to use threaded prefetching
   - Performance characteristics
   - Thread safety guarantees

### Phase 3: Format-Specific Optimizations (Future)

1. **Optimize for specific formats**
   - CSV: Prefetch raw lines, parse on-demand
   - JSONL: Prefetch raw lines, parse on-demand
   - Parquet: Prefetch batches

2. **Adaptive buffer sizing**
   - Adjust buffer size based on I/O speed
   - Larger buffers for slow I/O

## Testing Strategy

### Unit Tests

1. **ReadAheadBuffer Tests**
   - Buffer refilling behavior
   - Exhaustion handling
   - Peek functionality
   - Reset/clear operations

2. **ThreadedReadAheadBuffer Tests**
   - Thread safety
   - Error propagation
   - Cleanup on close
   - Queue size limits

### Integration Tests

1. **Format Integration**
   - CSV with read-ahead
   - JSONL with read-ahead
   - JSON with read-ahead (verify no conflicts)

2. **Configuration**
   - Enable/disable read-ahead
   - Different buffer sizes
   - Threaded vs non-threaded

3. **Edge Cases**
   - Empty files
   - Errors during prefetching
   - Reset operations
   - Context manager cleanup

### Performance Tests

1. **Benchmark I/O Wait Time**
   - Measure time spent waiting for I/O
   - Compare with/without read-ahead

2. **Network Source Tests**
   - S3, GCS, Azure
   - Measure throughput improvement
   - Compare threaded vs non-threaded

3. **Memory Usage**
   - Verify buffer memory usage
   - Check for memory leaks

## Usage Examples

### Basic Usage

```python
# Enable read-ahead with default settings (10 rows)
with open_iterable("data.csv", iterableargs={"read_ahead": True}) as source:
    for row in source:
        process(row)
```

### Custom Buffer Size

```python
# Prefetch 50 rows ahead
with open_iterable(
    "data.jsonl",
    iterableargs={"read_ahead": True, "read_ahead_size": 50}
) as source:
    for row in source:
        process(row)
```

### Thread-Based Prefetching for Network Sources

```python
# Use threaded prefetching for S3 (high latency)
with open_iterable(
    "s3://bucket/data.csv",
    iterableargs={
        "read_ahead": True,
        "read_ahead_size": 100,
        "read_ahead_threaded": True
    }
) as source:
    for row in source:
        process(row)
```

### Bulk Operations with Read-Ahead

```python
# Prefetch next batch while processing current batch
with open_iterable(
    "data.csv",
    iterableargs={"read_ahead": True, "read_ahead_size": 2}
) as source:
    while True:
        batch = source.read_bulk(1000)
        if not batch:
            break
        process_batch(batch)
        # Next 2000 rows prefetched during processing
```

### Disable Read-Ahead

```python
# Explicitly disable (default behavior)
with open_iterable("data.csv", iterableargs={"read_ahead": False}) as source:
    for row in source:
        process(row)
```

## Migration Path

### Backward Compatibility

- **Default Behavior**: Read-ahead disabled by default
- **No API Changes**: Existing code continues to work
- **Opt-In Feature**: Users enable read-ahead when beneficial

### Gradual Adoption

1. **Phase 1**: Simple buffer-based read-ahead (opt-in)
2. **Phase 2**: Thread-based prefetching (opt-in)
3. **Phase 3**: Consider enabling by default for network sources

### Documentation

- Add read-ahead to performance guide
- Include examples in format-specific docs
- Document when read-ahead helps vs doesn't help

## Recommendations

### Immediate Implementation (Phase 1)

1. **Implement simple buffer-based read-ahead**
   - `ReadAheadBuffer` class
   - Integration into `BaseFileIterable`
   - Configuration via `iterableargs`

2. **Test with CSV and JSONL**
   - Verify correctness
   - Measure performance improvements
   - Document usage

3. **Keep it simple**
   - No threading initially
   - Focus on correctness and usability
   - Measure real-world benefits

### Future Enhancements (Phase 2+)

1. **Thread-based prefetching** for network sources
2. **Format-specific optimizations** (prefetch raw lines, parse on-demand)
3. **Adaptive buffer sizing** based on I/O characteristics
4. **Integration with async/await** support (Task 13.1)

## Conclusion

Read-ahead caching provides significant performance benefits for sequential processing, especially for network-based sources and slow I/O. The recommended approach is to start with a simple buffer-based implementation (Phase 1) and add thread-based prefetching (Phase 2) for network sources where the benefit is highest.

The system should be opt-in initially, with clear documentation on when it helps vs doesn't help. Backward compatibility is maintained by keeping read-ahead disabled by default.
