# Async/Await Support Patterns Research

## Executive Summary

This document researches async/await support patterns for IterableData, analyzing use cases, design approaches, implementation strategies, and trade-offs. The goal is to provide a foundation for implementing async support while maintaining backward compatibility with the existing synchronous API.

## Current State

### Synchronous I/O Operations

IterableData currently uses synchronous I/O operations throughout:

1. **File Operations**: `open()`, `read()`, `write()`, `seek()` - all blocking
2. **Stream Operations**: Reading from/writing to file-like objects
3. **Database Queries**: DuckDB queries execute synchronously
4. **Network Operations**: Cloud storage (S3, GCS, Azure) and database connections use synchronous libraries
5. **Compression/Decompression**: Codec operations are synchronous

### Key I/O Points

- `BaseFileIterable.read()` - Reads single record (blocking)
- `BaseFileIterable.read_bulk()` - Reads multiple records (blocking)
- `BaseFileIterable.write()` - Writes single record (blocking)
- `BaseFileIterable.write_bulk()` - Writes multiple records (blocking)
- `BaseFileIterable.__iter__()` / `__next__()` - Iterator protocol (blocking)
- File opening/closing operations
- Format detection (file reading for magic numbers)

## Use Cases for Async/Await

### 1. Concurrent File Processing

**Scenario**: Process multiple files concurrently without blocking

```python
# Current (sequential)
for filename in files:
    with open_iterable(filename) as source:
        process(source)

# With async (concurrent)
async def process_file(filename):
    async with aopen_iterable(filename) as source:
        async for row in source:
            await process(row)

await asyncio.gather(*[process_file(f) for f in files])
```

**Benefit**: Significant speedup when I/O-bound (network storage, multiple files)

### 2. Network-Based Sources

**Scenario**: Reading from cloud storage (S3, GCS, Azure) or remote databases

```python
# Current (blocking on network I/O)
with open_iterable('s3://bucket/data.csv') as source:
    for row in source:
        process(row)  # Blocks waiting for network

# With async (non-blocking)
async with aopen_iterable('s3://bucket/data.csv') as source:
    async for row in source:
        await process(row)  # Can handle other tasks while waiting
```

**Benefit**: Better resource utilization, can handle other operations while waiting for network

### 3. Database Queries

**Scenario**: Multiple concurrent database queries

```python
# Current (sequential queries)
results1 = list(open_iterable('postgresql://...', iterableargs={'query': 'SELECT ...'}))
results2 = list(open_iterable('postgresql://...', iterableargs={'query': 'SELECT ...'}))

# With async (concurrent queries)
async def query_db(query):
    async with aopen_iterable('postgresql://...', iterableargs={'query': query}) as source:
        return [row async for row in source]

results = await asyncio.gather(query_db('SELECT ...'), query_db('SELECT ...'))
```

**Benefit**: Parallel database queries, better throughput

### 4. Pipeline Processing with External Services

**Scenario**: Transform data while calling external APIs

```python
# Current (blocking on API calls)
with open_iterable('input.csv') as source:
    with open_iterable('output.jsonl', mode='w') as dest:
        for row in source:
            enriched = call_external_api(row)  # Blocks
            dest.write(enriched)

# With async (non-blocking API calls)
async with aopen_iterable('input.csv') as source:
    async with aopen_iterable('output.jsonl', mode='w') as dest:
        async for row in source:
            enriched = await call_external_api(row)  # Non-blocking
            await dest.write(enriched)
```

**Benefit**: Can process multiple rows while waiting for API responses

### 5. Real-Time Data Streaming

**Scenario**: Process streaming data from network sources

```python
# With async (natural fit for streaming)
async with aopen_iterable(stream=network_stream) as source:
    async for row in source:
        await process_realtime(row)
```

**Benefit**: Natural fit for async I/O patterns

## Design Patterns

### Pattern 1: Dual API (Synchronous + Async)

Provide both synchronous and async versions of the API:

```python
# Synchronous (existing)
def open_iterable(...) -> BaseIterable:
    ...

# Async (new)
async def aopen_iterable(...) -> AsyncBaseIterable:
    ...
```

**Pros**:
- Maintains backward compatibility
- Clear separation of concerns
- Users choose based on needs

**Cons**:
- Code duplication (mitigated by shared implementation)
- Two APIs to maintain

**Examples**: `aiofiles`, `aiohttp` (has both sync and async APIs)

### Pattern 2: Async Iterators

Implement async iterator protocol:

