# Parallel Processing Support Design

## Executive Summary

This document designs parallel processing support for IterableData, enabling concurrent processing of records in pipelines and parallel file conversion in `bulk_convert()`. The system will support both threading (for I/O-bound operations) and multiprocessing (for CPU-bound operations) while maintaining thread safety, proper error handling, and progress tracking.

## Current State

### Sequential Processing

1. **Pipeline Processing** (`iterable/pipeline/core.py`)
   - Processes records sequentially, one at a time
   - Single-threaded execution
   - No parallel processing capabilities

2. **Bulk Conversion** (`iterable/convert/core.py`)
   - `bulk_convert()` processes files sequentially
   - Each file conversion waits for previous to complete
   - No parallel file processing

3. **Record Processing**
   - `process_func` in pipelines executes sequentially
   - No concurrent record processing

### Limitations

1. **CPU-Bound Operations**: Sequential processing doesn't utilize multiple CPU cores
2. **I/O-Bound Operations**: Sequential file conversion doesn't parallelize I/O operations
3. **Slow Transformations**: CPU-intensive transformations process one record at a time
4. **Multiple File Conversion**: `bulk_convert()` processes files one-by-one

## Use Cases

### 1. Parallel Record Processing in Pipelines

**Problem**: CPU-bound transformations process records sequentially, not utilizing multiple CPU cores.

**Benefit**: Parallel processing of records speeds up CPU-intensive transformations.

**Example**:
```python
# Sequential processing (current)
def complex_transform(record, state):
    # CPU-intensive operation (e.g., ML inference, complex calculations)
    return process_record(record)

pipeline(
    source=source,
    destination=dest,
    process_func=complex_transform  # Processes one record at a time
)

# Parallel processing (proposed)
pipeline(
    source=source,
    destination=dest,
    process_func=complex_transform,
    parallel=True,  # Enable parallel processing
    workers=4  # Use 4 worker processes
)
```

### 2. Parallel File Conversion

**Problem**: `bulk_convert()` processes files sequentially, not utilizing I/O parallelism.

**Benefit**: Parallel file conversion speeds up batch operations.

**Example**:
```python
# Sequential conversion (current)
bulk_convert('data/*.csv', 'output/', to_ext='parquet')
# Processes files one-by-one

# Parallel conversion (proposed)
bulk_convert(
    'data/*.csv',
    'output/',
    to_ext='parquet',
    parallel=True,  # Enable parallel conversion
    workers=4  # Convert 4 files concurrently
)
```

### 3. Parallel Reading/Writing

**Problem**: Reading from multiple sources or writing to multiple destinations is sequential.

**Benefit**: Parallel I/O operations improve throughput.

**Example**:
```python
# Parallel reading from multiple sources
sources = ['file1.csv', 'file2.csv', 'file3.csv']
with parallel_read(sources, workers=3) as reader:
    for record in reader:
        process(record)
```

## Design Options

### Option 1: Threading (Recommended for I/O-Bound Operations)

**Approach**: Use `threading.ThreadPoolExecutor` for I/O-bound operations.

**Pros**:
- Good for I/O-bound operations (file reading/writing, network I/O)
- Lower overhead than multiprocessing
- Shared memory (easier state management)
- Works well with GIL for I/O operations

**Cons**:
- Limited benefit for CPU-bound operations (GIL limitation)
- Thread synchronization complexity
- Potential race conditions

**Use Cases**:
- Parallel file conversion (`bulk_convert()`)
- Parallel reading from multiple sources
- I/O-bound transformations

### Option 2: Multiprocessing (Recommended for CPU-Bound Operations)

**Approach**: Use `multiprocessing.Pool` or `concurrent.futures.ProcessPoolExecutor` for CPU-bound operations.

**Pros**:
- True parallelism for CPU-bound operations
- Bypasses GIL limitations
- Utilizes multiple CPU cores effectively

