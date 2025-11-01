# -*- coding: utf-8 -*- 
import pytest
from iterable.datatypes import CSVIterable
from iterable.codecs import GZIPCodec
from fixdata import FIXTURES

class TestGZIP:
    def test_fileexts(self):
        assert GZIPCodec.fileexts() == ['gz',]


    def test_openclose(self):
        iterable = CSVIterable(codec=GZIPCodec('fixtures/2cols6rows.csv.gz', mode='r', open_it=True))        
        iterable.close()
                
    def test_parsesimple_readone(self):
        codecobj = GZIPCodec('fixtures/2cols6rows.csv.gz', mode='r', open_it=True)
        iterable = CSVIterable(codec=codecobj)        
        row = iterable.read()
        assert row == FIXTURES[0]
        iterable.close()
           
    def test_parsesimple_reset(self):
        codecobj = GZIPCodec('fixtures/2cols6rows.csv.gz', mode='r', open_it=True)
        iterable = CSVIterable(codec=codecobj)        
        row = iterable.read()
        assert row == FIXTURES[0]
        iterable.reset() 
        row_reset = iterable.read()
        assert row_reset == FIXTURES[0]
        iterable.close()
           
    def test_parsesimple_next(self):
        codecobj = GZIPCodec('fixtures/2cols6rows.csv.gz', mode='r', open_it=True)
        iterable = CSVIterable(codec=codecobj)        
        row = next(iterable)
        assert row == FIXTURES[0]
        iterable.reset() 
        row_reset = next(iterable)
        assert row_reset == FIXTURES[0]
        iterable.close()

    def test_parsesimple_count(self):
        codecobj = GZIPCodec('fixtures/2cols6rows.csv.gz', mode='r', open_it=True)
        iterable = CSVIterable(codec=codecobj)        
        n = 0
        for row in iterable:
            n += 1
        assert n == len(FIXTURES)
        iterable.close()

    def test_parsesimple_iterateall(self):
        codecobj = GZIPCodec('fixtures/2cols6rows.csv.gz', mode='r', open_it=True)
        iterable = CSVIterable(codec=codecobj)        
        n = 0
        for row in iterable:
            assert row == FIXTURES[n]
            n += 1
        iterable.close()

    def test_write_read(self):
        codecobj = GZIPCodec('testdata/2cols6rows_test.csv.gz', mode='w', open_it=True)
        iterable = CSVIterable(codec=codecobj, mode='w', keys=['id', 'name'])        
        for row in FIXTURES:
            iterable.write(row)
        iterable.close()
        codecobj = GZIPCodec('testdata/2cols6rows_test.csv.gz', mode='r', open_it=True)
        iterable = CSVIterable(codec=codecobj)        
        n = 0
        for row in iterable:
            assert row == FIXTURES[n]
            n += 1
        assert n == len(FIXTURES)
        iterable.close()
