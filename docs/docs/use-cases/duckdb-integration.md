---
sidebar_position: 4
title: DuckDB Integration
description: High-performance querying with DuckDB engine
---

# DuckDB Integration

Iterable Data includes optional DuckDB engine support for high-performance querying of supported formats. DuckDB provides SQL-like operations and fast analytics on large datasets.

## Overview

The DuckDB engine provides:
- **Fast queries**: SQL-like operations on data files
- **Totals counting**: Efficient row counting
- **Filtering**: Fast filtering and selection
- **Compression support**: Works with compressed files

## Supported Formats

The DuckDB engine supports:
- **Formats**: CSV, JSONL, NDJSON, JSON
- **Compression**: GZIP (`.gz`), ZStandard (`.zst`, `.zstd`)

## Basic Usage

Enable DuckDB engine by specifying `engine='duckdb'`:

```python
from iterable.helpers.detect import open_iterable

# Recommended: Using context manager
# Use DuckDB engine for CSV files
with open_iterable('data.csv.gz', engine='duckdb') as source:
    # DuckDB engine supports totals
    total = source.totals()
    print(f"Total records: {total}")
    
    for row in source:
        print(row)
# File automatically closed
```

## Counting Records

DuckDB engine provides fast row counting:

```python
from iterable.helpers.detect import open_iterable

# Recommended: Using context manager
with open_iterable('data.jsonl.zst', engine='duckdb') as source:
    # Fast total count
    total = source.totals()
    print(f"Total records: {total}")
# File automatically closed
```

## Working with Compressed Files

DuckDB engine handles compressed files efficiently:

```python
from iterable.helpers.detect import open_iterable

# Recommended: Using context manager
# GZIP compressed CSV
with open_iterable('data.csv.gz', engine='duckdb') as source:
    for row in source:
        process(row)

# ZStandard compressed JSONL
with open_iterable('data.jsonl.zst', engine='duckdb') as source:
    for row in source:
        process(row)
# Files automatically closed
```

## Direct DuckDB Queries

You can also use DuckDB directly for more complex queries:

```python
import duckdb

# Connect to DuckDB
conn = duckdb.connect()

# Query JSONL file directly
result = conn.execute("""
    SELECT * 
    FROM 'data.jsonl.zst' 
    WHERE age > 18
    LIMIT 100
""").fetchall()

for row in result:
    print(row)
```

## Querying Nested Data

DuckDB can query nested JSON structures:

```python
import duckdb

conn = duckdb.connect()

# Query nested JSON fields
result = conn.execute("""
    SELECT 
        user.name,
        user.email,
        items[0].price
    FROM 'data.jsonl.zst'
    WHERE user.age > 25
""").fetchall()
```

## Performance Comparison

DuckDB engine is significantly faster for:
- **Large files**: Files with millions of rows
- **Filtering**: Selecting specific records
- **Counting**: Getting total row counts
- **Compressed files**: Efficient decompression

## When to Use DuckDB Engine

Use DuckDB engine when:
- ✅ You need fast queries on large files
- ✅ You're working with CSV or JSONL files
- ✅ You need to count or filter records
- ✅ Files are compressed with GZIP or ZStandard

Use internal engine when:
- ❌ You need formats not supported by DuckDB
- ❌ You need other compression codecs
- ❌ You're working with nested XML or other complex formats

## Installation

DuckDB is an optional dependency. Install it separately:

```bash
pip install duckdb
```

## Example: Wikipedia Query

Query Wikipedia data converted to JSONL:

```python
from iterable.helpers.detect import open_iterable

# Recommended: Using context manager
with open_iterable('wikipedia.jsonl.zst', engine='duckdb') as source:
    # Get total pages
    total = source.totals()
    print(f"Total pages: {total}")
    
    # Iterate and filter
    for page in source:
        if 'Argentina' in page.get('categories', []):
            print(page['title'])
# File automatically closed
```

## Best Practices

1. **Use for large files**: DuckDB shines with files > 100MB
2. **Choose right format**: JSONL is ideal for DuckDB queries
3. **Use compression**: ZStandard provides best balance
4. **Combine with pipelines**: Use DuckDB for queries, pipelines for transformations

## Limitations

- Only supports CSV, JSONL, NDJSON, and JSON formats
- Only supports GZIP and ZStandard compression
- Requires DuckDB to be installed separately
- Not suitable for streaming very large files (use internal engine)

## Related Topics

- [Wikipedia Processing](/use-cases/wikipedia-processing) - Real-world example
- [API Reference: Engines](/api/engines) - Engine documentation
- [Format Conversion](/use-cases/format-conversion) - Convert to DuckDB-compatible formats
