# -*- coding: utf-8 -*- 
import pytest
import os
from iterable.datatypes import MessagePackIterable
from fixdata import FIXTURES

# Create fixture file if it doesn't exist
FIXTURE_FILE = 'fixtures/2cols6rows_flat.msgpack'

def setup_module():
    """Create fixture file if it doesn't exist"""
    try:
        import msgpack
        if not os.path.exists(FIXTURE_FILE):
            with open(FIXTURE_FILE, 'wb') as f:
                packer = msgpack.Packer(use_bin_type=True)
                for record in FIXTURES:
                    f.write(packer.pack(record))
    except ImportError:
        pass  # Skip if msgpack not available

class TestMessagePack:
    def test_id(self):
        datatype_id = MessagePackIterable.id()
        assert datatype_id == 'msgpack'

    def test_flatonly(self):
        flag = MessagePackIterable.is_flatonly()
        assert flag == False

    def test_openclose(self):
        iterable = MessagePackIterable(FIXTURE_FILE)        
        iterable.close()

    def test_read_bulk_returns_n_records(self):
        iterable = MessagePackIterable(FIXTURE_FILE)
        chunk = iterable.read_bulk(3)
        assert len(chunk) == 3
        assert chunk == FIXTURES[:3]
        iterable.close()
                
    def test_parsesimple_readone(self):
        iterable = MessagePackIterable(FIXTURE_FILE)        
        row = iterable.read()
        assert row == FIXTURES[0]
        iterable.close()
           
    def test_parsesimple_reset(self):
        iterable = MessagePackIterable(FIXTURE_FILE)        
        row = iterable.read()
        assert row == FIXTURES[0]
        iterable.reset() 
        row_reset = iterable.read()
        assert row_reset == FIXTURES[0]
        iterable.close()
           
    def test_parsesimple_next(self):
        iterable = MessagePackIterable(FIXTURE_FILE)        
        row = next(iterable)
        assert row == FIXTURES[0]
        iterable.reset() 
        row_reset = next(iterable)
        assert row_reset == FIXTURES[0]
        iterable.close()

    def test_parsesimple_count(self):
        iterable = MessagePackIterable(FIXTURE_FILE)        
        n = 0
        for row in iterable:
            n += 1
        assert n == len(FIXTURES)
        iterable.close()

    def test_parsesimple_iterateall(self):
        iterable = MessagePackIterable(FIXTURE_FILE)        
        n = 0
        for row in iterable:
            assert row == FIXTURES[n]
            n += 1
        iterable.close()

    def test_write_read(self):
        iterable = MessagePackIterable('testdata/2cols6rows_test.msgpack', mode='w')        
        for row in FIXTURES:
            iterable.write(row)
        iterable.close()
        iterable = MessagePackIterable('testdata/2cols6rows_test.msgpack')        
        n = 0
        for row in iterable:
            assert row == FIXTURES[n]
            n += 1
        iterable.close()
