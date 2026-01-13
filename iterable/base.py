import io
import typing
from abc import ABC, abstractmethod

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
    def reset(self):
        """Reset iterator"""
        pass

    @staticmethod
    @abstractmethod
    def id():
        """Identifier of selected destination"""
        pass

    @staticmethod
    def has_totals():
        """Has totals. Default: False"""
        return False

    @staticmethod
    def has_tables():
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

    def read(self, skip_empty: bool = True):
        """Read single record"""
        raise NotImplementedError

    def read_bulk(self, num: int = DEFAULT_BULK_NUMBER):
        """Read multiple records"""
        raise NotImplementedError

    @staticmethod
    def is_flatonly():
        """Is source flat by only. Default: False"""
        return False

    def is_flat(self):
        """Is source flat. Default: False"""
        if self.__class__().is_flatonly():
            return True
        # For non-flat-only formats, default to False
        return False

    def is_streaming(self):
        """Is source streaming. Default: False"""
        return False

    def __next__(self):
        return self.read()

    def __iter__(self):
        #        self.reset()
        return self

    def write(self, record: dict):
        """Write single record"""
        raise NotImplementedError

    def write_bulk(self, records: list[dict]):
        """Write multiple records"""
        raise NotImplementedError


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
        return False
