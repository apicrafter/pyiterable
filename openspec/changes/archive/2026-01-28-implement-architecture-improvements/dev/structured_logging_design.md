# Structured Logging Framework Design

## Executive Summary

This document designs a structured logging framework for IterableData that uses structured data (JSON) instead of plain text logs, enabling better log analysis, filtering, and integration with log aggregation systems. The framework provides consistent log structure across all operations while maintaining backward compatibility with Python's standard logging module.

## Current State

### Existing Logging

1. **Basic Logging** (`iterable/pipeline/core.py`)
   - Uses Python's `logging` module
   - Plain text log messages
   - Limited structured information
   - No consistent log format

2. **Error Logging** (`iterable/base.py`)
   - Structured JSON error logs (via `error_log` parameter)
   - Includes: timestamp, filename, row_number, byte_offset, error_message, original_line
   - Only for errors, not for general operations

3. **No Structured Logging Framework**
   - No consistent log structure
   - No structured logging for operations
   - No integration with log aggregation systems
   - No structured context propagation

### Limitations

1. **Plain Text Logs**: Hard to parse and analyze programmatically
2. **Inconsistent Format**: Different log formats across components
3. **No Context**: Missing structured context (operation ID, correlation IDs, etc.)
4. **No Filtering**: Difficult to filter logs by operation type, format, etc.
5. **No Aggregation**: Not optimized for log aggregation systems (ELK, Splunk, etc.)

## Use Cases

### 1. Log Analysis and Monitoring

**Problem**: Need to analyze logs programmatically, filter by operation type, track performance.

**Benefit**: Structured logs enable easy parsing, filtering, and analysis.

**Example**:
```python
# Structured logs enable:
# - Filtering by operation type
# - Tracking performance metrics
# - Analyzing error patterns
# - Monitoring system health
```

### 2. Log Aggregation Systems

**Problem**: Need to integrate with ELK stack, Splunk, CloudWatch, etc.

**Benefit**: Structured JSON logs integrate seamlessly with log aggregation systems.

**Example**:
```python
# Logs automatically formatted for:
# - Elasticsearch/Kibana (ELK stack)
# - Splunk
# - AWS CloudWatch Logs
# - Google Cloud Logging
# - Azure Monitor
```

### 3. Debugging and Troubleshooting

**Problem**: Need to trace operations across multiple components, correlate events.

**Benefit**: Structured logs with correlation IDs enable end-to-end tracing.

**Example**:
```python
# Structured logs include:
# - Operation IDs for correlation
# - Context propagation
# - Performance metrics
# - Error details with context
```

### 4. Production Monitoring

**Problem**: Need to monitor production systems, track metrics, detect issues.

**Benefit**: Structured logs enable automated monitoring and alerting.

**Example**:
```python
# Structured logs enable:
# - Automated alerting on errors
# - Performance monitoring
# - Usage analytics
# - Capacity planning
```

## Design Options

### Option 1: JSON Structured Logging (Recommended)

**Approach**: Use JSON format for all structured logs, integrate with Python logging.

**Pros**:
- Standard format (JSON)
- Easy to parse and analyze
- Integrates with log aggregation systems
- Flexible and extensible

**Cons**:
- Slightly more verbose than plain text
- Requires JSON serialization

**Implementation**:
- Use `structlog` library or custom JSON formatter
- JSON logs with consistent structure
- Context propagation via logging context

### Option 2: Key-Value Structured Logging

**Approach**: Use key-value pairs in log messages (e.g., `key=value key2=value2`).

**Pros**:
- Human-readable
- Easy to parse
- Works with existing log parsers

**Cons**:
- Less structured than JSON
- Harder to nest complex data
- Not as standard as JSON

**Implementation**:
- Custom formatter for key-value pairs
- Consistent key names
- Context in log messages

### Option 3: Hybrid Approach (Recommended)

**Approach**: Support both JSON (for machine processing) and human-readable (for development).

**Pros**:
- Best of both worlds
- JSON for production/log aggregation
- Human-readable for development
- Configurable output format

