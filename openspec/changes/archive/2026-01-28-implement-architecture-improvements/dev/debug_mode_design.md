# Debug Mode with Verbose Logging Design

## Executive Summary

This document designs a comprehensive debug mode with verbose logging for IterableData, enabling detailed logging of operations, format detection, file I/O, parsing, errors, and performance metrics. The system integrates with Python's standard logging framework and provides actionable debugging information for troubleshooting and development.

## Current State

### Existing Logging

1. **Basic Logging** (`iterable/pipeline/core.py`)
   - Uses Python's `logging` module
   - Logger: `logger = logging.getLogger(__name__)`
   - Limited logging: Only error messages in exception handlers
   - No debug/verbose logging

2. **Debug Parameter** (`pipeline()` function)
   - `debug: bool = False` parameter exists
   - **Current behavior**: Only controls exception raising (`raise` vs `catch`)
   - **Limitation**: Doesn't enable verbose logging

3. **No Global Debug Mode**
   - No way to enable debug logging globally
   - No verbose logging of operations
   - No detailed format detection logging
   - No file I/O operation logging

### Limitations

1. **No Operation Visibility**: Can't see what operations are being performed
2. **No Format Detection Logging**: Can't debug format detection issues
3. **No File I/O Logging**: Can't debug file opening/closing/reading issues
4. **No Performance Logging**: Can't see timing information
5. **No Parsing Logging**: Can't debug parsing issues
6. **No State Logging**: Can't see internal state changes

## Use Cases

### 1. Troubleshooting Format Detection

**Problem**: File format not detected correctly, need to understand why.

**Benefit**: Verbose logging shows detection steps, confidence scores, fallback logic.

**Example**:
```python
# Enable debug mode
import logging
logging.basicConfig(level=logging.DEBUG)

with open_iterable('data.unknown', debug=True) as source:
    # Logs show:
    # - Filename extension check
    # - Content-based detection attempts
    # - Magic number checks
    # - Confidence scores
    # - Final format decision
    for row in source:
        process(row)
```

### 2. Debugging File I/O Issues

**Problem**: File not opening, reading errors, need to see what's happening.

**Benefit**: Verbose logging shows file operations, errors, retries.

**Example**:
```python
# Debug file operations
with open_iterable('data.csv', debug=True) as source:
    # Logs show:
    # - File opening attempts
    # - Codec detection and initialization
    # - Read operations
    # - Error details
    for row in source:
        process(row)
```

### 3. Performance Debugging

**Problem**: Slow operations, need to identify bottlenecks.

**Benefit**: Verbose logging shows timing information, operation counts.

**Example**:
```python
# Debug performance
pipeline(
    source=source,
    destination=dest,
    process_func=transform,
    debug=True  # Logs show:
    # - Time per operation
    # - Throughput metrics
    # - Bottleneck identification
)
```

### 4. Parsing Error Debugging

**Problem**: Parsing errors, need to see what data caused the error.

**Benefit**: Verbose logging shows problematic data, parsing context.

**Example**:
```python
# Debug parsing
with open_iterable('data.csv', debug=True) as source:
    # Logs show:
    # - Row-by-row parsing
    # - Problematic data samples
    # - Parsing context
    # - Error details
    for row in source:
        process(row)
```

## Design Options

### Option 1: Python Logging Integration (Recommended)

**Approach**: Use Python's standard `logging` module with debug levels.

**Pros**:
- Standard Python approach
- Integrates with existing logging infrastructure
- Configurable via logging configuration
- Supports multiple handlers (file, console, etc.)
- Can be controlled globally or per-module

**Cons**:
- Requires logging configuration
- May be verbose for production

**Implementation**:
- Use `logger.debug()` for verbose information
- Use `logger.info()` for important operations
- Use `logger.warning()` for warnings
- Use `logger.error()` for errors

### Option 2: Custom Debug Flag

**Approach**: Add `debug` parameter to functions, enable verbose output.

**Pros**:
- Simple to use
- Explicit control
- No logging configuration needed

**Cons**:
- Not standard Python approach
- Harder to integrate with logging infrastructure
- Less flexible

**Implementation**:
- Add `debug: bool = False` parameter
- Print debug information when enabled
- Can't easily redirect to files/logs

### Option 3: Hybrid Approach (Recommended)

**Approach**: Combine Python logging with `debug` parameter for convenience.

