"""Tests for DataFrame bridges (Pandas, Polars, Dask)."""

from unittest.mock import patch

import pytest

from iterable.helpers.bridges import to_dask
from iterable.helpers.detect import open_iterable


class TestPandasBridge:
    """Test to_pandas() method."""

    def test_to_pandas_single_dataframe(self):
        """Test converting entire iterable to single DataFrame."""
        try:
            import pandas as pd
        except ImportError:
            pytest.skip("pandas not installed")

        with open_iterable("fixtures/2cols6rows.csv") as source:
            df = source.to_pandas()

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 6
        assert list(df.columns) == ["id", "name"]
        assert df.iloc[0]["id"] == 1
        assert df.iloc[0]["name"] == "Alice"

    def test_to_pandas_chunked(self):
        """Test converting iterable to chunked DataFrames."""
        try:
            import pandas as pd
        except ImportError:
            pytest.skip("pandas not installed")

        with open_iterable("fixtures/2cols6rows.csv") as source:
            chunks = list(source.to_pandas(chunksize=2))

        assert len(chunks) == 3  # 6 rows / 2 = 3 chunks
        assert all(isinstance(chunk, pd.DataFrame) for chunk in chunks)
        assert all(len(chunk) == 2 for chunk in chunks[:2])
        assert len(chunks[2]) == 2  # Last chunk also has 2 rows

        # Verify data integrity
        total_rows = sum(len(chunk) for chunk in chunks)
        assert total_rows == 6

    def test_to_pandas_empty(self):
        """Test converting empty iterable."""
        try:
            import pandas as pd
        except ImportError:
            pytest.skip("pandas not installed")

        # Create empty CSV file
        with open("testdata/empty.csv", "w") as f:
            f.write("id,name\n")

        try:
            with open_iterable("testdata/empty.csv") as source:
                df = source.to_pandas()

            assert isinstance(df, pd.DataFrame)
            assert len(df) == 0
            assert list(df.columns) == ["id", "name"]
        finally:
            import os

            if os.path.exists("testdata/empty.csv"):
                os.remove("testdata/empty.csv")

    def test_to_pandas_nested_data(self):
        """Test converting iterable with nested data structures."""
        try:
            import pandas as pd
        except ImportError:
            pytest.skip("pandas not installed")

        # Create JSONL with nested data
        with open("testdata/nested.jsonl", "w") as f:
            f.write('{"id": 1, "data": {"nested": "value"}}\n')
            f.write('{"id": 2, "data": {"nested": "value2"}}\n')

        try:
            with open_iterable("testdata/nested.jsonl") as source:
                df = source.to_pandas()

            assert isinstance(df, pd.DataFrame)
            assert len(df) == 2
            assert "id" in df.columns
            assert "data" in df.columns
            # Nested data should be preserved as dict
            assert isinstance(df.iloc[0]["data"], dict)
        finally:
            import os

            if os.path.exists("testdata/nested.jsonl"):
                os.remove("testdata/nested.jsonl")

    def test_to_pandas_import_error(self):
        """Test ImportError when pandas is not installed."""
        with patch.dict("sys.modules", {"pandas": None}):
            with open_iterable("fixtures/2cols6rows.csv") as source:
                with pytest.raises(ImportError) as exc_info:
                    source.to_pandas()
                assert "pandas is required" in str(exc_info.value)
                assert "pip install pandas" in str(exc_info.value)

    def test_to_pandas_various_formats(self):
        """Test to_pandas with various formats."""
        try:
            import pandas as pd
        except ImportError:
            pytest.skip("pandas not installed")

        # Test with JSONL
        with open("testdata/test.jsonl", "w") as f:
            f.write('{"a": 1, "b": 2}\n')
            f.write('{"a": 3, "b": 4}\n')

        try:
            with open_iterable("testdata/test.jsonl") as source:
                df = source.to_pandas()
            assert isinstance(df, pd.DataFrame)
            assert len(df) == 2
        finally:
            import os

            if os.path.exists("testdata/test.jsonl"):
                os.remove("testdata/test.jsonl")