```python
class AsyncBaseIterable:
    async def __aiter__(self):
        return self
    
    async def __anext__(self):
        row = await self.aread()
        if row is None:
            raise StopAsyncIteration
        return row
    
    async def aread(self) -> dict:
        # Async read implementation
        ...
```

**Usage**:
```python
async with aopen_iterable('data.csv') as source:
    async for row in source:
        process(row)
```

### Pattern 3: Async Context Managers

Support async context managers:

```python
class AsyncBaseIterable:
    async def __aenter__(self):
        await self.aopen()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.aclose()
```

### Pattern 4: Async Factory Methods

Extend factory methods to async:

```python
class AsyncBaseFileIterable:
    @classmethod
    async def afrom_file(cls, filename: str, ...):
        instance = cls.__new__(cls)
        await instance._ainit_source(filename=filename, ...)
        return instance
    
    @classmethod
    async def afrom_stream(cls, stream: AsyncIO, ...):
        ...
```

## Implementation Approaches

### Approach 1: Wrapper Layer (Recommended)

Create async wrappers around synchronous operations using `asyncio.to_thread()` or `run_in_executor()`:

```python
class AsyncBaseIterable:
    def __init__(self, sync_iterable: BaseIterable):
        self._sync = sync_iterable
    
    async def aread(self) -> dict:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._sync.read)
    
    async def __aiter__(self):
        return self
    
    async def __anext__(self):
        loop = asyncio.get_event_loop()
        try:
            row = await loop.run_in_executor(None, self._sync.read)
            return row
        except StopIteration:
            raise StopAsyncIteration
```

**Pros**:
- Minimal changes to existing code
- Reuses all existing implementations
- Easy to implement

**Cons**:
- Not truly async (still uses threads)
- Overhead of thread pool
- May not provide benefits for CPU-bound operations

### Approach 2: Native Async I/O

Implement true async I/O using `aiofiles`, `aiosqlite`, etc.:

```python
import aiofiles
from aiofiles import open as aio_open

class AsyncCSVIterable(AsyncBaseFileIterable):
    async def aopen(self):
        self._file = await aio_open(self.filename, mode='r', encoding=self.encoding)
        self._reader = csv.DictReader(self._file)
    
    async def aread(self) -> dict:
        row = await self._reader.__anext__()
        return row
```

**Pros**:
- True async I/O (no threads)
- Better performance for I/O-bound operations
- Natural fit for network operations

**Cons**:
- Requires async versions of all I/O libraries
- More complex implementation
- Not all libraries have async support

### Approach 3: Hybrid Approach (Recommended)

Use native async where available (network, databases), wrapper for file I/O:

```python
class AsyncBaseFileIterable:
    async def aopen(self):
        if self._is_network_source(self.filename):
            # Use native async (aiofiles, aioboto3, etc.)
            await self._aopen_network()
        else:
            # Use thread pool for file I/O
            await self._aopen_file()
```

**Pros**:
- Best of both worlds
- Native async for network (where it matters most)
- Simple wrapper for file I/O (where async benefits are limited)

**Cons**:
- More complex implementation
- Need to detect source type

## Library Examples

### aiofiles

Provides async file I/O:

```python
import aiofiles

async with aiofiles.open('file.txt', 'r') as f:
    content = await f.read()
```

**Pattern**: Wrapper around synchronous file operations using threads

### aiocsv

Async CSV reading:

```python
import aiocsv
import aiofiles

async with aiofiles.open('file.csv', 'r') as f:
    async for row in aiocsv.AsyncDictReader(f):
        process(row)
```

**Pattern**: Async iterator over async file handle

### aiobotocore / aioboto3

Async AWS SDK:

```python
import aioboto3

async with aioboto3.Session().client('s3') as s3:
    obj = await s3.get_object(Bucket='bucket', Key='key')
    async for chunk in obj['Body']:
        process(chunk)
```

**Pattern**: Native async network operations

## Implementation Strategy

### Phase 1: Foundation (Low Risk)

1. **Create Async Base Classes**
   - `AsyncBaseIterable` - async version of `BaseIterable`
   - `AsyncBaseFileIterable` - async version of `BaseFileIterable`
   - Implement async iterator protocol (`__aiter__`, `__anext__`)
   - Implement async context manager (`__aenter__`, `__aexit__`)

2. **Wrapper Implementation**
   - Use `run_in_executor()` to wrap synchronous operations
   - Implement `aopen_iterable()` function
   - Support async factory methods

