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

## How to interpret “Streaming”

Some formats (e.g. Parquet) read in record batches but still require internal buffering; others (JSON) load everything. In general:\n+
- Prefer **JSONL/CSV** for truly streamy pipelines.\n+- Prefer **Parquet** for analytics and columnar storage.\n+


