---
sidebar_position: 4
title: Troubleshooting
description: Common issues and solutions when using Iterable Data
---

# Troubleshooting

This guide helps you resolve common issues when using Iterable Data.

## General Issues

### File Not Found Errors

**Error**: `FileNotFoundError: [Errno 2] No such file or directory`

**Solutions**:
- Verify the file path is correct (use absolute paths if relative paths don't work)
- Check file permissions - ensure you have read access
- For compressed files, ensure the file extension matches the compression type
- Use `os.path.exists()` to verify file exists before opening

```python
import os
from iterable.helpers.detect import open_iterable

file_path = 'data.csv.gz'
if os.path.exists(file_path):
    with open_iterable(file_path) as source:
        for row in source:
            print(row)
else:
    print(f"File not found: {file_path}")
```

### Encoding Errors

**Error**: `UnicodeDecodeError: 'utf-8' codec can't decode byte...`

**Solutions**:
- Specify encoding explicitly in `iterableargs`
- Try common encodings: `latin-1`, `cp1252`, `iso-8859-1`
- Use encoding detection utilities

```python
from iterable.helpers.detect import open_iterable
from iterable.helpers.utils import detect_encoding

# Detect encoding first
encoding_info = detect_encoding('data.csv')
print(f"Detected encoding: {encoding_info['encoding']}")

# Use detected encoding
with open_iterable('data.csv', iterableargs={
    'encoding': encoding_info['encoding']
}) as source:
    for row in source:
        print(row)
```

### Memory Issues

**Error**: `MemoryError` or system runs out of memory

**Solutions**:
- Process files in smaller batches
- Use `read_bulk()` with smaller batch sizes
- Use streaming/iterative processing instead of loading all data
- Use compressed formats to reduce memory usage
- Consider using DuckDB engine for large CSV/JSONL files

```python
from iterable.helpers.detect import open_iterable

# Process in smaller batches
with open_iterable('large_file.csv') as source:
    batch = []
    for row in source:
        batch.append(row)
        if len(batch) >= 1000:  # Smaller batch size
            process_batch(batch)
            batch = []  # Clear batch to free memory
```

### Format Detection Issues

**Error**: Wrong format detected or format not recognized

**Solutions**:
- Check file extension matches the actual format
- Use `detect_file_type()` to verify format detection
- Specify format explicitly if auto-detection fails
- Check file is not corrupted

```python
from iterable.helpers.detect import detect_file_type

result = detect_file_type('data.csv.gz')
print(f"Detected type: {result['datatype']}")
print(f"Detected codec: {result['codec']}")
print(f"Success: {result['success']}")
```

## Format-Specific Issues

### CSV Format Issues

**Issue**: Wrong delimiter detected or parsing errors

**Solutions**:
- Use `autodetect=True` to automatically detect delimiter
- Specify delimiter explicitly: `iterableargs={'delimiter': ';'}`
- Check for special characters or encoding issues
- Verify CSV file has proper quoting for fields containing delimiters

```python
from iterable.helpers.detect import open_iterable

# Auto-detect delimiter
with open_iterable('data.csv', iterableargs={
    'autodetect': True
}) as source:
    for row in source:
        print(row)
```

**Issue**: Missing headers or wrong column names

**Solutions**:
- Provide `keys` parameter when reading files without headers
- Check first row of CSV file to verify headers
- Use `keys` parameter to specify column names explicitly

```python
with open_iterable('data.csv', iterableargs={
    'keys': ['col1', 'col2', 'col3']  # Specify column names
}) as source:
    for row in source:
        print(row)
```

### JSON/JSONL Format Issues

**Issue**: `JSONDecodeError` - Invalid JSON on a line

**Solutions**:
- Check for malformed JSON in the file
- Verify encoding is correct (should be UTF-8)
- Use line-by-line processing to identify problematic lines
- Validate JSON before processing

```python
import json
from iterable.helpers.detect import open_iterable

try:
    with open_iterable('data.jsonl') as source:
        for i, row in enumerate(source):
            # Process row
            pass
except json.JSONDecodeError as e:
    print(f"Invalid JSON on line {e.lineno if hasattr(e, 'lineno') else 'unknown'}")
```

**Issue**: Nested data not preserved

**Solutions**:
- JSON/JSONL formats preserve nested structures by default
- Check that you're not flattening data unintentionally
- Verify output format supports nested data (not CSV/Parquet without flattening)

### Parquet Format Issues

**Issue**: Schema mismatch errors

**Solutions**:
- Use `adapt_schema=True` to automatically adapt schema
- Ensure all records have consistent structure
- Provide `keys` parameter if schema is known
- Check first batch of records for schema consistency

```python
with open_iterable('output.parquet', mode='w', iterableargs={
    'adapt_schema': True,  # Automatically adapt schema
    'batch_size': 10000
}) as dest:
    dest.write_bulk(records)
```

**Issue**: Missing PyArrow dependency

**Solutions**:
- Install PyArrow: `pip install pyarrow`
- Verify installation: `python -c "import pyarrow; print(pyarrow.__version__)"`

### XML Format Issues

**Issue**: "tagname parameter is required"

**Solutions**:
- Always provide `tagname` parameter when reading XML files
- Check XML structure to identify correct tag name
- Use XML viewer to inspect file structure

```python
with open_iterable('data.xml', iterableargs={
    'tagname': 'item'  # Required parameter
}) as source:
    for row in source:
        print(row)
```

**Issue**: Memory errors with large XML files

**Solutions**:
- XML uses iterative parsing but may still use significant memory
- Process in chunks if possible
- Consider converting to a more memory-efficient format first

### Database Format Issues (SQLite/DuckDB)

**Issue**: "Table not found" error

**Solutions**:
- Check table name spelling
- Omit `table` parameter to use first table
- List tables in database to verify table exists
- Ensure write mode is used when creating new tables

**Issue**: "File path required" error

**Solutions**:
- Database formats require file paths, not streams
- Use absolute paths if relative paths don't work
- Ensure file path is a string, not a file object

## Performance Issues

### Slow Reading/Writing

**Solutions**:
- Use bulk operations (`write_bulk()`, `read_bulk()`) instead of individual operations
- Increase batch sizes (10,000-50,000 records)
- Use compressed formats for better I/O performance
- Use DuckDB engine for CSV/JSONL files when appropriate
- Process files in parallel if possible

```python
# Slow: Individual writes
with open_iterable('output.jsonl', mode='w') as dest:
    for record in records:
        dest.write(record)  # Slow

# Fast: Bulk writes
with open_iterable('output.jsonl', mode='w') as dest:
    dest.write_bulk(records)  # Much faster
```

### Slow Format Conversion

**Solutions**:
- Adjust `batch_size` parameter in `convert()` function
- Use appropriate compression for output format
- Monitor progress with `silent=False`
- Consider using pipeline for more control

```python
from iterable.convert.core import convert

convert(
    'input.jsonl.gz',
    'output.parquet',
    batch_size=50000,  # Larger batch size
    silent=False  # Monitor progress
)
```

## Engine-Specific Issues

### DuckDB Engine Issues

**Issue**: DuckDB not available or ImportError

**Solutions**:
- Install DuckDB: `pip install duckdb`
- Verify installation
- Fallback to internal engine if DuckDB not available

```python
try:
    with open_iterable('data.csv.gz', engine='duckdb') as source:
        for row in source:
            process(row)
except ImportError:
    # Fallback to internal engine
    with open_iterable('data.csv.gz', engine='internal') as source:
        for row in source:
            process(row)
```

**Issue**: Format not supported by DuckDB engine

**Solutions**:
- DuckDB only supports CSV, JSONL, NDJSON, and JSON
- Use internal engine for other formats
- Check compression - only GZIP and ZStandard supported

## Pipeline Issues

### Records Not Being Written

**Solutions**:
- Ensure `process_func` returns a dictionary (not `None`)
- Check `skip_nulls` parameter - if `True`, `None` returns are skipped
- Verify destination file is opened in write mode
- Enable `debug=True` to see exceptions

```python
from iterable.pipeline.core import pipeline

def transform_record(record, state):
    # Must return dict or None
    if record.get('valid', False):
        return record  # Return dict to write
    return None  # Return None to skip

pipeline(
    source=source,
    destination=destination,
    process_func=transform_record,
    skip_nulls=True,  # Skip None returns
    debug=True  # See errors
)
```

### Pipeline Runs Slowly

**Solutions**:
- Optimize `process_func` - avoid expensive operations
- Reduce `trigger_on` frequency
- Use bulk operations in destination if possible
- Profile your code to identify bottlenecks

## Getting Help

If you're still experiencing issues:

1. **Check the documentation**: Review format-specific documentation for your format
2. **Check error messages**: Error messages often contain helpful information
3. **Enable debug mode**: Use `debug=True` in pipeline or check verbose output
4. **Test with small files**: Reproduce issue with small sample files
5. **Check dependencies**: Verify all required packages are installed
6. **File issues**: Report bugs or ask questions on GitHub

## Common Error Messages Reference

| Error Message | Common Cause | Solution |
|---------------|--------------|----------|
| `FileNotFoundError` | File doesn't exist | Check file path |
| `UnicodeDecodeError` | Wrong encoding | Specify encoding explicitly |
| `JSONDecodeError` | Invalid JSON | Check file format |
| `ValueError: tagname parameter is required` | Missing XML tag name | Provide `tagname` parameter |
| `ImportError: No module named 'duckdb'` | DuckDB not installed | Install with `pip install duckdb` |
| `MemoryError` | File too large | Use smaller batches or streaming |
| `AttributeError` | Missing key in record | Check record structure before accessing |

## Related Topics

- [Basic Usage](/getting-started/basic-usage) - Common usage patterns
- [API Reference](/api/open-iterable) - Full API documentation
- [Format Documentation](/formats/) - Format-specific documentation

