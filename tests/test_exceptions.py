"""Tests for exception hierarchy in iterable.exceptions module."""

import pytest

from iterable.exceptions import (
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
    StreamNotSeekableError,
    StreamingNotSupportedError,
    WriteError,
)


class TestIterableDataError:
    """Test base exception class."""

    def test_basic_instantiation(self):
        """Test basic exception instantiation."""
        error = IterableDataError("Test message")
        assert str(error) == "Test message"
        assert error.message == "Test message"
        assert error.error_code is None

    def test_with_error_code(self):
        """Test exception with error code."""
        error = IterableDataError("Test message", error_code="TEST_ERROR")
        assert error.message == "Test message"
        assert error.error_code == "TEST_ERROR"


class TestFormatError:
    """Test format error exceptions."""

    def test_format_error_basic(self):
        """Test basic FormatError."""
        error = FormatError("Format error", format_id="csv")
        assert error.message == "Format error"
        assert error.format_id == "csv"
        assert error.error_code is None
        assert isinstance(error, IterableDataError)

    def test_format_error_with_code(self):
        """Test FormatError with error code."""
        error = FormatError("Format error", format_id="json", error_code="FORMAT_ERR")
        assert error.format_id == "json"
        assert error.error_code == "FORMAT_ERR"

    def test_format_not_supported_error(self):
        """Test FormatNotSupportedError."""
        error = FormatNotSupportedError("xml", reason="Missing dependency")
        assert error.format_id == "xml"
        assert error.reason == "Missing dependency"
        assert error.error_code == "FORMAT_NOT_SUPPORTED"
        assert "xml" in str(error)
        assert "Missing dependency" in str(error)

    def test_format_not_supported_error_no_reason(self):
        """Test FormatNotSupportedError without reason."""
        error = FormatNotSupportedError("parquet")
        assert error.format_id == "parquet"
        assert error.reason is None
        assert "parquet" in str(error)

    def test_format_detection_error(self):
        """Test FormatDetectionError."""
        error = FormatDetectionError(filename="data.unknown", reason="Unknown extension")
        assert error.filename == "data.unknown"
        assert error.reason == "Unknown extension"
        assert error.error_code == "FORMAT_DETECTION_FAILED"
        assert "data.unknown" in str(error)
        assert "Unknown extension" in str(error)

    def test_format_detection_error_no_args(self):
        """Test FormatDetectionError without filename or reason."""
        error = FormatDetectionError()
        assert error.filename is None
        assert error.reason is None
        assert "Could not detect file format" in str(error)

    def test_format_parse_error(self):
        """Test FormatParseError."""
        error = FormatParseError("json", "Invalid JSON syntax", position=42)
        assert error.format_id == "json"
        assert error.position == 42
        assert error.error_code == "FORMAT_PARSE_FAILED"
        assert "json" in str(error)
        assert "42" in str(error)

    def test_format_parse_error_no_position(self):
        """Test FormatParseError without position."""
        error = FormatParseError("csv", "Missing delimiter")
        assert error.format_id == "csv"
        assert error.position is None
        assert "csv" in str(error)


class TestCodecError:
    """Test codec error exceptions."""

    def test_codec_error_basic(self):
        """Test basic CodecError."""
        error = CodecError("Codec error", codec_name="gzip")
        assert error.message == "Codec error"
        assert error.codec_name == "gzip"
        assert error.error_code is None
        assert isinstance(error, IterableDataError)

    def test_codec_error_with_code(self):
        """Test CodecError with error code."""
        error = CodecError("Codec error", codec_name="bzip2", error_code="CODEC_ERR")
        assert error.codec_name == "bzip2"
        assert error.error_code == "CODEC_ERR"

    def test_codec_not_supported_error(self):
        """Test CodecNotSupportedError."""
        error = CodecNotSupportedError("lz4", reason="Package not installed")
        assert error.codec_name == "lz4"
        assert error.reason == "Package not installed"
        assert error.error_code == "CODEC_NOT_SUPPORTED"
        assert "lz4" in str(error)
        assert "Package not installed" in str(error)

    def test_codec_decompression_error(self):
        """Test CodecDecompressionError."""
        error = CodecDecompressionError("gzip", "Corrupted data")
        assert error.codec_name == "gzip"
        assert error.error_code == "CODEC_DECOMPRESSION_FAILED"
        assert "gzip" in str(error)
        assert "Corrupted data" in str(error)

    def test_codec_decompression_error_no_message(self):
        """Test CodecDecompressionError without message."""
        error = CodecDecompressionError("zstd")
        assert error.codec_name == "zstd"
        assert "zstd" in str(error)

    def test_codec_compression_error(self):
        """Test CodecCompressionError."""
        error = CodecCompressionError("bzip2", "Write failed")
        assert error.codec_name == "bzip2"
        assert error.error_code == "CODEC_COMPRESSION_FAILED"
        assert "bzip2" in str(error)
        assert "Write failed" in str(error)


