import os

import pytest

from iterable.datatypes import SPSSIterable

# Note: SPSS files require actual .sav files
# This test will be skipped if pyreadstat is not available
# or if fixture file doesn't exist

FIXTURE_FILE = "fixtures/2cols6rows.sav"


@pytest.mark.skipif(not os.path.exists(FIXTURE_FILE), reason="SPSS fixture file not found")
class TestSPSS:
    def test_id(self):
        try:
            datatype_id = SPSSIterable.id()
            assert datatype_id == "sav"
        except ImportError:
            pytest.skip("SPSS support requires pyreadstat package")

    def test_flatonly(self):
        try:
            flag = SPSSIterable.is_flatonly()
            assert flag
        except ImportError:
            pytest.skip("SPSS support requires pyreadstat package")

    def test_openclose(self):
        try:
            iterable = SPSSIterable(FIXTURE_FILE)
            iterable.close()
        except ImportError:
            pytest.skip("SPSS support requires pyreadstat package")

    def test_has_totals(self):
        try:
            iterable = SPSSIterable(FIXTURE_FILE)
            assert SPSSIterable.has_totals()
            total = iterable.totals()
            assert total > 0
            iterable.close()
        except ImportError:
            pytest.skip("SPSS support requires pyreadstat package")

    def test_read(self):
        try:
            iterable = SPSSIterable(FIXTURE_FILE)
            row = iterable.read()
            assert isinstance(row, dict)
            iterable.close()
        except ImportError:
            pytest.skip("SPSS support requires pyreadstat package")
