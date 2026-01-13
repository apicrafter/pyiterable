"""Exception hierarchy for IterableData library.

This module defines a comprehensive exception hierarchy that allows users
to catch and handle specific error types programmatically.
"""


class IterableDataError(Exception):
    """Base exception for all iterable data errors.

    All exceptions raised by the IterableData library inherit from this class,
    allowing users to catch all iterable errors with a single exception handler.
    """

    def __init__(self, message: str, error_code: str = None):
        """Initialize exception.

        Args:
            message: Human-readable error message
            error_code: Optional error code for programmatic handling
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code


class FormatError(IterableDataError):
    """Base exception for format-specific errors.

    Raised when an error occurs related to data format handling.
    """

    def __init__(self, message: str, format_id: str = None, error_code: str = None):
        """Initialize format error.

        Args:
            message: Human-readable error message
            format_id: Optional format identifier (e.g., "csv", "json")
            error_code: Optional error code for programmatic handling
        """
        super().__init__(message, error_code)
        self.format_id = format_id


class FormatNotSupportedError(FormatError):
    """Format is not supported or not available.

    Raised when a requested format is not supported by the library,
    or when required dependencies are missing.

    Error code: FORMAT_NOT_SUPPORTED
    """

    def __init__(self, format_id: str, reason: str = None):
        """Initialize format not supported error.

        Args:
            format_id: Format identifier that is not supported
            reason: Optional reason why format is not supported
        """
        message = f"Format '{format_id}' is not supported"
        if reason:
            message += f": {reason}"
        super().__init__(message, format_id=format_id, error_code="FORMAT_NOT_SUPPORTED")
        self.reason = reason


class FormatDetectionError(FormatError):
    """Could not detect file format.

    Raised when the system cannot determine the format of a file,
    either from filename extension or content analysis.

    Error code: FORMAT_DETECTION_FAILED
    """

    def __init__(self, filename: str = None, reason: str = None):
        """Initialize format detection error.

        Args:
            filename: Optional filename that could not be detected
            reason: Optional reason why detection failed
        """
        message = "Could not detect file format"
        if filename:
            message += f" for file: {filename}"
        if reason:
            message += f". {reason}"
        super().__init__(message, error_code="FORMAT_DETECTION_FAILED")
        self.filename = filename
        self.reason = reason


class FormatParseError(FormatError):
    """Format parsing failed.

    Raised when a file cannot be parsed as the expected format,
    typically due to malformed data.

    Error code: FORMAT_PARSE_FAILED
    """

    def __init__(self, format_id: str, message: str, position: int = None):
        """Initialize format parse error.

        Args:
            format_id: Format identifier
            message: Error message describing the parse failure
            position: Optional position in file where error occurred
        """
        full_message = f"Failed to parse {format_id} format"
        if position is not None:
            full_message += f" at position {position}"
        full_message += f": {message}"
        super().__init__(full_message, format_id=format_id, error_code="FORMAT_PARSE_FAILED")
        self.position = position


class CodecError(IterableDataError):
    """Base exception for compression codec errors.

    Raised when an error occurs related to compression/decompression.
    """

    def __init__(self, message: str, codec_name: str = None, error_code: str = None):
        """Initialize codec error.

        Args:
            message: Human-readable error message
            codec_name: Optional codec name (e.g., "gzip", "bzip2")
            error_code: Optional error code for programmatic handling
        """
        super().__init__(message, error_code)
        self.codec_name = codec_name


class CodecNotSupportedError(CodecError):
    """Compression codec is not supported.

    Raised when a requested codec is not available,
    typically due to missing dependencies.

    Error code: CODEC_NOT_SUPPORTED
    """

    def __init__(self, codec_name: str, reason: str = None):
        """Initialize codec not supported error.

        Args:
            codec_name: Codec name that is not supported
            reason: Optional reason why codec is not supported
        """
        message = f"Codec '{codec_name}' is not supported"
        if reason:
            message += f": {reason}"
        super().__init__(message, codec_name=codec_name, error_code="CODEC_NOT_SUPPORTED")
        self.reason = reason


class CodecDecompressionError(CodecError):
    """Decompression failed.

    Raised when decompressing data fails.

    Error code: CODEC_DECOMPRESSION_FAILED
    """

    def __init__(self, codec_name: str, message: str = None):
        """Initialize decompression error.

        Args:
            codec_name: Codec name
            message: Optional error message
        """
        error_message = f"Failed to decompress using {codec_name} codec"
        if message:
            error_message += f": {message}"
        super().__init__(error_message, codec_name=codec_name, error_code="CODEC_DECOMPRESSION_FAILED")


class CodecCompressionError(CodecError):
    """Compression failed.

    Raised when compressing data fails.

    Error code: CODEC_COMPRESSION_FAILED
    """

    def __init__(self, codec_name: str, message: str = None):
        """Initialize compression error.

        Args:
            codec_name: Codec name
            message: Optional error message
        """
        error_message = f"Failed to compress using {codec_name} codec"
        if message:
            error_message += f": {message}"
        super().__init__(error_message, codec_name=codec_name, error_code="CODEC_COMPRESSION_FAILED")


class ReadError(IterableDataError):
    """Base exception for reading errors.

    Raised when an error occurs during data reading operations.
    """

    def __init__(self, message: str, filename: str = None, error_code: str = None):
        """Initialize read error.

        Args:
            message: Human-readable error message
            filename: Optional filename being read
            error_code: Optional error code for programmatic handling
        """
        super().__init__(message, error_code)
        self.filename = filename


class WriteError(IterableDataError):
    """Base exception for writing errors.

    Raised when an error occurs during data writing operations.
    """

    def __init__(self, message: str, filename: str = None, error_code: str = None):
        """Initialize write error.

        Args:
            message: Human-readable error message
            filename: Optional filename being written
            error_code: Optional error code for programmatic handling
        """
        super().__init__(message, error_code)
        self.filename = filename


class StreamingNotSupportedError(ReadError):
    """Format doesn't support streaming.

    Raised when a streaming operation is attempted on a format
    that doesn't support streaming (e.g., formats that load entire file).

    Error code: STREAMING_NOT_SUPPORTED
    """

    def __init__(self, format_id: str, reason: str = None):
        """Initialize streaming not supported error.

        Args:
            format_id: Format identifier that doesn't support streaming
            reason: Optional reason why streaming is not supported
        """
        message = f"Format '{format_id}' does not support streaming"
        if reason:
            message += f": {reason}"
        super().__init__(message, error_code="STREAMING_NOT_SUPPORTED")
        self.format_id = format_id
        self.reason = reason


class ResourceError(IterableDataError):
    """Base exception for resource management errors.

    Raised when an error occurs related to resource management
    (file handles, streams, connections, etc.).
    """

    def __init__(self, message: str, error_code: str = None):
        """Initialize resource error.

        Args:
            message: Human-readable error message
            error_code: Optional error code for programmatic handling
        """
        super().__init__(message, error_code)


class StreamNotSeekableError(ResourceError):
    """Stream is not seekable.

    Raised when an operation requires seeking (e.g., reset())
    but the stream doesn't support seeking.

    Error code: STREAM_NOT_SEEKABLE
    """

    def __init__(self, operation: str = None):
        """Initialize stream not seekable error.

        Args:
            operation: Optional operation that requires seeking
        """
        message = "Stream is not seekable"
        if operation:
            message += f" (required for {operation})"
        super().__init__(message, error_code="STREAM_NOT_SEEKABLE")
        self.operation = operation


class ResourceLeakError(ResourceError):
    """Resource leak detected.

    Raised when a resource (file, connection, etc.) is not properly closed.

    Error code: RESOURCE_LEAK
    """

    def __init__(self, resource_type: str = None):
        """Initialize resource leak error.

        Args:
            resource_type: Optional type of resource that leaked
        """
        message = "Resource leak detected"
        if resource_type:
            message += f": {resource_type}"
        super().__init__(message, error_code="RESOURCE_LEAK")
        self.resource_type = resource_type
