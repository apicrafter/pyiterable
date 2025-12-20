# -*- coding: utf-8 -*-
import pytest
import os
from iterable.datatypes import EMLIterable


class TestEML:
    def test_id(self):
        datatype_id = EMLIterable.id()
        assert datatype_id == 'eml'

    def test_flatonly(self):
        flag = EMLIterable.is_flatonly()
        assert flag == False

    def test_openclose(self):
        """Test basic open/close"""
        test_file = 'testdata/test_eml.eml'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('From: test@example.com\nTo: user@example.com\nSubject: Test\n\nBody content\n')
        
        iterable = EMLIterable(test_file)
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_one(self):
        """Test reading single email"""
        test_file = 'testdata/test_eml_read.eml'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('From: test@example.com\nTo: user@example.com\nSubject: Test\n\nBody content\n')
        
        iterable = EMLIterable(test_file)
        record = iterable.read()
        assert isinstance(record, dict)
        assert 'from' in record or 'subject' in record
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_bulk(self):
        """Test reading bulk emails (EML typically has one email per file)"""
        test_file = 'testdata/test_eml_bulk.eml'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('From: test@example.com\nTo: user@example.com\nSubject: Test\n\nBody content\n')
        
        iterable = EMLIterable(test_file)
        chunk = iterable.read_bulk(1)
        assert isinstance(chunk, list)
        assert len(chunk) > 0
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_reset(self):
        """Test reset functionality"""
        test_file = 'testdata/test_eml_reset.eml'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('From: test@example.com\nTo: user@example.com\nSubject: Test\n\nBody content\n')
        
        iterable = EMLIterable(test_file)
        record1 = iterable.read()
        iterable.reset()
        record2 = iterable.read()
        assert record1 == record2
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

