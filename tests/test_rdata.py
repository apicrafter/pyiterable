import os

import pytest

from iterable.datatypes import RDataIterable

# Note: RData files require actual .rdata or .RData files
# This test will be skipped if pyreadr is not available
# or if fixture file doesn't exist

FIXTURE_FILE = "fixtures/2cols6rows.rdata"


@pytest.mark.skipif(not os.path.exists(FIXTURE_FILE), reason="RData fixture file not found")
class TestRData:
    def test_id(self):
        try:
            datatype_id = RDataIterable.id()
            assert datatype_id == "rdata"
        except ImportError:
            pytest.skip("RData support requires pyreadr package")

    def test_flatonly(self):
        try:
            flag = RDataIterable.is_flatonly()
            assert flag
        except ImportError:
            pytest.skip("RData support requires pyreadr package")

    def test_openclose(self):
        try:
            iterable = RDataIterable(FIXTURE_FILE)
            iterable.close()
        except ImportError:
            pytest.skip("RData support requires pyreadr package")

    def test_has_totals(self):
        try:
            iterable = RDataIterable(FIXTURE_FILE)
            assert RDataIterable.has_totals()
            total = iterable.totals()
            assert total > 0
            iterable.close()
        except ImportError:
            pytest.skip("RData support requires pyreadr package")

    def test_read(self):
        try:
            iterable = RDataIterable(FIXTURE_FILE)
            row = iterable.read()
            assert isinstance(row, dict)
            iterable.close()
        except ImportError:
            pytest.skip("RData support requires pyreadr package")

    def test_has_tables(self):
        try:
            flag = RDataIterable.has_tables()
            assert flag is True
        except ImportError:
            pytest.skip("RData support requires pyreadr package")

    def test_list_tables_instance_method(self):
        """Test list_tables on an already-opened instance"""
        try:
            iterable = RDataIterable(FIXTURE_FILE)
            # Read a row to ensure data is loaded
            _ = iterable.read()
            # Now list tables
            objects = iterable.list_tables()
            assert isinstance(objects, list)
            assert len(objects) > 0
            iterable.close()
        except ImportError:
            pytest.skip("RData support requires pyreadr package")

    def test_list_tables_with_filename(self):
        """Test list_tables with filename parameter (class-like usage)"""
        try:
            iterable = RDataIterable(FIXTURE_FILE)
            objects = iterable.list_tables(FIXTURE_FILE)
            assert isinstance(objects, list)
            assert len(objects) > 0
            iterable.close()
        except ImportError:
            pytest.skip("RData support requires pyreadr package")
