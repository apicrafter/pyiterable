# -*- coding: utf-8 -*- 
import pytest
from iterable.datatypes import ORCIterable
from fixdata import FIXTURES

class TestORC:
    def test_id(self):
        datatype_id = ORCIterable.id()
        assert datatype_id == 'orc'

    def test_flatonly(self):
        flag = ORCIterable.is_flatonly()
        assert flag == True

    def test_openclose(self):
        iterable = ORCIterable('fixtures/2cols6rows.orc')        
        iterable.close()
                
    def test_parsesimple_readone(self):
        iterable = ORCIterable('fixtures/2cols6rows.orc')        
        row = iterable.read()
        assert row == FIXTURES[0]
        iterable.close()
           
    def test_parsesimple_reset(self):
        iterable = ORCIterable('fixtures/2cols6rows.orc')        
        row = iterable.read()
        assert row == FIXTURES[0]
        iterable.reset() 
        row_reset = iterable.read()
        assert row_reset == FIXTURES[0]
        iterable.close()
           
    def test_parsesimple_next(self):
        iterable = ORCIterable('fixtures/2cols6rows.orc')        
        row = next(iterable)
        assert row == FIXTURES[0]
        iterable.reset() 
        row_reset = next(iterable)
        assert row_reset == FIXTURES[0]
        iterable.close()

    def test_parsesimple_count(self):
        iterable = ORCIterable('fixtures/2cols6rows.orc')        
        n = 0
        for row in iterable:
            n += 1
        assert n == len(FIXTURES)
        iterable.close()

    def test_parsesimple_iterateall(self):
        iterable = ORCIterable('fixtures/2cols6rows.orc')        
        n = 0
        for row in iterable:
            assert row == FIXTURES[n]
            n += 1
        iterable.close()
