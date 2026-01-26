---
sidebar_position: 5
title: Database Engines
description: Read-only database access as iterable data sources
---

# Database Engines

IterableData supports reading from SQL and NoSQL databases as iterable data sources. Database engines provide streaming, memory-efficient access to database tables and queries, enabling seamless integration with existing IterableData workflows.

## Overview

Database engines allow you to use databases as data sources in IterableData, treating database queries as iterable collections. This enables:

- **Streaming access**: Large result sets are streamed in batches, avoiding memory issues
- **Unified interface**: Database sources work with `open_iterable()`, `convert()`, and `pipeline()` just like file sources
- **Read-only safety**: All database operations are read-only by default, preventing accidental data modification
- **Memory efficiency**: Server-side cursors and batch processing minimize memory usage

## Supported Database Engines

### PostgreSQL

PostgreSQL support is available via the `postgres` or `postgresql` engine.

**Status**: ✅ Available  
**Driver**: `psycopg2`  
**Optional dependency**: `psycopg2-binary`

### MySQL/MariaDB

**Status**: 🚧 Planned  
**Driver**: `pymysql`  
**Optional dependency**: `pymysql`

### Microsoft SQL Server

**Status**: 🚧 Planned  
**Driver**: `pyodbc`  
**Optional dependency**: `pyodbc`

### SQLite

**Status**: 🚧 Planned  
**Driver**: `sqlite3` (standard library)

### MongoDB

**Status**: 🚧 Planned  
**Driver**: `pymongo`  
**Optional dependency**: `pymongo`

### Elasticsearch/OpenSearch

**Status**: 🚧 Planned  
**Driver**: `elasticsearch`  
**Optional dependency**: `elasticsearch`

## Installation

Database engines require optional dependencies. Install them based on your database:

### PostgreSQL

```bash
pip install psycopg2-binary
```

Or install all database dependencies:

```bash
pip install iterabledata[db]
```

Or install SQL databases only:

```bash
pip install iterabledata[db-sql]
```

Or install NoSQL databases only:

```bash
pip install iterabledata[db-nosql]
```

## Basic Usage

### Opening a Database Source

Use `open_iterable()` with a database engine and connection string:

```python
from iterable.helpers.detect import open_iterable

# Connect to PostgreSQL database
with open_iterable(
    "postgresql://user:password@localhost:5432/mydb",
    engine="postgres",
    iterableargs={"query": "users"}
) as source:
    for row in source:
        print(row)
```

### Using with Context Manager

Always use the context manager (`with` statement) to ensure proper connection cleanup:

```python
from iterable.helpers.detect import open_iterable

with open_iterable(
    "postgresql://localhost/mydb",
    engine="postgres",
    iterableargs={"query": "SELECT * FROM users WHERE active = TRUE"}
) as source:
    # Process rows
    for row in source:
        process(row)
# Connection automatically closed
```

## PostgreSQL

### Connection String Format

PostgreSQL connection strings follow the standard PostgreSQL URI format:

```
postgresql://[user[:password]@][host][:port][/database][?param1=value1&...]
```

Examples:

```python
# Basic connection
"postgresql://localhost/mydb"

# With authentication
"postgresql://user:password@localhost:5432/mydb"

# With SSL
"postgresql://user:password@localhost/mydb?sslmode=require"

# Using existing connection object
import psycopg2
conn = psycopg2.connect("postgresql://localhost/mydb")
# Pass connection object directly
with open_iterable(conn, engine="postgres", iterableargs={"query": "users"}) as source:
    ...
```

### Query Parameters

The `iterableargs` parameter accepts database-specific options:

#### `query` (required)

SQL query string or table name:

```python
# Table name (auto-builds SELECT * FROM table)
iterableargs={"query": "users"}

# SQL query string
iterableargs={"query": "SELECT id, name FROM users WHERE age > 18"}

# Complex query
iterableargs={"query": """
    SELECT u.id, u.name, COUNT(o.id) as order_count
    FROM users u
    LEFT JOIN orders o ON u.id = o.user_id
    GROUP BY u.id, u.name
    HAVING COUNT(o.id) > 5
"""}
```

#### `schema` (optional)

Schema name for table references:

```python
iterableargs={
    "query": "users",
    "schema": "public"
}
# Builds: SELECT * FROM "public"."users"
```

#### `columns` (optional)

List of column names for projection (only read specified columns):

```python
iterableargs={
    "query": "users",
    "columns": ["id", "name", "email"]
}
# Builds: SELECT "id", "name", "email" FROM "users"
```

#### `filter` (optional)

WHERE clause fragment (simple filtering):

