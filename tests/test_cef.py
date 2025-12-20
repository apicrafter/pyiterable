# -*- coding: utf-8 -*-
import pytest
import os
from iterable.datatypes import CEFIterable


class TestCEF:
    def test_id(self):
        datatype_id = CEFIterable.id()
        assert datatype_id == 'cef'

    def test_flatonly(self):
        flag = CEFIterable.is_flatonly()
        assert flag == True

    def test_has_totals(self):
        flag = CEFIterable.has_totals()
        assert flag == True

    def test_openclose(self):
        """Test basic open/close"""
        test_file = 'testdata/test_cef.cef'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('CEF:0|Vendor|Product|1.0|100|Event|5|src=1.2.3.4\n')
        
        iterable = CEFIterable(test_file)
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_one(self):
        """Test reading single CEF record"""
        test_file = 'testdata/test_cef_read.cef'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('CEF:0|Vendor|Product|1.0|100|Event|5|src=1.2.3.4\n')
        
        iterable = CEFIterable(test_file)
        record = iterable.read()
        assert isinstance(record, dict)
        assert 'cef_version' in record or 'device_vendor' in record
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_bulk(self):
        """Test reading bulk CEF records"""
        test_file = 'testdata/test_cef_bulk.cef'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('CEF:0|Vendor|Product|1.0|100|Event1|5|src=1.2.3.4\n')
            f.write('CEF:0|Vendor|Product|1.0|101|Event2|6|src=5.6.7.8\n')
        
        iterable = CEFIterable(test_file)
        chunk = iterable.read_bulk(2)
        assert isinstance(chunk, list)
        assert len(chunk) == 2
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_totals(self):
        """Test totals() method"""
        test_file = 'testdata/test_cef_totals.cef'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('CEF:0|Vendor|Product|1.0|100|Event|5|src=1.2.3.4\n')
            f.write('CEF:0|Vendor|Product|1.0|101|Event|6|src=5.6.7.8\n')
        
        iterable = CEFIterable(test_file)
        total = iterable.totals()
        assert total >= 2
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_reset(self):
        """Test reset functionality"""
        test_file = 'testdata/test_cef_reset.cef'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('CEF:0|Vendor|Product|1.0|100|Event|5|src=1.2.3.4\n')
        
        iterable = CEFIterable(test_file)
        record1 = iterable.read()
        iterable.reset()
        record2 = iterable.read()
        assert record1 == record2
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_write(self):
        """Test writing CEF record"""
        test_file = 'testdata/test_cef_write.cef'
        os.makedirs('testdata', exist_ok=True)
        
        iterable = CEFIterable(test_file, mode='w')
        record = {
            'cef_version': '0',
            'device_vendor': 'Vendor',
            'device_product': 'Product',
            'device_version': '1.0',
            'signature_id': '100',
            'name': 'Test Event',
            'severity': '5',
            'extension': 'src=1.2.3.4'
        }
        iterable.write(record)
        iterable.close()
        
        assert os.path.exists(test_file)
        
        if os.path.exists(test_file):
            os.unlink(test_file)

