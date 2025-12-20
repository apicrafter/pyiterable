# Apache Hudi Format

## Description

Apache Hudi (Hadoop Upserts Deletes and Incrementals) is a data lake platform that brings stream processing to data lakes. It provides upserts, deletes, and incremental processing capabilities on top of data stored in cloud storage.

## File Extensions

- No specific extension (Hudi tables are directories)

## Implementation Details

### Reading

The Hudi implementation:
- Uses `pyhudi` or `hudi` library for reading
- Requires `table_path` parameter (path to Hudi table)
- Loads table and converts to pandas DataFrame, then to dictionaries
- Requires table path (not stream)

### Writing

Writing is not currently supported for Hudi format.

### Key Features

- **Upserts**: Update and insert operations
- **Deletes**: Delete operations
- **Incremental processing**: Process only changed data
- **Totals support**: Can count total rows
- **Data lake**: Designed for data lake architectures

## Usage

```python
from iterable.helpers.detect import open_iterable

# Reading Hudi table
source = open_iterable('/path/to/hudi/table', iterableargs={
    'table_path': '/path/to/hudi/table'
})
for row in source:
    print(row)
source.close()
```

## Parameters

- `table_path` (str): **Required** - Path to the Hudi table directory

## Limitations

1. **Read-only**: Hudi format does not support writing
2. **Dependency**: Requires `pyhudi` or `hudi` package
3. **Table path required**: Requires path to table directory
4. **Flat data only**: Only supports tabular data
5. **Memory usage**: Entire table may be loaded into memory

## Compression Support

Hudi uses underlying file formats (typically Parquet) which have built-in compression. Hudi tables themselves are directories.

## Use Cases

- **Data lakes**: Managing data in data lakes
- **Upserts**: When you need update/insert operations
- **Streaming**: Real-time data processing
- **Incremental processing**: Processing only changed data

## Related Formats

- [Parquet](parquet.md) - Common underlying format
- [Delta Lake](delta.md) - Similar data lake format
- [Iceberg](iceberg.md) - Another table format
