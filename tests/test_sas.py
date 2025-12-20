# -*- coding: utf-8 -*- 
import pytest
import os
from iterable.datatypes import SASIterable
from fixdata import FIXTURES

# Note: SAS files require actual .sas7bdat files
# This test will be skipped if pyreadstat/sas7bdat is not available
# or if fixture file doesn't exist

FIXTURE_FILE = 'fixtures/2cols6rows.sas7bdat'

@pytest.mark.skipif(not os.path.exists(FIXTURE_FILE), reason="SAS fixture file not found")
class TestSAS:
    def test_id(self):
        try:
            datatype_id = SASIterable.id()
            assert datatype_id == 'sas7bdat'
        except ImportError:
            pytest.skip("SAS support requires pyreadstat or sas7bdat package")

    def test_flatonly(self):
        try:
            flag = SASIterable.is_flatonly()
            assert flag == True
        except ImportError:
            pytest.skip("SAS support requires pyreadstat or sas7bdat package")

    def test_openclose(self):
        try:
            iterable = SASIterable(FIXTURE_FILE)        
            iterable.close()
        except ImportError:
            pytest.skip("SAS support requires pyreadstat or sas7bdat package")

    def test_has_totals(self):
        try:
            iterable = SASIterable(FIXTURE_FILE)
            assert SASIterable.has_totals() == True
            total = iterable.totals()
            assert total > 0
            iterable.close()
        except ImportError:
            pytest.skip("SAS support requires pyreadstat or sas7bdat package")

    def test_read(self):
        try:
            iterable = SASIterable(FIXTURE_FILE)
            row = iterable.read()
            assert isinstance(row, dict)
            iterable.close()
        except ImportError:
            pytest.skip("SAS support requires pyreadstat or sas7bdat package")