**Cons**:
- More complex implementation
- Need to maintain both formats

**Recommendation**: Option 3 (Hybrid Approach) - JSON for production, human-readable for development.

## Implementation Design

### 1. Structured Logging Infrastructure

#### Using structlog Library

```python
# In iterable/helpers/logging.py
import structlog
import logging
import json
from typing import Any

# Configure structlog
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()  # JSON output
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

def get_logger(name: str) -> structlog.BoundLogger:
    """Get structured logger for a module."""
    return structlog.get_logger(name)
```

#### Custom JSON Formatter (Alternative)

```python
# In iterable/helpers/logging.py
import json
import logging
from datetime import datetime
from typing import Any

class StructuredJSONFormatter(logging.Formatter):
    """JSON formatter for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add extra context from record
        for key, value in record.__dict__.items():
            if key not in [
                "name", "msg", "args", "created", "filename", "funcName",
                "levelname", "levelno", "lineno", "module", "msecs",
                "message", "pathname", "process", "processName", "relativeCreated",
                "thread", "threadName", "exc_info", "exc_text", "stack_info"
            ]:
                log_data[key] = value
        
        return json.dumps(log_data)
```

### 2. Structured Log Events

#### Log Event Structure

```python
# Standard log event structure
{
    "timestamp": "2026-01-27T10:30:45.123Z",
    "level": "INFO",
    "logger": "iterable.detect",
    "message": "File format detected",
    "event_type": "format_detection",
    "context": {
        "filename": "data.csv",
        "format_id": "csv",
        "confidence": 1.0,
        "method": "extension"
    },
    "module": "detect",
    "function": "detect_file_type",
    "line": 123
}
```

#### Event Types

```python
# In iterable/helpers/logging.py
class LogEventType:
    """Standard log event types."""
    FORMAT_DETECTION = "format_detection"
    FILE_IO = "file_io"
    PARSING = "parsing"
    CONVERSION = "conversion"
    PIPELINE = "pipeline"
    ERROR = "error"
    PERFORMANCE = "performance"
    VALIDATION = "validation"
```

### 3. Context Propagation

#### Operation Context

```python
# In iterable/helpers/logging.py
import contextvars
from typing import Any

# Context variables for operation tracking
operation_id: contextvars.ContextVar[str | None] = contextvars.ContextVar('operation_id', default=None)
correlation_id: contextvars.ContextVar[str | None] = contextvars.ContextVar('correlation_id', default=None)
user_id: contextvars.ContextVar[str | None] = contextvars.ContextVar('user_id', default=None)

class OperationContext:
    """Context manager for operation tracking."""
    
    def __init__(self, operation_type: str, **context):
        self.operation_type = operation_type
        self.context = context
        self.operation_id = self._generate_operation_id()
    
    def __enter__(self):
        operation_id.set(self.operation_id)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        operation_id.set(None)
    
    def _generate_operation_id(self) -> str:
        """Generate unique operation ID."""
        import uuid
        return str(uuid.uuid4())
```

### 4. Structured Logging Integration

#### Format Detection Logging

```python
# In iterable/helpers/detect.py
from ..helpers.logging import get_logger, LogEventType

logger = get_logger(__name__)

def detect_file_type(filename: str, debug: bool = False) -> FileTypeResult:
    """Detect file type with structured logging."""
    logger.info(
        "File format detection started",
        event_type=LogEventType.FORMAT_DETECTION,
        filename=filename,
    )
    
    # ... detection logic ...
    
    logger.info(
        "File format detected",
        event_type=LogEventType.FORMAT_DETECTION,
        filename=filename,
        format_id=format_id,
        confidence=confidence,
        method=method,
    )
    
    return FileTypeResult(...)
```

#### File I/O Logging