```python
iterableargs={
    "query": "users",
    "filter": "active = TRUE AND age > 18"
}
# Builds: SELECT * FROM "users" WHERE active = TRUE AND age > 18
```

**Note**: When using a full SQL query string, `columns` and `filter` parameters are ignored.

#### `batch_size` (optional)

Number of rows per batch for streaming (default: 10000):

```python
iterableargs={
    "query": "users",
    "batch_size": 5000
}
```

#### `read_only` (optional)

Use read-only transaction (default: `True`):

```python
iterableargs={
    "query": "users",
    "read_only": True  # Default, prevents accidental writes
}
```

#### `server_side_cursor` (optional)

Use server-side cursor for streaming (default: `True`):

```python
iterableargs={
    "query": "users",
    "server_side_cursor": True  # Recommended for large result sets
}
```

#### `connect_args` (optional)

Additional arguments passed to `psycopg2.connect()`:

```python
iterableargs={
    "query": "users",
    "connect_args": {
        "sslmode": "require",
        "connect_timeout": 10
    }
}
```

### Examples

#### Reading a Table

```python
from iterable.helpers.detect import open_iterable

# Read entire table
with open_iterable(
    "postgresql://localhost/mydb",
    engine="postgres",
    iterableargs={"query": "users"}
) as source:
    for row in source:
        print(row)
```

#### Reading Specific Columns

```python
# Only read id, name, and email columns
with open_iterable(
    "postgresql://localhost/mydb",
    engine="postgres",
    iterableargs={
        "query": "users",
        "columns": ["id", "name", "email"]
    }
) as source:
    for row in source:
        print(row)  # Only contains id, name, email keys
```

#### Filtering Rows

```python
# Filter active users
with open_iterable(
    "postgresql://localhost/mydb",
    engine="postgres",
    iterableargs={
        "query": "users",
        "filter": "active = TRUE AND created_at > '2024-01-01'"
    }
) as source:
    for row in source:
        print(row)
```

#### Complex SQL Query

```python
# Use full SQL for complex queries
with open_iterable(
    "postgresql://localhost/mydb",
    engine="postgres",
    iterableargs={
        "query": """
            SELECT 
                u.id,
                u.name,
                COUNT(o.id) as order_count,
                SUM(o.total) as total_spent
            FROM users u
            LEFT JOIN orders o ON u.id = o.user_id
            WHERE u.active = TRUE
            GROUP BY u.id, u.name
            HAVING COUNT(o.id) > 5
            ORDER BY total_spent DESC
            LIMIT 100
        """
    }
) as source:
    for row in source:
        print(row)
```

#### Schema-Specific Table

```python
# Access table in specific schema
with open_iterable(
    "postgresql://localhost/mydb",
    engine="postgres",
    iterableargs={
        "query": "users",
        "schema": "analytics"
    }
) as source:
    for row in source:
        print(row)
```

### Helper Functions

#### List Tables

The `list_tables()` function lists all tables in a PostgreSQL database:

```python
from iterable.db.postgres import PostgresDriver

# List all tables
tables = PostgresDriver.list_tables("postgresql://localhost/mydb")
for table in tables:
    print(f"{table['schema']}.{table['table']}: {table['row_count']} rows")

# List tables in specific schema
tables = PostgresDriver.list_tables(
    "postgresql://localhost/mydb",
    schema="public"
)
```

Returns a list of dictionaries with keys:
- `schema`: Schema name
- `table`: Table name
- `row_count`: Estimated row count (may be `None` if statistics unavailable)

## Integration with convert()

Database sources work seamlessly with the `convert()` function:

```python
from iterable.convert import convert

# Convert database table to Parquet file
convert(
    fromfile="postgresql://localhost/mydb",
    tofile="users.parquet",
    iterableargs={"engine": "postgres", "query": "users"}
)

# Convert database query to JSONL
convert(
    fromfile="postgresql://localhost/mydb",
    tofile="active_users.jsonl",
    iterableargs={
        "engine": "postgres",
        "query": "users",
        "filter": "active = TRUE"
    }
)
```

## Integration with pipeline()

Database sources can be used in data pipelines:

```python
from iterable.helpers.detect import open_iterable
from iterable.pipeline import Pipeline

# Create pipeline with database source
source = open_iterable(
    "postgresql://localhost/mydb",
    engine="postgres",
    iterableargs={"query": "users"}
)

destination = open_iterable("output.jsonl", mode="w")

pipeline = Pipeline(source, destination)
result = pipeline.run()

print(f"Processed {result.rows_processed} rows")
```

## Integration with DataFrame Bridges

Database sources support DataFrame conversion methods:

