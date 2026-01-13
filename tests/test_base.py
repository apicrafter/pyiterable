"""Tests for iterable/base.py"""

import io

import pytest

from iterable.base import (
    ITERABLE_TYPE_CODEC,
    ITERABLE_TYPE_FILE,
    ITERABLE_TYPE_STREAM,
    BaseCodec,
    BaseFileIterable,
    BaseIterable,
)


class TestBaseCodec:
    """Test BaseCodec class"""

    def test_init_with_filename(self):
        """Test BaseCodec initialization with filename"""
        codec = BaseCodec(filename="test.txt")
        assert codec.filename == "test.txt"
        assert codec.mode == "r"
        assert codec._fileobj is None

    def test_init_with_fileobj(self):
        """Test BaseCodec initialization with file object"""
        fileobj = io.BytesIO(b"test data")
        codec = BaseCodec(fileobj=fileobj)
        assert codec._fileobj == fileobj
        assert codec.filename is None

    def test_init_with_mode(self):
        """Test BaseCodec initialization with mode"""
        codec = BaseCodec(filename="test.txt", mode="w")
        assert codec.mode == "w"

    def test_init_with_options(self):
        """Test BaseCodec initialization with options"""
        options = {"compression_level": 9, "custom_option": "value"}
        codec = BaseCodec(filename="test.txt", options=options)
        assert codec.compression_level == 9
        assert codec.custom_option == "value"

    def test_fileexts_not_implemented(self):
        """Test that fileexts raises NotImplementedError"""
        codec = BaseCodec()
        with pytest.raises(NotImplementedError):
            codec.fileexts()

    def test_open_not_implemented(self):
        """Test that open raises NotImplementedError"""
        codec = BaseCodec(filename="test.txt")
        with pytest.raises(NotImplementedError):
            codec.open()

    def test_close_not_implemented(self):
        """Test that close raises NotImplementedError"""
        codec = BaseCodec()
        with pytest.raises(NotImplementedError):
            codec.close()

    def test_fileobj(self):
        """Test fileobj method"""
        fileobj = io.BytesIO(b"test")
        codec = BaseCodec(fileobj=fileobj)
        assert codec.fileobj() == fileobj

    def test_reset(self):
        """Test reset method"""
        codec = BaseCodec(filename="test.txt")
        # Should call close and open, but will raise NotImplementedError
        with pytest.raises(NotImplementedError):
            codec.reset()

    def test_context_manager(self):
        """Test context manager protocol"""
        # This will fail because open() is not implemented
        codec = BaseCodec(filename="test.txt")
        with pytest.raises(NotImplementedError):
            with codec:
                pass

    def test_textIO(self):
        """Test textIO method"""
        fileobj = io.BytesIO(b"test")
        codec = BaseCodec(fileobj=fileobj)
        text_wrapper = codec.textIO(encoding="utf-8")
        assert isinstance(text_wrapper, io.TextIOWrapper)


class TestBaseIterable:
    """Test BaseIterable class"""

    def test_init(self):
        """Test BaseIterable initialization"""
        iterable = BaseIterable()
        assert iterable is not None

    def test_reset_not_implemented(self):
        """Test that reset raises NotImplementedError"""
        iterable = BaseIterable()
        with pytest.raises(NotImplementedError):
            iterable.reset()

    def test_id_not_implemented(self):
        """Test that id raises NotImplementedError"""
        with pytest.raises(NotImplementedError):
            BaseIterable.id()

    def test_has_totals(self):
        """Test has_totals returns False by default"""
        assert BaseIterable.has_totals() is False

    def test_read_not_implemented(self):
        """Test that read raises NotImplementedError"""
        iterable = BaseIterable()
        with pytest.raises(NotImplementedError):
            iterable.read()

    def test_read_bulk_not_implemented(self):
        """Test that read_bulk raises NotImplementedError"""
        iterable = BaseIterable()
        with pytest.raises(NotImplementedError):
            iterable.read_bulk()

    def test_is_flatonly(self):
        """Test is_flatonly returns False by default"""
        assert BaseIterable.is_flatonly() is False

    def test_is_flat(self):
        """Test is_flat raises NotImplementedError when not flatonly"""
        iterable = BaseIterable()
        with pytest.raises(NotImplementedError):
            iterable.is_flat()

    def test_is_streaming(self):
        """Test is_streaming returns False by default"""
        iterable = BaseIterable()
        assert iterable.is_streaming() is False

    def test_write_not_implemented(self):
        """Test that write raises NotImplementedError"""
        iterable = BaseIterable()
        with pytest.raises(NotImplementedError):
            iterable.write({})

    def test_write_bulk_not_implemented(self):
        """Test that write_bulk raises NotImplementedError"""
        iterable = BaseIterable()
        with pytest.raises(NotImplementedError):
            iterable.write_bulk([{}])

    def test_iter_protocol(self):
        """Test iterator protocol"""
        iterable = BaseIterable()
        # __iter__ returns self
        assert iter(iterable) == iterable

    def test_next_not_implemented(self):
        """Test that __next__ raises NotImplementedError via read"""
        iterable = BaseIterable()
        with pytest.raises(NotImplementedError):
            next(iterable)