**Cons**:
- Higher overhead (process creation, IPC)
- Serialization overhead (pickle)
- More complex state management
- Not suitable for I/O-bound operations

**Use Cases**:
- CPU-bound record transformations
- Complex calculations
- ML inference

### Option 3: Hybrid Approach (Recommended)

**Approach**: Use threading for I/O-bound operations, multiprocessing for CPU-bound operations.

**Pros**:
- Optimal for both I/O and CPU-bound operations
- Flexible configuration
- Best performance for different workloads

**Cons**:
- More complex implementation
- Need to detect operation type (I/O vs CPU)

**Recommendation**: Hybrid approach with automatic detection or explicit configuration.

## Implementation Design

### 1. Parallel Pipeline Processing

#### API Design

```python
def pipeline(
    source: BaseIterable,
    destination: BaseIterable | None,
    process_func: Callable[[Row, dict[str, Any]], Row | None],
    # ... existing parameters ...
    parallel: bool = False,
    workers: int | None = None,
    parallel_mode: Literal["auto", "thread", "process"] = "auto",
    chunk_size: int = 1000,
) -> PipelineResult:
    """
    Args:
        parallel: If True, enable parallel processing
        workers: Number of worker threads/processes (default: CPU count)
        parallel_mode: "auto" (detect), "thread" (I/O-bound), "process" (CPU-bound)
        chunk_size: Number of records to process in each batch
    """
```

#### Implementation Strategy

**Thread-Based (I/O-Bound)**:
```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def _process_chunk_threaded(chunk, process_func, state):
    """Process chunk of records in thread."""
    results = []
    for record in chunk:
        try:
            result = process_func(record, state)
            results.append(result)
        except Exception as e:
            results.append(None)  # Handle errors
    return results

# In pipeline.run()
if parallel and parallel_mode in ("auto", "thread"):
    with ThreadPoolExecutor(max_workers=workers) as executor:
        chunk = []
        futures = []
        
        for record in self.source:
            chunk.append(record)
            if len(chunk) >= chunk_size:
                future = executor.submit(_process_chunk_threaded, chunk, self.process_func, state)
                futures.append(future)
                chunk = []
        
        # Process remaining chunk
        if chunk:
            future = executor.submit(_process_chunk_threaded, chunk, self.process_func, state)
            futures.append(future)
        
        # Collect results and write to destination
        for future in as_completed(futures):
            results = future.result()
            for result in results:
                if result is not None:
                    self.destination.write(result)
```

**Process-Based (CPU-Bound)**:
```python
from concurrent.futures import ProcessPoolExecutor, as_completed

def _process_chunk_process(chunk, process_func_pickleable):
    """Process chunk of records in process (must be pickleable)."""
    results = []
    state = {}  # State must be serializable
    for record in chunk:
        try:
            result = process_func_pickleable(record, state)
            results.append(result)
        except Exception as e:
            results.append(None)
    return results

# In pipeline.run()
if parallel and parallel_mode in ("auto", "process"):
    with ProcessPoolExecutor(max_workers=workers) as executor:
        # Similar to thread-based, but with pickleable functions
        # ...
```

### 2. Parallel Bulk Conversion

#### API Design

```python
def bulk_convert(
    source: str,
    dest: str,
    # ... existing parameters ...
    parallel: bool = False,
    workers: int | None = None,
) -> BulkConversionResult:
    """
    Args:
        parallel: If True, enable parallel file conversion
        workers: Number of worker threads (default: min(4, CPU count))
    """
```

#### Implementation Strategy

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def _convert_file(file_info):
    """Convert single file (for parallel execution)."""
    source_file, dest_file, kwargs = file_info
    try:
        result = convert(
            fromfile=source_file,
            tofile=dest_file,
            **kwargs
        )
        return (source_file, result, None)
    except Exception as e:
        return (source_file, None, e)

