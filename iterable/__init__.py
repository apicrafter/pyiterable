__author__ = "Ivan Begtin"
__version__ = "1.0.10"
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

open_it = open_iterable

__all__ = [
    "open_iterable",
    "open_it",
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