```python
# In iterable/base.py
from ..helpers.logging import get_logger, LogEventType

logger = get_logger(__name__)

class BaseFileIterable(BaseIterable):
    def open(self, debug: bool = False) -> typing.IO[Any] | None:
        """Open file with structured logging."""
        logger.info(
            "Opening file",
            event_type=LogEventType.FILE_IO,
            operation="open",
            filename=self.filename,
            mode=self.mode,
            binary=self.binary,
            encoding=self.encoding,
        )
        
        try:
            # ... open logic ...
            logger.info(
                "File opened successfully",
                event_type=LogEventType.FILE_IO,
                operation="open",
                filename=self.filename,
            )
            return self.fobj
        except Exception as e:
            logger.error(
                "Failed to open file",
                event_type=LogEventType.FILE_IO,
                operation="open",
                filename=self.filename,
                error=str(e),
                error_type=type(e).__name__,
                exc_info=True,
            )
            raise
```

#### Pipeline Logging

```python
# In iterable/pipeline/core.py
from ..helpers.logging import get_logger, LogEventType, OperationContext

logger = get_logger(__name__)

class Pipeline:
    def run(self, debug: bool = False) -> PipelineResult:
        """Run pipeline with structured logging."""
        with OperationContext("pipeline", source=str(self.source), destination=str(self.destination)):
            logger.info(
                "Pipeline execution started",
                event_type=LogEventType.PIPELINE,
                operation="start",
                source=str(self.source),
                destination=str(self.destination),
            )
            
            # ... pipeline logic ...
            
            logger.info(
                "Pipeline execution completed",
                event_type=LogEventType.PIPELINE,
                operation="complete",
                records_processed=stats["rec_count"],
                elapsed_seconds=total_time,
                throughput=stats["rec_count"] / total_time if total_time > 0 else 0,
            )
```

### 5. Configuration Options

#### Output Format Configuration

```python
# In iterable/helpers/logging.py
def configure_structured_logging(
    format: Literal["json", "human"] = "json",
    level: int = logging.INFO,
    output: str | None = None,
    **kwargs
):
    """
    Configure structured logging.
    
    Args:
        format: Output format - "json" for JSON, "human" for human-readable
        level: Logging level
        output: Output file path (None for stdout/stderr)
        **kwargs: Additional configuration
    """
    if format == "json":
        # Configure JSON output
        processors = [
            # ... JSON processors ...
            structlog.processors.JSONRenderer()
        ]
    else:
        # Configure human-readable output
        processors = [
            # ... human-readable processors ...
            structlog.dev.ConsoleRenderer()
        ]
    
    structlog.configure(processors=processors, **kwargs)
```

#### Environment-Based Configuration

```python
# In iterable/helpers/logging.py
import os

def auto_configure_logging():
    """Auto-configure logging based on environment."""
    format = os.getenv("ITERABLEDATA_LOG_FORMAT", "json")
    level = os.getenv("ITERABLEDATA_LOG_LEVEL", "INFO")
    output = os.getenv("ITERABLEDATA_LOG_OUTPUT", None)
    
    configure_structured_logging(
        format=format,
        level=getattr(logging, level.upper()),
        output=output,
    )
```

### 6. Log Aggregation Integration

#### CloudWatch Integration

```python
# In iterable/helpers/logging.py
def configure_cloudwatch_logging(log_group: str, log_stream: str | None = None):
    """Configure logging for AWS CloudWatch."""
    try:
        import watchtower
        handler = watchtower.CloudWatchLogHandler(
            log_group=log_group,
            stream_name=log_stream,
        )
        # Configure logger with CloudWatch handler
        # ...
    except ImportError:
        raise ImportError("CloudWatch logging requires 'watchtower'. Install it with: pip install watchtower")
```

#### Elasticsearch Integration

```python
# In iterable/helpers/logging.py
def configure_elasticsearch_logging(hosts: list[str], index: str):
    """Configure logging for Elasticsearch."""
    try:
        from pythonjsonlogger import jsonlogger
        # Configure Elasticsearch handler
        # ...
    except ImportError:
        raise ImportError("Elasticsearch logging requires 'python-json-logger'. Install it with: pip install python-json-logger")
```

