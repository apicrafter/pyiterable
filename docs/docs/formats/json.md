# JSON Format

## Description

JSON (JavaScript Object Notation) is a lightweight data interchange format. It supports nested data structures including objects, arrays, strings, numbers, booleans, and null values. The JSON format in Iterable Data expects an array of objects at the root level.

## File Extensions

- `.json` - Standard JSON files

## Implementation Details

### Reading

The JSON implementation:
- Loads the entire JSON file into memory
- Expects the root element to be an array of objects
- Supports optional `tagname` parameter to extract a specific key from the root object
- Iterates over array elements, returning each as a dictionary

### Writing

Writing is not directly supported for JSON format. Use JSONL format for writing individual records.

### Key Features

- **Nested data support**: Preserves complex nested structures
- **Totals support**: Can count total records in the array
- **Tag extraction**: Can extract a specific key from root object before iterating

## Usage

```python
from iterable.helpers.detect import open_iterable

# Basic usage - expects array of objects
source = open_iterable('data.json')
for row in source:
    print(row)
source.close()

# Extract specific key from root object
source = open_iterable('data.json', iterableargs={
    'tagname': 'items'  # Extract 'items' array from root
})
```

## Parameters

- `tagname` (str): Optional key name to extract from root object before iterating

## Limitations

1. **Read-only**: JSON format does not support writing (use JSONL for writing)
2. **Memory usage**: Entire file is loaded into memory
3. **Array requirement**: Root element must be an array of objects
4. **No streaming**: Cannot process very large JSON files efficiently
5. **Single document**: Only supports single JSON document per file

## Compression Support

JSON files can be compressed with all supported codecs:
- GZip (`.json.gz`)
- BZip2 (`.json.bz2`)
- LZMA (`.json.xz`)
- LZ4 (`.json.lz4`)
- ZIP (`.json.zip`)
- Brotli (`.json.br`)
- ZStandard (`.json.zst`)

## DuckDB Engine Support

JSON files are supported by the DuckDB engine:
- Supports compressed JSON (`.gz`, `.zst`)
- Fast querying and filtering
- SQL-like operations

## Related Formats

- [JSONL](jsonl.md) - For writing and streaming JSON records
- [GeoJSON](geojson.md) - For geographic data
