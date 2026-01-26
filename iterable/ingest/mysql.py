"""
MySQL database ingestor.
"""

from __future__ import annotations

import collections.abc
import time
from typing import Any, Callable

try:
    import mysql.connector
except ImportError:
    mysql = None

from ..types import Row
from .core import IngestionResult


def ingest(
    iterable: collections.abc.Iterable[Row],
    db_url: str,
    table: str,
    mode: str = "insert",
    upsert_key: str | list[str] | None = None,
    batch: int = 5000,
    create_table: bool = False,
    progress: Callable[[dict[str, Any]], None] | None = None,
) -> IngestionResult:
    """
    Ingest data into MySQL database.

    Args:
        iterable: An iterable of row dictionaries
        db_url: MySQL connection URL (mysql://user:pass@host:port/dbname)
        table: Table name
        mode: Ingestion mode - "insert" or "upsert"
        upsert_key: Field name(s) for upsert matching
        batch: Batch size for bulk inserts
        create_table: Whether to auto-create table
        progress: Optional progress callback

    Returns:
        IngestionResult with statistics
    """
    if mysql is None:
        raise ImportError("mysql-connector-python is required for MySQL ingestion. Install with: pip install mysql-connector-python")

    start_time = time.time()
    rows_processed = 0
    rows_inserted = 0
    rows_updated = 0
    errors: list[str] = []

    try:
        # Parse connection URL (simplified)
        # mysql://user:pass@host:port/dbname
        from urllib.parse import urlparse
        parsed = urlparse(db_url.replace("mysql://", "http://"))
        conn = mysql.connector.connect(
            host=parsed.hostname or "localhost",
            port=parsed.port or 3306,
            user=parsed.username,
            password=parsed.password,
            database=parsed.path.lstrip("/") if parsed.path else None,
        )
        cursor = conn.cursor()

        # Get first row to determine schema
        first_row = next(iter(iterable), None)
        if first_row is None:
            return IngestionResult(elapsed_seconds=time.time() - start_time)

        # Create table if needed
        if create_table:
            columns = list(first_row.keys())
            columns_def = ", ".join([f"{col} TEXT" for col in columns])
            create_query = f"CREATE TABLE IF NOT EXISTS {table} ({columns_def})"
            cursor.execute(create_query)
            conn.commit()

        # Prepare batch
        batch_rows: list[Row] = [first_row]
        rows_processed = 1

        # Process remaining rows
        for row in iterable:
            batch_rows.append(row)
            rows_processed += 1

            if len(batch_rows) >= batch:
                _insert_batch(cursor, conn, table, batch_rows, mode, upsert_key)
                rows_inserted += len(batch_rows)
                batch_rows = []

                if progress:
                    progress({"rows_processed": rows_processed, "rows_inserted": rows_inserted})

        # Insert remaining batch
        if batch_rows:
            _insert_batch(cursor, conn, table, batch_rows, mode, upsert_key)
            rows_inserted += len(batch_rows)

        conn.commit()
        cursor.close()
        conn.close()

    except Exception as e:
        errors.append(str(e))

    return IngestionResult(
        rows_processed=rows_processed,
        rows_inserted=rows_inserted,
        rows_updated=rows_updated,
        errors=errors,
        elapsed_seconds=time.time() - start_time,
    )


def _insert_batch(
    cursor: Any,
    conn: Any,
    table: str,
    rows: list[Row],
    mode: str,
    upsert_key: str | list[str] | None,
):
    """Insert a batch of rows into MySQL."""
    if not rows:
        return

    columns = list(rows[0].keys())
    columns_str = ", ".join(columns)
    placeholders = ", ".join(["%s" for _ in columns])

    if mode == "upsert" and upsert_key:
        # MySQL UPSERT (INSERT ... ON DUPLICATE KEY UPDATE)
        if isinstance(upsert_key, str):
            upsert_key = [upsert_key]
        update_cols = [col for col in columns if col not in upsert_key]
        update_clause = ", ".join([f"{col} = VALUES({col})" for col in update_cols])
        query = f"""INSERT INTO {table} ({columns_str}) 
                    VALUES ({placeholders})
                    ON DUPLICATE KEY UPDATE {update_clause}"""
    else:
        query = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"

    values = [[row.get(col) for col in columns] for row in rows]
    cursor.executemany(query, values)
    conn.commit()
