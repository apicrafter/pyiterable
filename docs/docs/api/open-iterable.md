---
sidebar_position: 1
title: open_iterable()
description: Main entry point for opening data files
---

# open_iterable()

The `open_iterable()` function is the main entry point for reading and writing data files. It automatically detects the file format and compression codec from the filename.

## Signature

```python
open_iterable(
    filename: str,
    mode: str = 'r',
    engine: str = 'internal',
    codecargs: dict = {},
    iterableargs: dict = {}
) -> BaseIterable
```

## Parameters

### `filename` (str, required)

Path to the file to open. The function automatically detects:
- **Format**: From file extension (`.csv`, `.jsonl`, `.parquet`, etc.) or content analysis (magic numbers and heuristics)
- **Compression**: From file extension (`.gz`, `.bz2`, `.xz`, `.zst`, etc.)

**Format Detection Strategy:**
1. **Primary**: Filename extension detection (fast and reliable)
2. **Fallback**: Content-based detection when extension is missing or unknown
   - **Binary formats**: Magic number detection (e.g., `PAR1` for Parquet, `ORC` for ORC)
   - **Text formats**: Content heuristics (e.g., JSON structure, CSV delimiter patterns)
3. Works with files without extensions, streams, and files with incorrect extensions

### `mode` (str, optional)

File mode:
- `'r'` - Read mode (default)
- `'w'` - Write mode

### `engine` (str, optional)

Processing engine:
- `'internal'` - Internal Python engine (default, supports all formats)
- `'duckdb'` - DuckDB engine (faster for CSV/JSONL, limited format support)

### `codecargs` (dict, optional)

Arguments passed to the compression codec initialization. Most codecs don't require additional arguments.

### `iterableargs` (dict, optional)

Format-specific arguments. Common options:
- `delimiter` - Field delimiter for CSV/TSV files (default: `,`)
- `encoding` - File encoding for text files (default: auto-detected)
- `tagname` - XML tag name to iterate over (required for XML files)
- `page` - Sheet/page number or name for Excel files
- `keys` - Column names for files without headers
- `autodetect` - Automatically detect delimiter (CSV files)

## Returns

Returns a `BaseIterable` object that can be iterated over or used for writing.

## Examples

### Basic Reading

```python
from iterable.helpers.detect import open_iterable

# Automatically detects format and compression
source = open_iterable('data.csv.gz')
for row in source:
    print(row)
source.close()
```

### Writing Data

```python
from iterable.helpers.detect import open_iterable

dest = open_iterable('output.jsonl.zst', mode='w')
dest.write({'name': 'John', 'age': 30})
dest.close()
```

### With Format-Specific Options

```python
from iterable.helpers.detect import open_iterable

# CSV with custom delimiter
source = open_iterable('data.csv', iterableargs={
    'delimiter': ';',
    'encoding': 'utf-8'
})

# XML with tag name
source = open_iterable('data.xml', iterableargs={
    'tagname': 'item'
})

# Excel with specific sheet
source = open_iterable('data.xlsx', iterableargs={
    'page': 'Sheet2'
})
```

### Using DuckDB Engine

```python
from iterable.helpers.detect import open_iterable

# Use DuckDB for fast queries
source = open_iterable('data.csv.gz', engine='duckdb')
total = source.totals()
for row in source:
    print(row)
source.close()
```

## Supported Formats

The function supports 80+ formats. See [Supported Formats](/formats/) for a complete list.

## Supported Compression Codecs

- GZip (`.gz`)
- BZip2 (`.bz2`)
- LZMA (`.xz`, `.lzma`)
- LZ4 (`.lz4`)
- ZIP (`.zip`)
- Brotli (`.br`)
- ZStandard (`.zst`, `.zstd`)
- Snappy (`.snappy`, `.sz`)
- LZO (`.lzo`, `.lzop`)

## Error Handling

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
except ValueError as e:
    print(f"Format error: {e}")
    # Common causes: missing required parameters, unsupported format
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Common Exceptions

The library uses a comprehensive exception hierarchy for better error handling:

**Base Exception:**
- **IterableDataError**: Base exception for all library errors

**Format Exceptions:**
- **FormatError**: Base exception for format-related errors
- **FormatNotSupportedError**: Format is not supported or dependencies are missing
- **FormatDetectionError**: Could not detect file format from filename or content
- **FormatParseError**: Format parsing failed (malformed data)

**Codec Exceptions:**
- **CodecError**: Base exception for compression codec errors
- **CodecNotSupportedError**: Compression codec is not supported
- **CodecDecompressionError**: Decompression failed
- **CodecCompressionError**: Compression failed

**Read/Write Exceptions:**
- **ReadError**: Error during data reading operations
- **WriteError**: Error during data writing operations
- **StreamingNotSupportedError**: Format doesn't support streaming

**Resource Exceptions:**
- **ResourceError**: Base exception for resource management errors
- **StreamNotSeekableError**: Stream doesn't support seeking (required for `reset()`)
- **ResourceLeakError**: Resource leak detected

**Standard Exceptions:**
- **FileNotFoundError**: File doesn't exist or path is incorrect
- **UnicodeDecodeError**: Encoding issue - specify encoding explicitly
- **ImportError**: Missing optional dependency (e.g., `duckdb`, `pyarrow`)
- **PermissionError**: Insufficient file permissions

**Example Error Handling:**
```python
from iterable.helpers.detect import open_iterable
from iterable.exceptions import (
    FormatDetectionError,
    FormatNotSupportedError,
    CodecError
)

try:
    with open_iterable('data.unknown') as source:
        for row in source:
            process(row)
except FormatDetectionError as e:
    print(f"Could not detect format: {e.reason}")
    # Try with explicit format or check file content
except FormatNotSupportedError as e:
    print(f"Format '{e.format_id}' not supported: {e.reason}")
    # Install missing dependencies or use different format
except CodecError as e:
    print(f"Compression error with {e.codec_name}: {e}")
    # Check file integrity or try different codec
except FileNotFoundError:
    print("File not found")
```

## Troubleshooting

### File Not Opening

- **Check file path**: Verify file exists and path is correct
- **Check format**: Ensure file extension matches format
- **Check permissions**: Verify read/write permissions
- **Check dependencies**: Some formats require optional packages

### Wrong Format Detected

- **Check extension**: File extension is the primary method for format detection
- **Content-based detection**: The library automatically uses content analysis (magic numbers/heuristics) when extension detection fails
- **Files without extensions**: Content-based detection works for files without extensions or with incorrect extensions
- **Use `detect_file_type()`**: Verify format detection before opening
- **Specify format explicitly**: Some formats may need explicit parameters

### Performance Issues

- **Use context managers**: Automatic resource cleanup
- **Use bulk operations**: `write_bulk()` and `read_bulk()` for better performance
- **Use appropriate engine**: DuckDB engine for large CSV/JSONL files
- **Use compression**: Compressed formats often process faster

## Related Functions

- [`detect_file_type()`](#) - Detect file type and compression
- [`convert()`](/api/convert) - Convert between formats

## See Also

- [Quick Start Guide](/getting-started/quick-start)
- [Basic Usage](/getting-started/basic-usage)
- [BaseIterable Methods](/api/base-iterable)
- [Exception Hierarchy](/api/exceptions) - Comprehensive exception reference
