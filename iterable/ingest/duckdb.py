"""
DuckDB database ingestor.
"""

from __future__ import annotations

import collections.abc
import time
from typing import Any, Callable

try:
    import duckdb
except ImportError:
    duckdb = None

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
    Ingest data into DuckDB database.

    Args:
        iterable: An iterable of row dictionaries
        db_url: DuckDB database file path (or ":memory:" for in-memory)
        table: Table name
        mode: Ingestion mode - "insert" or "upsert"
        upsert_key: Field name(s) for upsert matching
        batch: Batch size for bulk inserts
        create_table: Whether to auto-create table
        progress: Optional progress callback

    Returns:
        IngestionResult with statistics
    """
    if duckdb is None:
        raise ImportError("DuckDB is required for DuckDB ingestion. Install with: pip install duckdb")

    start_time = time.time()
    rows_processed = 0
    rows_inserted = 0
    rows_updated = 0
    errors: list[str] = []

    try:
        conn = duckdb.connect(db_url)

        # Get first row to determine schema
        first_row = next(iter(iterable), None)
        if first_row is None:
            return IngestionResult(elapsed_seconds=time.time() - start_time)

        # Create table if needed
        if create_table:
            columns = list(first_row.keys())
            # Infer types from first row
            def _duckdb_type_from_value(v):
                if isinstance(v, bool):
                    return "BOOLEAN"
                if isinstance(v, int):
                    return "BIGINT"
                if isinstance(v, float):
                    return "DOUBLE"
                return "VARCHAR"

            columns_def = ", ".join([f"{col} {_duckdb_type_from_value(first_row.get(col))}" for col in columns])
            create_query = f"CREATE TABLE IF NOT EXISTS {table} ({columns_def})"
            conn.execute(create_query)

        # Prepare batch
        batch_rows: list[Row] = [first_row]
        rows_processed = 1

        # Process remaining rows
        for row in iterable:
            batch_rows.append(row)
            rows_processed += 1

            if len(batch_rows) >= batch:
                _insert_batch(conn, table, batch_rows, mode, upsert_key)
                rows_inserted += len(batch_rows)
                batch_rows = []

                if progress:
                    progress({"rows_processed": rows_processed, "rows_inserted": rows_inserted})

        # Insert remaining batch
        if batch_rows:
            _insert_batch(conn, table, batch_rows, mode, upsert_key)
            rows_inserted += len(batch_rows)

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
    conn: Any,
    table: str,
    rows: list[Row],
    mode: str,
    upsert_key: str | list[str] | None,
):
    """Insert a batch of rows into DuckDB."""
    if not rows:
        return

    columns = list(rows[0].keys())
    columns_str = ", ".join(columns)
    placeholders = ", ".join(["?" for _ in columns])

    if mode == "upsert" and upsert_key:
        # DuckDB UPSERT (INSERT OR REPLACE)
        if isinstance(upsert_key, str):
            upsert_key = [upsert_key]
        query = f"INSERT OR REPLACE INTO {table} ({columns_str}) VALUES ({placeholders})"
    else:
        query = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"

    values = [[row.get(col) for col in columns] for row in rows]
    conn.executemany(query, values)
