# -*- coding: utf-8 -*- 
import pytest
from iterable.datatypes import XLSIterable

from fixdata import FIXTURES_TYPES

class TestXLS:
    def test_id(self):
        datatype_id = XLSIterable.id()
        assert datatype_id == 'xls'

    def test_flatonly(self):
        flag = XLSIterable.is_flatonly()
        assert flag == True

    def test_openclose(self):
        iterable = XLSIterable('fixtures/2cols6rows.xls')        
        iterable.close()
                
    def test_parsesimple_readone(self):
        iterable = XLSIterable('fixtures/2cols6rows.xls')
        row = iterable.read()
        assert row == FIXTURES_TYPES[0]
        iterable.close()

    def test_parsesimple_fixedkeys_readone(self):
        iterable = XLSIterable('fixtures/2cols6rows.xls', keys=['id', 'name'], start_line=1)
        row = iterable.read()
        assert row == FIXTURES_TYPES[0]
        iterable.close()

           
    def test_parsesimple_reset(self):
        iterable = XLSIterable('fixtures/2cols6rows.xls')        
        row = iterable.read()
        assert row == FIXTURES_TYPES[0]
        iterable.reset() 
        row_reset = iterable.read()
        assert row_reset == FIXTURES_TYPES[0]
        iterable.close()
           
    def test_parsesimple_next(self):
        iterable = XLSIterable('fixtures/2cols6rows.xls')        
        row = next(iterable)
        assert row == FIXTURES_TYPES[0]
        iterable.reset() 
        row_reset = next(iterable)
        assert row_reset == FIXTURES_TYPES[0]
        iterable.close()

    def test_parsesimple_count(self):
        iterable = XLSIterable('fixtures/2cols6rows.xls')        
        n = 0
        for row in iterable:
            n += 1
        assert n == len(FIXTURES_TYPES)
        iterable.close()

    def test_parsesimple_iterateall(self):
        iterable = XLSIterable('fixtures/2cols6rows.xls')        
        n = 0
        for row in iterable:
            assert row == FIXTURES_TYPES[n]
            n += 1
        iterable.close()


    def test_parsesimple_fixedkeys_iterateall(self):
        iterable = XLSIterable('fixtures/2cols6rows.xls', keys=['id', 'name'], start_line=1)
        n = 0
        for row in iterable:
            assert row == FIXTURES_TYPES[n]
            n += 1
        iterable.close()





