---
sidebar_position: 4
title: Observability
description: Progress tracking, metrics, and logging for conversions and pipelines
---

# Observability

IterableData provides comprehensive observability features for monitoring progress and performance of data conversions and pipelines. This includes progress callbacks, built-in progress bars, and standardized metrics objects.

## Overview

Observability features enable you to:
- Track progress in real-time during long-running operations
- Access structured metrics for programmatic workflows
- Integrate with monitoring systems and CI/CD pipelines
- Monitor performance and throughput

## Progress Callbacks

Progress callbacks allow you to receive real-time updates during conversion or pipeline execution.

### Conversion Progress Callbacks

```python
from iterable.convert.core import convert

def progress_callback(stats):
    """Called periodically during conversion"""
    print(f"Rows read: {stats['rows_read']}, "
          f"Rows written: {stats['rows_written']}, "
          f"Elapsed: {stats['elapsed']:.2f}s")
    
    if stats['estimated_total']:
        percent = (stats['rows_read'] / stats['estimated_total']) * 100
        print(f"Progress: {percent:.1f}%")

result = convert(
    'input.csv',
    'output.parquet',
    progress=progress_callback
)
```

The progress callback receives a dictionary with:
- `rows_read`: Number of rows read from source
- `rows_written`: Number of rows written to destination
- `elapsed`: Elapsed time in seconds
- `estimated_total`: Estimated total rows (if available, otherwise `None`)

### Pipeline Progress Callbacks

```python
from iterable.helpers.detect import open_iterable
from iterable.pipeline.core import pipeline

def progress_callback(stats):
    """Called periodically during pipeline execution"""
    print(f"Rows processed: {stats['rows_processed']}, "
          f"Elapsed: {stats['elapsed']:.2f}s")
    
    if stats.get('throughput'):
        print(f"Throughput: {stats['throughput']:.0f} rows/second")

with open_iterable('input.csv') as source:
    with open_iterable('output.jsonl', mode='w') as destination:
        def process_func(record, state):
            return record
        
        result = pipeline(
            source=source,
            destination=destination,
            process_func=process_func,
            progress=progress_callback
        )
```

The progress callback receives a dictionary with:
- `rows_processed`: Number of rows processed
- `elapsed`: Elapsed time in seconds
- `throughput`: Rows per second (if calculable)
- `rec_count`: Total record count
- `exceptions`: Number of exceptions encountered
- `nulls`: Number of null results

## Built-in Progress Bars

The `convert()` function supports built-in progress bars using `tqdm` when available.

```python
from iterable.convert.core import convert

# Show progress bar during conversion
result = convert(
    'input.jsonl.gz',
    'output.parquet',
    show_progress=True
)
```

The progress bar:
- Shows rows processed and estimated time remaining
- Works automatically with `tqdm` if installed
- Gracefully falls back if `tqdm` is not available (no error)
- Respects the `silent` parameter (no progress bar if `silent=True`)

## Conversion Metrics

The `convert()` function returns a `ConversionResult` object with structured metrics.

### ConversionResult

```python
from iterable.convert.core import convert
from iterable.types import ConversionResult

result: ConversionResult = convert('input.csv', 'output.jsonl')

# Access metrics
print(f"Rows in: {result.rows_in}")
print(f"Rows out: {result.rows_out}")
print(f"Elapsed: {result.elapsed_seconds:.2f}s")
print(f"Bytes read: {result.bytes_read}")
print(f"Bytes written: {result.bytes_written}")

# Check for errors
if result.errors:
    print(f"Encountered {len(result.errors)} errors")
    for error in result.errors:
        print(f"  - {error}")
```

### ConversionResult Attributes

- `rows_in` (int): Total number of rows read from source
- `rows_out` (int): Total number of rows written to destination
- `elapsed_seconds` (float): Total elapsed time in seconds
- `bytes_read` (int | None): Number of bytes read (if available)
- `bytes_written` (int | None): Number of bytes written (if available)
- `errors` (list[Exception]): List of errors encountered (empty if none)

## Pipeline Metrics

The `pipeline()` function returns a `PipelineResult` object with structured metrics.

### PipelineResult

```python
from iterable.helpers.detect import open_iterable
from iterable.pipeline.core import pipeline
from iterable.types import PipelineResult

with open_iterable('input.csv') as source:
    with open_iterable('output.jsonl', mode='w') as destination:
        def process_func(record, state):
            return record
        
        result: PipelineResult = pipeline(
            source=source,
            destination=destination,
            process_func=process_func
        )
        
        # Access metrics using attributes
        print(f"Rows processed: {result.rows_processed}")
        print(f"Elapsed: {result.elapsed_seconds:.2f}s")
        print(f"Throughput: {result.throughput:.0f} rows/second")
        print(f"Exceptions: {result.exceptions}")
        
        # Or use dictionary-style access (backward compatible)
        print(f"Record count: {result['rec_count']}")
        print(f"Duration: {result['duration']:.2f}s")
```

