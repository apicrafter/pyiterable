import io
import json
import typing
import warnings
from abc import ABC, abstractmethod
from datetime import datetime

from .types import Row

ITERABLE_TYPE_STREAM = 10
ITERABLE_TYPE_FILE = 20
ITERABLE_TYPE_CODEC = 30
DEFAULT_BULK_NUMBER = 100


class BaseCodec:
    """Basic codec class"""

    def __init__(
        self,
        filename: str = None,
        fileobj: typing.IO = None,
        mode: str = "r",
        open_it: bool = False,
        options: dict = None,
    ):
        if options is None:
            options = {}
        self._fileobj = fileobj
        self.filename = filename
        self.mode = mode
        if open_it:
            self.open()

        if len(options) > 0:
            for k, v in options.items():
                setattr(self, k, v)
        pass

    @staticmethod
    def fileexts():
        """Return file extensions"""
        raise NotImplementedError

    def reset(self):
        """Reset file"""
        #        if self._fileobj.seekable():
        #            self._fileobj.seek(0)
        #        else:
        self.close()
        self.open()

    def open(self):
        raise NotImplementedError

    def fileobj(self):
        """Return file object"""
        return self._fileobj

    def close(self):
        """Close codec. Not implemented by default"""
        raise NotImplementedError

    def __enter__(self):
        """Context manager entry"""
        if self._fileobj is None and self.filename is not None:
            self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
        return False

    def textIO(self, encoding: str = "utf8"):
        """Return text wrapper over binary stream"""
        return io.TextIOWrapper(self.fileobj(), encoding=encoding, write_through=False)


