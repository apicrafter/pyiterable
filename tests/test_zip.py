# -*- coding: utf-8 -*- 
import pytest
from iterable.datatypes import CSVIterable
from iterable.codecs import ZIPCodec
from fixdata import FIXTURES

class TestZIP:
    def test_fileexts(self):
        assert ZIPCodec.fileexts() == ['zip',]


    def test_openclose(self):
        codecobj = ZIPCodec('fixtures/2cols6rows.csv.zip', mode='r')
        iterable = CSVIterable(codec=codecobj)        
        iterable.close()
                
    def test_parsesimple_readone(self):
        codecobj = ZIPCodec('fixtures/2cols6rows.csv.zip', mode='r')
        iterable = CSVIterable(codec=codecobj)        
        row = iterable.read()
        assert row == FIXTURES[0]
        iterable.close()
           
    def test_parsesimple_reset(self):
        codecobj = ZIPCodec('fixtures/2cols6rows.csv.zip', mode='r')
        iterable = CSVIterable(codec=codecobj)        
        row = iterable.read()
        assert row == FIXTURES[0]
        iterable.reset() 
        row_reset = iterable.read()
        assert row_reset == FIXTURES[0]
        iterable.close()
           
    def test_parsesimple_next(self):
        codecobj = ZIPCodec('fixtures/2cols6rows.csv.zip', mode='r')
        iterable = CSVIterable(codec=codecobj)        
        row = next(iterable)
        assert row == FIXTURES[0]
        iterable.reset() 
        row_reset = next(iterable)
        assert row_reset == FIXTURES[0]
        iterable.close()

    def test_parsesimple_count(self):
        codecobj = ZIPCodec('fixtures/2cols6rows.csv.zip', mode='r')
        iterable = CSVIterable(codec=codecobj)        
        n = 0
        for row in iterable:
            n += 1
        assert n == len(FIXTURES)
        iterable.close()

    def test_parsesimple_iterateall(self):
        codecobj = ZIPCodec('fixtures/2cols6rows.csv.zip', mode='r')
        iterable = CSVIterable(codec=codecobj)        
        n = 0
        for row in iterable:
            assert row == FIXTURES[n]
            n += 1
        iterable.close()

