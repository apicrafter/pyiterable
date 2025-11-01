# -*- coding: utf-8 -*- 
import pytest
from iterable.datatypes import AVROIterable
from fixdata import FIXTURES

class TestAVRO:
    def test_id(self):
        datatype_id = AVROIterable.id()
        assert datatype_id == 'avro'

    def test_flatonly(self):
        flag = AVROIterable.is_flatonly()
        assert flag == True

    def test_openclose(self):
        iterable = AVROIterable('fixtures/2cols6rows.avro')        
        iterable.close()
                
    def test_parsesimple_readone(self):
        iterable = AVROIterable('fixtures/2cols6rows.avro')        
        row = iterable.read()
        assert row == FIXTURES[0]
        iterable.close()
           
    def test_parsesimple_reset(self):
        iterable = AVROIterable('fixtures/2cols6rows.avro')        
        row = iterable.read()
        assert row == FIXTURES[0]
        iterable.reset() 
        row_reset = iterable.read()
        assert row_reset == FIXTURES[0]
        iterable.close()
           
    def test_parsesimple_next(self):
        iterable = AVROIterable('fixtures/2cols6rows.avro')        
        row = next(iterable)
        assert row == FIXTURES[0]
        iterable.reset() 
        row_reset = next(iterable)
        assert row_reset == FIXTURES[0]
        iterable.close()

    def test_parsesimple_count(self):
        iterable = AVROIterable('fixtures/2cols6rows.avro')        
        n = 0
        for row in iterable:
            n += 1
        assert n == len(FIXTURES)
        iterable.close()

    def test_parsesimple_iterateall(self):
        iterable = AVROIterable('fixtures/2cols6rows.avro')        
        n = 0
        for row in iterable:
            assert row == FIXTURES[n]
            n += 1
        iterable.close()
