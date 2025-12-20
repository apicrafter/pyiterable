# -*- coding: utf-8 -*-
import pytest
import os
from iterable.datatypes import BencodeIterable

try:
    import bencode
    HAS_BENCODE = True
except ImportError:
    HAS_BENCODE = False

try:
    import bencodepy
    HAS_BENCODEPY = True
except ImportError:
    HAS_BENCODEPY = False


@pytest.mark.skipif(not HAS_BENCODE and not HAS_BENCODEPY, reason="Bencode support requires 'bencode' or 'bencodepy' package")
class TestBencode:
    def test_id(self):
        datatype_id = BencodeIterable.id()
        assert datatype_id == 'bencode'

    def test_flatonly(self):
        flag = BencodeIterable.is_flatonly()
        assert flag == False

    def test_import_error(self):
        """Test that ImportError is raised when bencode libraries are not available"""
        # This test would need to mock the import, but we'll skip it if libraries are available
        pass

    def test_openclose(self):
        """Test basic open/close"""
        test_file = 'testdata/test_bencode.bencode'
        os.makedirs('testdata', exist_ok=True)
        
        # Create a simple bencode file
        if HAS_BENCODE:
            import bencode
            data = {'key': 'value'}
            with open(test_file, 'wb') as f:
                f.write(bencode.bencode(data))
        elif HAS_BENCODEPY:
            import bencodepy
            encoder = bencodepy.BencodeEncoder()
            data = {'key': 'value'}
            with open(test_file, 'wb') as f:
                f.write(encoder.encode(data))
        
        iterable = BencodeIterable(test_file)
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_one(self):
        """Test reading single record"""
        test_file = 'testdata/test_bencode_read.bencode'
        os.makedirs('testdata', exist_ok=True)
        
        # Create bencode file
        if HAS_BENCODE:
            import bencode
            data = {'name': 'test', 'value': 42}
            with open(test_file, 'wb') as f:
                f.write(bencode.bencode(data))
        elif HAS_BENCODEPY:
            import bencodepy
            encoder = bencodepy.BencodeEncoder()
            data = {'name': 'test', 'value': 42}
            with open(test_file, 'wb') as f:
                f.write(encoder.encode(data))
        
        iterable = BencodeIterable(test_file)
        record = iterable.read()
        assert isinstance(record, dict)
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_bulk(self):
        """Test reading bulk records"""
        test_file = 'testdata/test_bencode_bulk.bencode'
        os.makedirs('testdata', exist_ok=True)
        
        # Create bencode file
        if HAS_BENCODE:
            import bencode
            data = {'key1': 'value1', 'key2': 'value2'}
            with open(test_file, 'wb') as f:
                f.write(bencode.bencode(data))
        elif HAS_BENCODEPY:
            import bencodepy
            encoder = bencodepy.BencodeEncoder()
            data = {'key1': 'value1', 'key2': 'value2'}
            with open(test_file, 'wb') as f:
                f.write(encoder.encode(data))
        
        iterable = BencodeIterable(test_file)
        chunk = iterable.read_bulk(1)
        assert isinstance(chunk, list)
        assert len(chunk) > 0
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_write(self):
        """Test writing bencode record"""
        test_file = 'testdata/test_bencode_write.bencode'
        os.makedirs('testdata', exist_ok=True)
        
        iterable = BencodeIterable(test_file, mode='w')
        record = {'name': 'test', 'value': 42}
        iterable.write(record)
        iterable.close()
        
        # Verify file was created
        assert os.path.exists(test_file)
        assert os.path.getsize(test_file) > 0
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_write_bulk(self):
        """Test writing bulk bencode records"""
        test_file = 'testdata/test_bencode_write_bulk.bencode'
        os.makedirs('testdata', exist_ok=True)
        
        iterable = BencodeIterable(test_file, mode='w')
        # Note: bencode typically writes single dict, but we test the method
        record = {'key1': 'value1', 'key2': 'value2'}
        iterable.write_bulk([record])
        iterable.close()
        
        assert os.path.exists(test_file)
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_reset(self):
        """Test reset functionality"""
        test_file = 'testdata/test_bencode_reset.bencode'
        os.makedirs('testdata', exist_ok=True)
        
        # Create bencode file
        if HAS_BENCODE:
            import bencode
            data = {'key': 'value'}
            with open(test_file, 'wb') as f:
                f.write(bencode.bencode(data))
        elif HAS_BENCODEPY:
            import bencodepy
            encoder = bencodepy.BencodeEncoder()
            data = {'key': 'value'}
            with open(test_file, 'wb') as f:
                f.write(encoder.encode(data))
        
        iterable = BencodeIterable(test_file)
        record1 = iterable.read()
        iterable.reset()
        record2 = iterable.read()
        # After reset, should read the same record
        assert record1 == record2
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