# In bulk_convert()
if parallel:
    # Prepare file conversion tasks
    tasks = []
    for source_file in source_files:
        dest_file = _generate_output_filename(source_file, dest, pattern, to_ext)
        tasks.append((
            source_file,
            dest_file,
            {
                'iterableargs': iterableargs,
                'toiterableargs': toiterableargs,
                'scan_limit': scan_limit,
                'batch_size': batch_size,
                'silent': True,  # Don't show per-file progress
                'is_flatten': is_flatten,
                'use_totals': use_totals,
                'progress': None,  # Handle progress separately
                'show_progress': False,
                'atomic': atomic,
            }
        ))
    
    # Execute conversions in parallel
    with ThreadPoolExecutor(max_workers=workers or min(4, os.cpu_count() or 1)) as executor:
        futures = {executor.submit(_convert_file, task): task[0] for task in tasks}
        
        for future in as_completed(futures):
            source_file, result, error = future.result()
            if error:
                all_errors.append(error)
                file_results.append(FileConversionResult(
                    source_file=source_file,
                    success=False,
                    error=error
                ))
            else:
                total_rows_in += result.rows_in
                total_rows_out += result.rows_out
                successful_files += 1
                file_results.append(FileConversionResult(
                    source_file=source_file,
                    success=True,
                    result=result
                ))
else:
    # Sequential processing (existing code)
    # ...
```

### 3. Parallel Reading/Writing

#### API Design

```python
def parallel_read(
    sources: list[str] | list[BaseIterable],
    workers: int | None = None,
    **iterableargs
) -> ParallelReader:
    """
    Read from multiple sources in parallel.
    
    Args:
        sources: List of file paths or BaseIterable instances
        workers: Number of worker threads
        **iterableargs: Arguments passed to open_iterable()
    
    Returns:
        ParallelReader: Iterator that yields records from all sources
    """
```

#### Implementation Strategy

```python
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import threading

class ParallelReader:
    """Iterator that reads from multiple sources in parallel."""
    
    def __init__(self, sources, workers=None, **iterableargs):
        self.sources = sources
        self.workers = workers or min(len(sources), os.cpu_count() or 1)
        self.iterableargs = iterableargs
        self.queue = Queue()
        self.stop_event = threading.Event()
        self.threads = []
    
    def __iter__(self):
        return self
    
    def __enter__(self):
        # Start worker threads
        for source in self.sources:
            thread = threading.Thread(
                target=self._read_worker,
                args=(source,),
                daemon=True
            )
            thread.start()
            self.threads.append(thread)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_event.set()
        for thread in self.threads:
            thread.join(timeout=1.0)
    
    def _read_worker(self, source):
        """Worker thread that reads from a source."""
        try:
            if isinstance(source, str):
                iterable = open_iterable(source, **self.iterableargs)
            else:
                iterable = source
            
            with iterable:
                for record in iterable:
                    if self.stop_event.is_set():
                        break
                    self.queue.put(record)
        except Exception as e:
            self.queue.put(('__error__', e))
        finally:
            self.queue.put(('__done__', None))
    
    def __next__(self):
        while True:
            item = self.queue.get()
            if item[0] == '__error__':
                raise item[1]
            elif item[0] == '__done__':
                raise StopIteration
            else:
                return item
