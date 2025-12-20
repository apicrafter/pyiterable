# -*- coding: utf-8 -*- 
import pytest
import os
from iterable.datatypes import DeltaIterable

# Note: Delta Lake requires a delta table directory
# This test will be skipped if deltalake is not available
# or if fixture directory doesn't exist

FIXTURE_DIR = 'fixtures/2cols6rows_delta'

@pytest.mark.skipif(not os.path.exists(FIXTURE_DIR), reason="Delta Lake fixture directory not found")
class TestDelta:
    def test_id(self):
        try:
            datatype_id = DeltaIterable.id()
            assert datatype_id == 'delta'
        except ImportError:
            pytest.skip("Delta Lake support requires deltalake package")

    def test_flatonly(self):
        try:
            flag = DeltaIterable.is_flatonly()
            assert flag == True
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
            assert DeltaIterable.has_totals() == True
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