**Pros**:
- Best of both worlds
- Standard logging infrastructure
- Convenient `debug` parameter
- Flexible configuration

**Cons**:
- Slightly more complex

**Implementation**:
- Use Python logging for all logging
- `debug` parameter enables DEBUG level logging
- Can also configure via logging configuration

## Implementation Design

### 1. Logging Infrastructure

#### Logger Hierarchy

```python
# In iterable/__init__.py or iterable/config.py
import logging

# Root logger for iterable package
logger = logging.getLogger('iterable')

# Sub-loggers for different components
format_detection_logger = logging.getLogger('iterable.detect')
file_io_logger = logging.getLogger('iterable.io')
parsing_logger = logging.getLogger('iterable.parse')
performance_logger = logging.getLogger('iterable.perf')
```

#### Debug Mode Configuration

```python
# In iterable/config.py or iterable/helpers/debug.py
def enable_debug_mode(level: int = logging.DEBUG, handler: logging.Handler | None = None):
    """
    Enable debug mode with verbose logging.
    
    Args:
        level: Logging level (default: logging.DEBUG)
        handler: Optional logging handler (default: StreamHandler to stderr)
    """
    if handler is None:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
    
    logger = logging.getLogger('iterable')
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.propagate = False  # Don't propagate to root logger
```

### 2. Format Detection Logging

#### Implementation

```python
# In iterable/helpers/detect.py
import logging

format_detection_logger = logging.getLogger('iterable.detect')

def detect_file_type(filename: str, debug: bool = False) -> FileTypeResult:
    """Detect file type with optional debug logging."""
    if debug:
        format_detection_logger.setLevel(logging.DEBUG)
    
    format_detection_logger.debug(f"Detecting file type for: {filename}")
    
    # Check filename extension
    ext = os.path.splitext(filename)[1].lower()
    format_detection_logger.debug(f"File extension: {ext}")
    
    # Try extension-based detection
    if ext in EXTENSION_MAP:
        format_id = EXTENSION_MAP[ext]
        format_detection_logger.debug(f"Detected format from extension: {format_id}")
        return FileTypeResult(format_id=format_id, confidence=1.0, method="extension")
    
    # Try content-based detection
    format_detection_logger.debug("Extension detection failed, trying content-based detection")
    format_id, confidence, method = detect_file_type_from_content(filename)
    format_detection_logger.debug(f"Content-based detection: {format_id} (confidence: {confidence}, method: {method})")
    
    return FileTypeResult(format_id=format_id, confidence=confidence, method=method)
```

### 3. File I/O Logging

#### Implementation

```python
# In iterable/base.py
import logging

file_io_logger = logging.getLogger('iterable.io')

class BaseFileIterable(BaseIterable):
    def open(self, debug: bool = False) -> typing.IO[Any] | None:
        """Open file with optional debug logging."""
        if debug:
            file_io_logger.setLevel(logging.DEBUG)
        
        file_io_logger.debug(f"Opening file: {self.filename}")
        
        try:
            if self.stype == ITERABLE_TYPE_FILE:
                file_io_logger.debug(f"File mode: {self.mode}, binary: {self.binary}, encoding: {self.encoding}")
                self.fobj = open(self.filename, self.mode + ("b" if self.binary else ""), encoding=self.encoding)
                file_io_logger.debug(f"File opened successfully: {self.filename}")
                return self.fobj
        except Exception as e:
            file_io_logger.error(f"Failed to open file {self.filename}: {e}", exc_info=True)
            raise
    
    def read(self, skip_empty: bool = True) -> Row:
        """Read record with optional debug logging."""
        if hasattr(self, '_debug') and self._debug:
            file_io_logger.debug(f"Reading record from: {self.filename}")
        
        try:
            row = self._read_impl(skip_empty)
            if hasattr(self, '_debug') and self._debug:
                file_io_logger.debug(f"Read record #{self.pos}: {len(row)} fields")
            return row
        except Exception as e:
            if hasattr(self, '_debug') and self._debug:
                file_io_logger.error(f"Error reading record #{self.pos}: {e}", exc_info=True)
            raise
```

### 4. Parsing Logging

#### Implementation

