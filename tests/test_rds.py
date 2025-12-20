# -*- coding: utf-8 -*- 
import pytest
import os
from iterable.datatypes import RDSIterable
from fixdata import FIXTURES

# Note: RDS files require actual .rds files
# This test will be skipped if pyreadr is not available
# or if fixture file doesn't exist

FIXTURE_FILE = 'fixtures/2cols6rows.rds'

@pytest.mark.skipif(not os.path.exists(FIXTURE_FILE), reason="RDS fixture file not found")
class TestRDS:
    def test_id(self):
        try:
            datatype_id = RDSIterable.id()
            assert datatype_id == 'rds'
        except ImportError:
            pytest.skip("RDS support requires pyreadr package")

    def test_flatonly(self):
        try:
            flag = RDSIterable.is_flatonly()
            assert flag == True
        except ImportError:
            pytest.skip("RDS support requires pyreadr package")

    def test_openclose(self):
        try:
            iterable = RDSIterable(FIXTURE_FILE)        
            iterable.close()
        except ImportError:
            pytest.skip("RDS support requires pyreadr package")

    def test_has_totals(self):
        try:
            iterable = RDSIterable(FIXTURE_FILE)
            assert RDSIterable.has_totals() == True
            total = iterable.totals()
            assert total > 0
            iterable.close()
        except ImportError:
            pytest.skip("RDS support requires pyreadr package")

    def test_read(self):
        try:
            iterable = RDSIterable(FIXTURE_FILE)
            row = iterable.read()
            assert isinstance(row, dict)
            iterable.close()
        except ImportError:
            pytest.skip("RDS support requires pyreadr package")
