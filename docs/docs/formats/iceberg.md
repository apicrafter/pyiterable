# Apache Iceberg Format

## Description

Apache Iceberg is an open table format for huge analytic tables. It provides schema evolution, hidden partitioning, and time travel capabilities. Iceberg tables are managed through catalogs and store metadata separately from data.

## File Extensions

- No specific extension (Iceberg tables are managed through catalogs)

## Implementation Details

### Reading

The Iceberg implementation:
- Uses `pyiceberg` library for reading
- Requires `catalog_name` and `table_name` parameters
- Loads table from catalog
- Scans table and converts to dictionaries
- Supports catalog properties file

### Writing

Writing is not currently supported for Iceberg format.

### Key Features

- **Catalog-based**: Tables managed through catalogs
- **Schema evolution**: Handles schema changes
- **Hidden partitioning**: Automatic partitioning
- **Time travel**: Access historical snapshots
- **Totals support**: Can count total rows

## Usage

```python
from iterable.helpers.detect import open_iterable

# Reading Iceberg table
source = open_iterable('catalog.properties', iterableargs={
    'catalog_name': 'my_catalog',
    'table_name': 'my_table'
})
for row in source:
    print(row)
source.close()
```

## Parameters

- `catalog_name` (str): **Required** - Name of the Iceberg catalog
- `table_name` (str): **Required** - Name of the table in the catalog
- `filename` (str): Optional path to catalog properties file

## Limitations

1. **Read-only**: Iceberg format does not support writing
2. **pyiceberg dependency**: Requires `pyiceberg` package
3. **Catalog required**: Must have catalog and table names
4. **Flat data only**: Only supports tabular data
5. **Configuration**: Requires proper catalog configuration

## Compression Support

Iceberg uses underlying file formats (typically Parquet) which have built-in compression. Iceberg tables themselves are managed through catalogs.

## Use Cases

- **Data lakes**: Managing large analytic tables
- **Schema evolution**: When schemas change frequently
- **Partitioning**: Automatic data partitioning
- **Time travel**: Accessing historical data versions

## Related Formats

- [Parquet](parquet.md) - Common underlying format
- [Delta Lake](delta.md) - Similar table format
- [Hudi](hudi.md) - Another data lake format