```python
# In iterable/datatypes/csv.py
import logging

parsing_logger = logging.getLogger('iterable.parse')

class CSVIterable(BaseFileIterable):
    def read(self, skip_empty: bool = True) -> Row:
        """Read CSV record with optional debug logging."""
        debug = getattr(self, '_debug', False)
        
        if debug:
            parsing_logger.debug(f"Reading CSV record from: {self.filename}")
        
        try:
            row = next(self.reader)
            if debug:
                parsing_logger.debug(f"Parsed CSV record #{self.reader.line_num}: {len(row)} fields")
                parsing_logger.debug(f"Record fields: {list(row.keys())[:5]}...")  # First 5 fields
            
            self.pos += 1
            return row
        except Exception as e:
            if debug:
                parsing_logger.error(
                    f"CSV parsing error at line {self.reader.line_num}: {e}",
                    exc_info=True
                )
                if hasattr(self, '_current_line'):
                    parsing_logger.debug(f"Problematic line: {self._current_line}")
            raise
```

### 5. Performance Logging

#### Implementation

```python
# In iterable/pipeline/core.py
import logging
import time

performance_logger = logging.getLogger('iterable.perf')

class Pipeline:
    def run(self, debug: bool = False) -> PipelineResult:
        """Run pipeline with optional performance logging."""
        if debug:
            performance_logger.setLevel(logging.DEBUG)
        
        time_start = time.time()
        performance_logger.debug("Pipeline execution started")
        
        stats = {"rec_count": 0, "nulls": 0, "exceptions": 0}
        
        for record in self.source:
            record_start = time.time()
            
            try:
                result = self.process_func(record, state)
                
                record_time = time.time() - record_start
                if performance_logger.isEnabledFor(logging.DEBUG):
                    performance_logger.debug(f"Processed record #{stats['rec_count']} in {record_time:.4f}s")
                
                # ... rest of processing ...
            except Exception as e:
                record_time = time.time() - record_start
                performance_logger.warning(f"Error processing record #{stats['rec_count']} after {record_time:.4f}s: {e}")
                # ... error handling ...
        
        total_time = time.time() - time_start
        performance_logger.info(f"Pipeline completed: {stats['rec_count']} records in {total_time:.2f}s ({stats['rec_count']/total_time:.0f} records/sec)")
        
        return PipelineResult(...)
```

### 6. Debug Parameter Integration

#### API Design

```python
# In iterable/helpers/detect.py
def open_iterable(
    filename: str,
    mode: Literal["r", "w", "rb", "wb"] = "r",
    engine: str = "internal",
    codecargs: CodecArgs | None = None,
    iterableargs: IterableArgs | None = None,
    debug: bool = False,  # New parameter
) -> BaseIterable:
    """
    Args:
        debug: If True, enable verbose debug logging for this operation
    """
    if debug:
        # Enable debug logging for this operation
        logger = logging.getLogger('iterable')
        logger.setLevel(logging.DEBUG)
        if not logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            ))
            logger.addHandler(handler)
    
    # ... rest of implementation ...
    # Pass debug flag to iterable instance
    if iterableargs is None:
        iterableargs = {}
    iterableargs['_debug'] = debug
    
    # ...
```

#### Pipeline Debug Integration

```python
# In iterable/pipeline/core.py
def pipeline(
    source: BaseIterable,
    destination: BaseIterable | None,
    process_func: Callable[[Row, dict[str, Any]], Row | None],
    # ... existing parameters ...
    debug: bool = False,  # Enhanced: now enables verbose logging
) -> PipelineResult:
    """
    Args:
        debug: If True, enable verbose debug logging and raise exceptions immediately
    """
    if debug:
        # Enable debug logging
        logger = logging.getLogger('iterable')
        logger.setLevel(logging.DEBUG)
        if not logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            ))
            logger.addHandler(handler)
    
    runner = Pipeline(
        # ... pass debug flag ...
        debug=debug,
    )
    return runner.run(debug)
```

## Configuration Options

### Global Debug Mode

```python
# Enable debug mode globally
from iterable.helpers.debug import enable_debug_mode

enable_debug_mode(level=logging.DEBUG)
```

### Per-Operation Debug Mode

```python
# Enable debug for specific operation
with open_iterable('data.csv', debug=True) as source:
    for row in source:
        process(row)
```

### Logging Configuration

```python
# Configure logging via standard Python logging
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)
```

### Environment Variable

```python
# Enable debug via environment variable
import os
if os.getenv('ITERABLEDATA_DEBUG', '').lower() in ('1', 'true', 'yes'):
    enable_debug_mode()
```

