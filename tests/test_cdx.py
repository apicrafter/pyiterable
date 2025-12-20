# -*- coding: utf-8 -*-
import pytest
import os
from iterable.datatypes import CDXIterable


class TestCDX:
    def test_id(self):
        datatype_id = CDXIterable.id()
        assert datatype_id == 'cdx'

    def test_flatonly(self):
        flag = CDXIterable.is_flatonly()
        assert flag == True

    def test_has_totals(self):
        flag = CDXIterable.has_totals()
        assert flag == True

    def test_openclose(self):
        """Test basic open/close"""
        test_file = 'testdata/test_cdx.cdx'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('http://example.com 20240101120000 http://example.com text/html 200 -\n')
        
        iterable = CDXIterable(test_file)
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_one(self):
        """Test reading single CDX record"""
        test_file = 'testdata/test_cdx_read.cdx'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('http://example.com 20240101120000 http://example.com text/html 200 - - file.warc 0\n')
        
        iterable = CDXIterable(test_file)
        record = iterable.read()
        assert isinstance(record, dict)
        assert 'url' in record or 'timestamp' in record
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_bulk(self):
        """Test reading bulk CDX records"""
        test_file = 'testdata/test_cdx_bulk.cdx'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('http://example.com 20240101120000 http://example.com text/html 200 - - file.warc 0\n')
            f.write('http://example.org 20240101120001 http://example.org text/html 200 - - file.warc 100\n')
        
        iterable = CDXIterable(test_file)
        chunk = iterable.read_bulk(2)
        assert isinstance(chunk, list)
        assert len(chunk) == 2
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_totals(self):
        """Test totals() method"""
        test_file = 'testdata/test_cdx_totals.cdx'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('http://example.com 20240101120000 http://example.com text/html 200 - - file.warc 0\n')
            f.write('http://example.org 20240101120001 http://example.org text/html 200 - - file.warc 100\n')
        
        iterable = CDXIterable(test_file)
        total = iterable.totals()
        assert total >= 2
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_reset(self):
        """Test reset functionality"""
        test_file = 'testdata/test_cdx_reset.cdx'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('http://example.com 20240101120000 http://example.com text/html 200 - - file.warc 0\n')
        
        iterable = CDXIterable(test_file)
        record1 = iterable.read()
        iterable.reset()
        record2 = iterable.read()
        assert record1 == record2
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_write(self):
        """Test writing CDX record"""
        test_file = 'testdata/test_cdx_write.cdx'
        os.makedirs('testdata', exist_ok=True)
        
        iterable = CDXIterable(test_file, mode='w')
        record = {
            'url': 'http://example.com',
            'timestamp': '20240101120000',
            'original_url': 'http://example.com',
            'mime_type': 'text/html',
            'status_code': '200'
        }
        iterable.write(record)
        iterable.close()
        
        assert os.path.exists(test_file)
        
        if os.path.exists(test_file):
            os.unlink(test_file)

