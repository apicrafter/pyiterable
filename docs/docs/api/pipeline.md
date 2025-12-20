---
sidebar_position: 3
title: pipeline()
description: Build data processing pipelines with transformation and progress tracking
---

# pipeline()

The `pipeline()` function provides a framework for processing data with transformation functions, progress tracking, and state management.

## Signature

```python
pipeline(
    source: BaseIterable,
    destination: BaseIterable = None,
    process_func: Callable[[dict, dict], dict] = None,
    trigger_func: Callable[[dict, dict], None] = None,
    trigger_on: int = 1000,
    final_func: Callable[[dict, dict], None] = None,
    reset_iterables: bool = True,
    skip_nulls: bool = True,
    start_state: dict = {},
    debug: bool = False
) -> None
```

## Parameters

### `source` (BaseIterable, required)

Input iterable object (from `open_iterable()`).

### `destination` (BaseIterable, optional)

Output iterable object (from `open_iterable()`). If `None`, records are processed but not written.

### `process_func` (Callable, optional)

Function to transform each record. Signature:
```python
def process_func(record: dict, state: dict) -> dict:
    # Transform record
    return transformed_record  # or None to skip
```

### `trigger_func` (Callable, optional)

Function called periodically for progress tracking. Signature:
```python
def trigger_func(stats: dict, state: dict) -> None:
    # Report progress
    pass
```

### `trigger_on` (int, optional)

Number of records between `trigger_func` calls. Default: `1000`.

### `final_func` (Callable, optional)

Function called when processing completes. Signature:
```python
def final_func(stats: dict, state: dict) -> None:
    # Report final statistics
    pass
```

### `reset_iterables` (bool, optional)

If `True`, resets iterables before processing. Default: `True`.

### `skip_nulls` (bool, optional)

If `True`, skips records where `process_func` returns `None`. Default: `True`.

### `start_state` (dict, optional)

Initial state dictionary passed to all callback functions. Default: `{}`.

### `debug` (bool, optional)

Enable debug mode for additional logging. Default: `False`.

## Statistics Dictionary

The `stats` dictionary passed to callbacks contains:
- `rec_count` - Number of records processed
- `nulls` - Number of null/skipped records
- `exceptions` - Number of exceptions encountered
- `time_start` - Processing start time
- `duration` - Processing duration (in final_func)

## Examples

### Basic Pipeline

```python
from iterable.helpers.detect import open_iterable
from iterable.pipeline.core import pipeline

# Recommended: Using context managers
with open_iterable('input.parquet') as source:
    with open_iterable('output.jsonl.xz', mode='w') as destination:
        def transform_record(record, state):
            """Transform each record"""
            return {'id': record.get('id'), 'value': record.get('value')}
        
        pipeline(
            source=source,
            destination=destination,
            process_func=transform_record
        )
# Files automatically closed
```

### Pipeline with Progress Tracking

```python
from iterable.helpers.detect import open_iterable
from iterable.pipeline.core import pipeline

# Recommended: Using context managers
with open_iterable('input.parquet') as source:
    with open_iterable('output.jsonl.xz', mode='w') as destination:
        def transform_record(record, state):
            return record
        
        def progress_callback(stats, state):
            print(f"Processed {stats['rec_count']} records")
        
        def final_callback(stats, state):
            print(f"Total: {stats['rec_count']} records")
            print(f"Duration: {stats['duration']:.2f}s")
        
        pipeline(
            source=source,
            destination=destination,
            process_func=transform_record,
            trigger_func=progress_callback,
            trigger_on=1000,
            final_func=final_callback
        )
# Files automatically closed
```

### Pipeline with State

```python
from iterable.helpers.detect import open_iterable
from iterable.pipeline.core import pipeline

# Recommended: Using context managers
with open_iterable('input.jsonl') as source:
    with open_iterable('output.jsonl', mode='w') as destination:
        def transform_with_state(record, state):
            state['count'] = state.get('count', 0) + 1
            record['sequence'] = state['count']
            return record
        
        def final_callback(stats, state):
            print(f"Processed {state['count']} records")
        
        pipeline(
            source=source,
            destination=destination,
            process_func=transform_with_state,
            final_func=final_callback,
            start_state={'count': 0}
        )
# Files automatically closed
```

### Filtering Records

```python
from iterable.helpers.detect import open_iterable
from iterable.pipeline.core import pipeline

# Recommended: Using context managers
with open_iterable('input.csv') as source:
    with open_iterable('output.csv', mode='w') as destination:
        def filter_records(record, state):
            """Only process records that meet criteria"""
            if record.get('age', 0) >= 18:
                return record
            return None  # Skip this record
        
        pipeline(
            source=source,
            destination=destination,
            process_func=filter_records,
            skip_nulls=True
        )
# Files automatically closed
```

## Error Handling

```python
from iterable.helpers.detect import open_iterable
from iterable.pipeline.core import pipeline

try:
    with open_iterable('input.csv') as source:
        with open_iterable('output.csv', mode='w') as destination:
            def transform_record(record, state):
                # Include error handling in transform function
                try:
                    # Your transformation logic
                    return transformed_record
                except Exception as e:
                    # Log error and skip record
                    state['errors'] = state.get('errors', 0) + 1
                    return None  # Skip this record
            
            pipeline(
                source=source,
                destination=destination,
                process_func=transform_record,
                debug=True  # Enable debug mode for more error details
            )
except Exception as e:
    print(f"Pipeline error: {e}")
```

### Common Errors

- **AttributeError**: Check that records have expected keys before accessing
- **TypeError**: Ensure `process_func` returns a dictionary or `None`
- **FileNotFoundError**: Verify input file exists and output directory is writable
- **MemoryError**: Process in smaller batches or reduce `trigger_on` frequency

## Troubleshooting

### Pipeline Runs Slowly

- **Check `process_func`**: Ensure transformation logic is efficient
- **Reduce `trigger_on` frequency**: Less frequent callbacks improve performance
- **Use bulk operations**: Consider using `write_bulk()` in destination if supported
- **Profile your code**: Identify bottlenecks in transformation logic

### Records Not Being Written

- **Check return value**: `process_func` must return a dictionary (not `None`) to write
- **Check `skip_nulls`**: If `True`, `None` returns are skipped
- **Check destination**: Verify destination file is opened in write mode
- **Check errors**: Enable `debug=True` to see exceptions

### State Not Persisting

- **State is per-pipeline**: State is reset for each pipeline run
- **Use `start_state`**: Initialize state with `start_state` parameter
- **State is mutable**: Modify state dictionary directly (it's passed by reference)

## Best Practices

1. **Use context managers**: Prefer `with` statements for automatic file cleanup
2. **Handle errors**: Include error handling in `process_func` to skip bad records
3. **Use state wisely**: Accumulate statistics or lookup data in state
4. **Monitor progress**: Use `trigger_func` for long-running pipelines
5. **Filter early**: Return `None` to skip records you don't need
6. **Enable debug mode**: Use `debug=True` during development to catch errors early

## Related Topics

- [Data Pipelines Use Case](/use-cases/data-pipelines)
- [open_iterable()](/api/open-iterable) - Opening files
- [BaseIterable Methods](/api/base-iterable)