```

## Configuration Options

### Pipeline Parallel Processing

```python
pipeline(
    source=source,
    destination=dest,
    process_func=transform_func,
    parallel=True,              # Enable parallel processing
    workers=4,                  # Use 4 workers
    parallel_mode="auto",       # Auto-detect (I/O vs CPU)
    chunk_size=1000,            # Process 1000 records per chunk
)
```

### Bulk Conversion Parallel Processing

```python
bulk_convert(
    'data/*.csv',
    'output/',
    to_ext='parquet',
    parallel=True,              # Enable parallel conversion
    workers=4,                  # Convert 4 files concurrently
)
```

### Global Configuration

```python
# In iterable/config.py or similar
DEFAULT_PARALLEL_WORKERS = None  # Auto-detect (CPU count)
DEFAULT_PARALLEL_MODE = "auto"   # Auto-detect I/O vs CPU
DEFAULT_CHUNK_SIZE = 1000        # Records per chunk
```

## Thread Safety Considerations

### Thread-Safe Operations

1. **Reading from Iterables**
   - Each thread should have its own iterable instance
   - Don't share iterables across threads
   - Use separate file handles

2. **Writing to Destinations**
   - Synchronize writes (use locks or queues)
   - Ensure write order if needed
   - Handle concurrent writes safely

3. **State Management**
   - Thread-local state for process_func
   - Shared state requires synchronization
   - Use locks for shared mutable state

### Thread Safety Implementation

```python
import threading

class ThreadSafeWriter:
    """Thread-safe wrapper for destination iterable."""
    
    def __init__(self, destination):
        self.destination = destination
        self.lock = threading.Lock()
    
    def write(self, record):
        with self.lock:
            self.destination.write(record)
    
    def write_bulk(self, records):
        with self.lock:
            self.destination.write_bulk(records)
```

## Error Handling

### Parallel Processing Errors

1. **Record Processing Errors**
   - Catch exceptions in worker threads/processes
   - Return error indicators in results
   - Aggregate errors for reporting

2. **File Conversion Errors**
   - Continue processing other files on error
   - Collect errors per file
   - Report in BulkConversionResult

3. **Worker Failures**
   - Handle worker thread/process crashes
   - Retry failed operations (optional)
   - Graceful degradation

### Error Handling Implementation

```python
def _process_chunk_safe(chunk, process_func, state):
    """Process chunk with error handling."""
    results = []
    errors = []
    
    for i, record in enumerate(chunk):
        try:
            result = process_func(record, state)
            results.append((i, result, None))
        except Exception as e:
            errors.append((i, e))
            results.append((i, None, e))
    
    return results, errors
```

## Performance Considerations

### Expected Improvements

1. **CPU-Bound Operations**
   - **Sequential**: 1x speed
   - **Parallel (4 workers)**: 3-4x speed (near-linear scaling)
   - **Benefit**: Significant for CPU-intensive transformations

2. **I/O-Bound Operations**
   - **Sequential**: 1x speed
   - **Parallel (4 workers)**: 2-4x speed (depends on I/O bandwidth)
   - **Benefit**: Good for file conversion, network I/O

3. **Mixed Workloads**
   - **Sequential**: 1x speed
   - **Parallel**: 2-3x speed (depends on I/O vs CPU ratio)
   - **Benefit**: Moderate improvement

### Overhead

1. **Threading Overhead**
   - Thread creation: ~1ms per thread
   - Context switching: Minimal for I/O-bound
   - Memory: ~8MB per thread (stack)

2. **Multiprocessing Overhead**
   - Process creation: ~10-50ms per process
   - IPC serialization: Depends on data size
   - Memory: Higher (separate process memory)

3. **Synchronization Overhead**
   - Lock contention: Depends on write frequency
   - Queue operations: Minimal overhead
   - State synchronization: Depends on state size

### When Parallel Processing Helps

1. **CPU-Bound Transformations**: Complex calculations, ML inference
2. **Multiple File Conversion**: Converting many files
3. **I/O-Bound Operations**: Reading/writing multiple files
4. **Large Batch Sizes**: Processing large chunks

### When Parallel Processing Doesn't Help

1. **Small Datasets**: Overhead exceeds benefit
2. **Simple Transformations**: Overhead dominates
3. **Single File**: No parallelism opportunity
4. **Memory-Constrained**: Multiple workers increase memory usage

## Testing Strategy

### Unit Tests

1. **Parallel Pipeline Tests**
   - Test parallel processing correctness
   - Verify record order (if required)
   - Test error handling
   - Test worker configuration

2. **Parallel Bulk Conversion Tests**
   - Test parallel file conversion
   - Verify all files processed
   - Test error handling per file
   - Test worker configuration

3. **Thread Safety Tests**
   - Test concurrent writes
   - Test shared state synchronization
   - Test error isolation

### Performance Tests

1. **Benchmark Parallel Processing**
   - Compare sequential vs parallel
   - Measure speedup for different worker counts
   - Test with CPU-bound and I/O-bound workloads

2. **Scalability Tests**
   - Test with varying worker counts
   - Test with varying chunk sizes
   - Identify optimal configurations

### Integration Tests

1. **End-to-End Tests**
   - Test parallel processing in real scenarios
   - Test with large datasets
   - Test error recovery

## Usage Examples

### Parallel Pipeline Processing

```python
# CPU-bound transformation
def ml_inference(record, state):
    # CPU-intensive ML inference
    return model.predict(record)

