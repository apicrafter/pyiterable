# -*- coding: utf-8 -*- 
import pytest
from iterable.datatypes import BSONIterable

from fixdata import FIXTURES

class TestBSON:
    def test_id(self):
        datatype_id = BSONIterable.id()
        assert datatype_id == 'bson'

    def test_flatonly(self):
        flag = BSONIterable.is_flatonly()
        assert flag == False

    def test_openclose(self):
        iterable = BSONIterable('fixtures/2cols6rows_flat.bson')        
        iterable.close()
                
    def test_parsesimple_readone(self):
        iterable = BSONIterable('fixtures/2cols6rows_flat.bson')        
        row = iterable.read()
        assert row == FIXTURES[0]
        iterable.close()
           
    def test_parsesimple_reset(self):
        iterable = BSONIterable('fixtures/2cols6rows_flat.bson')        
        row = iterable.read()
        assert row == FIXTURES[0]
        iterable.reset() 
        row_reset = iterable.read()
        assert row_reset == FIXTURES[0]
        iterable.close()
           
    def test_parsesimple_next(self):
        iterable = BSONIterable('fixtures/2cols6rows_flat.bson')        
        row = next(iterable)
        assert row == FIXTURES[0]
        iterable.reset() 
        row_reset = next(iterable)
        assert row_reset == FIXTURES[0]
        iterable.close()

    def test_parsesimple_count(self):
        iterable = BSONIterable('fixtures/2cols6rows_flat.bson')        
        n = 0
        for row in iterable:
            n += 1
        assert n == len(FIXTURES)
        iterable.close()

    def test_parsesimple_iterateall(self):
        iterable = BSONIterable('fixtures/2cols6rows_flat.bson')        
        n = 0
        for row in iterable:
            assert row == FIXTURES[n]
            n += 1
        iterable.close()
