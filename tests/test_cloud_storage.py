"""Tests for cloud storage support (S3, GCS, Azure)"""

import io
import tempfile
from unittest.mock import MagicMock, patch

import pytest

from iterable.helpers.detect import open_iterable


class TestCloudStorageURIDetection:
    """Test cloud storage URI detection"""

    def test_detect_s3_uri(self):
        """Test S3 URI detection"""
        from iterable.helpers.detect import _is_cloud_storage_uri

        assert _is_cloud_storage_uri("s3://bucket/file.csv") is True
        assert _is_cloud_storage_uri("s3a://bucket/file.csv") is True
        assert _is_cloud_storage_uri("/local/path/file.csv") is False
        assert _is_cloud_storage_uri("file.csv") is False

    def test_detect_gcs_uri(self):
        """Test GCS URI detection"""
        from iterable.helpers.detect import _is_cloud_storage_uri

        assert _is_cloud_storage_uri("gs://bucket/file.csv") is True
        assert _is_cloud_storage_uri("gcs://bucket/file.csv") is True
        assert _is_cloud_storage_uri("/local/path/file.csv") is False

    def test_detect_azure_uri(self):
        """Test Azure URI detection"""
        from iterable.helpers.detect import _is_cloud_storage_uri

        assert _is_cloud_storage_uri("az://container/file.csv") is True
        assert _is_cloud_storage_uri("abfs://container/file.csv") is True
        assert _is_cloud_storage_uri("abfss://container/file.csv") is True

    def test_get_cloud_backend(self):
        """Test getting cloud backend package name"""
        from iterable.helpers.detect import _get_cloud_backend

        assert _get_cloud_backend("s3://bucket/file.csv") == "s3fs"
        assert _get_cloud_backend("gs://bucket/file.csv") == "gcsfs"
        assert _get_cloud_backend("az://container/file.csv") == "adlfs"
        assert _get_cloud_backend("/local/path/file.csv") is None


class TestCloudStorageWithoutDependencies:
    """Test cloud storage error handling when dependencies are missing"""

    def test_s3_uri_without_fsspec(self):
        """Test S3 URI raises ImportError when fsspec is missing"""
        with patch("iterable.helpers.detect.fsspec", None):
            with pytest.raises(ImportError, match="fsspec"):
                open_iterable("s3://bucket/file.csv")

    def test_s3_uri_without_s3fs(self):
        """Test S3 URI raises ImportError when s3fs is missing"""
        # Mock fsspec import success but s3fs import failure
        mock_fsspec = MagicMock()
        with patch("iterable.helpers.detect.fsspec", mock_fsspec):
            with patch("builtins.__import__", side_effect=lambda x, **kwargs: (_ if x != "s3fs" else (_ for _ in ()).throw(ImportError("No module named 's3fs'")))):
                with pytest.raises(ImportError, match="s3fs"):
                    open_iterable("s3://bucket/file.csv")


