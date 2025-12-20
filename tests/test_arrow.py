# -*- coding: utf-8 -*- 
import pytest
import os
from iterable.datatypes import ArrowIterable
from fixdata import FIXTURES_TYPES, FIXTURES

# Create fixture file if it doesn't exist
FIXTURE_FILE = 'fixtures/2cols6rows.arrow'

def setup_module():
    """Create fixture file if it doesn't exist"""
    if not os.path.exists(FIXTURE_FILE):
        import pyarrow.feather
        import pyarrow
        table = pyarrow.Table.from_pylist(FIXTURES_TYPES)
        pyarrow.feather.write_feather(table, FIXTURE_FILE)

class TestArrow:
    def test_id(self):
        datatype_id = ArrowIterable.id()
        assert datatype_id == 'arrow'

    def test_flatonly(self):
        flag = ArrowIterable.is_flatonly()
        assert flag == True

    def test_openclose(self):
        iterable = ArrowIterable(FIXTURE_FILE)        
        iterable.close()

    def test_read_bulk_returns_n_records(self):
        iterable = ArrowIterable(FIXTURE_FILE)
        chunk = iterable.read_bulk(2)
        assert len(chunk) == 2
        assert chunk == FIXTURES_TYPES[:2]
        iterable.close()
                
    def test_parsesimple_readone(self):
        iterable = ArrowIterable(FIXTURE_FILE)        
        row = iterable.read()
        assert row == FIXTURES_TYPES[0]
        iterable.close()
           
    def test_parsesimple_reset(self):
        iterable = ArrowIterable(FIXTURE_FILE)        
        row = iterable.read()
        assert row == FIXTURES_TYPES[0]
        iterable.reset() 
        row_reset = iterable.read()
        assert row_reset == FIXTURES_TYPES[0]
        iterable.close()
           
    def test_parsesimple_next(self):
        iterable = ArrowIterable(FIXTURE_FILE)        
        row = next(iterable)
        assert row == FIXTURES_TYPES[0]
        iterable.reset() 
        row_reset = next(iterable)
        assert row_reset == FIXTURES_TYPES[0]
        iterable.close()

    def test_parsesimple_count(self):
        iterable = ArrowIterable(FIXTURE_FILE)        
        n = 0
        for row in iterable:
            n += 1
        assert n == len(FIXTURES_TYPES)
        iterable.close()

    def test_parsesimple_iterateall(self):
        iterable = ArrowIterable(FIXTURE_FILE)        
        n = 0
        for row in iterable:
            assert row == FIXTURES_TYPES[n]
            n += 1
        iterable.close()

    def test_write_read(self):
        iterable = ArrowIterable('testdata/2cols6rows_test.arrow', mode='w')
        iterable.write_bulk(FIXTURES)
        iterable.close()
        iterable = ArrowIterable('testdata/2cols6rows_test.arrow', mode='r')
        n = 0
        for row in iterable:
            assert row == FIXTURES[n]
            n += 1
        assert n == len(FIXTURES)
        iterable.close()

    def test_has_totals(self):
        iterable = ArrowIterable(FIXTURE_FILE)
        assert ArrowIterable.has_totals() == True
        total = iterable.totals()
        assert total == len(FIXTURES_TYPES)
        iterable.close()
