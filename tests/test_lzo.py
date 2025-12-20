# -*- coding: utf-8 -*- 
import pytest
from iterable.datatypes import CSVIterable
from iterable.codecs import LZOCodec
from fixdata import FIXTURES

# Check if LZO is available
try:
    import lzo
    LZO_AVAILABLE = True
except ImportError:
    LZO_AVAILABLE = False

@pytest.mark.skipif(not LZO_AVAILABLE, reason="python-lzo library not available")
class TestLZO:
    def test_fileexts(self):
        assert LZOCodec.fileexts() == ['lzo', 'lzop']


    def test_openclose(self):
        codecobj = LZOCodec('fixtures/2cols6rows.csv.lzo', mode='r')
        iterable = CSVIterable(codec=codecobj)        
        iterable.close()
                
    def test_parsesimple_readone(self):
        codecobj = LZOCodec('fixtures/2cols6rows.csv.lzo', mode='r')
        iterable = CSVIterable(codec=codecobj)        
        row = iterable.read()
        assert row == FIXTURES[0]
        iterable.close()
           
    def test_parsesimple_reset(self):
        codecobj = LZOCodec('fixtures/2cols6rows.csv.lzo', mode='r')
        iterable = CSVIterable(codec=codecobj)        
        row = iterable.read()
        assert row == FIXTURES[0]
        iterable.reset() 
        row_reset = iterable.read()
        assert row_reset == FIXTURES[0]
        iterable.close()
           
    def test_parsesimple_next(self):
        codecobj = LZOCodec('fixtures/2cols6rows.csv.lzo', mode='r')
        iterable = CSVIterable(codec=codecobj)        
        row = next(iterable)
        assert row == FIXTURES[0]
        iterable.reset() 
        row_reset = next(iterable)
        assert row_reset == FIXTURES[0]
        iterable.close()

    def test_parsesimple_count(self):
        codecobj = LZOCodec('fixtures/2cols6rows.csv.lzo', mode='r')
        iterable = CSVIterable(codec=codecobj)        
        n = 0
        for row in iterable:
            n += 1
        assert n == len(FIXTURES)
        iterable.close()

    def test_parsesimple_iterateall(self):
        codecobj = LZOCodec('fixtures/2cols6rows.csv.lzo', mode='r')
        iterable = CSVIterable(codec=codecobj)        
        n = 0
        for row in iterable:
            assert row == FIXTURES[n]
            n += 1
        iterable.close()

    def test_write_read(self):
        codecobj = LZOCodec('testdata/2cols6rows_test.csv.lzo', mode='w')
        iterable = CSVIterable(codec=codecobj, mode='w', keys=['id', 'name'])
        for row in FIXTURES:
            iterable.write(row)
        iterable.close()
        codecobj = LZOCodec('fixtures/2cols6rows.csv.lzo', mode='r')
        iterable = CSVIterable(codec=codecobj)        
        n = 0
        for row in iterable:
            assert row == FIXTURES[n]
            n += 1
        assert n == len(FIXTURES)
        iterable.close()