class TestCloudStorageWithMocks:
    """Test cloud storage functionality with mocked fsspec"""

    @pytest.fixture
    def mock_fsspec_open(self):
        """Create a mock fsspec.open that returns a file-like object"""
        mock_file = io.BytesIO(b"name,age\nAlice,30\nBob,25\n")
        mock_context = MagicMock()
        mock_context.__enter__ = MagicMock(return_value=mock_file)
        mock_context.__exit__ = MagicMock(return_value=False)
        mock_open = MagicMock(return_value=mock_context)
        return mock_open

    def test_s3_csv_read(self, mock_fsspec_open):
        """Test reading CSV from S3"""
        with patch("iterable.helpers.detect.fsspec") as mock_fsspec_module:
            mock_fsspec_module.open = mock_fsspec_open
            with patch("builtins.__import__", return_value=MagicMock()):  # Mock s3fs import
                with open_iterable("s3://bucket/data.csv") as source:
                    rows = list(source)
                    assert len(rows) == 2
                    assert rows[0]["name"] == "Alice"
                    assert rows[0]["age"] == "30"

    def test_gcs_jsonl_read(self, mock_fsspec_open):
        """Test reading JSONL from GCS"""
        mock_file = io.BytesIO(b'{"name":"Alice","age":30}\n{"name":"Bob","age":25}\n')
        mock_context = MagicMock()
        mock_context.__enter__ = MagicMock(return_value=mock_file)
        mock_context.__exit__ = MagicMock(return_value=False)
        mock_open = MagicMock(return_value=mock_context)

        with patch("iterable.helpers.detect.fsspec") as mock_fsspec_module:
            mock_fsspec_module.open = mock_open
            with patch("builtins.__import__", return_value=MagicMock()):  # Mock gcsfs import
                with open_iterable("gs://bucket/data.jsonl") as source:
                    rows = list(source)
                    assert len(rows) == 2
                    assert rows[0]["name"] == "Alice"
                    assert rows[0]["age"] == 30

    def test_azure_uri_detection(self):
        """Test Azure URI is detected correctly"""
        from iterable.helpers.detect import _is_cloud_storage_uri, _get_cloud_backend

        assert _is_cloud_storage_uri("az://container/file.csv") is True
        assert _get_cloud_backend("az://container/file.csv") == "adlfs"

    def test_compressed_file_from_s3(self, mock_fsspec_open):
        """Test reading compressed file from S3"""
        # Create a gzipped CSV content
        import gzip

        csv_content = b"name,age\nAlice,30\nBob,25\n"
        gzipped_content = gzip.compress(csv_content)
        mock_file = io.BytesIO(gzipped_content)
        mock_context = MagicMock()
        mock_context.__enter__ = MagicMock(return_value=mock_file)
        mock_context.__exit__ = MagicMock(return_value=False)
        mock_open = MagicMock(return_value=mock_context)

        with patch("iterable.helpers.detect.fsspec") as mock_fsspec_module:
            mock_fsspec_module.open = mock_open
            with patch("builtins.__import__", return_value=MagicMock()):  # Mock s3fs import
                with open_iterable("s3://bucket/data.csv.gz") as source:
                    rows = list(source)
                    assert len(rows) == 2
                    assert rows[0]["name"] == "Alice"

    def test_storage_options_passed_to_fsspec(self):
        """Test that storage_options are passed to fsspec.open"""
        mock_file = io.BytesIO(b"name,age\nAlice,30\n")
        mock_context = MagicMock()
        mock_context.__enter__ = MagicMock(return_value=mock_file)
        mock_context.__exit__ = MagicMock(return_value=False)
        mock_open = MagicMock(return_value=mock_context)

        storage_options = {"key": "test-key", "secret": "test-secret"}

        with patch("iterable.helpers.detect.fsspec") as mock_fsspec_module:
            mock_fsspec_module.open = mock_open
            with patch("builtins.__import__", return_value=MagicMock()):
                with open_iterable("s3://bucket/data.csv", iterableargs={"storage_options": storage_options}):
                    pass

                # Verify fsspec.open was called with storage_options
                mock_open.assert_called_once()
                call_kwargs = mock_open.call_args[1]
                assert call_kwargs["key"] == "test-key"
                assert call_kwargs["secret"] == "test-secret"

    def test_duckdb_engine_not_supported(self, mock_fsspec_open):
        """Test that DuckDB engine raises error for cloud storage"""
        with patch("iterable.helpers.detect.fsspec") as mock_fsspec_module:
            mock_fsspec_module.open = mock_fsspec_open
            with patch("builtins.__import__", return_value=MagicMock()):
                with pytest.raises(ValueError, match="DuckDB engine does not support cloud storage"):
                    open_iterable("s3://bucket/data.csv", engine="duckdb")

    def test_local_file_still_works(self):
        """Test that local file paths still work (backward compatibility)"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("name,age\nAlice,30\nBob,25\n")
            temp_path = f.name

        try:
            with open_iterable(temp_path) as source:
                rows = list(source)
                assert len(rows) == 2
                assert rows[0]["name"] == "Alice"
        finally:
            import os

            os.unlink(temp_path)

    def test_cloud_uri_format_detection(self, mock_fsspec_open):
        """Test format detection works with cloud URIs"""
        # Test CSV detection
        mock_file = io.BytesIO(b"name,age\nAlice,30\n")
        mock_context = MagicMock()
        mock_context.__enter__ = MagicMock(return_value=mock_file)
        mock_context.__exit__ = MagicMock(return_value=False)
        mock_open = MagicMock(return_value=mock_context)

        with patch("iterable.helpers.detect.fsspec") as mock_fsspec_module:
            mock_fsspec_module.open = mock_open
            with patch("builtins.__import__", return_value=MagicMock()):
                with open_iterable("s3://bucket/data.csv") as source:
                    # Should work as CSV
                    assert hasattr(source, "read")

        # Test JSONL detection
        mock_file = io.BytesIO(b'{"name":"Alice"}\n')
        mock_context = MagicMock()
        mock_context.__enter__ = MagicMock(return_value=mock_file)
        mock_context.__exit__ = MagicMock(return_value=False)
        mock_open = MagicMock(return_value=mock_context)

        with patch("iterable.helpers.detect.fsspec") as mock_fsspec_module:
            mock_fsspec_module.open = mock_open
            with patch("builtins.__import__", return_value=MagicMock()):
                with open_iterable("gs://bucket/data.jsonl") as source:
                    # Should work as JSONL
                    assert hasattr(source, "read")


class TestCloudStorageErrorHandling:
    """Test error handling for cloud storage"""

    def test_file_not_found_error(self):
        """Test FileNotFoundError for non-existent cloud files"""
        mock_context = MagicMock()
        mock_context.__enter__ = MagicMock(side_effect=FileNotFoundError("NoSuchKey: The specified key does not exist"))
        mock_context.__exit__ = MagicMock(return_value=False)
        mock_open = MagicMock(return_value=mock_context)

        with patch("iterable.helpers.detect.fsspec") as mock_fsspec_module:
            mock_fsspec_module.open = mock_open
            with patch("builtins.__import__", return_value=MagicMock()):
                with pytest.raises(FileNotFoundError, match="File not found in cloud storage"):
                    open_iterable("s3://bucket/nonexistent.csv")

    def test_authentication_error(self):
        """Test authentication error handling"""
        mock_context = MagicMock()
        mock_context.__enter__ = MagicMock(side_effect=Exception("NoCredentialsError: Unable to locate credentials"))
        mock_context.__exit__ = MagicMock(return_value=False)
        mock_open = MagicMock(return_value=mock_context)

        with patch("iterable.helpers.detect.fsspec") as mock_fsspec_module:
            mock_fsspec_module.open = mock_open
            with patch("builtins.__import__", return_value=MagicMock()):
                with pytest.raises(RuntimeError, match="Authentication failed"):
                    open_iterable("s3://bucket/data.csv")
