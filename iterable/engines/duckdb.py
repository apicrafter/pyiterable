from __future__ import annotations

import typing
import warnings

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

        # Extract pushdown parameters from options
        self._columns = options.get("columns")
        self._filter = options.get("filter")
        self._query = options.get("query")

        # Validate parameters
        if self._query and (self._columns or self._filter):
            warnings.warn(
                "When 'query' parameter is provided, 'columns' and 'filter' parameters are ignored.",
                UserWarning,
                stacklevel=2,
            )

        # Detect file format for appropriate DuckDB function
        self._file_format = self._detect_file_format()
        self._duckdb_function = self._get_duckdb_function()

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

    def _detect_file_format(self) -> str:
        """Detect file format from filename extension"""
        if not self.filename:
            return "csv"  # Default fallback

        filename_lower = self.filename.lower()

        # Handle compressed files - remove compression extension
        compression_extensions = (".gz", ".zst", ".zstd")
        if filename_lower.endswith(compression_extensions):
            # Remove compression extension
            base_name = filename_lower.rsplit(".", 1)[0]
        else:
            base_name = filename_lower

        # Detect format from extension (check in order of specificity)
        if base_name.endswith(".parquet"):
            return "parquet"
        elif base_name.endswith((".jsonl", ".ndjson")):
            return "jsonl"
        elif base_name.endswith(".json"):
            return "json"
        elif base_name.endswith(".csv"):
            return "csv"
        else:
            # Default to CSV for backward compatibility
            return "csv"

    def _get_duckdb_function(self) -> str:
        """Get the appropriate DuckDB function name for the file format"""
        format_to_function = {
            "csv": "read_csv_auto",
            "jsonl": "read_json_auto",
            "json": "read_json_auto",
            "parquet": "read_parquet",
        }
        return format_to_function.get(self._file_format, "read_csv_auto")

    def _escape_filename(self, filename: str) -> str:
        """Escape single quotes in filename to prevent SQL injection"""
        return filename.replace("'", "''")

    def _validate_query(self, query: str) -> None:
        """Validate that query is read-only (no DDL/DML operations)"""
        query_upper = query.upper().strip()

        # Check for DDL operations
        ddl_keywords = ["CREATE", "DROP", "ALTER", "TRUNCATE"]
        for keyword in ddl_keywords:
            if keyword in query_upper:
                raise ValueError(f"Query contains DDL operation '{keyword}'. Only SELECT queries are allowed.")

        # Check for DML operations
        dml_keywords = ["INSERT", "UPDATE", "DELETE", "MERGE"]
        for keyword in dml_keywords:
            if keyword in query_upper:
                raise ValueError(f"Query contains DML operation '{keyword}'. Only SELECT queries are allowed.")

        # Check that it starts with SELECT
        if not query_upper.startswith("SELECT"):
            raise ValueError("Query must be a SELECT statement.")

    def _translate_callable_filter(self, filter_func: typing.Callable) -> str | None:
        """Attempt to translate a Python callable filter to SQL WHERE clause"""
        # This is a simplified translator for common patterns
        # For complex callables, returns None to fall back to Python filtering

        # TODO: Implement AST-based translation for simple patterns like:
        # lambda row: row['col'] > value -> col > value
        # For now, return None to use Python-side filtering for callables
        return None

    def _build_sql_query(self, limit: int | None = None, offset: int | None = None) -> str:
        """Build SQL query with pushdown optimizations"""
        safe_filename = self._escape_filename(self.filename)

        # If custom query is provided, use it directly (after validation)
        if self._query:
            self._validate_query(self._query)
            query = self._query
            # Users must reference files correctly in their query using read functions
            # Example: SELECT * FROM read_csv_auto('file.csv') WHERE col > 10
            # Add LIMIT and OFFSET if needed (only if not already present)
            if limit is not None and "LIMIT" not in query.upper():
                query += f" LIMIT {limit}"
            if offset is not None and "OFFSET" not in query.upper():
                query += f" OFFSET {offset}"
            return query

        # Build SELECT clause
        if self._columns:
            # Validate columns exist (basic check - can be enhanced)
            columns_str = ", ".join(self._columns)
            select_clause = f"SELECT {columns_str}"
        else:
            select_clause = "SELECT *"

        # Build FROM clause
        from_clause = f"FROM {self._duckdb_function}('{safe_filename}')"

        # Build WHERE clause
        where_clause = ""
        if self._filter:
            if isinstance(self._filter, str):
                # SQL string filter - use directly
                where_clause = f"WHERE {self._filter}"
            elif callable(self._filter):
                # Python callable - try to translate
                sql_filter = self._translate_callable_filter(self._filter)
                if sql_filter:
                    where_clause = f"WHERE {sql_filter}"
                # If translation fails, filtering will be done in Python (handled in read methods)

        # Combine query parts
        query_parts = [select_clause, from_clause]
        if where_clause:
            query_parts.append(where_clause)

        query = " ".join(query_parts)

        # Add LIMIT and OFFSET
        if limit is not None:
            query += f" LIMIT {limit}"
        if offset is not None:
            query += f" OFFSET {offset}"

        return query

    def _ensure_connection(self):
        """Ensure DuckDB connection is established"""
        if self._connection is None:
            self._connection = duckdb.connect()
            # Validate filename is a string (not user input SQL)
            if not isinstance(self.filename, str):
                raise ValueError("Filename must be a string")
            # DuckDB's read functions handle file paths safely
            # The filename is validated and escaped before use

    def totals(self):
        """Returns total number of records"""
        self._ensure_connection()

        # If custom query is provided, we need to count from that query
        if self._query:
            self._validate_query(self._query)
            # Wrap query in a subquery to count
            count_query = f"SELECT COUNT(*) FROM ({self._query})"
            result = self._connection.execute(count_query).fetchone()
            return result[0] if result else 0

        # Build query with filter pushdown
        safe_filename = self._escape_filename(self.filename)

        # Build WHERE clause if filter is provided
        where_clause = ""
        if self._filter and isinstance(self._filter, str):
            where_clause = f"WHERE {self._filter}"

        count_query = f"SELECT COUNT(*) FROM {self._duckdb_function}('{safe_filename}')"
        if where_clause:
            count_query += f" {where_clause}"

        result = self._connection.execute(count_query).fetchone()
        count = result[0] if result else 0

        # If filter is a callable, we need to count in Python (fallback)
        if self._filter and callable(self._filter):
            # Count all rows and filter in Python
            all_query = f"SELECT * FROM {self._duckdb_function}('{safe_filename}')"
            result = self._connection.execute(all_query)
            all_rows = result.fetchall()
            columns = [desc[0] for desc in result.description] if result.description else []
            count = sum(1 for row in all_rows if self._filter(dict(zip(columns, row, strict=False))))

        return count

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
            # Build SQL query with pushdown optimizations
            query = self._build_sql_query(limit=self._batch_size, offset=batch_offset)
            result = self._connection.execute(query)

            # Fetch all rows and convert to dicts efficiently
            rows = result.fetchall()
            columns = [desc[0] for desc in result.description] if result.description else []
            batch = [dict(zip(columns, row, strict=False)) for row in rows]

            # If filter is a callable and couldn't be translated, filter in Python
            if self._filter and callable(self._filter):
                batch = [row for row in batch if self._filter(row)]

            # If columns were specified, ensure only those columns are in the dict
            if self._columns:
                batch = [{k: row.get(k) for k in self._columns if k in row} for row in batch]

            self._current_batch = batch
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

        # Build SQL query with pushdown optimizations
        query = self._build_sql_query(limit=num, offset=self.pos)
        result = self._connection.execute(query)

        rows = result.fetchall()
        columns = [desc[0] for desc in result.description] if result.description else []
        chunk = [dict(zip(columns, row, strict=False)) for row in rows]

        # If filter is a callable and couldn't be translated, filter in Python
        if self._filter and callable(self._filter):
            chunk = [row for row in chunk if self._filter(row)]

        # If columns were specified, ensure only those columns are in the dict
        if self._columns:
            chunk = [{k: row.get(k) for k in self._columns if k in row} for row in chunk]

        self.pos += len(chunk)
        return chunk


# Backwards-compatible alias (engine)
DuckDBIterable = DuckDBEngineIterable
