# -*- coding: utf-8 -*- 
import pytest
from iterable.datatypes import CSVIterable
from iterable.codecs import SnappyCodec
from fixdata import FIXTURES

class TestSnappy:
    def test_fileexts(self):
        assert SnappyCodec.fileexts() == ['snappy', 'sz']


    def test_openclose(self):
        codecobj = SnappyCodec('fixtures/2cols6rows.csv.snappy', mode='r')
        iterable = CSVIterable(codec=codecobj)        
        iterable.close()
                
    def test_parsesimple_readone(self):
        codecobj = SnappyCodec('fixtures/2cols6rows.csv.snappy', mode='r')
        iterable = CSVIterable(codec=codecobj)        
        row = iterable.read()
        assert row == FIXTURES[0]
        iterable.close()
           
    def test_parsesimple_reset(self):
        codecobj = SnappyCodec('fixtures/2cols6rows.csv.snappy', mode='r')
        iterable = CSVIterable(codec=codecobj)        
        row = iterable.read()
        assert row == FIXTURES[0]
        iterable.reset() 
        row_reset = iterable.read()
        assert row_reset == FIXTURES[0]
        iterable.close()
           
    def test_parsesimple_next(self):
        codecobj = SnappyCodec('fixtures/2cols6rows.csv.snappy', mode='r')
        iterable = CSVIterable(codec=codecobj)        
        row = next(iterable)
        assert row == FIXTURES[0]
        iterable.reset() 
        row_reset = next(iterable)
        assert row_reset == FIXTURES[0]
        iterable.close()

    def test_parsesimple_count(self):
        codecobj = SnappyCodec('fixtures/2cols6rows.csv.snappy', mode='r')
        iterable = CSVIterable(codec=codecobj)        
        n = 0
        for row in iterable:
            n += 1
        assert n == len(FIXTURES)
        iterable.close()

    def test_parsesimple_iterateall(self):
        codecobj = SnappyCodec('fixtures/2cols6rows.csv.snappy', mode='r')
        iterable = CSVIterable(codec=codecobj)        
        n = 0
        for row in iterable:
            assert row == FIXTURES[n]
            n += 1
        iterable.close()

    def test_write_read(self):
        codecobj = SnappyCodec('testdata/2cols6rows_test.csv.snappy', mode='w')
        iterable = CSVIterable(codec=codecobj, mode='w', keys=['id', 'name'])
        for row in FIXTURES:
            iterable.write(row)
        iterable.close()
        codecobj = SnappyCodec('fixtures/2cols6rows.csv.snappy', mode='r')
        iterable = CSVIterable(codec=codecobj)        
        n = 0
        for row in iterable:
            assert row == FIXTURES[n]
            n += 1
        assert n == len(FIXTURES)
        iterable.close()
