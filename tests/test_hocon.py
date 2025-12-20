# -*- coding: utf-8 -*-
import pytest
import os
from iterable.datatypes import HOCONIterable

try:
    from pyhocon import ConfigFactory
    HAS_PYHOCON = True
except ImportError:
    HAS_PYHOCON = False


@pytest.mark.skipif(not HAS_PYHOCON, reason="HOCON support requires 'pyhocon' package")
class TestHOCON:
    def test_id(self):
        datatype_id = HOCONIterable.id()
        assert datatype_id == 'hocon'

    def test_flatonly(self):
        flag = HOCONIterable.is_flatonly()
        assert flag == False

    def test_openclose(self):
        """Test basic open/close"""
        test_file = 'testdata/test_hocon.conf'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('name = "test"\nvalue = 42')
        
        iterable = HOCONIterable(test_file)
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_one(self):
        """Test reading single record"""
        test_file = 'testdata/test_hocon_read.conf'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('name = "test"\nvalue = 42')
        
        iterable = HOCONIterable(test_file)
        record = iterable.read()
        assert isinstance(record, dict)
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_bulk(self):
        """Test reading bulk records"""
        test_file = 'testdata/test_hocon_bulk.conf'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('items = [\n  {name: "item1"},\n  {name: "item2"}\n]')
        
        iterable = HOCONIterable(test_file)
        chunk = iterable.read_bulk(2)
        assert isinstance(chunk, list)
        assert len(chunk) > 0
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_reset(self):
        """Test reset functionality"""
        test_file = 'testdata/test_hocon_reset.conf'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('key = "value"')
        
        iterable = HOCONIterable(test_file)
        record1 = iterable.read()
        iterable.reset()
        record2 = iterable.read()
        # After reset, should read the same record
        assert record1 == record2
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

