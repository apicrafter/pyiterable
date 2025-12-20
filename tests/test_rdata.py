# -*- coding: utf-8 -*- 
import pytest
import os
from iterable.datatypes import RDataIterable
from fixdata import FIXTURES

# Note: RData files require actual .rdata or .RData files
# This test will be skipped if pyreadr is not available
# or if fixture file doesn't exist

FIXTURE_FILE = 'fixtures/2cols6rows.rdata'

@pytest.mark.skipif(not os.path.exists(FIXTURE_FILE), reason="RData fixture file not found")
class TestRData:
    def test_id(self):
        try:
            datatype_id = RDataIterable.id()
            assert datatype_id == 'rdata'
        except ImportError:
            pytest.skip("RData support requires pyreadr package")

    def test_flatonly(self):
        try:
            flag = RDataIterable.is_flatonly()
            assert flag == True
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
            assert RDataIterable.has_totals() == True
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
