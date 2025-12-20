# -*- coding: utf-8 -*- 
import pytest
import os
from iterable.datatypes import StataIterable
from fixdata import FIXTURES

# Note: Stata files require actual .dta files
# This test will be skipped if pyreadstat is not available
# or if fixture file doesn't exist

FIXTURE_FILE = 'fixtures/2cols6rows.dta'

@pytest.mark.skipif(not os.path.exists(FIXTURE_FILE), reason="Stata fixture file not found")
class TestStata:
    def test_id(self):
        try:
            datatype_id = StataIterable.id()
            assert datatype_id == 'dta'
        except ImportError:
            pytest.skip("Stata support requires pyreadstat package")

    def test_flatonly(self):
        try:
            flag = StataIterable.is_flatonly()
            assert flag == True
        except ImportError:
            pytest.skip("Stata support requires pyreadstat package")

    def test_openclose(self):
        try:
            iterable = StataIterable(FIXTURE_FILE)        
            iterable.close()
        except ImportError:
            pytest.skip("Stata support requires pyreadstat package")

    def test_has_totals(self):
        try:
            iterable = StataIterable(FIXTURE_FILE)
            assert StataIterable.has_totals() == True
            total = iterable.totals()
            assert total > 0
            iterable.close()
        except ImportError:
            pytest.skip("Stata support requires pyreadstat package")

    def test_read(self):
        try:
            iterable = StataIterable(FIXTURE_FILE)
            row = iterable.read()
            assert isinstance(row, dict)
            iterable.close()
        except ImportError:
            pytest.skip("Stata support requires pyreadstat package")