class TestPolarsBridge:
    """Test to_polars() method."""

    def test_to_polars_single_dataframe(self):
        """Test converting entire iterable to single DataFrame."""
        try:
            import polars as pl
        except ImportError:
            pytest.skip("polars not installed")

        with open_iterable("fixtures/2cols6rows.csv") as source:
            df = source.to_polars()

        assert isinstance(df, pl.DataFrame)
        assert len(df) == 6
        assert df.columns == ["id", "name"]
        assert df[0, "id"] == 1
        assert df[0, "name"] == "Alice"

    def test_to_polars_chunked(self):
        """Test converting iterable to chunked DataFrames."""
        try:
            import polars as pl
        except ImportError:
            pytest.skip("polars not installed")

        with open_iterable("fixtures/2cols6rows.csv") as source:
            chunks = list(source.to_polars(chunksize=2))

        assert len(chunks) == 3  # 6 rows / 2 = 3 chunks
        assert all(isinstance(chunk, pl.DataFrame) for chunk in chunks)
        assert all(len(chunk) == 2 for chunk in chunks[:2])
        assert len(chunks[2]) == 2  # Last chunk also has 2 rows

        # Verify data integrity
        total_rows = sum(len(chunk) for chunk in chunks)
        assert total_rows == 6

    def test_to_polars_empty(self):
        """Test converting empty iterable."""
        try:
            import polars as pl
        except ImportError:
            pytest.skip("polars not installed")

        # Create empty CSV file
        with open("testdata/empty.csv", "w") as f:
            f.write("id,name\n")

        try:
            with open_iterable("testdata/empty.csv") as source:
                df = source.to_polars()

            assert isinstance(df, pl.DataFrame)
            assert len(df) == 0
            assert df.columns == ["id", "name"]
        finally:
            import os

            if os.path.exists("testdata/empty.csv"):
                os.remove("testdata/empty.csv")

    def test_to_polars_nested_data(self):
        """Test converting iterable with nested data structures."""
        try:
            import polars as pl
        except ImportError:
            pytest.skip("polars not installed")

        # Create JSONL with nested data
        with open("testdata/nested.jsonl", "w") as f:
            f.write('{"id": 1, "data": {"nested": "value"}}\n')
            f.write('{"id": 2, "data": {"nested": "value2"}}\n')

        try:
            with open_iterable("testdata/nested.jsonl") as source:
                df = source.to_polars()

            assert isinstance(df, pl.DataFrame)
            assert len(df) == 2
            assert "id" in df.columns
            assert "data" in df.columns
        finally:
            import os

            if os.path.exists("testdata/nested.jsonl"):
                os.remove("testdata/nested.jsonl")

    def test_to_polars_import_error(self):
        """Test ImportError when polars is not installed."""
        with patch.dict("sys.modules", {"polars": None}):
            with open_iterable("fixtures/2cols6rows.csv") as source:
                with pytest.raises(ImportError) as exc_info:
                    source.to_polars()
                assert "polars is required" in str(exc_info.value)
                assert "pip install polars" in str(exc_info.value)

    def test_to_polars_various_formats(self):
        """Test to_polars with various formats."""
        try:
            import polars as pl
        except ImportError:
            pytest.skip("polars not installed")

        # Test with JSONL
        with open("testdata/test.jsonl", "w") as f:
            f.write('{"a": 1, "b": 2}\n')
            f.write('{"a": 3, "b": 4}\n')

        try:
            with open_iterable("testdata/test.jsonl") as source:
                df = source.to_polars()
            assert isinstance(df, pl.DataFrame)
            assert len(df) == 2
        finally:
            import os

            if os.path.exists("testdata/test.jsonl"):
                os.remove("testdata/test.jsonl")


