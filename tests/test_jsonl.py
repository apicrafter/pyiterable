# -*- coding: utf-8 -*- 
import pytest
from iterable.datatypes import JSONLinesIterable

from fixdata import FIXTURES
TESTING_DIR = 'testdata'

class TestJSONLines:
    def test_id(self):
        datatype_id = JSONLinesIterable.id()
        assert datatype_id == 'jsonl'

    def test_flatonly(self):
        flag = JSONLinesIterable.is_flatonly()
        assert flag == False

    def test_openclose(self):
        iterable = JSONLinesIterable('fixtures/2cols6rows_flat.jsonl')        
        iterable.close()
                
    def test_parsesimple_readone(self):
        iterable = JSONLinesIterable('fixtures/2cols6rows_flat.jsonl')        
        row = iterable.read()
        assert row == FIXTURES[0]
        iterable.close()
           
    def test_parsesimple_reset(self):
        iterable = JSONLinesIterable('fixtures/2cols6rows_flat.jsonl')        
        row = iterable.read()
        assert row == FIXTURES[0]
        iterable.reset() 
        row_reset = iterable.read()
        assert row_reset == FIXTURES[0]
        iterable.close()
           
    def test_parsesimple_next(self):
        iterable = JSONLinesIterable('fixtures/2cols6rows_flat.jsonl')        
        row = next(iterable)
        assert row == FIXTURES[0]
        iterable.reset() 
        row_reset = next(iterable)
        assert row_reset == FIXTURES[0]
        iterable.close()

    def test_parsesimple_count(self):
        iterable = JSONLinesIterable('fixtures/2cols6rows_flat.jsonl')        
        n = 0
        for row in iterable:
            n += 1
        assert n == len(FIXTURES)
        iterable.close()

    def test_parsesimple_iterateall(self):
        iterable = JSONLinesIterable('fixtures/2cols6rows_flat.jsonl')        
        n = 0
        for row in iterable:
            assert row == FIXTURES[n]
            n += 1
        iterable.close()

    def test_write_read(self):
        iterable = JSONLinesIterable('testdata/2cols6rows_test.jsonl', mode='w')        
        for row in FIXTURES:
            iterable.write(row)
        iterable.close()
        iterable = JSONLinesIterable('testdata/2cols6rows_test.jsonl')        
        n = 0
        for row in iterable:
            assert row == FIXTURES[n]
            n += 1
        iterable.close()

