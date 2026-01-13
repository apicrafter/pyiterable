---
sidebar_position: 6
title: Capability Matrix
description: Read/write/bulk/totals/streaming support overview by format
---

# Capability Matrix

IterableData supports many formats, but **capabilities vary** (some are read-only; some support `totals()`, bulk ops, or streaming).

This page is an overview to help pick formats and avoid surprises. For format-specific details, see the corresponding page under **Data File Formats**.

## Legend

- **Read**: supports `read()` / iteration
- **Write**: supports `write()` / `write_bulk()`
- **Bulk**: supports `read_bulk()` and/or `write_bulk()` efficiently
- **Totals**: supports `has_totals()` + `totals()`
- **Streaming**: can process large inputs without loading whole file into memory

## Common formats (high usage)

| Format | Read | Write | Bulk | Totals | Streaming | Notes |
|---|:--:|:--:|:--:|:--:|:--:|---|
| CSV/TSV | ✅ | ✅ | ✅ | ✅ | ✅ | Delimiter/encoding detection supported |
| JSONL/NDJSON | ✅ | ✅ | ✅ | ✅ | ✅ | Best for streaming JSON records |
| JSON | ✅ | ✅ | ✅ | ✅ | ❌ | Loads whole document in memory (array JSON) |
| Parquet | ✅ | ✅ | ✅ | ✅ | ⚠️ | Read is streaming in batches; write is batched |
| XML | ✅ | ❌ | ✅ | ❌ | ✅ | Requires `tagname`; iterative parse |
| DuckDB (engine) | ✅ | ❌ | ✅ | ✅ | ⚠️ | Fast scans via DuckDB; limited codec support |
| DuckDB (datatype) | ✅ | ✅ | ✅ | ✅ | ❌ | Database file `.duckdb`/`.ddb` |
| WARC | ✅ | ✅ | ✅ | ❌ | ✅ | Uses `warcio` |

## How to interpret "Streaming"

Some formats (e.g. Parquet) read in record batches but still require internal buffering; others (JSON) load everything. In general:
- Prefer **JSONL/CSV** for truly streamy pipelines.
- Prefer **Parquet** for analytics and columnar storage.

## Programmatic Capability Queries

You can programmatically query format capabilities using the `iterable.helpers.capabilities` module:

```python
from iterable.helpers.capabilities import (
    get_format_capabilities,
    get_capability,
    list_all_capabilities
)

# Get all capabilities for a format
caps = get_format_capabilities("csv")
print(caps)
# {
#   'readable': True,
#   'writable': True,
#   'bulk_read': True,
#   'bulk_write': True,
#   'totals': True,
#   'streaming': True,
#   'flat_only': True,
#   'tables': False,
#   'compression': True,
#   'nested': False
# }

# Query a specific capability
is_writable = get_capability("json", "writable")  # True
has_totals = get_capability("parquet", "totals")  # True
supports_tables = get_capability("xlsx", "tables")  # True

# List capabilities for all formats
all_caps = list_all_capabilities()
for format_id, capabilities in all_caps.items():
    if capabilities.get("tables"):
        print(f"{format_id} supports multiple tables")
```

### Available Capabilities

- **readable**: Format supports reading data (`read()` method)
- **writable**: Format supports writing data (`write()` method)
- **bulk_read**: Format supports bulk reading (`read_bulk()` method)
- **bulk_write**: Format supports bulk writing (`write_bulk()` method)
- **totals**: Format supports row count totals (`has_totals()` returns True)
- **streaming**: Format supports streaming (doesn't load entire file into memory)
- **flat_only**: Format only supports flat (non-nested) data structures
- **tables**: Format supports multiple tables/sheets/datasets (`has_tables()` returns True)
- **compression**: Format supports compression codecs (GZIP, BZIP2, etc.)
- **nested**: Format can preserve nested data structures (opposite of flat_only)

Values are `True` (supported), `False` (not supported), or `None` (unknown/unsupported, e.g., when optional dependencies are missing).


