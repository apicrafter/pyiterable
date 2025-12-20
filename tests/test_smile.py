# -*- coding: utf-8 -*-
import pytest
import os
from iterable.datatypes import SMILEIterable

try:
    import smile
    HAS_SMILE = True
except ImportError:
    HAS_SMILE = False


@pytest.mark.skipif(not HAS_SMILE, reason="SMILE support requires 'smile-json' package")
class TestSMILE:
    def test_id(self):
        datatype_id = SMILEIterable.id()
        assert datatype_id == 'smile'

    def test_flatonly(self):
        flag = SMILEIterable.is_flatonly()
        assert flag == False

    def test_openclose(self):
        """Test basic open/close"""
        test_file = 'testdata/test_smile.smile'
        os.makedirs('testdata', exist_ok=True)
        
        # Create a simple SMILE file
        data = {'name': 'test', 'value': 42}
        smile_data = smile.dumps(data)
        with open(test_file, 'wb') as f:
            f.write(smile_data)
        
        iterable = SMILEIterable(test_file)
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_one(self):
        """Test reading single record"""
        test_file = 'testdata/test_smile_read.smile'
        os.makedirs('testdata', exist_ok=True)
        
        # Create SMILE file
        data = {'name': 'test', 'value': 42}
        smile_data = smile.dumps(data)
        with open(test_file, 'wb') as f:
            f.write(smile_data)
        
        iterable = SMILEIterable(test_file)
        record = iterable.read()
        assert isinstance(record, dict)
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_bulk(self):
        """Test reading bulk records"""
        test_file = 'testdata/test_smile_bulk.smile'
        os.makedirs('testdata', exist_ok=True)
        
        # Create SMILE file with array
        data = [{'name': 'test1'}, {'name': 'test2'}]
        smile_data = smile.dumps(data)
        with open(test_file, 'wb') as f:
            f.write(smile_data)
        
        iterable = SMILEIterable(test_file)
        chunk = iterable.read_bulk(2)
        assert isinstance(chunk, list)
        assert len(chunk) > 0
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_write(self):
        """Test writing SMILE record"""
        test_file = 'testdata/test_smile_write.smile'
        os.makedirs('testdata', exist_ok=True)
        
        iterable = SMILEIterable(test_file, mode='w')
        record = {'name': 'test', 'value': 42}
        iterable.write(record)
        iterable.close()
        
        # Verify file was created
        assert os.path.exists(test_file)
        assert os.path.getsize(test_file) > 0
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_write_bulk(self):
        """Test writing bulk SMILE records"""
        test_file = 'testdata/test_smile_write_bulk.smile'
        os.makedirs('testdata', exist_ok=True)
        
        iterable = SMILEIterable(test_file, mode='w')
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
        test_file = 'testdata/test_smile_reset.smile'
        os.makedirs('testdata', exist_ok=True)
        
        # Create SMILE file
        data = {'key': 'value'}
        smile_data = smile.dumps(data)
        with open(test_file, 'wb') as f:
            f.write(smile_data)
        
        iterable = SMILEIterable(test_file)
        record1 = iterable.read()
        iterable.reset()
        record2 = iterable.read()
        # After reset, should read the same record
        assert record1 == record2
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

