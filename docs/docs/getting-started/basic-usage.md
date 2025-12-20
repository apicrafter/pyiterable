---
sidebar_position: 3
title: Basic Usage
description: Common usage patterns and best practices
---

# Basic Usage

This guide covers common usage patterns and best practices for working with Iterable Data.

## Reading Compressed Files

Iterable Data seamlessly handles compressed files:

```python
from iterable.helpers.detect import open_iterable

# Recommended: Using context manager (automatic cleanup)
# Read compressed CSV file (supports .gz, .bz2, .xz, .zst, .lz4, .br, .snappy, .lzo)
with open_iterable('data.csv.xz') as source:
    n = 0
    for row in source:
        n += 1
        # Process row data
        if n % 1000 == 0:
            print(f'Processed {n} rows')
# File automatically closed
```

## Format Detection and Encoding

You can detect file types and encoding before opening:

```python
from iterable.helpers.detect import open_iterable, detect_file_type
from iterable.helpers.utils import detect_encoding, detect_delimiter

# Detect file type and compression
result = detect_file_type('data.csv.gz')
print(f"Type: {result['datatype']}, Codec: {result['codec']}")

# Detect encoding for CSV files
encoding_info = detect_encoding('data.csv')
print(f"Encoding: {encoding_info['encoding']}, Confidence: {encoding_info['confidence']}")

# Detect delimiter for CSV files
delimiter = detect_delimiter('data.csv', encoding=encoding_info['encoding'])

# Open with detected settings
source = open_iterable('data.csv', iterableargs={
    'encoding': encoding_info['encoding'],
    'delimiter': delimiter
})
```

## Working with Excel Files

Excel files can be read with sheet selection:

```python
from iterable.helpers.detect import open_iterable

# Recommended: Using context manager
# Read Excel file (specify sheet or page)
with open_iterable('data.xlsx', iterableargs={'page': 0}) as xls_file:
    for row in xls_file:
        print(row)
# File automatically closed

# Read specific sheet in XLSX
with open_iterable('data.xlsx', iterableargs={'page': 'Sheet2'}) as xlsx_file:
    for row in xlsx_file:
        print(row)
```

## XML Processing

XML files require specifying the tag name to iterate over:

```python
from iterable.helpers.detect import open_iterable

# Recommended: Using context manager
# Parse XML with specific tag name
with open_iterable(
    'data.xml',
    iterableargs={
        'tagname': 'book',
        'prefix_strip': True  # Strip XML namespace prefixes
    }
) as xml_file:
    for item in xml_file:
        print(item)
# File automatically closed
```

## Bulk Operations

For better performance with large files, use bulk operations:

```python
from iterable.helpers.detect import open_iterable

# Recommended: Using context managers
with open_iterable('input.jsonl') as source:
    with open_iterable('output.parquet', mode='w') as destination:
        # Read and write in batches for better performance
        batch = []
        for row in source:
            batch.append(row)
            if len(batch) >= 10000:
                destination.write_bulk(batch)
                batch = []
        
        # Write remaining records
        if batch:
            destination.write_bulk(batch)
# Files automatically closed
```

## Using Context Managers

Iterable Data supports Python's context manager protocol (`with` statements) for automatic resource cleanup:

```python
from iterable.helpers.detect import open_iterable

# Recommended: Using context manager (automatic cleanup)
with open_iterable('data.csv') as source:
    for row in source:
        process(row)
# File automatically closed when exiting the block

# Alternative: Manual close (still supported)
source = open_iterable('data.csv')
try:
    for row in source:
        process(row)
finally:
    source.close()
```

## Error Handling

Always handle potential errors when working with files:

```python
from iterable.helpers.detect import open_iterable

# Recommended: Using context manager with error handling
try:
    with open_iterable('data.csv') as source:
        for row in source:
            process(row)
except FileNotFoundError:
    print("File not found")
except UnicodeDecodeError:
    print("Encoding error - try specifying encoding explicitly")
    # Retry with explicit encoding
    with open_iterable('data.csv', iterableargs={'encoding': 'latin-1'}) as source:
        for row in source:
            process(row)
except Exception as e:
    print(f"Error processing file: {e}")
```

## Best Practices

1. **Use context managers**: Prefer `with` statements for automatic resource cleanup
2. **Use bulk operations**: For large files, use `write_bulk()` and `read_bulk()` for better performance
3. **Handle encoding**: For text files, let the library auto-detect encoding or specify it explicitly
4. **Use compression**: Compressed files save space and often process faster
5. **Check format support**: Verify that your format supports read/write operations before use
6. **Handle errors**: Always wrap file operations in try/except blocks for production code
7. **Batch processing**: Process large files in batches (10,000-50,000 records) for optimal performance

## Next Steps

- [Use Cases](/use-cases/format-conversion) - See real-world examples
- [API Reference](/api/open-iterable) - Explore the full API
- [Supported Formats](/formats/) - Learn about specific formats
