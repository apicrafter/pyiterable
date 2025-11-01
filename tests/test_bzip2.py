# -*- coding: utf-8 -*- 
import pytest
from iterable.datatypes import CSVIterable
from iterable.codecs import BZIP2Codec
from fixdata import FIXTURES

class TestBZ2:
    def test_fileexts(self):
        assert BZIP2Codec.fileexts() == ['bz2',]


    def test_openclose(self):
        codecobj = BZIP2Codec('fixtures/2cols6rows.csv.bz2', mode='r')
        iterable = CSVIterable(codec=codecobj)        
        iterable.close()
                
    def test_parsesimple_readone(self):
        codecobj = BZIP2Codec('fixtures/2cols6rows.csv.bz2', mode='r')
        iterable = CSVIterable(codec=codecobj)        
        row = iterable.read()
        assert row == FIXTURES[0]
        iterable.close()
           
    def test_parsesimple_reset(self):
        codecobj = BZIP2Codec('fixtures/2cols6rows.csv.bz2', mode='r')
        iterable = CSVIterable(codec=codecobj)        
        row = iterable.read()
        assert row == FIXTURES[0]
        iterable.reset() 
        row_reset = iterable.read()
        assert row_reset == FIXTURES[0]
        iterable.close()
           
    def test_parsesimple_next(self):
        codecobj = BZIP2Codec('fixtures/2cols6rows.csv.bz2', mode='r')
        iterable = CSVIterable(codec=codecobj)        
        row = next(iterable)
        assert row == FIXTURES[0]
        iterable.reset() 
        row_reset = next(iterable)
        assert row_reset == FIXTURES[0]
        iterable.close()

    def test_parsesimple_count(self):
        codecobj = BZIP2Codec('fixtures/2cols6rows.csv.bz2', mode='r')
        iterable = CSVIterable(codec=codecobj)        
        n = 0
        for row in iterable:
            n += 1
        assert n == len(FIXTURES)
        iterable.close()

    def test_parsesimple_iterateall(self):
        codecobj = BZIP2Codec('fixtures/2cols6rows.csv.bz2', mode='r')
        iterable = CSVIterable(codec=codecobj)        
        n = 0
        for row in iterable:
            assert row == FIXTURES[n]
            n += 1
        iterable.close()

    def test_write_read(self):
        codecobj = BZIP2Codec('testdata/2cols6rows_test.csv.bz2', mode='w')
        iterable = CSVIterable(codec=codecobj, mode='w', keys=['id', 'name'])
        for row in FIXTURES:
            iterable.write(row)
        iterable.close()
        codecobj = BZIP2Codec('fixtures/2cols6rows.csv.bz2', mode='r')
        iterable = CSVIterable(codec=codecobj)        
        n = 0
        for row in iterable:
            assert row == FIXTURES[n]
            n += 1
        assert n == len(FIXTURES)
        iterable.close()