pipeline(
    source=source,
    destination=dest,
    process_func=ml_inference,
    parallel=True,          # Enable parallel processing
    workers=4,              # Use 4 worker processes
    parallel_mode="process", # CPU-bound, use processes
    chunk_size=100          # Process 100 records per chunk
)
```

### Parallel Bulk Conversion

```python
# Convert multiple files in parallel
result = bulk_convert(
    'data/raw/*.csv.gz',
    'data/processed/',
    to_ext='parquet',
    parallel=True,  # Enable parallel conversion
    workers=4       # Convert 4 files concurrently
)

print(f"Converted {result.successful_files} files in parallel")
```

### Parallel Reading

```python
# Read from multiple sources in parallel
sources = ['file1.csv', 'file2.csv', 'file3.csv']
with parallel_read(sources, workers=3) as reader:
    for record in reader:
        process(record)
```

## Migration Path

### Backward Compatibility

- **Default Behavior**: Parallel processing disabled by default
- **No API Changes**: Existing code continues to work
- **Opt-In Feature**: Users enable parallel processing when beneficial

### Gradual Adoption

1. **Phase 1**: Implement parallel bulk conversion (I/O-bound)
2. **Phase 2**: Implement parallel pipeline processing (CPU-bound)
3. **Phase 3**: Add parallel reading/writing utilities
4. **Phase 4**: Optimize and tune defaults

### Documentation

- Add parallel processing guide
- Document when to use parallel processing
- Provide performance guidance
- Include examples

## Recommendations

### Immediate Implementation (Phase 1)

1. **Implement parallel bulk conversion**
   - Thread-based (I/O-bound)
   - Easy to implement
   - High impact for batch operations

2. **Add configuration options**
   - `parallel` parameter
   - `workers` parameter
   - Backward compatible defaults

3. **Test thoroughly**
   - Verify correctness
   - Measure performance improvements
   - Test error handling

### Future Enhancements (Phase 2+)

1. **Parallel pipeline processing**
   - Thread-based for I/O-bound
   - Process-based for CPU-bound
   - Auto-detection of operation type

2. **Parallel reading/writing utilities**
   - `parallel_read()` function
   - `parallel_write()` function
   - Advanced parallel patterns

3. **Performance optimizations**
   - Adaptive worker count
   - Dynamic chunk sizing
   - Work stealing for load balancing

## Conclusion

Parallel processing support provides significant performance improvements for CPU-bound transformations and I/O-bound file conversion operations. The recommended approach is to:

1. **Phase 1**: Implement parallel bulk conversion (threading, I/O-bound)
2. **Phase 2**: Implement parallel pipeline processing (threading + multiprocessing, I/O + CPU-bound)
3. **Phase 3**: Add parallel reading/writing utilities
4. **Phase 4**: Optimize and tune defaults

All implementations maintain backward compatibility by keeping parallel processing opt-in and disabled by default. The system should automatically detect optimal worker counts and provide clear guidance on when parallel processing is beneficial.
