---
sidebar_position: 2
title: convert()
description: Convert data between different file formats
---

# convert()

The `convert()` function converts data between different file formats with automatic format detection, schema extraction, and efficient batch processing.

## Signature

```python
convert(
    fromfile: str,
    tofile: str,
    iterableargs: dict = {},
    scan_limit: int = 1000,
    batch_size: int = 50000,
    silent: bool = True,
    is_flatten: bool = False,
    use_totals: bool = False
) -> None
```

## Parameters

### `fromfile` (str, required)

Path to the source file. Format and compression are automatically detected from the filename.

### `tofile` (str, required)

Path to the destination file. Format and compression are automatically detected from the filename.

### `iterableargs` (dict, optional)

Format-specific arguments for reading the source file. Common options:
- `delimiter` - Field delimiter for CSV files
- `encoding` - File encoding for text files
- `tagname` - XML tag name
- `page` - Excel sheet/page

### `scan_limit` (int, optional)

Number of records to scan for schema detection when converting to flat formats (CSV, Parquet, etc.). Default: `1000`.

### `batch_size` (int, optional)

Number of records to process in each batch. Larger batches improve performance but use more memory. Default: `50000`.

### `silent` (bool, optional)

If `False`, shows progress bars during conversion. Default: `True`.

### `is_flatten` (bool, optional)

If `True`, flattens nested structures when converting to flat formats. Nested dictionaries become dot-notation keys (e.g., `user.name`). Default: `False`.

### `use_totals` (bool, optional)

If `True`, uses total count for progress tracking (if available). Default: `False`.

## Examples

### Simple Conversion

```python
from iterable.convert.core import convert

# Convert JSONL to Parquet (handles compression automatically)
convert('input.jsonl.gz', 'output.parquet')
```

### Conversion with Options

```python
from iterable.convert.core import convert

# Convert CSV with custom delimiter
convert(
    'input.csv.xz',
    'output.jsonl.zst',
    iterableargs={'delimiter': ';', 'encoding': 'utf-8'},
    batch_size=10000
)
```

### Flattening Nested Structures

```python
from iterable.convert.core import convert

# Convert JSONL to CSV with flattening
convert(
    'input.jsonl',
    'output.csv',
    is_flatten=True,
    batch_size=50000
)
```

### With Progress Tracking

```python
from iterable.convert.core import convert

# Show progress during conversion
convert(
    'input.parquet',
    'output.jsonl.zst',
    silent=False,  # Show progress bars
    use_totals=True  # Use total count if available
)
```

## How It Works

1. **Format Detection**: Automatically detects input and output formats from file extensions
2. **Schema Extraction**: For flat output formats, scans the first `scan_limit` records to extract schema
3. **Batch Processing**: Processes data in batches of `batch_size` records for efficiency
4. **Compression Handling**: Automatically handles compression for both input and output files

## Supported Conversions

You can convert between any supported formats:
- Tabular formats: CSV, TSV, PSV, Excel, Parquet, ORC
- JSON formats: JSON, JSONL, GeoJSON
- Binary formats: BSON, MessagePack, Avro, Arrow
- Other formats: XML, YAML, and 80+ more

## Error Handling

```python
from iterable.convert.core import convert

try:
    # Convert with error handling
    convert('input.jsonl.gz', 'output.parquet')
except FileNotFoundError:
    print("Input file not found")
except ValueError as e:
    print(f"Conversion error: {e}")
    # Common causes: unsupported format, schema mismatch
except Exception as e:
    print(f"Unexpected error during conversion: {e}")
```

### Common Errors

- **FileNotFoundError**: Input file doesn't exist or path is incorrect
- **ValueError**: Format not supported, schema mismatch, or invalid parameters
- **MemoryError**: Batch size too large or file too large for available memory
- **PermissionError**: Insufficient permissions to read input or write output file

## Limitations

- **Flat formats**: When converting to flat formats (CSV, Parquet), nested structures must be flattened (use `is_flatten=True`)
- **Schema detection**: For flat formats, schema is extracted from the first `scan_limit` records - ensure first records are representative
- **Memory usage**: Large `batch_size` values use more memory - adjust based on available memory
- **Format compatibility**: Some format conversions may lose data (e.g., nested structures to CSV)

## Troubleshooting

### Conversion Fails or Hangs

- **Check file formats**: Verify both input and output formats are supported
- **Check file size**: Very large files may require more memory or smaller batch sizes
- **Check permissions**: Ensure read access to input file and write access to output directory
- **Monitor memory**: Use smaller `batch_size` if running out of memory

### Data Loss or Incorrect Results

- **Nested data**: Use `is_flatten=True` when converting nested formats to flat formats
- **Schema issues**: Increase `scan_limit` if first records don't represent full schema
- **Encoding issues**: Specify encoding in `iterableargs` for text files
- **Type conversion**: Some formats may not preserve all data types exactly

### Performance Issues

- **Batch size**: Adjust `batch_size` - larger is faster but uses more memory
- **Compression**: Use compressed formats for better I/O performance
- **Progress tracking**: Set `silent=False` to monitor conversion progress

## Best Practices

1. **Choose appropriate batch size**: 10,000-50,000 records works well for most cases
2. **Use flattening carefully**: Only flatten when converting to flat formats
3. **Monitor progress**: Set `silent=False` for long conversions
4. **Use compression**: Compressed formats save space and often process faster
5. **Test with small files**: Test conversion logic on small samples before processing large files
6. **Handle errors**: Always wrap conversions in try/except blocks

## Related Topics

- [Format Conversion Use Case](/use-cases/format-conversion)
- [open_iterable()](/api/open-iterable) - Manual conversion
- [Supported Formats](/formats/)
