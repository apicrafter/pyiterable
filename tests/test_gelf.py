# -*- coding: utf-8 -*-
import pytest
import os
from iterable.datatypes import GELIterable


class TestGELF:
    def test_id(self):
        datatype_id = GELIterable.id()
        assert datatype_id == 'gelf'

    def test_flatonly(self):
        flag = GELIterable.is_flatonly()
        assert flag == False

    def test_has_totals(self):
        flag = GELIterable.has_totals()
        assert flag == True

    def test_openclose(self):
        """Test basic open/close"""
        test_file = 'testdata/test_gelf.gelf'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('{"version":"1.1","host":"test","short_message":"Test"}\n')
        
        iterable = GELIterable(test_file)
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_one(self):
        """Test reading single GELF record"""
        test_file = 'testdata/test_gelf_read.gelf'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('{"version":"1.1","host":"test","short_message":"Test"}\n')
        
        iterable = GELIterable(test_file)
        record = iterable.read()
        assert isinstance(record, dict)
        assert 'version' in record or 'host' in record
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_bulk(self):
        """Test reading bulk GELF records"""
        test_file = 'testdata/test_gelf_bulk.gelf'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('{"version":"1.1","host":"test1","short_message":"Test1"}\n')
            f.write('{"version":"1.1","host":"test2","short_message":"Test2"}\n')
        
        iterable = GELIterable(test_file)
        chunk = iterable.read_bulk(2)
        assert isinstance(chunk, list)
        assert len(chunk) == 2
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_totals(self):
        """Test totals() method"""
        test_file = 'testdata/test_gelf_totals.gelf'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('{"version":"1.1","host":"test","short_message":"Test"}\n')
            f.write('{"version":"1.1","host":"test2","short_message":"Test2"}\n')
        
        iterable = GELIterable(test_file)
        total = iterable.totals()
        assert total >= 2
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_reset(self):
        """Test reset functionality"""
        test_file = 'testdata/test_gelf_reset.gelf'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('{"version":"1.1","host":"test","short_message":"Test"}\n')
        
        iterable = GELIterable(test_file)
        record1 = iterable.read()
        iterable.reset()
        record2 = iterable.read()
        assert record1 == record2
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_write(self):
        """Test writing GELF record"""
        test_file = 'testdata/test_gelf_write.gelf'
        os.makedirs('testdata', exist_ok=True)
        
        iterable = GELIterable(test_file, mode='w')
        record = {'version': '1.1', 'host': 'test', 'short_message': 'Test message'}
        iterable.write(record)
        iterable.close()
        
        assert os.path.exists(test_file)
        
        if os.path.exists(test_file):
            os.unlink(test_file)

