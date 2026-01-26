---
sidebar_position: 11
title: Filter Operations
description: Expression-based filtering, regex search, and query support
---

# Filter Operations

The `iterable.ops.filter` module provides functions for filtering rows using expressions, regular expressions, and SQL-like queries.

## Overview

Filter operations help you select specific rows from datasets:
- **Expression-based filtering** with safe evaluation
- **Regex pattern matching** across fields
- **SQL-like queries** for complex filtering
- **DuckDB pushdown** for performance optimization

## Functions

### `filter_expr()`

Filter rows using a boolean expression.

Supports field access with backticks, comparisons, and boolean operators.
Uses DuckDB pushdown for performance when available.

```python
from iterable.ops import filter as f

# Filter with simple expression
for row in f.filter_expr("data.csv", "`status` == 'active'"):
    print(row)

# Filter with complex expression
for row in f.filter_expr("data.csv", "`status` == 'active' and `price` > 100"):
    print(row)
```

**Parameters:**
- `iterable`: An iterable of row dictionaries, or a file path/stream
- `expression`: Boolean expression string
  - Field access: Use backticks (e.g., `` `status` ``, `` `price` ``)
  - Comparisons: `==`, `!=`, `<`, `>`, `<=`, `>=`
  - Boolean operators: `and`, `or`, `not`
  - String literals: `'value'` or `"value"`
  - Numeric literals: `100`, `3.14`
- `engine`: Optional engine to use ('duckdb' for optimization)

**Returns:** Iterator of row dictionaries matching the expression

**Example Expressions:**
```python
# Simple equality
"`status` == 'active'"

# Numeric comparison
"`price` > 100"

# Multiple conditions
"`status` == 'active' and `price` > 100"

# OR condition
"`status` == 'active' or `status` == 'pending'"

# Not condition
"not `deleted`"

# Complex expression
"(`status` == 'active' and `price` > 100) or `priority` == 'high'"
```

### `search()`

Filter rows using regular expression pattern matching.

Searches for the pattern in specified fields (or all fields if None).
Returns rows where the pattern matches in any of the searched fields.

```python
from iterable.ops import filter as f

# Search across all fields
for row in f.search("logs.jsonl", pattern="error|warning"):
    print(row)

# Search in specific fields
for row in f.search("data.csv", pattern=r"\d{3}-\d{3}-\d{4}", fields=["phone"]):
    print(row)

# Case-insensitive search
for row in f.search("data.csv", pattern="ERROR", ignore_case=True):
    print(row)
```

**Parameters:**
- `iterable`: An iterable of row dictionaries, or a file path/stream
- `pattern`: Regular expression pattern to search for
- `fields`: List of field names to search (None for all string fields)
- `ignore_case`: Whether to perform case-insensitive search (default: False)

**Returns:** Iterator of row dictionaries where pattern matches

**Example Patterns:**
```python
# Find errors or warnings
pattern="error|warning"

# Find phone numbers
pattern=r"\d{3}-\d{3}-\d{4}"

# Find email addresses
pattern=r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

# Find words starting with "test"
pattern=r"\btest\w*"
```

### `query_mistql()`

Filter and select rows using a basic SQL-like query (MistQL-inspired).

Supports SELECT and WHERE clauses with basic SQL syntax.

```python
from iterable.ops import filter as f

# Simple WHERE query
for row in f.query_mistql("data.csv", "SELECT * WHERE status = 'active'"):
    print(row)

# Select specific fields
for row in f.query_mistql("data.csv", "SELECT id, name WHERE price > 100"):
    print(row)
```

**Parameters:**
- `iterable`: An iterable of row dictionaries, or a file path/stream
- `query`: SQL-like query string
  - Format: `SELECT field1, field2, ... WHERE condition` or `SELECT * WHERE condition`
  - Use `SELECT *` to return all fields
  - WHERE clause supports same expressions as `filter_expr()`
- `engine`: Optional engine to use ('duckdb' for optimization)

**Returns:** Iterator of row dictionaries matching the query

**Example Queries:**
```python
# Select all rows matching condition
"SELECT * WHERE status = 'active'"

# Select specific fields
"SELECT id, name, email WHERE status = 'active'"

# Complex WHERE clause
"SELECT * WHERE status = 'active' AND price > 100"

# OR condition
"SELECT * WHERE status = 'active' OR priority = 'high'"
```