class TestDaskBridge:
    """Test to_dask() method and helper function."""

    def test_to_dask_single_file(self):
        """Test converting single file iterable to Dask DataFrame."""
        try:
            import dask.dataframe as dd
        except ImportError:
            pytest.skip("dask not installed")

        with open_iterable("fixtures/2cols6rows.csv") as source:
            ddf = source.to_dask()

        assert isinstance(ddf, dd.DataFrame)
        # Compute to verify data
        df = ddf.compute()
        assert len(df) == 6
        assert list(df.columns) == ["id", "name"]

    def test_to_dask_empty(self):
        """Test converting empty iterable."""
        try:
            import dask.dataframe as dd
        except ImportError:
            pytest.skip("dask not installed")

        # Create empty CSV file
        with open("testdata/empty.csv", "w") as f:
            f.write("id,name\n")

        try:
            with open_iterable("testdata/empty.csv") as source:
                ddf = source.to_dask()

            assert isinstance(ddf, dd.DataFrame)
            df = ddf.compute()
            assert len(df) == 0
            assert list(df.columns) == ["id", "name"]
        finally:
            import os

            if os.path.exists("testdata/empty.csv"):
                os.remove("testdata/empty.csv")

    def test_to_dask_import_error(self):
        """Test ImportError when dask is not installed."""
        with patch.dict("sys.modules", {"dask": None}):
            with open_iterable("fixtures/2cols6rows.csv") as source:
                with pytest.raises(ImportError) as exc_info:
                    source.to_dask()
                assert "dask[dataframe] is required" in str(exc_info.value)
                assert "pip install 'dask[dataframe]'" in str(exc_info.value)

    def test_to_dask_multi_file_helper(self):
        """Test to_dask() helper function with multiple files."""
        try:
            import dask.dataframe as dd
        except ImportError:
            pytest.skip("dask not installed")

        # Create test files
        with open("testdata/file1.csv", "w") as f:
            f.write("id,name\n")
            f.write("1,Alice\n")
            f.write("2,Bob\n")

        with open("testdata/file2.jsonl", "w") as f:
            f.write('{"id": 3, "name": "Charlie"}\n')
            f.write('{"id": 4, "name": "Diana"}\n')

        try:
            ddf = to_dask(["testdata/file1.csv", "testdata/file2.jsonl"])

            assert isinstance(ddf, dd.DataFrame)
            df = ddf.compute()
            assert len(df) == 4
            assert list(df.columns) == ["id", "name"]
            # Verify data from both files
            assert df.iloc[0]["name"] == "Alice"
            assert df.iloc[3]["name"] == "Diana"
        finally:
            import os

            for fname in ["testdata/file1.csv", "testdata/file2.jsonl"]:
                if os.path.exists(fname):
                    os.remove(fname)

    def test_to_dask_multi_file_single_string(self):
        """Test to_dask() helper with single file as string."""
        try:
            import dask.dataframe as dd
        except ImportError:
            pytest.skip("dask not installed")

        with open("testdata/single.csv", "w") as f:
            f.write("id,name\n")
            f.write("1,Test\n")

        try:
            ddf = to_dask("testdata/single.csv")
            assert isinstance(ddf, dd.DataFrame)
            df = ddf.compute()
            assert len(df) == 1
        finally:
            import os

            if os.path.exists("testdata/single.csv"):
                os.remove("testdata/single.csv")

    def test_to_dask_multi_file_empty_list(self):
        """Test to_dask() helper with empty file list."""
        with pytest.raises(ValueError) as exc_info:
            to_dask([])
        assert "files list cannot be empty" in str(exc_info.value)

    def test_to_dask_multi_file_invalid_type(self):
        """Test to_dask() helper with invalid file type."""
        with pytest.raises(ValueError) as exc_info:
            to_dask(123)  # Invalid type
        assert "files must be a string or list of strings" in str(exc_info.value)

    def test_to_dask_multi_file_all_empty(self):
        """Test to_dask() helper when all files are empty."""
        try:
            import dask.dataframe as dd
        except ImportError:
            pytest.skip("dask not installed")

        # Create empty files
        with open("testdata/empty1.csv", "w") as f:
            f.write("id,name\n")
        with open("testdata/empty2.csv", "w") as f:
            f.write("id,name\n")

        try:
            ddf = to_dask(["testdata/empty1.csv", "testdata/empty2.csv"])
            assert isinstance(ddf, dd.DataFrame)
            df = ddf.compute()
            assert len(df) == 0
        finally:
            import os

            for fname in ["testdata/empty1.csv", "testdata/empty2.csv"]:
                if os.path.exists(fname):
                    os.remove(fname)