## Logging Levels

### DEBUG Level (Most Verbose)

- Format detection steps
- File I/O operations
- Row-by-row parsing
- Performance metrics per operation
- Internal state changes

### INFO Level (Moderate Verbosity)

- File opening/closing
- Format detection results
- Batch operations
- Summary statistics

### WARNING Level (Default)

- Warnings about operations
- Non-fatal errors
- Performance warnings

### ERROR Level (Minimal)

- Errors only
- Exception details

## Usage Examples

### Basic Debug Mode

```python
# Enable debug for single operation
with open_iterable('data.csv', debug=True) as source:
    for row in source:
        process(row)
```

### Global Debug Mode

```python
# Enable debug globally
from iterable.helpers.debug import enable_debug_mode
import logging

enable_debug_mode(level=logging.DEBUG)

# All operations now log debug information
with open_iterable('data.csv') as source:
    for row in source:
        process(row)
```

### Pipeline Debug Mode

```python
# Enable debug for pipeline
pipeline(
    source=source,
    destination=dest,
    process_func=transform,
    debug=True  # Enables verbose logging
)
```

### Custom Logging Configuration

```python
# Configure logging to file
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('iterabledata_debug.log'),
        logging.StreamHandler()
    ]
)

with open_iterable('data.csv', debug=True) as source:
    for row in source:
        process(row)
```

### Environment Variable Debug

```bash
# Enable debug via environment variable
export ITERABLEDATA_DEBUG=1
python script.py
```

## Performance Considerations

### Overhead

1. **Logging Overhead**
   - String formatting: Minimal
   - Handler processing: Depends on handler
   - File I/O: Can be significant for file handlers

2. **Debug Checks**
   - `if debug:` checks: Negligible
   - `logger.isEnabledFor()`: Minimal overhead

3. **Recommendations**
   - Disable debug in production
   - Use file handlers for large logs
   - Rotate log files
   - Use appropriate log levels

### Optimization

```python
# Use lazy evaluation for expensive debug operations
if logger.isEnabledFor(logging.DEBUG):
    logger.debug(f"Expensive debug info: {expensive_operation()}")
```

## Testing Strategy

### Unit Tests

1. **Debug Mode Tests**
   - Test debug parameter enables logging
   - Test log messages are generated
   - Test log levels are correct

2. **Logging Integration Tests**
   - Test logging configuration
   - Test multiple handlers
   - Test log file output

### Integration Tests

1. **End-to-End Debug Tests**
   - Test debug mode in real scenarios
   - Test log output correctness
   - Test performance impact

## Migration Path

### Backward Compatibility

- **Default Behavior**: Debug mode disabled by default
- **No Breaking Changes**: Existing code continues to work
- **Opt-In Feature**: Users enable debug when needed

### Gradual Adoption

1. **Phase 1**: Add debug parameter to `open_iterable()` and `pipeline()`
2. **Phase 2**: Add logging infrastructure
3. **Phase 3**: Add debug logging throughout codebase
4. **Phase 4**: Document and optimize

## Recommendations

### Immediate Implementation (Phase 1)

1. **Add debug parameter**
   - `open_iterable(debug=True)`
   - `pipeline(debug=True)`
   - `bulk_convert(debug=True)`

2. **Basic logging infrastructure**
   - Logger hierarchy
   - Debug mode configuration function
   - Basic logging in key operations

3. **Documentation**
   - Usage examples
   - Logging configuration guide
   - Troubleshooting guide

### Future Enhancements (Phase 2+)

1. **Comprehensive logging**
   - All operations logged
   - Performance metrics
   - State tracking

2. **Advanced features**
   - Log filtering
   - Structured logging (JSON)
   - Log aggregation support

3. **Performance optimization**
   - Lazy evaluation
   - Log sampling
   - Conditional compilation

## Conclusion

Debug mode with verbose logging provides essential visibility into IterableData operations, enabling effective troubleshooting and development. The recommended approach is to:

1. **Phase 1**: Add debug parameter and basic logging infrastructure
2. **Phase 2**: Add comprehensive logging throughout codebase
3. **Phase 3**: Optimize and enhance logging features

All implementations maintain backward compatibility by keeping debug mode opt-in and disabled by default. The system integrates with Python's standard logging framework, providing flexibility and standard tooling support.
