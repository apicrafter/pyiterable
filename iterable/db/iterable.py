"""
Database iterable wrapper.

Wraps database drivers to provide BaseIterable interface for database sources.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from ..base import DEFAULT_BULK_NUMBER, BaseIterable
from ..types import Row
from .base import DBDriver


class DatabaseIterable(BaseIterable):
    """Iterable wrapper for database sources.

    Wraps a DBDriver to provide BaseIterable interface, enabling database
    sources to work seamlessly with existing IterableData features.
    """

    def __init__(self, driver: DBDriver) -> None:
        """Initialize database iterable.

        Args:
            driver: Database driver instance
        """
        super().__init__()
        self.driver = driver
        self._iterator: Iterator[Row] | None = None
        self._current_row: Row | None = None
        self._reset_supported = False  # Most databases don't support reset

    @staticmethod
    def id() -> str:
        """Return identifier for database iterable."""
        return "database"

    def reset(self) -> None:
        """Reset iterator.

        Note: Most databases don't support reset. This will raise an error
        unless the specific database driver supports it.

        Raises:
            NotImplementedError: If reset is not supported by the database
        """
        if not self._reset_supported:
            raise NotImplementedError(
                "Reset is not supported for database iterables. "
                "Database queries cannot be re-executed after iteration starts."
            )
        # If reset is supported, reconnect and recreate iterator
        self.driver.close()
        self.driver.connect()
        self._iterator = None
        self._current_row = None

    def read(self, skip_empty: bool = True) -> Row:
        """Read single record from database.

        Args:
            skip_empty: Ignored for database sources (always True)

        Returns:
            dict: Database row as dictionary

        Raises:
            StopIteration: When no more rows available
        """
        if self._iterator is None:
            # Start iteration
            if not self.driver.is_connected:
                self.driver.connect()
            self._iterator = self.driver.iterate()
            self.driver._start_metrics()

        try:
            row = next(self._iterator)
            return row
        except StopIteration:
            self._current_row = None
            raise

    def read_bulk(self, num: int = DEFAULT_BULK_NUMBER) -> list[Row]:
        """Read multiple records from database.

        Args:
            num: Number of records to read

        Returns:
            List of dict rows
        """
        if self._iterator is None:
            # Start iteration
            if not self.driver.is_connected:
                self.driver.connect()
            self._iterator = self.driver.iterate()
            self.driver._start_metrics()

        results = []
        try:
            for _ in range(num):
                row = next(self._iterator)
                results.append(row)
        except StopIteration:
            pass

        return results

    def close(self) -> None:
        """Close database connection."""
        if self.driver is not None:
            self.driver.close()
        self._iterator = None
        self._current_row = None
        self._closed = True

    def __enter__(self) -> DatabaseIterable:
        """Context manager entry."""
        return self

    def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: Any) -> None:
        """Context manager exit."""
        self.close()

    def __iter__(self) -> Iterator[Row]:
        """Return iterator."""
        return self

    def __next__(self) -> Row:
        """Get next row."""
        return self.read()

    @property
    def metrics(self) -> dict[str, Any]:
        """Get current metrics from driver.

        Returns:
            Dictionary with metrics (rows_read, bytes_read, elapsed_seconds)
        """
        return self.driver.metrics

    def is_streaming(self) -> bool:
        """Database sources are always streaming."""
        return True

    def is_flat(self) -> bool:
        """Database sources are typically flat (dict rows)."""
        return True

    @staticmethod
    def is_flatonly() -> bool:
        """Database sources are flat-only."""
        return True