## Usage Examples

### Basic Structured Logging

```python
# Enable structured logging
from iterable.helpers.logging import configure_structured_logging

configure_structured_logging(format="json", level=logging.INFO)

# Logs are automatically structured
with open_iterable('data.csv') as source:
    for row in source:
        process(row)
```

### Human-Readable Format (Development)

```python
# Use human-readable format for development
configure_structured_logging(format="human", level=logging.DEBUG)

# Logs are formatted for human reading
with open_iterable('data.csv', debug=True) as source:
    for row in source:
        process(row)
```

### File Output

```python
# Write structured logs to file
configure_structured_logging(
    format="json",
    level=logging.INFO,
    output="iterabledata.log"
)

# Logs written to file in JSON format
```

### CloudWatch Integration

```python
# Configure CloudWatch logging
from iterable.helpers.logging import configure_cloudwatch_logging

configure_cloudwatch_logging(
    log_group="iterabledata",
    log_stream="production"
)

# Logs automatically sent to CloudWatch
```

### Operation Context

```python
# Use operation context for correlation
from iterable.helpers.logging import OperationContext

with OperationContext("conversion", source_file="input.csv", dest_file="output.parquet"):
    convert("input.csv", "output.parquet")
    # All logs within this context include operation_id
```

## Performance Considerations

### Overhead

1. **JSON Serialization**
   - Minimal overhead for simple data
   - Can be significant for large objects
   - Use lazy evaluation for expensive operations

2. **Context Propagation**
   - Context variables are efficient
   - Minimal overhead for operation tracking

3. **Recommendations**
   - Use structured logging in production
   - Disable in high-performance scenarios if needed
   - Use appropriate log levels

### Optimization

```python
# Use lazy evaluation for expensive operations
if logger.isEnabledFor(logging.DEBUG):
    logger.debug(
        "Expensive debug info",
        expensive_data=expensive_operation()  # Only called if DEBUG enabled
    )
```

## Testing Strategy

### Unit Tests

1. **Structured Logging Tests**
   - Test log format (JSON/human-readable)
   - Test context propagation
   - Test event types

2. **Integration Tests**
   - Test log aggregation integration
   - Test file output
   - Test CloudWatch/Elasticsearch integration

### Integration Tests

1. **End-to-End Logging Tests**
   - Test structured logging in real scenarios
   - Verify log structure
   - Test log aggregation

## Migration Path

### Backward Compatibility

- **Default Behavior**: Structured logging disabled by default
- **No Breaking Changes**: Existing logging continues to work
- **Opt-In Feature**: Users enable structured logging when needed

### Gradual Adoption

1. **Phase 1**: Add structured logging infrastructure
2. **Phase 2**: Add structured logging to key operations
3. **Phase 3**: Expand to all operations
4. **Phase 4**: Add log aggregation integrations

## Recommendations

### Immediate Implementation (Phase 1)

1. **Add structured logging infrastructure**
   - Use `structlog` library or custom JSON formatter
   - Create logging helper functions
   - Add configuration options

2. **Add structured logging to key operations**
   - Format detection
   - File I/O
   - Pipeline operations
   - Error handling

3. **Documentation**
   - Usage examples
   - Configuration guide
   - Log aggregation integration

### Future Enhancements (Phase 2+)

1. **Expand structured logging**
   - All operations
   - Performance metrics
   - User actions

2. **Log aggregation integrations**
   - CloudWatch
   - Elasticsearch
   - Splunk
   - Custom integrations

3. **Advanced features**
   - Log sampling
   - Log filtering
   - Log rotation
   - Log compression

## Conclusion

A structured logging framework provides essential observability for IterableData operations, enabling better log analysis, monitoring, and integration with log aggregation systems. The recommended approach is to use a hybrid system supporting both JSON (for production) and human-readable (for development) formats.

All implementations maintain backward compatibility by keeping structured logging opt-in and disabled by default. The system integrates with Python's standard logging module and provides flexible configuration options for different use cases.
