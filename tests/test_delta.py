import os

import pytest

from iterable.datatypes import DeltaIterable

# Note: Delta Lake requires a delta table directory
# This test will be skipped if deltalake is not available
# or if fixture directory doesn't exist

FIXTURE_DIR = "fixtures/2cols6rows_delta"


@pytest.mark.skipif(not os.path.exists(FIXTURE_DIR), reason="Delta Lake fixture directory not found")
class TestDelta:
    def test_id(self):
        try:
            datatype_id = DeltaIterable.id()
            assert datatype_id == "delta"
        except ImportError:
            pytest.skip("Delta Lake support requires deltalake package")

    def test_flatonly(self):
        try:
            flag = DeltaIterable.is_flatonly()
            assert flag
        except ImportError:
            pytest.skip("Delta Lake support requires deltalake package")

    def test_openclose(self):
        try:
            iterable = DeltaIterable(FIXTURE_DIR)
            iterable.close()
        except ImportError:
            pytest.skip("Delta Lake support requires deltalake package")

    def test_has_totals(self):
        try:
            iterable = DeltaIterable(FIXTURE_DIR)
            assert DeltaIterable.has_totals()
            total = iterable.totals()
            assert total >= 0
            iterable.close()
        except ImportError:
            pytest.skip("Delta Lake support requires deltalake package")

    def test_read(self):
        try:
            iterable = DeltaIterable(FIXTURE_DIR)
            row = iterable.read()
            assert isinstance(row, dict)
            iterable.close()
        except ImportError:
            pytest.skip("Delta Lake support requires deltalake package")

    def test_has_tables(self):
        """Test has_tables static method"""
        try:
            # Delta returns False for single table directories (most common case)
            assert DeltaIterable.has_tables() is False
        except ImportError:
            pytest.skip("Delta Lake support requires deltalake package")

    def test_list_tables(self):
        """Test list_tables method (returns None for single table directories)"""
        try:
            iterable = DeltaIterable(FIXTURE_DIR)
            # For single table directories, list_tables should return None
            tables = iterable.list_tables()
            assert tables is None or isinstance(tables, list)
            iterable.close()
        except ImportError:
            pytest.skip("Delta Lake support requires deltalake package")

    def test_list_tables_with_filename(self):
        """Test list_tables with filename parameter"""
        try:
            iterable = DeltaIterable(FIXTURE_DIR)
            # Should work with filename parameter too
            tables = iterable.list_tables(FIXTURE_DIR)
            assert tables is None or isinstance(tables, list)
            iterable.close()
        except ImportError:
            pytest.skip("Delta Lake support requires deltalake package")
