# -*- coding: utf-8 -*- 
import pytest
from iterable.datatypes import XLSXIterable

from fixdata import FIXTURES_TYPES, FIXTURES

class TestXLSX:
    def test_id(self):
        datatype_id = XLSXIterable.id()
        assert datatype_id == 'xlsx'

    def test_flatonly(self):
        flag = XLSXIterable.is_flatonly()
        assert flag == True

    def test_openclose(self):
        iterable = XLSXIterable('fixtures/2cols6rows.xlsx')        
        iterable.close()
                
    def test_parsesimple_readone(self):
        iterable = XLSXIterable('fixtures/2cols6rows.xlsx')
        row = iterable.read()
        assert row == FIXTURES[0]
        iterable.close()

    def test_parsesimple_fixedkeys_readone(self):
        iterable = XLSXIterable('fixtures/2cols6rows.xlsx', keys=['id', 'name'], start_line=1)
        row = iterable.read()
        assert row == FIXTURES[0]
        iterable.close()

           
    def test_parsesimple_reset(self):
        iterable = XLSXIterable('fixtures/2cols6rows.xlsx')        
        row = iterable.read()
        assert row == FIXTURES[0]
        iterable.reset() 
        row_reset = iterable.read()
        assert row_reset == FIXTURES[0]
        iterable.close()
           
    def test_parsesimple_next(self):
        iterable = XLSXIterable('fixtures/2cols6rows.xlsx')        
        row = next(iterable)
        assert row == FIXTURES[0]
        iterable.reset() 
        row_reset = next(iterable)
        assert row_reset == FIXTURES[0]
        iterable.close()

    def test_parsesimple_count(self):
        iterable = XLSXIterable('fixtures/2cols6rows.xlsx')        
        n = 0
        for row in iterable:
            n += 1
        assert n == len(FIXTURES)
        iterable.close()

    def test_parsesimple_iterateall(self):
        iterable = XLSXIterable('fixtures/2cols6rows.xlsx')        
        n = 0
        for row in iterable:
            assert row == FIXTURES[n]
            n += 1
        iterable.close()


    def test_parsesimple_fixedkeys_iterateall(self):
        iterable = XLSXIterable('fixtures/2cols6rows.xlsx', keys=['id', 'name'], start_line=1)
        n = 0
        for row in iterable:
            assert row == FIXTURES[n]
            n += 1
        iterable.close()
