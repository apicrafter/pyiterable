# -*- coding: utf-8 -*- 
import pytest
from iterable.datatypes import CSVIterable
from fixdata import FIXTURES

class TestCSV:
    def test_id(self):
        datatype_id = CSVIterable.id()
        assert datatype_id == 'csv'

    def test_flatonly(self):
        flag = CSVIterable.is_flatonly()
        assert flag == True

    def test_openclose(self):
        iterable = CSVIterable('fixtures/2cols6rows.csv')        
        iterable.close()
                
    def test_parsesimple_readone(self):
        iterable = CSVIterable('fixtures/2cols6rows.csv')        
        row = iterable.read()
        assert row == FIXTURES[0]
        iterable.close()
           
    def test_parsesimple_reset(self):
        iterable = CSVIterable('fixtures/2cols6rows.csv')        
        row = iterable.read()
        assert row == FIXTURES[0]
        iterable.reset() 
        row_reset = iterable.read()
        assert row_reset == FIXTURES[0]
        iterable.close()
           
    def test_parsesimple_next(self):
        iterable = CSVIterable('fixtures/2cols6rows.csv')        
        row = next(iterable)
        assert row == FIXTURES[0]
        iterable.reset() 
        row_reset = next(iterable)
        assert row_reset == FIXTURES[0]
        iterable.close()

    def test_parsesimple_count(self):
        iterable = CSVIterable('fixtures/2cols6rows.csv')        
        n = 0
        for row in iterable:
            n += 1
        assert n == len(FIXTURES)
        iterable.close()

    def test_parsesimple_iterateall(self):
        iterable = CSVIterable('fixtures/2cols6rows.csv')        
        n = 0
        for row in iterable:
            assert row == FIXTURES[n]
            n += 1
        iterable.close()

    def test_write_read(self):
        iterable = CSVIterable('testdata/2cols6rows_test.csv', mode='w', keys=['id', 'name'])        
        for row in FIXTURES:
            iterable.write(row)
        iterable.close()
        iterable = CSVIterable('testdata/2cols6rows_test.csv')
        n = 0
        for row in iterable:
            assert row == FIXTURES[n]
            n += 1
        iterable.close()

    def test_read_bulk_advances_and_stops(self):
        iterable = CSVIterable('fixtures/2cols6rows.csv')
        chunk = iterable.read_bulk(4)
        assert len(chunk) == 4
        assert chunk == FIXTURES[:4]
        # Next read should give the 5th row
        row = iterable.read()
        assert row == FIXTURES[4]
        # Exhaust
        _ = iterable.read()
        with pytest.raises(StopIteration):
            _ = iterable.read()
        iterable.close()