3. **Core Methods**
   - `aread()` - async read
   - `aread_bulk()` - async bulk read
   - `awrite()` - async write
   - `awrite_bulk()` - async bulk write

### Phase 2: Native Async I/O (Medium Risk)

1. **Network Sources**
   - Implement native async for S3, GCS, Azure
   - Use `aioboto3`, `aio-gcs`, etc.

2. **Database Sources**
   - Implement async database drivers
   - Use `asyncpg`, `aiomysql`, etc.

3. **Streaming Sources**
   - Native async for network streams
   - Use `aiohttp` for HTTP streams

### Phase 3: Advanced Features (Higher Risk)

1. **Async Pipeline**
   - `apipeline()` function for async data pipelines
   - Support async transformation functions

2. **Async Conversion**
   - `aconvert()` function for async format conversion
   - Concurrent file conversion

3. **Async Progress Callbacks**
   - Async progress callbacks for long operations

## API Design

### Proposed API

```python
# Async version of open_iterable
async def aopen_iterable(
    filename: str | None = None,
    stream: AsyncIO | None = None,
    mode: str = "r",
    **kwargs
) -> AsyncBaseIterable:
    """Async version of open_iterable"""
    ...

# Usage
async def main():
    async with aopen_iterable('data.csv') as source:
        async for row in source:
            await process(row)
    
    # Bulk operations
    async with aopen_iterable('data.csv') as source:
        batch = await source.aread_bulk(1000)
        for row in batch:
            await process(row)
    
    # Writing
    async with aopen_iterable('output.jsonl', mode='w') as dest:
        await dest.awrite({'key': 'value'})
        await dest.awrite_bulk([{'k': 'v'}, {'k': 'v'}])
```

### Factory Methods

```python
# Async factory methods
source = await CSVIterable.afrom_file('data.csv')
source = await CSVIterable.afrom_stream(async_stream)
```

## Trade-offs and Considerations

### Benefits

1. **Concurrency**: Process multiple files/sources concurrently
2. **Non-blocking I/O**: Better resource utilization
3. **Natural fit**: Async/await is natural for I/O-bound operations
4. **Modern Python**: Aligns with modern Python async ecosystem

### Challenges

1. **Complexity**: Adds significant complexity to codebase
2. **Maintenance**: Two APIs to maintain (sync + async)
3. **Limited Benefits for Files**: File I/O on local filesystem may not benefit much
4. **Thread Pool Overhead**: Wrapper approach uses threads (overhead)
5. **Library Support**: Not all underlying libraries have async support
6. **Backward Compatibility**: Must maintain existing synchronous API

### When Async Makes Sense

✅ **Good Use Cases**:
- Network-based sources (S3, GCS, databases)
- Concurrent processing of multiple files
- Integration with async web frameworks (FastAPI, etc.)
- Real-time streaming from network sources

❌ **Limited Benefit**:
- Single file processing on local filesystem
- CPU-bound operations
- Simple sequential processing

## Recommendations

### Short Term (Phase 1)

1. **Research Complete** ✅
   - Document use cases and patterns
   - Analyze implementation approaches
   - Review similar libraries

2. **Prototype** (Next Step)
   - Implement `AsyncBaseIterable` wrapper
   - Implement `aopen_iterable()` function
   - Test with simple CSV/JSONL formats
   - Measure performance vs synchronous version

3. **Evaluate**
   - Is wrapper approach sufficient?
   - What's the performance impact?
   - Is the API ergonomic?

### Medium Term (Phase 2)

1. **Native Async for Network Sources**
   - Implement native async for S3, GCS, Azure
   - Implement async database drivers
   - Measure performance improvements

2. **Documentation**
   - Add async examples to documentation
   - Create migration guide (sync → async)
   - Document when to use async vs sync

### Long Term (Phase 3)

1. **Advanced Features**
   - Async pipeline processing
   - Async conversion
   - Async progress callbacks

2. **Optimization**
   - Optimize async implementations
   - Reduce overhead where possible
   - Benchmark and improve

## Conclusion

Async/await support would be valuable for IterableData, particularly for:
- Network-based sources (cloud storage, databases)
- Concurrent file processing
- Integration with async frameworks

The recommended approach is a **hybrid strategy**:
- Start with wrapper implementation (low risk, quick to implement)
- Add native async for network sources (where benefits are greatest)
- Maintain backward compatibility with synchronous API

**Next Steps**: Create prototype implementation to validate approach and measure performance impact.
