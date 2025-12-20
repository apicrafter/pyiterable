---
sidebar_position: 5
title: BaseIterable Methods
description: Methods available on all iterable objects
---

# BaseIterable Methods

All iterable objects returned by `open_iterable()` inherit from `BaseIterable` and provide a consistent interface for reading and writing data.

## Reading Methods

### `read(skip_empty: bool = True) -> dict`

Read a single record from the iterable.

**Parameters:**
- `skip_empty` (bool): Skip empty records. Default: `True`

**Returns:** Dictionary representing a single record, or raises `StopIteration` when no more records.

**Example:**
```python
source = open_iterable('data.csv')
record = source.read()
print(record)
source.close()
```

### `read_bulk(num: int = 1000) -> list[dict]`

Read multiple records at once for better performance.

**Parameters:**
- `num` (int): Number of records to read. Default: `1000`

**Returns:** List of dictionaries representing records.

**Example:**
```python
source = open_iterable('data.jsonl')
batch = source.read_bulk(10000)
for record in batch:
    process(record)
source.close()
```

### `__iter__()` and `__next__()`

Iterables support Python's iterator protocol, so you can use them in `for` loops:

```python
source = open_iterable('data.csv')
for row in source:
    print(row)
source.close()
```

## Writing Methods

### `write(record: dict) -> None`

Write a single record to the iterable.

**Parameters:**
- `record` (dict): Dictionary representing a single record

**Example:**
```python
dest = open_iterable('output.jsonl', mode='w')
dest.write({'name': 'John', 'age': 30})
dest.close()
```

### `write_bulk(records: list[dict]) -> None`

Write multiple records at once for better performance.

**Parameters:**
- `records` (list[dict]): List of dictionaries to write

**Example:**
```python
dest = open_iterable('output.jsonl', mode='w')
batch = [
    {'id': 1, 'value': 'a'},
    {'id': 2, 'value': 'b'},
    {'id': 3, 'value': 'c'}
]
dest.write_bulk(batch)
dest.close()
```

## Utility Methods

### `reset() -> None`

Reset the iterator to the beginning of the file. Useful for re-reading files.

**Example:**
```python
source = open_iterable('data.csv')

# Read all records
for row in source:
    print(row)

# Reset and read again
source.reset()
for row in source:
    process(row)

source.close()
```

### `close() -> None`

Close the file handle and release resources. Always call this when done with an iterable.

**Example:**
```python
source = open_iterable('data.csv')
try:
    for row in source:
        process(row)
finally:
    source.close()
```

### `totals() -> int | None`

Get the total number of records in the file. Only available for some formats and engines.

**Returns:** Integer count of records, or `None` if not available.

**Example:**
```python
source = open_iterable('data.csv.gz', engine='duckdb')
total = source.totals()
print(f"Total records: {total}")
source.close()
```

### `has_totals() -> bool`

Check if the iterable supports the `totals()` method.

**Returns:** `True` if totals are available, `False` otherwise.

**Example:**
```python
source = open_iterable('data.csv')
if source.has_totals():
    total = source.totals()
    print(f"Total: {total}")
source.close()
```

## Complete Example

```python
from iterable.helpers.detect import open_iterable

# Reading
source = open_iterable('input.csv')
try:
    # Method 1: Iterator protocol
    for row in source:
        print(row)
    
    # Method 2: Reset and read again
    source.reset()
    record = source.read()
    print(record)
    
    # Method 3: Bulk reading
    source.reset()
    batch = source.read_bulk(1000)
    for record in batch:
        process(record)
finally:
    source.close()

# Writing
dest = open_iterable('output.jsonl', mode='w')
try:
    # Method 1: Single writes
    dest.write({'id': 1, 'value': 'a'})
    dest.write({'id': 2, 'value': 'b'})
    
    # Method 2: Bulk writes
    batch = [
        {'id': 3, 'value': 'c'},
        {'id': 4, 'value': 'd'}
    ]
    dest.write_bulk(batch)
finally:
    dest.close()
```

## Best Practices

1. **Always close files**: Use `close()` or try/finally blocks
2. **Use bulk operations**: `read_bulk()` and `write_bulk()` are faster for large files
3. **Check totals availability**: Use `has_totals()` before calling `totals()`
4. **Reset when needed**: Use `reset()` to re-read files

## Related Topics

- [open_iterable()](/api/open-iterable) - Creating iterables
- [Basic Usage](/getting-started/basic-usage) - Common patterns
- [Data Pipelines](/use-cases/data-pipelines) - Processing pipelines