### PipelineResult Attributes

- `rows_processed` (int): Total number of rows processed
- `elapsed_seconds` (float): Total elapsed time in seconds
- `exceptions` (int): Number of exceptions encountered
- `nulls` (int): Number of null results
- `rec_count` (int): Total record count (alias for rows_processed)
- `time_start` (float | None): Start time timestamp
- `time_end` (float | None): End time timestamp
- `duration` (float | None): Duration in seconds (alias for elapsed_seconds)
- `throughput` (float | None): Rows per second (property, calculated)

### Backward Compatibility

`PipelineResult` supports both attribute access and dictionary-style access for backward compatibility:

```python
result = pipeline(...)

# New style (attribute access)
rows = result.rows_processed

# Old style (dictionary access) - still works
rows = result["rec_count"]
```

## Integration Examples

### CI/CD Integration

```python
from iterable.convert.core import convert

result = convert('input.csv', 'output.parquet')

# Log metrics for CI/CD
print(f"::set-output name=rows_in::{result.rows_in}")
print(f"::set-output name=rows_out::{result.rows_out}")
print(f"::set-output name=elapsed::{result.elapsed_seconds}")

# Fail build if errors occurred
if result.errors:
    raise Exception(f"Conversion failed with {len(result.errors)} errors")
```

### Monitoring Integration

```python
from iterable.convert.core import convert
import time

def send_metrics(stats):
    """Send metrics to monitoring system"""
    # Example: Send to Prometheus, Datadog, etc.
    metrics.gauge('conversion.rows_read', stats['rows_read'])
    metrics.gauge('conversion.rows_written', stats['rows_written'])
    metrics.gauge('conversion.elapsed', stats['elapsed'])

result = convert(
    'input.jsonl',
    'output.parquet',
    progress=send_metrics
)

# Send final metrics
metrics.gauge('conversion.total_rows', result.rows_out)
metrics.gauge('conversion.total_time', result.elapsed_seconds)
```

### Custom Progress Reporting

```python
from iterable.convert.core import convert
from datetime import datetime

class ProgressReporter:
    def __init__(self):
        self.start_time = datetime.now()
        self.updates = []
    
    def __call__(self, stats):
        """Progress callback"""
        update = {
            'timestamp': datetime.now(),
            'rows_read': stats['rows_read'],
            'rows_written': stats['rows_written'],
            'elapsed': stats['elapsed']
        }
        self.updates.append(update)
        
        # Print formatted progress
        elapsed_str = f"{stats['elapsed']:.1f}s"
        print(f"[{elapsed_str}] {stats['rows_read']} read, "
              f"{stats['rows_written']} written")

reporter = ProgressReporter()
result = convert('input.csv', 'output.jsonl', progress=reporter)

# Analyze progress updates
print(f"Total updates: {len(reporter.updates)}")
print(f"Average rows per second: "
      f"{result.rows_out / result.elapsed_seconds:.0f}")
```

## Error Handling in Callbacks

Progress callbacks are designed to be non-blocking. If a callback raises an exception, it's logged but doesn't stop the conversion or pipeline:

```python
def progress_callback(stats):
    # This error won't stop the conversion
    if stats['rows_read'] > 1000:
        raise ValueError("Test error")

result = convert('input.csv', 'output.jsonl', progress=progress_callback)
# Conversion continues even if callback raises an exception
```

## Best Practices

1. **Use progress callbacks for long operations**: Progress callbacks are most useful for conversions or pipelines that take significant time
2. **Keep callbacks lightweight**: Avoid heavy operations in progress callbacks to maintain performance
3. **Handle errors gracefully**: Progress callbacks should handle errors internally to avoid disrupting the main operation
4. **Use metrics for automation**: Access `ConversionResult` and `PipelineResult` metrics programmatically for CI/CD and monitoring
5. **Combine with logging**: Use progress callbacks alongside logging for comprehensive observability

## Related Topics

- [convert()](/api/convert) - Conversion function with progress support
- [pipeline()](/api/pipeline) - Pipeline function with progress support
- [Format Conversion Use Case](/use-cases/format-conversion)
- [Data Pipelines Use Case](/use-cases/data-pipelines)
