# -*- coding: utf-8 -*- 
import pytest
from iterable.datatypes import CSVIterable
from iterable.codecs import LZMACodec
from fixdata import FIXTURES

class TestLZMA:
    def test_fileexts(self):
        assert LZMACodec.fileexts() == ['xz', 'lzma']


    def test_openclose(self):
        codecobj = LZMACodec('fixtures/2cols6rows.csv.xz', mode='r')
        iterable = CSVIterable(codec=codecobj)        
        iterable.close()
                
    def test_parsesimple_readone(self):
        codecobj = LZMACodec('fixtures/2cols6rows.csv.xz', mode='r')
        iterable = CSVIterable(codec=codecobj)        
        row = iterable.read()
        assert row == FIXTURES[0]
        iterable.close()
           
    def test_parsesimple_reset(self):
        codecobj = LZMACodec('fixtures/2cols6rows.csv.xz', mode='r')
        iterable = CSVIterable(codec=codecobj)        
        row = iterable.read()
        assert row == FIXTURES[0]
        iterable.reset() 
        row_reset = iterable.read()
        assert row_reset == FIXTURES[0]
        iterable.close()
           
    def test_parsesimple_next(self):
        codecobj = LZMACodec('fixtures/2cols6rows.csv.xz', mode='r')
        iterable = CSVIterable(codec=codecobj)        
        row = next(iterable)
        assert row == FIXTURES[0]
        iterable.reset() 
        row_reset = next(iterable)
        assert row_reset == FIXTURES[0]
        iterable.close()

    def test_parsesimple_count(self):
        codecobj = LZMACodec('fixtures/2cols6rows.csv.xz', mode='r')
        iterable = CSVIterable(codec=codecobj)        
        n = 0
        for row in iterable:
            n += 1
        assert n == len(FIXTURES)
        iterable.close()

    def test_parsesimple_iterateall(self):
        codecobj = LZMACodec('fixtures/2cols6rows.csv.xz', mode='r')
        iterable = CSVIterable(codec=codecobj)        
        n = 0
        for row in iterable:
            assert row == FIXTURES[n]
            n += 1
        iterable.close()

    def test_write_read(self):
        codecobj = LZMACodec('testdata/2cols6rows_test.csv.xz', mode='w')
        iterable = CSVIterable(codec=codecobj, mode='w', keys=['id', 'name'])
        for row in FIXTURES:
            iterable.write(row)
        iterable.close()
        codecobj = LZMACodec('fixtures/2cols6rows.csv.xz', mode='r')
        iterable = CSVIterable(codec=codecobj)        
        n = 0
        for row in iterable:
            assert row == FIXTURES[n]
            n += 1
        assert n == len(FIXTURES)
        iterable.close()