class BaseIterable(ABC):
    """Base iterable data class"""

    def __init__(self):
        """Initialize base iterable"""
        self._closed = False

    @abstractmethod
    def reset(self) -> None:
        """Reset iterator"""
        pass

    @staticmethod
    @abstractmethod
    def id() -> str:
        """Identifier of selected destination"""
        pass

    @staticmethod
    def has_totals() -> bool:
        """Has totals. Default: False"""
        return False

    @staticmethod
    def has_tables() -> bool:
        """Indicates if this format supports multiple tables/sheets/datasets.

        Returns:
            bool: True if format supports table listing, False otherwise.
        """
        return False

    def list_tables(self, filename: str | None = None) -> list[str] | None:
        """List available tables, sheets, datasets, or other named collections.

        Can be called as:
        - Instance method: `iterable.list_tables()` - uses already opened file
        - Class method: `XLSXIterable.list_tables(filename)` - opens file temporarily

        Args:
            filename: Optional filename for class method usage. If None, uses instance's filename.

        Returns:
            list[str] | None: List of table/sheet names, or None if not supported.
            Returns empty list [] if file has no tables.
        """
        return None

    def read(self, skip_empty: bool = True) -> Row:
        """Read single record"""
        raise NotImplementedError

    def read_bulk(self, num: int = DEFAULT_BULK_NUMBER) -> list[Row]:
        """Read multiple records"""
        raise NotImplementedError

    @staticmethod
    def is_flatonly() -> bool:
        """Is source flat by only. Default: False"""
        return False

    def is_flat(self) -> bool:
        """Is source flat. Default: False"""
        if self.__class__().is_flatonly():
            return True
        # For non-flat-only formats, default to False
        return False

    def is_streaming(self) -> bool:
        """Is source streaming. Default: False"""
        return False

    def __next__(self) -> Row:
        return self.read()

    def __iter__(self) -> typing.Iterator[Row]:
        #        self.reset()
        return self

    def write(self, record: Row) -> None:
        """Write single record"""
        raise NotImplementedError

    def write_bulk(self, records: list[Row]) -> None:
        """Write multiple records"""
        raise NotImplementedError

    def to_pandas(self, chunksize: int | None = None):
        """Convert iterable to pandas DataFrame(s).

        Args:
            chunksize: If None, return a single DataFrame with all data.
                       If specified, return an iterator of DataFrames with at most
                       chunksize rows each (except possibly the last chunk).

        Returns:
            If chunksize is None: pandas DataFrame
            If chunksize is specified: Iterator of pandas DataFrames

        Raises:
            ImportError: If pandas is not installed. Message includes installation instructions.
        """
        try:
            import pandas as pd
        except ImportError:
            raise ImportError("pandas is required for to_pandas(). Install it with: pip install pandas") from None

        if chunksize is None:
            # Collect all rows and return single DataFrame
            rows = list(self)
            if not rows:
                return pd.DataFrame()
            return pd.DataFrame(rows)
        else:
            # Return iterator of DataFrames
            def _chunked_iterator():
                chunk = []
                for row in self:
                    chunk.append(row)
                    if len(chunk) >= chunksize:
                        yield pd.DataFrame(chunk)
                        chunk = []
                if chunk:
                    yield pd.DataFrame(chunk)

            return _chunked_iterator()

    def to_polars(self, chunksize: int | None = None):
        """Convert iterable to Polars DataFrame(s).

        Args:
            chunksize: If None, return a single DataFrame with all data.
                       If specified, return an iterator of DataFrames with at most
                       chunksize rows each (except possibly the last chunk).

        Returns:
            If chunksize is None: polars DataFrame
            If chunksize is specified: Iterator of polars DataFrames

        Raises:
            ImportError: If polars is not installed. Message includes installation instructions.
        """
        try:
            import polars as pl
        except ImportError:
            raise ImportError("polars is required for to_polars(). Install it with: pip install polars") from None

        if chunksize is None:
            # Collect all rows and return single DataFrame
            rows = list(self)
            if not rows:
                return pl.DataFrame()
            return pl.DataFrame(rows)
        else:
            # Return iterator of DataFrames
            def _chunked_iterator():
                chunk = []
                for row in self:
                    chunk.append(row)
                    if len(chunk) >= chunksize:
                        yield pl.DataFrame(chunk)
                        chunk = []
                if chunk:
                    yield pl.DataFrame(chunk)

            return _chunked_iterator()

    def to_dask(self, chunksize: int = 1000000):
        """Convert iterable to Dask DataFrame.

        Args:
            chunksize: Number of rows per partition. Default: 1000000.

        Returns:
            Dask DataFrame representing the iterable data.

        Raises:
            ImportError: If dask or pandas is not installed. Message includes installation instructions.
        """
        try:
            import dask.dataframe as dd
            import pandas as pd
        except ImportError as e:
            if "dask" in str(e).lower():
                raise ImportError(
                    "dask[dataframe] is required for to_dask(). Install it with: pip install 'dask[dataframe]'"
                ) from None
            else:
                raise ImportError("pandas is required for to_dask(). Install it with: pip install pandas") from None

        # Collect all rows first (Dask needs to know the structure)
        rows = list(self)
        if not rows:
            # Return empty Dask DataFrame
            return dd.from_pandas(pd.DataFrame(), npartitions=1)

        # Convert to pandas first, then to Dask
        df = pd.DataFrame(rows)
        return dd.from_pandas(df, npartitions=max(1, len(df) // chunksize))


class BaseFileIterable(BaseIterable):
    """Basic file iterable"""

    datamode = "text"

    def __init__(
        self,
        filename: str = None,
        stream: typing.IO = None,
        codec: BaseCodec = None,
        binary: bool = False,
        encoding: str = "utf8",
        noopen: bool = False,
        mode: str = "r",
        options: dict = None,
    ):
        """Init basic file iterable"""
        if options is None:
            options = {}
        self.filename = filename
        self.noopen = noopen
        self.encoding = encoding
        self.binary = binary
        self.mode = mode
        self.codec = codec
        if stream is not None:
            self.stype = ITERABLE_TYPE_STREAM
        elif filename is not None:
            self.stype = ITERABLE_TYPE_FILE
        elif codec is not None:
            self.stype = ITERABLE_TYPE_CODEC
        else:
            raise ValueError("BaseFileIterable requires filename, stream, or codec")
        self.fobj = None

        if self.stype == ITERABLE_TYPE_FILE:
            if not noopen:
                self.open()
        elif self.stype == ITERABLE_TYPE_STREAM:
            self.fobj = stream
        elif self.stype == ITERABLE_TYPE_CODEC:
            if not noopen:
                self.fobj = self.codec.open()
                if self.datamode == "text":
                    self.fobj = self.codec.textIO(encoding=self.encoding)

        # Initialize error handling configuration
        self._on_error = options.get("on_error", "raise")
        self._error_log = options.get("error_log", None)
        self._error_log_file = None
        self._error_log_owned = False

        # Validate error policy
        if self._on_error not in ("raise", "skip", "warn"):
            raise ValueError(f"Invalid 'on_error' value: '{self._on_error}'. Valid values are: 'raise', 'skip', 'warn'")

        # Setup error logging
        if self._error_log is not None:
            if isinstance(self._error_log, str):
                # File path - we'll open it when needed
                self._error_log_file = None
                self._error_log_owned = True
            elif hasattr(self._error_log, "write"):
                # File-like object
                self._error_log_file = self._error_log
                self._error_log_owned = False
            else:
                raise ValueError(
                    f"Invalid 'error_log' value: must be file path (str) or file-like object, "
                    f"got {type(self._error_log).__name__}"
                )

        if len(options) > 0:
            for k, v in options.items():
                setattr(self, k, v)

    def open(self):
        """Open file as file data source"""
        if self.stype == ITERABLE_TYPE_FILE:
            self.fobj = (
                open(self.filename, self.mode + "b")
                if self.binary
                else open(self.filename, self.mode, encoding=self.encoding)
            )
            return self.fobj
        else:
            raise NotImplementedError

    def reset(self):
        """Reset file using seek(0)"""
        if self.stype == ITERABLE_TYPE_FILE:
            if self.fobj is not None:
                self.fobj.seek(0)
        elif self.stype == ITERABLE_TYPE_CODEC:
            if self.fobj is not None and self.mode not in ["w", "wb"]:
                # Close any existing wrapper to avoid leaks and ensure buffers are flushed.
                try:
                    self.fobj.close()
                except Exception:
                    pass
                self.codec.reset()
                self.fobj = self.codec.fileobj()
                if self.datamode == "text":
                    self.fobj = self.codec.textIO(encoding=self.encoding)

    #                if self.fobj.seekable():
    #                   self.fobj.seek(0)

    def close(self):
        """Close file as file data source"""
        if self.stype == ITERABLE_TYPE_FILE:
            if self.fobj is not None:
                self.fobj.close()
        elif self.stype == ITERABLE_TYPE_CODEC:
            # Close wrapper first to flush any buffered text, which is critical for codecs.
            if self.fobj is not None:
                try:
                    self.fobj.close()
                finally:
                    self.fobj = None
            elif self.codec is not None:
                self.codec.close()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
        # Close error log file if we own it
        if self._error_log_owned and self._error_log_file is not None:
            try:
                self._error_log_file.close()
            except Exception:
                pass
            self._error_log_file = None
        return False

    def _handle_error(
        self,
        error: Exception,
        row_number: int = None,
        byte_offset: int = None,
        original_line: str = None,
    ) -> None:
        """Handle error according to configured error policy.

        Args:
            error: The exception that occurred
            row_number: Optional row number where error occurred
            byte_offset: Optional byte offset where error occurred
            original_line: Optional original line content that failed

        Raises:
            The original error if policy is 'raise', otherwise returns None
        """
        from .exceptions import FormatParseError, ReadError

        # Enhance error with contextual information if it's a parse/read error
        if isinstance(error, (FormatParseError, ReadError)):
            if not hasattr(error, "filename") or error.filename is None:
                error.filename = getattr(self, "filename", None)
            if not hasattr(error, "row_number") or error.row_number is None:
                error.row_number = row_number
            if not hasattr(error, "byte_offset") or error.byte_offset is None:
                error.byte_offset = byte_offset
            if not hasattr(error, "original_line") or error.original_line is None:
                error.original_line = original_line

        # Log error if logging is enabled
        if self._error_log is not None:
            self._log_error(error, row_number, byte_offset, original_line)

        # Apply error policy
        if self._on_error == "raise":
            raise error
        elif self._on_error == "warn":
            # Build warning message with context
            warning_msg = "Parse error"
            if hasattr(error, "filename") and error.filename:
                warning_msg += f" in {error.filename}"
            if row_number is not None:
                warning_msg += f" at row {row_number}"
            if byte_offset is not None:
                warning_msg += f" (byte {byte_offset})"
            warning_msg += f": {str(error)}"
            warnings.warn(warning_msg, UserWarning, stacklevel=3)
        # For 'skip', just return None (error is logged but not raised)

    def _log_error(
        self,
        error: Exception,
        row_number: int = None,
        byte_offset: int = None,
        original_line: str = None,
    ) -> None:
        """Log error to error log file.

        Args:
            error: The exception that occurred
            row_number: Optional row number where error occurred
            byte_offset: Optional byte offset where error occurred
            original_line: Optional original line content that failed
        """
        # Open error log file if needed (for file path strings)
        if self._error_log_owned and self._error_log_file is None:
            try:
                self._error_log_file = open(self._error_log, "a", encoding="utf-8")
            except Exception:
                # If we can't open the log file, silently fail
                return

        if self._error_log_file is None:
            return

        # Build log entry
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "filename": getattr(self, "filename", None),
            "row_number": row_number,
            "byte_offset": byte_offset,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "original_line": original_line[:1000] if original_line else None,  # Truncate very long lines
        }

        # Write as JSON line
        try:
            self._error_log_file.write(json.dumps(log_entry) + "\n")
            self._error_log_file.flush()
        except Exception:
            # If logging fails, silently continue
            pass
