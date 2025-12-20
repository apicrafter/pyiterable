# -*- coding: utf-8 -*-
import pytest
import os
from iterable.datatypes import EDNIterable

try:
    import edn_format
    HAS_EDN_FORMAT = True
except ImportError:
    HAS_EDN_FORMAT = False

try:
    import pyedn
    HAS_PYEDN = True
except ImportError:
    HAS_PYEDN = False


@pytest.mark.skipif(not HAS_EDN_FORMAT and not HAS_PYEDN, reason="EDN support requires 'edn_format' or 'pyedn' package")
class TestEDN:
    def test_id(self):
        datatype_id = EDNIterable.id()
        assert datatype_id == 'edn'

    def test_flatonly(self):
        flag = EDNIterable.is_flatonly()
        assert flag == False

    def test_openclose(self):
        """Test basic open/close"""
        test_file = 'testdata/test_edn.edn'
        os.makedirs('testdata', exist_ok=True)
        
        # Create a simple EDN file
        with open(test_file, 'w') as f:
            f.write('{:name "test" :value 42}')
        
        iterable = EDNIterable(test_file)
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_one(self):
        """Test reading single record"""
        test_file = 'testdata/test_edn_read.edn'
        os.makedirs('testdata', exist_ok=True)
        
        # Create EDN file
        with open(test_file, 'w') as f:
            if HAS_EDN_FORMAT:
                f.write('{:name "test" :value 42}')
            else:
                f.write('{:name "test" :value 42}')
        
        iterable = EDNIterable(test_file)
        record = iterable.read()
        assert isinstance(record, dict)
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_bulk(self):
        """Test reading bulk records"""
        test_file = 'testdata/test_edn_bulk.edn'
        os.makedirs('testdata', exist_ok=True)
        
        # Create EDN file with multiple values
        with open(test_file, 'w') as f:
            f.write('{:key1 "value1"}\n{:key2 "value2"}')
        
        iterable = EDNIterable(test_file)
        chunk = iterable.read_bulk(2)
        assert isinstance(chunk, list)
        assert len(chunk) > 0
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_write(self):
        """Test writing EDN record"""
        test_file = 'testdata/test_edn_write.edn'
        os.makedirs('testdata', exist_ok=True)
        
        iterable = EDNIterable(test_file, mode='w')
        record = {'name': 'test', 'value': 42}
        iterable.write(record)
        iterable.close()
        
        # Verify file was created
        assert os.path.exists(test_file)
        assert os.path.getsize(test_file) > 0
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_write_bulk(self):
        """Test writing bulk EDN records"""
        test_file = 'testdata/test_edn_write_bulk.edn'
        os.makedirs('testdata', exist_ok=True)
        
        iterable = EDNIterable(test_file, mode='w')
        records = [
            {'key1': 'value1'},
            {'key2': 'value2'}
        ]
        iterable.write_bulk(records)
        iterable.close()
        
        assert os.path.exists(test_file)
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_reset(self):
        """Test reset functionality"""
        test_file = 'testdata/test_edn_reset.edn'
        os.makedirs('testdata', exist_ok=True)
        
        # Create EDN file
        with open(test_file, 'w') as f:
            f.write('{:key "value"}')
        
        iterable = EDNIterable(test_file)
        record1 = iterable.read()
        iterable.reset()
        record2 = iterable.read()
        # After reset, should read the same record
        assert record1 == record2
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

