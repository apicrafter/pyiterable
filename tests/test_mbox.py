# -*- coding: utf-8 -*-
import pytest
import os
from iterable.datatypes import MBOXIterable


class TestMBOX:
    def test_id(self):
        datatype_id = MBOXIterable.id()
        assert datatype_id == 'mbox'

    def test_flatonly(self):
        flag = MBOXIterable.is_flatonly()
        assert flag == False

    def test_openclose(self):
        """Test basic open/close"""
        test_file = 'testdata/test_mbox.mbox'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('From test@example.com Mon Jan  1 00:00:00 2024\n')
            f.write('From: test@example.com\nTo: user@example.com\nSubject: Test\n\nBody\n')
        
        iterable = MBOXIterable(test_file)
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_one(self):
        """Test reading single email from mbox"""
        test_file = 'testdata/test_mbox_read.mbox'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('From test@example.com Mon Jan  1 00:00:00 2024\n')
            f.write('From: test@example.com\nTo: user@example.com\nSubject: Test\n\nBody\n')
        
        iterable = MBOXIterable(test_file)
        record = iterable.read()
        assert isinstance(record, dict)
        assert 'from' in record or 'subject' in record
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_bulk(self):
        """Test reading bulk emails from mbox"""
        test_file = 'testdata/test_mbox_bulk.mbox'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('From test@example.com Mon Jan  1 00:00:00 2024\n')
            f.write('From: test@example.com\nSubject: Test1\n\nBody1\n')
            f.write('From test2@example.com Mon Jan  1 00:00:01 2024\n')
            f.write('From: test2@example.com\nSubject: Test2\n\nBody2\n')
        
        iterable = MBOXIterable(test_file)
        chunk = iterable.read_bulk(2)
        assert isinstance(chunk, list)
        assert len(chunk) > 0
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_reset(self):
        """Test reset functionality"""
        test_file = 'testdata/test_mbox_reset.mbox'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('From test@example.com Mon Jan  1 00:00:00 2024\n')
            f.write('From: test@example.com\nSubject: Test\n\nBody\n')
        
        iterable = MBOXIterable(test_file)
        record1 = iterable.read()
        iterable.reset()
        record2 = iterable.read()
        assert record1 == record2
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_write(self):
        """Test writing email to mbox"""
        test_file = 'testdata/test_mbox_write.mbox'
        os.makedirs('testdata', exist_ok=True)
        
        iterable = MBOXIterable(test_file, mode='w')
        record = {
            'from': 'test@example.com',
            'to': 'user@example.com',
            'subject': 'Test',
            'body': 'Test body'
        }
        iterable.write(record)
        iterable.close()
        
        assert os.path.exists(test_file)
        
        if os.path.exists(test_file):
            os.unlink(test_file)