```python
from iterable.helpers.detect import open_iterable

with open_iterable(
    "postgresql://localhost/mydb",
    engine="postgres",
    iterableargs={"query": "users"}
) as source:
    # Convert to pandas DataFrame
    df = source.to_pandas()
    
    # Convert to pandas with chunking (for large datasets)
    for chunk_df in source.to_pandas(chunksize=10000):
        process_chunk(chunk_df)
    
    # Convert to Polars DataFrame
    df = source.to_polars()
    
    # Convert to Dask DataFrame
    df = source.to_dask()
```

## Read-Only Behavior and Safety

All database operations are **read-only by default**. This ensures:

- ✅ **Safety**: No accidental data modification
- ✅ **ETL-friendly**: Safe for analytical workloads
- ✅ **Transaction isolation**: Read-only transactions prevent locks

The `read_only` parameter defaults to `True` and sets the database transaction to read-only mode. This prevents:
- `INSERT`, `UPDATE`, `DELETE` statements
- `CREATE`, `DROP`, `ALTER` statements
- Other write operations

**Note**: Write support is planned for future releases.

## Error Handling

Database operations support error handling policies:

```python
# Raise exceptions (default)
iterableargs={
    "query": "users",
    "on_error": "raise"  # Default
}

# Skip errors and continue
iterableargs={
    "query": "users",
    "on_error": "skip"
}

# Warn and continue
iterableargs={
    "query": "users",
    "on_error": "warn"
}
```

### Handling Import Errors

If the required database driver is not installed:

```python
from iterable.helpers.detect import open_iterable

try:
    with open_iterable(
        "postgresql://localhost/mydb",
        engine="postgres",
        iterableargs={"query": "users"}
    ) as source:
        for row in source:
            print(row)
except ImportError as e:
    print(f"Database driver not installed: {e}")
    print("Install with: pip install psycopg2-binary")
except ConnectionError as e:
    print(f"Connection failed: {e}")
except Exception as e:
    print(f"Error: {e}")
```

## Metrics Tracking

Database sources track metrics during iteration:

```python
from iterable.helpers.detect import open_iterable

with open_iterable(
    "postgresql://localhost/mydb",
    engine="postgres",
    iterableargs={"query": "users"}
) as source:
    for row in source:
        process(row)
    
    # Get metrics after iteration
    metrics = source.metrics
    print(f"Rows read: {metrics['rows_read']}")
    print(f"Elapsed time: {metrics['elapsed_seconds']:.2f} seconds")
```

Available metrics:
- `rows_read`: Number of rows read
- `bytes_read`: Bytes read (may be `None` for database sources)
- `elapsed_seconds`: Time elapsed during iteration
- `start_time`: Timestamp when iteration started

## Limitations

### Reset Not Supported

Database queries cannot be reset after iteration starts:

```python
with open_iterable(
    "postgresql://localhost/mydb",
    engine="postgres",
    iterableargs={"query": "users"}
) as source:
    # First iteration works
    for row in source:
        print(row)
    
    # Reset not supported - will raise NotImplementedError
    try:
        source.reset()
    except NotImplementedError:
        # Recreate the iterable if needed
        pass
```

### Write Operations Not Supported

Database write operations (INSERT, UPDATE, DELETE) are not yet supported. This is planned for future releases.

## Troubleshooting

### Database Driver Not Available

**Error**: `Database engine 'postgres' is not available`

**Solution**: Install the required driver:

```bash
pip install psycopg2-binary
```

Or install all database dependencies:

```bash
pip install iterabledata[db]
```

### Connection Failed

**Error**: `Failed to connect to PostgreSQL: ...`

**Solutions**:
- Verify connection string format
- Check database server is running
- Verify network connectivity
- Check authentication credentials
- Review firewall settings

### Query Execution Failed

**Error**: SQL syntax errors or permission issues

**Solutions**:
- Verify SQL query syntax
- Check table/schema names are correct
- Verify database user has SELECT permissions
- Test query directly in database client

### Memory Issues with Large Result Sets

**Solutions**:
- Use `batch_size` parameter to control batch size
- Ensure `server_side_cursor=True` (default)
- Process data in chunks using DataFrame bridges with `chunksize`
- Use filtering to reduce result set size

### Import Errors

**Error**: `psycopg2-binary is required for PostgreSQL support`

**Solution**: Install the missing dependency:

```bash
pip install psycopg2-binary
```

## Related Topics

- [open_iterable()](/api/open-iterable) - Opening database sources
- [convert()](/api/convert) - Converting database data to files
- [pipeline()](/api/pipeline) - Using databases in data pipelines
- [Engines](/api/engines) - File processing engines
- [DataFrame Bridges](/api/dataframe-bridges) - Converting to pandas/polars/dask
