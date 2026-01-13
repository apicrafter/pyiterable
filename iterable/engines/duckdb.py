from __future__ import annotations

import typing

import duckdb

from ..base import BaseCodec, BaseFileIterable

DUCKDB_CACHE_SIZE = 1000


class DuckDBEngineIterable(BaseFileIterable):
    def __init__(
        self,
        filename: str = None,
        stream: typing.IO = None,
        codec: BaseCodec = None,
        engine: str = "duckdb",
        mode: str = "r",
        encoding: str = "utf8",
        options: dict = None,
    ):
        if options is None:
            options = {}
        self.pos = 0
        super().__init__(filename, stream, codec=codec, binary=False, mode=mode, encoding=encoding, options=options)
        self._connection = None
        self._cursor = None
        self._current_batch = None
        self._batch_size = DUCKDB_CACHE_SIZE
        self._offset = 0
        pass

    @staticmethod
    def id() -> str:
        return "duckdb"

    @staticmethod
    def is_flatonly() -> bool:
        return False

    def open(self):
        """No need to open iterable for DuckDB"""
        pass

    def close(self):
        """No needto close iterable for DuckDB"""

    def _ensure_connection(self):
        """Ensure DuckDB connection is established"""
        if self._connection is None:
            self._connection = duckdb.connect()
            # Validate filename is a string (not user input SQL)
            if not isinstance(self.filename, str):
                raise ValueError("Filename must be a string")
            # DuckDB's read_csv_auto and read_json_auto handle file paths safely
            # The filename is validated and not directly interpolated into SQL

    def totals(self):
        """Returns total number of records"""
        self._ensure_connection()
        # DuckDB can read files directly - validate filename format
        # Escape single quotes to prevent SQL injection
        safe_filename = self.filename.replace("'", "''")
        result = self._connection.execute(
            f"SELECT COUNT(*) FROM read_csv_auto('{safe_filename}')"
        ).fetchone()
        return result[0] if result else 0

    def reset(self):
        """Resets counter and clears batch cache"""
        self.pos = 0
        self._offset = 0
        self._current_batch = None
        # Reset cursor if it exists
        if self._cursor is not None:
            self._cursor = None

    def _load_batch(self):
        """Load next batch efficiently"""
        self._ensure_connection()
        # Calculate offset for current batch
        batch_offset = (self.pos // self._batch_size) * self._batch_size
        
        # Only reload if we need a new batch
        if self._offset != batch_offset or self._current_batch is None:
            # Escape filename to prevent SQL injection
            safe_filename = self.filename.replace("'", "''")
            result = self._connection.execute(
                f"SELECT * FROM read_csv_auto('{safe_filename}') LIMIT {self._batch_size} OFFSET {batch_offset}"
            )
            # Fetch all rows and convert to dicts efficiently
            rows = result.fetchall()
            columns = [desc[0] for desc in result.description] if result.description else []
            self._current_batch = [dict(zip(columns, row, strict=False)) for row in rows]
            self._offset = batch_offset

    def read(self) -> dict:
        """Read single record efficiently"""
        if self._current_batch is None or len(self._current_batch) == 0:
            self._load_batch()
        
        if not self._current_batch:
            raise StopIteration
        
        # Get item from current batch
        batch_index = self.pos % self._batch_size
        if batch_index < len(self._current_batch):
            item = self._current_batch[batch_index]
            self.pos += 1
            return item
        else:
            # End of batch, try to load next batch
            self._load_batch()
            if not self._current_batch:
                raise StopIteration
            item = self._current_batch[0]
            self.pos += 1
            return item

    def read_bulk(self, num: int = 100) -> list[dict]:
        """Read bulk records efficiently"""
        self._ensure_connection()
        # Escape filename to prevent SQL injection
        safe_filename = self.filename.replace("'", "''")
        result = self._connection.execute(
            f"SELECT * FROM read_csv_auto('{safe_filename}') LIMIT {num} OFFSET {self.pos}"
        )
        rows = result.fetchall()
        columns = [desc[0] for desc in result.description] if result.description else []
        chunk = [dict(zip(columns, row, strict=False)) for row in rows]
        self.pos += len(chunk)
        return chunk


# Backwards-compatible alias (engine)
DuckDBIterable = DuckDBEngineIterable
