# -*- coding: utf-8 -*- 
import pytest
from iterable.datatypes import JSONIterable

from fixdata import FIXTURES


class TestJSON:
    def test_id(self):
        datatype_id = JSONIterable.id()
        assert datatype_id == 'json'

    def test_flatonly(self):
        flag = JSONIterable.is_flatonly()
        assert flag == False

    def test_openclose(self):
        iterable = JSONIterable('fixtures/2cols6rows_array.json')        
        iterable.close()
                
    def test_parsesimple_readone(self):
        iterable = JSONIterable('fixtures/2cols6rows_array.json')        
        row = iterable.read()
        assert row == FIXTURES[0]
        iterable.close()
           
    def test_parsesimple_reset(self):
        iterable = JSONIterable('fixtures/2cols6rows_tag.json', tagname="persons")        
        row = iterable.read()
        assert row == FIXTURES[0]
        iterable.reset() 
        row_reset = iterable.read()
        assert row_reset == FIXTURES[0]
        iterable.close()
           
    def test_parsesimple_next(self):
        iterable = JSONIterable('fixtures/2cols6rows_array.json')        
        row = next(iterable)
        assert row == FIXTURES[0]
        iterable.reset() 
        row_reset = next(iterable)
        assert row_reset == FIXTURES[0]
        iterable.close()

    def test_parsesimple_count(self):
        iterable = JSONIterable('fixtures/2cols6rows_array.json')        
        n = 0
        for row in iterable:
            n += 1
        assert n == len(FIXTURES)
        iterable.close()

    def test_parsesimple_iterateall(self):
        iterable = JSONIterable('fixtures/2cols6rows_array.json')        
        n = 0
        for row in iterable:
            assert row == FIXTURES[n]
            n += 1
        iterable.close()
