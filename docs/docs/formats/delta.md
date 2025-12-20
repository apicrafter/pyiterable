# Delta Lake Format

## Description

Delta Lake is an open-source storage layer that brings ACID transactions to Apache Spark and big data workloads. It provides data versioning, time travel, and schema evolution capabilities on top of Parquet files.

## File Extensions

- No specific extension (Delta tables are directories)

## Implementation Details

### Reading

The Delta Lake implementation:
- Uses `deltalake` library for reading
- Requires path to Delta table directory (not a file)
- Converts Delta table to PyArrow table
- Iterates over records as dictionaries
- Requires file path (not stream)

### Writing

Writing is not currently supported for Delta Lake format.

### Key Features

- **ACID transactions**: Transactional guarantees
- **Time travel**: Access historical versions of data
- **Schema evolution**: Handles schema changes
- **Totals support**: Can count total rows
- **Parquet-based**: Built on Parquet format

## Usage

```python
from iterable.helpers.detect import open_iterable

# Reading Delta table (path to table directory)
source = open_iterable('/path/to/delta/table')
for row in source:
    print(row)
source.close()
```

## Parameters

No specific parameters required. The filename should be the path to the Delta table directory.

## Limitations

1. **Read-only**: Delta Lake format does not support writing
2. **deltalake dependency**: Requires `deltalake` package
3. **Directory path required**: Requires path to table directory, not a file
4. **Flat data only**: Only supports tabular data
5. **Memory usage**: Entire table may be loaded into memory

## Compression Support

Delta Lake uses Parquet files internally, which have built-in compression. Delta tables themselves are directories, so file-level compression doesn't apply directly.

## Use Cases

- **Data lakes**: Managing data in data lakes
- **ETL pipelines**: Transactional data processing
- **Data versioning**: When you need data versioning
- **Schema evolution**: When schemas change over time

## Related Formats

- [Parquet](parquet.md) - Base format used by Delta Lake
- [Iceberg](iceberg.md) - Similar table format
- [Hudi](hudi.md) - Another data lake format
