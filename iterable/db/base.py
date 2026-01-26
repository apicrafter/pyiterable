"""
Base database driver class.

Provides the abstract interface for database drivers that enable reading
from SQL and NoSQL databases as iterable data sources.
"""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import Any

from ..types import Row


class DBDriver(ABC):
    """Base class for database drivers.

    Database drivers provide a unified interface for reading data from
    various database systems (SQL and NoSQL) as iterable sources.

    All database drivers must implement:
    - `connect()`: Establish database connection
    - `iterate()`: Return iterator of dict rows/documents
    - `close()`: Clean up resources (implemented by default, can be overridden)
    """

    def __init__(self, source: str | Any, **kwargs: Any) -> None:
        """Initialize database driver.

        Args:
            source: Database connection string/URL, or existing connection object
            **kwargs: Additional driver-specific parameters
        """
        self.source = source
        self.kwargs = kwargs
        self.conn: Any = None
        self._connected = False
        self._closed = False

        # Metrics tracking
        self._metrics: dict[str, Any] = {
            "rows_read": 0,
            "bytes_read": None,  # May not be available for all databases
            "elapsed_seconds": 0.0,
            "start_time": None,
        }

        # Error handling configuration
        self._on_error = kwargs.get("on_error", "raise")
        if self._on_error not in ("raise", "skip", "warn"):
            raise ValueError(f"Invalid 'on_error' value: '{self._on_error}'. Valid values are: 'raise', 'skip', 'warn'")

    @abstractmethod
    def connect(self) -> None:
        """Establish database connection.

        This method should:
        - Parse connection string/URL if source is a string
        - Use existing connection if source is a connection object
        - Set self.conn to the connection object
        - Set self._connected = True on success

        Raises:
            ConnectionError: If connection fails
            ImportError: If required database driver is not installed
        """
        raise NotImplementedError

    @abstractmethod
    def iterate(self) -> Iterator[Row]:
        """Return an iterator of dict rows/documents.

        This method should:
        - Yield dict objects representing database rows/documents
        - Use batch processing for memory efficiency (via batch_size parameter)
        - Update metrics (rows_read, elapsed_seconds) during iteration
        - Handle errors according to on_error policy

        Yields:
            dict: Database row/document as a dictionary

        Raises:
            RuntimeError: If not connected (call connect() first)
        """
        raise NotImplementedError

    def close(self) -> None:
        """Close database connection and clean up resources.

        This method:
        - Closes the database connection if open
        - Cleans up any cursors or resources
        - Sets self._closed = True
        - Safe to call multiple times
        """
        if self.conn is not None and not self._closed:
            try:
                # Try to close connection (method varies by database)
                if hasattr(self.conn, "close"):
                    self.conn.close()
            except Exception:
                # Ignore errors during cleanup
                pass
            finally:
                self.conn = None
                self._connected = False
                self._closed = True

    def __enter__(self) -> DBDriver:
        """Context manager entry."""
        if not self._connected:
            self.connect()
        return self

    def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: Any) -> None:
        """Context manager exit."""
        self.close()

    def __del__(self) -> None:
        """Destructor - ensure connection is closed."""
        self.close()

    @property
    def metrics(self) -> dict[str, Any]:
        """Get current metrics.

        Returns:
            Dictionary with metrics:
            - rows_read: Number of rows read
            - bytes_read: Bytes read (may be None if not available)
            - elapsed_seconds: Time elapsed since start
        """
        if self._metrics["start_time"] is not None:
            self._metrics["elapsed_seconds"] = time.time() - self._metrics["start_time"]
        return self._metrics.copy()

    def _start_metrics(self) -> None:
        """Start metrics tracking."""
        self._metrics["start_time"] = time.time()
        self._metrics["rows_read"] = 0
        self._metrics["elapsed_seconds"] = 0.0

    def _update_metrics(self, rows_read: int = 0, bytes_read: int | None = None) -> None:
        """Update metrics during iteration.

        Args:
            rows_read: Number of rows read in this batch
            bytes_read: Bytes read in this batch (optional)
        """
        self._metrics["rows_read"] += rows_read
        if bytes_read is not None:
            if self._metrics["bytes_read"] is None:
                self._metrics["bytes_read"] = 0
            self._metrics["bytes_read"] += bytes_read
        if self._metrics["start_time"] is not None:
            self._metrics["elapsed_seconds"] = time.time() - self._metrics["start_time"]

    def _handle_error(self, error: Exception, context: str = "") -> None:
        """Handle errors according to on_error policy.

        Args:
            error: The exception that occurred
            context: Additional context about where the error occurred

        Raises:
            Exception: If on_error is 'raise'
        """
        if self._on_error == "raise":
            raise error
        elif self._on_error == "warn":
            import warnings

            warning_msg = f"Error in database driver{': ' + context if context else ''}: {error}"
            warnings.warn(warning_msg, UserWarning, stacklevel=2)
        # If on_error is 'skip', just return (error is ignored)

    @property
    def is_connected(self) -> bool:
        """Check if driver is connected to database.

        Returns:
            True if connected, False otherwise
        """
        return self._connected and not self._closed

    @property
    def is_closed(self) -> bool:
        """Check if driver is closed.

        Returns:
            True if closed, False otherwise
        """
        return self._closed
