# -*- coding: utf-8 -*- 
import pytest
import os
from iterable.datatypes import PXIterable
from fixdata import FIXTURES

FIXTURE_FILE = 'fixtures/2cols6rows.px'

@pytest.mark.skipif(not os.path.exists(FIXTURE_FILE), reason="PC-Axis fixture file not found")
class TestPX:
    def test_id(self):
        datatype_id = PXIterable.id()
        assert datatype_id == 'px'

    def test_flatonly(self):
        flag = PXIterable.is_flatonly()
        assert flag == True

    def test_openclose(self):
        iterable = PXIterable(FIXTURE_FILE)        
        iterable.close()

    def test_has_totals(self):
        iterable = PXIterable(FIXTURE_FILE)
        assert PXIterable.has_totals() == True
        total = iterable.totals()
        assert total == 18  # 3 ages * 2 genders * 3 years
        iterable.close()

    def test_read(self):
        iterable = PXIterable(FIXTURE_FILE)
        row = iterable.read()
        assert isinstance(row, dict)
        # Check that row has expected keys
        assert 'Age' in row
        assert 'Gender' in row
        assert 'Year' in row
        assert 'VALUE' in row
        iterable.close()

    def test_read_all(self):
        iterable = PXIterable(FIXTURE_FILE)
        rows = []
        try:
            while True:
                rows.append(iterable.read())
        except StopIteration:
            pass
        assert len(rows) == 18
        # Check first row
        assert rows[0]['Age'] == '0-4'
        assert rows[0]['Gender'] == 'Male'
        assert rows[0]['Year'] == '2020'
        assert rows[0]['VALUE'] == 100
        iterable.close()

    def test_read_bulk(self):
        iterable = PXIterable(FIXTURE_FILE)
        chunk = iterable.read_bulk(5)
        assert len(chunk) == 5
        assert all(isinstance(row, dict) for row in chunk)
        iterable.close()

    def test_metadata(self):
        iterable = PXIterable(FIXTURE_FILE)
        # Check that metadata is parsed
        assert hasattr(iterable, 'metadata')
        assert 'TITLE' in iterable.metadata or '_TITLE' in iterable.read()
        iterable.close()

    def test_reset(self):
        iterable = PXIterable(FIXTURE_FILE)
        row1 = iterable.read()
        iterable.reset()
        row2 = iterable.read()
        # After reset, should read from beginning
        assert row1 == row2
        iterable.close()