class MockCodec(BaseCodec):
    """Mock codec for testing"""

    def __init__(self, filename=None, fileobj=None, mode="r", open_it=False, options=None):
        super().__init__(filename, fileobj, mode, open_it, options)
        self.opened = False

    @staticmethod
    def fileexts():
        return ["mock"]

    def open(self):
        if self.filename:
            mode_str = f"{self.mode}b" if self.mode in ("r", "w") else self.mode
            self._fileobj = open(self.filename, mode_str)
        self.opened = True

    def close(self):
        if self._fileobj:
            if hasattr(self._fileobj, "closed") and not self._fileobj.closed:
                self._fileobj.close()
            self._fileobj = None
        self.opened = False

    def fileobj(self):
        return self._fileobj


class TestBaseFileIterable:
    """Test BaseFileIterable class"""

    def test_init_with_filename(self, tmp_path):
        """Test BaseFileIterable initialization with filename"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test data")

        iterable = BaseFileIterable(filename=str(test_file), noopen=True)
        assert iterable.filename == str(test_file)
        assert iterable.stype == ITERABLE_TYPE_FILE
        assert iterable.fobj is None

    def test_init_with_stream(self):
        """Test BaseFileIterable initialization with stream"""
        stream = io.StringIO("test data")
        iterable = BaseFileIterable(stream=stream, noopen=True)
        assert iterable.stype == ITERABLE_TYPE_STREAM
        assert iterable.fobj == stream

    def test_init_with_codec(self, tmp_path):
        """Test BaseFileIterable initialization with codec"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test data")

        codec = MockCodec(filename=str(test_file), mode="r")
        iterable = BaseFileIterable(codec=codec, noopen=True)
        assert iterable.stype == ITERABLE_TYPE_CODEC
        assert iterable.codec == codec

    def test_init_no_source_raises_error(self):
        """Test that BaseFileIterable raises error with no source"""
        with pytest.raises(ValueError, match="requires filename, stream, or codec"):
            BaseFileIterable(noopen=True)

    def test_init_with_options(self, tmp_path):
        """Test BaseFileIterable initialization with options"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test data")

        options = {"custom_option": "value"}
        iterable = BaseFileIterable(filename=str(test_file), noopen=True, options=options)
        assert iterable.custom_option == "value"

    def test_open_file_type(self, tmp_path):
        """Test open method with file type"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test data")

        iterable = BaseFileIterable(filename=str(test_file), noopen=True)
        iterable.open()
        assert iterable.fobj is not None
        iterable.close()

    def test_open_file_type_binary(self, tmp_path):
        """Test open method with binary mode"""
        test_file = tmp_path / "test.bin"
        test_file.write_bytes(b"test data")

        iterable = BaseFileIterable(filename=str(test_file), binary=True, noopen=True, mode="r")
        iterable.open()
        assert iterable.fobj is not None
        assert iterable.binary is True
        iterable.close()

    def test_open_stream_type_raises_error(self):
        """Test open raises error for stream type"""
        stream = io.StringIO("test")
        iterable = BaseFileIterable(stream=stream, noopen=True)
        with pytest.raises(NotImplementedError):
            iterable.open()

    def test_reset_file_type(self, tmp_path):
        """Test reset method with file type"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("line1\nline2\nline3")

        iterable = BaseFileIterable(filename=str(test_file), noopen=False)
        # Read first line
        first_pos = iterable.fobj.tell()
        iterable.fobj.readline()
        assert iterable.fobj.tell() > first_pos

        # Reset should seek to beginning
        iterable.reset()
        assert iterable.fobj.tell() == 0
        iterable.close()

    def test_reset_codec_type(self, tmp_path):
        """Test reset method with codec type"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test data")

        codec = MockCodec(filename=str(test_file), mode="r", open_it=True)
        iterable = BaseFileIterable(codec=codec, noopen=False)
        # Set datamode as class attribute
        iterable.datamode = "text"
        # Reset should close and reopen
        iterable.reset()
        assert iterable.fobj is not None
        iterable.close()

    def test_reset_codec_write_mode(self, tmp_path):
        """Test reset with codec in write mode doesn't reset"""
        test_file = tmp_path / "test.txt"

        codec = MockCodec(filename=str(test_file), mode="w", open_it=True)
        iterable = BaseFileIterable(codec=codec, noopen=False, mode="w")
        iterable.datamode = "text"
        # In write mode, reset should not close the file
        iterable.reset()
        iterable.close()

    def test_close_file_type(self, tmp_path):
        """Test close method with file type"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test data")

        iterable = BaseFileIterable(filename=str(test_file), noopen=False)
        assert iterable.fobj is not None
        assert not iterable.fobj.closed

        iterable.close()
        assert iterable.fobj.closed

    def test_close_codec_type(self, tmp_path):
        """Test close method with codec type"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test data")

        codec = MockCodec(filename=str(test_file), mode="r", open_it=True)
        iterable = BaseFileIterable(codec=codec, noopen=False)
        iterable.datamode = "text"
        iterable.close()
        assert iterable.fobj is None

    def test_close_codec_type_no_fobj(self, tmp_path):
        """Test close with codec when fobj is None"""
        test_file = tmp_path / "test.txt"
        codec = MockCodec(filename=str(test_file), mode="r")
        iterable = BaseFileIterable(codec=codec, noopen=True)
        iterable.close()
        # Should close codec
        assert codec.opened is False

    def test_context_manager(self, tmp_path):
        """Test context manager protocol"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test data")

        with BaseFileIterable(filename=str(test_file), noopen=False) as iterable:
            assert iterable.fobj is not None
        # File should be closed after context exit
        assert iterable.fobj.closed

    def test_datamode_default(self, tmp_path):
        """Test that datamode defaults to 'text'"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test")

        iterable = BaseFileIterable(filename=str(test_file), noopen=True)
        assert iterable.datamode == "text"
