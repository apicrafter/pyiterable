__author__ = "Ivan Begtin"
__version__ = "1.0.11"
__licence__ = "MIT"
__doc__ = "Iterable data processing Python library"

from .exceptions import (
    CodecCompressionError,
    CodecDecompressionError,
    CodecError,
    CodecNotSupportedError,
    FormatDetectionError,
    FormatError,
    FormatNotSupportedError,
    FormatParseError,
    IterableDataError,
    ReadError,
    ResourceError,
    ResourceLeakError,
    StreamingNotSupportedError,
    StreamNotSeekableError,
    WriteError,
)
from .helpers.detect import open_iterable
from .helpers.typed import as_dataclasses, as_pydantic
from .ai import doc as ai
from .ingest import to_db as ingest
from .ops import filter, inspect, schema, stats, transform
from .validate import iterable as validate
from .types import CodecArgs, IterableArgs, Row

open_it = open_iterable

__all__ = [
    "open_iterable",
    "open_it",
    "Row",
    "IterableArgs",
    "CodecArgs",
    "as_dataclasses",
    "as_pydantic",
    "ai",
    "filter",
    "inspect",
    "ingest",
    "schema",
    "stats",
    "transform",
    "validate",
    "IterableDataError",
    "FormatError",
    "FormatNotSupportedError",
    "FormatDetectionError",
    "FormatParseError",
    "CodecError",
    "CodecNotSupportedError",
    "CodecDecompressionError",
    "CodecCompressionError",
    "ReadError",
    "WriteError",
    "StreamingNotSupportedError",
    "ResourceError",
    "StreamNotSeekableError",
    "ResourceLeakError",
]