class TestReadWriteError:
    """Test read and write error exceptions."""

    def test_read_error(self):
        """Test ReadError."""
        error = ReadError("Read failed", filename="data.csv")
        assert error.message == "Read failed"
        assert error.filename == "data.csv"
        assert error.error_code is None
        assert isinstance(error, IterableDataError)

    def test_read_error_with_code(self):
        """Test ReadError with error code."""
        error = ReadError("Read failed", filename="data.json", error_code="READ_ERR")
        assert error.filename == "data.json"
        assert error.error_code == "READ_ERR"

    def test_write_error(self):
        """Test WriteError."""
        error = WriteError("Write failed", filename="output.csv")
        assert error.message == "Write failed"
        assert error.filename == "output.csv"
        assert error.error_code is None
        assert isinstance(error, IterableDataError)

    def test_streaming_not_supported_error(self):
        """Test StreamingNotSupportedError."""
        error = StreamingNotSupportedError("json", reason="Loads entire file")
        assert error.format_id == "json"
        assert error.reason == "Loads entire file"
        assert error.error_code == "STREAMING_NOT_SUPPORTED"
        assert "json" in str(error)
        assert isinstance(error, ReadError)


class TestResourceError:
    """Test resource error exceptions."""

    def test_resource_error(self):
        """Test ResourceError."""
        error = ResourceError("Resource error")
        assert error.message == "Resource error"
        assert error.error_code is None
        assert isinstance(error, IterableDataError)

    def test_stream_not_seekable_error(self):
        """Test StreamNotSeekableError."""
        error = StreamNotSeekableError(operation="reset")
        assert error.operation == "reset"
        assert error.error_code == "STREAM_NOT_SEEKABLE"
        assert "reset" in str(error)
        assert isinstance(error, ResourceError)

    def test_stream_not_seekable_error_no_operation(self):
        """Test StreamNotSeekableError without operation."""
        error = StreamNotSeekableError()
        assert error.operation is None
        assert "Stream is not seekable" in str(error)

    def test_resource_leak_error(self):
        """Test ResourceLeakError."""
        error = ResourceLeakError(resource_type="file handle")
        assert error.resource_type == "file handle"
        assert error.error_code == "RESOURCE_LEAK"
        assert "file handle" in str(error)
        assert isinstance(error, ResourceError)

    def test_resource_leak_error_no_type(self):
        """Test ResourceLeakError without resource type."""
        error = ResourceLeakError()
        assert error.resource_type is None
        assert "Resource leak detected" in str(error)


class TestExceptionHierarchy:
    """Test exception inheritance hierarchy."""

    def test_all_exceptions_inherit_from_base(self):
        """Test that all exceptions inherit from IterableDataError."""
        exceptions = [
            FormatError("test"),
            CodecError("test"),
            ReadError("test"),
            WriteError("test"),
            ResourceError("test"),
        ]
        for exc in exceptions:
            assert isinstance(exc, IterableDataError)

    def test_format_exceptions_inherit_from_format_error(self):
        """Test that format-specific exceptions inherit from FormatError."""
        assert issubclass(FormatNotSupportedError, FormatError)
        assert issubclass(FormatDetectionError, FormatError)
        assert issubclass(FormatParseError, FormatError)

    def test_codec_exceptions_inherit_from_codec_error(self):
        """Test that codec-specific exceptions inherit from CodecError."""
        assert issubclass(CodecNotSupportedError, CodecError)
        assert issubclass(CodecDecompressionError, CodecError)
        assert issubclass(CodecCompressionError, CodecError)

    def test_streaming_inherits_from_read_error(self):
        """Test that StreamingNotSupportedError inherits from ReadError."""
        assert issubclass(StreamingNotSupportedError, ReadError)

    def test_resource_exceptions_inherit_from_resource_error(self):
        """Test that resource-specific exceptions inherit from ResourceError."""
        assert issubclass(StreamNotSeekableError, ResourceError)
        assert issubclass(ResourceLeakError, ResourceError)
