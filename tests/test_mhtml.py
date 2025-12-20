# -*- coding: utf-8 -*-
import pytest
import os
from iterable.datatypes import MHTMLIterable


class TestMHTML:
    def test_id(self):
        datatype_id = MHTMLIterable.id()
        assert datatype_id == 'mhtml'

    def test_flatonly(self):
        flag = MHTMLIterable.is_flatonly()
        assert flag == False

    def test_openclose(self):
        """Test basic open/close"""
        test_file = 'testdata/test_mhtml.mhtml'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('From: test@example.com\n')
            f.write('MIME-Version: 1.0\n')
            f.write('Content-Type: multipart/related; boundary="boundary"\n\n')
            f.write('--boundary\n')
            f.write('Content-Type: text/html\n\n')
            f.write('<html><body>Test</body></html>\n')
            f.write('--boundary--\n')
        
        iterable = MHTMLIterable(test_file)
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_one(self):
        """Test reading single MHTML part"""
        test_file = 'testdata/test_mhtml_read.mhtml'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('From: test@example.com\n')
            f.write('MIME-Version: 1.0\n')
            f.write('Content-Type: multipart/related; boundary="boundary"\n\n')
            f.write('--boundary\n')
            f.write('Content-Type: text/html\n\n')
            f.write('<html><body>Test</body></html>\n')
            f.write('--boundary--\n')
        
        iterable = MHTMLIterable(test_file)
        record = iterable.read()
        assert isinstance(record, dict)
        assert 'content_type' in record or 'content' in record
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_bulk(self):
        """Test reading bulk MHTML parts"""
        test_file = 'testdata/test_mhtml_bulk.mhtml'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('From: test@example.com\n')
            f.write('MIME-Version: 1.0\n')
            f.write('Content-Type: multipart/related; boundary="boundary"\n\n')
            f.write('--boundary\n')
            f.write('Content-Type: text/html\n\n')
            f.write('<html><body>Part1</body></html>\n')
            f.write('--boundary\n')
            f.write('Content-Type: image/png\n')
            f.write('Content-ID: <img1>\n\n')
            f.write('data\n')
            f.write('--boundary--\n')
        
        iterable = MHTMLIterable(test_file)
        chunk = iterable.read_bulk(2)
        assert isinstance(chunk, list)
        assert len(chunk) > 0
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_reset(self):
        """Test reset functionality"""
        test_file = 'testdata/test_mhtml_reset.mhtml'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('From: test@example.com\n')
            f.write('MIME-Version: 1.0\n')
            f.write('Content-Type: multipart/related; boundary="boundary"\n\n')
            f.write('--boundary\n')
            f.write('Content-Type: text/html\n\n')
            f.write('<html><body>Test</body></html>\n')
            f.write('--boundary--\n')
        
        iterable = MHTMLIterable(test_file)
        record1 = iterable.read()
        iterable.reset()
        record2 = iterable.read()
        assert record1 == record2
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

