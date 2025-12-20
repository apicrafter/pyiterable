---
sidebar_position: 2
title: Quick Start
description: Get started with Iterable Data in minutes
---

# Quick Start

This guide will help you get started with Iterable Data quickly. In just a few minutes, you'll be reading and writing data files in various formats.

## Basic Reading

The simplest way to use Iterable Data is with the `open_iterable()` function, which automatically detects the file format and compression:

```python
from iterable.helpers.detect import open_iterable

# Automatically detects format and compression
source = open_iterable('data.csv.gz')
for row in source:
    print(row)
    # Process your data here
source.close()
```

The function automatically:
- Detects the file format from the extension (`.csv`, `.jsonl`, `.parquet`, etc.)
- Detects compression codec (`.gz`, `.bz2`, `.xz`, `.zst`, etc.)
- Opens the file with appropriate settings

## Writing Data

Writing data is just as simple:

```python
from iterable.helpers.detect import open_iterable

# Write compressed JSONL file
dest = open_iterable('output.jsonl.zst', mode='w')
for item in my_data:
    dest.write(item)
dest.close()
```

## Reading Different Formats

Iterable Data supports 80+ formats. Here are some common examples:

```python
from iterable.helpers.detect import open_iterable

# Read JSONL file
jsonl_file = open_iterable('data.jsonl')
for row in jsonl_file:
    print(row)
jsonl_file.close()

# Read Parquet file
parquet_file = open_iterable('data.parquet')
for row in parquet_file:
    print(row)
parquet_file.close()

# Read XML file (specify tag name)
xml_file = open_iterable('data.xml', iterableargs={'tagname': 'item'})
for row in xml_file:
    print(row)
xml_file.close()

# Read Excel file
xlsx_file = open_iterable('data.xlsx')
for row in xlsx_file:
    print(row)
xlsx_file.close()
```

## Format Conversion

Convert between formats easily:

```python
from iterable.helpers.detect import open_iterable
from iterable.convert.core import convert

# Simple format conversion
convert('input.jsonl.gz', 'output.parquet')
```

## What's Next?

- [Basic Usage](/getting-started/basic-usage) - Learn more advanced patterns
- [Use Cases](/use-cases/format-conversion) - See real-world examples
- [API Reference](/api/open-iterable) - Explore the full API
