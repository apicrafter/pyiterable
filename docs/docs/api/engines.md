---
sidebar_position: 4
title: Engines
description: Processing engines available in Iterable Data
---

# Engines

Iterable Data supports multiple processing engines, each optimized for different use cases.

## Internal Engine (Default)

The internal engine uses pure Python implementations for all formats. It supports all file types and compression codecs.

### Features

- ✅ Supports all 80+ formats
- ✅ Supports all compression codecs
- ✅ Works with nested data structures
- ✅ No additional dependencies required

### Usage

```python
from iterable.helpers.detect import open_iterable

# Internal engine is the default
# Recommended: Using context manager
with open_iterable('data.csv.gz', engine='internal') as source:
    for row in source:
        print(row)
# or simply (internal is default)
with open_iterable('data.csv.gz') as source:
    for row in source:
        print(row)
```

### When to Use

- Working with formats not supported by DuckDB
- Need other compression codecs (BZip2, LZMA, LZ4, etc.)
- Processing nested data structures
- General-purpose data processing

## DuckDB Engine

The DuckDB engine provides high-performance querying capabilities using the DuckDB database engine.

### Features

- ⚡ Fast queries on large files
- ⚡ Efficient row counting
- ⚡ SQL-like operations
- ⚡ Supports compressed files

### Supported Formats

- **Formats**: CSV, JSONL, NDJSON, JSON
- **Compression**: GZIP (`.gz`), ZStandard (`.zst`, `.zstd`)

### Installation

DuckDB is an optional dependency:

```bash
pip install duckdb
```

### Usage

```python
from iterable.helpers.detect import open_iterable

# Recommended: Using context manager
# Use DuckDB engine
with open_iterable('data.csv.gz', engine='duckdb') as source:
    # Fast row counting
    total = source.totals()
    print(f"Total records: {total}")
    
    for row in source:
        print(row)
# File automatically closed
```

### When to Use

- ✅ Large files (100MB+)
- ✅ Need fast row counting
- ✅ Working with CSV or JSONL files
- ✅ Files compressed with GZIP or ZStandard
- ✅ Need SQL-like querying capabilities

### Limitations

- ❌ Only supports CSV, JSONL, NDJSON, and JSON formats
- ❌ Only supports GZIP and ZStandard compression
- ❌ Requires DuckDB to be installed
- ❌ Not suitable for very large streaming files

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

## Performance Comparison

| Operation | Internal Engine | DuckDB Engine |
|-----------|----------------|---------------|
| Small files (< 10MB) | Fast | Fast |
| Large files (> 100MB) | Moderate | Very Fast |
| Row counting | Slow | Very Fast |
| Filtering | Moderate | Very Fast |
| Format support | All formats | CSV/JSONL only |
| Compression | All codecs | GZIP/ZStandard only |

## Choosing an Engine

**Use Internal Engine when:**
- Working with formats not supported by DuckDB
- Need other compression codecs
- Processing nested data structures
- General-purpose data processing

**Use DuckDB Engine when:**
- Working with large CSV or JSONL files
- Need fast row counting
- Need SQL-like querying
- Files are compressed with GZIP or ZStandard

## Error Handling

```python
from iterable.helpers.detect import open_iterable

try:
    # Using DuckDB engine with error handling
    with open_iterable('data.csv.gz', engine='duckdb') as source:
        total = source.totals()
        for row in source:
            process(row)
except ImportError:
    print("DuckDB not installed. Install with: pip install duckdb")
except FileNotFoundError:
    print("File not found")
except Exception as e:
    print(f"Error with DuckDB engine: {e}")
    # Fallback to internal engine
    with open_iterable('data.csv.gz', engine='internal') as source:
        for row in source:
            process(row)
```

## Troubleshooting

### DuckDB Engine Not Available

- **Install DuckDB**: `pip install duckdb`
- **Check format**: DuckDB only supports CSV, JSONL, NDJSON, and JSON
- **Check compression**: Only GZIP and ZStandard compression supported
- **Fallback**: Use `engine='internal'` as fallback

### Performance Issues

- **Large files**: DuckDB engine is faster for files > 100MB
- **Small files**: Internal engine may be faster for small files
- **Format support**: Use internal engine for unsupported formats
- **Compression**: DuckDB engine works best with GZIP and ZStandard

## Related Topics

- [DuckDB Integration Use Case](/use-cases/duckdb-integration)
- [open_iterable()](/api/open-iterable) - Opening files with engines
- [Supported Formats](/formats/)
