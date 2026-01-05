---
sidebar_position: 1
title: Installation
description: How to install Iterable Data library
---

# Installation

Iterable Data is a Python library for reading and writing data files row by row in a consistent, iterator-based interface. It provides a unified API for working with various data formats (CSV, JSON, Parquet, XML, etc.) similar to `csv.DictReader` but supporting many more formats.

## Requirements

- Python 3.10 or higher

## Install from PyPI

The easiest way to install Iterable Data is using pip:

```bash
pip install iterabledata
```

## Install from Source

To install the latest development version from source:

```bash
git clone https://github.com/datenoio/iterabledata.git
cd pyiterable
pip install .
```

## Optional Dependencies

Some formats require additional dependencies. Install them as needed:

```bash
# For Parquet support
pip install pyarrow

# For ORC support
pip install pyorc

# For Excel support
pip install openpyxl xlrd

# For DBF support
pip install dbfread

# For DuckDB engine
pip install duckdb

# For other formats, see individual format documentation
```

## Verify Installation

You can verify the installation by importing the library:

```python
from iterable.helpers.detect import open_iterable

# If this runs without errors, installation was successful
print("Iterable Data installed successfully!")
```

## Next Steps

- [Quick Start Guide](/getting-started/quick-start) - Get up and running quickly
- [Basic Usage](/getting-started/basic-usage) - Learn common patterns
- [Supported Formats](/formats/) - See all available formats