## Examples

### Basic Filtering

```python
from iterable.ops import filter as f

# Filter active items
active_items = list(f.filter_expr("products.csv", "`status` == 'active'"))

# Filter by price range
expensive = list(f.filter_expr("products.csv", "`price` > 100 and `price` < 1000"))

# Filter by date (if date fields exist)
recent = list(f.filter_expr("orders.csv", "`date` >= '2024-01-01'"))
```

### Regex Search

```python
from iterable.ops import filter as f

# Find all error messages
errors = list(f.search("logs.jsonl", pattern="error|exception|failure"))

# Find phone numbers in contact fields
phones = list(f.search(
    "contacts.csv",
    pattern=r"\d{3}-\d{3}-\d{4}",
    fields=["phone", "mobile", "fax"]
))

# Case-insensitive search for status
status_rows = list(f.search("data.csv", pattern="active|pending", ignore_case=True))
```

### Complex Queries

```python
from iterable.ops import filter as f

# Select specific fields with condition
result = list(f.query_mistql(
    "users.csv",
    "SELECT id, name, email WHERE status = 'active' AND age >= 18"
))

# Multiple conditions
result = list(f.query_mistql(
    "orders.csv",
    "SELECT * WHERE status = 'completed' AND total > 100 AND date >= '2024-01-01'"
))
```

### Combining with Other Operations

```python
from iterable.ops import filter as f, transform, stats

# Filter, then transform
filtered = f.filter_expr("data.csv", "`status` == 'active'")
sampled = transform.sample_rows(filtered, n=1000)
deduped = transform.deduplicate(sampled, keys=["email"])

# Process filtered data
for row in deduped:
    process(row)

# Filter and compute statistics
active_rows = f.filter_expr("data.csv", "`status` == 'active'")
summary = stats.compute(active_rows)
```

### DuckDB Optimization

```python
from iterable.ops import filter as f

# Use DuckDB for fast filtering on large files
try:
    filtered = f.filter_expr(
        "large_file.csv",
        "`status` == 'active' and `price` > 100",
        engine="duckdb"
    )
    for row in filtered:
        print(row)
except Exception:
    # Falls back to Python evaluation if DuckDB unavailable
    filtered = f.filter_expr(
        "large_file.csv",
        "`status` == 'active' and `price` > 100"
    )
```

## Expression Syntax

### Field Access

Use backticks to reference fields:
```python
"`field_name` == 'value'"
"`price` > 100"
"`user.name` == 'John'"  # Nested fields (basic support)
```

### Comparison Operators

- `==` - Equal to
- `!=` - Not equal to
- `<` - Less than
- `<=` - Less than or equal
- `>` - Greater than
- `>=` - Greater than or equal
- `in` - Membership test (e.g., `` `status` in ['active', 'pending'] ``)
- `not in` - Not in membership test

### Boolean Operators

- `and` - Logical AND
- `or` - Logical OR
- `not` - Logical NOT

### Literals

- **Strings**: `'value'` or `"value"`
- **Numbers**: `100`, `3.14`, `-5`
- **Booleans**: `True`, `False`
- **None**: `None`

## Safety

The expression evaluator is designed to be safe:
- **No arbitrary code execution** - Only safe operations are allowed
- **Restricted context** - No access to built-in functions or modules
- **Field access only** - Can only access row data, not external resources
- **Error handling** - Invalid expressions raise clear error messages

## Performance Notes

- **`filter_expr()`**: Use `engine="duckdb"` for 10-100x speedup on large CSV/JSONL/JSON/Parquet files
- **`search()`**: Efficient streaming implementation, but may be slower than expression filtering
- **`query_mistql()`**: Uses DuckDB when available for optimal performance

## Integration with DuckDB

When DuckDB engine is available and `engine="duckdb"` is specified:
- Expressions are converted to SQL WHERE clauses
- Filtering happens at the database level
- Only matching rows are read from disk
- Significant performance improvement for large datasets

## Limitations

- **Nested field access**: Basic support, complex nesting may not work
- **Complex expressions**: Very complex expressions may not convert to SQL
- **Type coercion**: Automatic type conversion is limited
- **Query language**: MistQL support is basic, not full SQL

For advanced querying, consider using DuckDB directly with custom SQL queries.
