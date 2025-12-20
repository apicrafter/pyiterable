# -*- coding: utf-8 -*-
import pytest
import os
from iterable.datatypes import TxtIterable


class TestTXT:
    def test_id(self):
        datatype_id = TxtIterable.id()
        assert datatype_id == 'txt'

    def test_flatonly(self):
        flag = TxtIterable.is_flatonly()
        assert flag == False

    def test_has_totals(self):
        flag = TxtIterable.has_totals()
        assert flag == True

    def test_openclose(self):
        test_file = 'testdata/test_txt.txt'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('line1\nline2\nline3\n')
        
        iterable = TxtIterable(test_file)
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_one(self):
        """Test reading single line"""
        test_file = 'testdata/test_txt_read.txt'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('line1\nline2\nline3\n')
        
        iterable = TxtIterable(test_file)
        line = iterable.read()
        assert isinstance(line, str)
        assert line == 'line1'
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_bulk(self):
        """Test reading bulk lines"""
        test_file = 'testdata/test_txt_bulk.txt'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('line1\nline2\nline3\n')
        
        iterable = TxtIterable(test_file)
        chunk = iterable.read_bulk(2)
        assert isinstance(chunk, list)
        assert len(chunk) == 2
        assert chunk[0] == 'line1'
        assert chunk[1] == 'line2'
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_with_parser(self):
        """Test reading with parser function"""
        test_file = 'testdata/test_txt_parser.txt'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('name1,value1\nname2,value2\n')
        
        def parser(line):
            parts = line.split(',')
            return {'name': parts[0], 'value': parts[1]}
        
        iterable = TxtIterable(test_file, parser=parser)
        record = iterable.read()
        assert isinstance(record, dict)
        assert 'name' in record
        assert 'value' in record
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_skip_empty(self):
        """Test reading with skip_empty=True"""
        test_file = 'testdata/test_txt_empty.txt'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('line1\n\nline2\n')
        
        iterable = TxtIterable(test_file)
        line1 = iterable.read(skip_empty=True)
        line2 = iterable.read(skip_empty=True)
        assert line1 == 'line1'
        assert line2 == 'line2'  # Empty line should be skipped
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_totals(self):
        """Test totals() method"""
        test_file = 'testdata/test_txt_totals.txt'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('line1\nline2\nline3\n')
        
        iterable = TxtIterable(test_file)
        total = iterable.totals()
        assert total >= 3
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_write(self):
        """Test writing line"""
        test_file = 'testdata/test_txt_write.txt'
        os.makedirs('testdata', exist_ok=True)
        
        iterable = TxtIterable(test_file, mode='w')
        iterable.write('test line')
        iterable.close()
        
        # Verify file was created and contains the line
        assert os.path.exists(test_file)
        with open(test_file, 'r') as f:
            content = f.read()
            assert 'test line' in content
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_write_bulk(self):
        """Test writing bulk lines"""
        test_file = 'testdata/test_txt_write_bulk.txt'
        os.makedirs('testdata', exist_ok=True)
        
        iterable = TxtIterable(test_file, mode='w')
        iterable.write_bulk(['line1', 'line2', 'line3'])
        iterable.close()
        
        assert os.path.exists(test_file)
        with open(test_file, 'r') as f:
            lines = f.readlines()
            assert len(lines) == 3
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_write_with_parser(self):
        """Test writing with parser (dict to string conversion)"""
        test_file = 'testdata/test_txt_write_parser.txt'
        os.makedirs('testdata', exist_ok=True)
        
        def parser(line):
            parts = line.split(',')
            return {'name': parts[0], 'value': parts[1]}
        
        iterable = TxtIterable(test_file, mode='w', parser=parser)
        record = {'name': 'test', 'value': 'value1'}
        iterable.write(record)
        iterable.close()
        
        assert os.path.exists(test_file)
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_reset(self):
        """Test reset functionality"""
        test_file = 'testdata/test_txt_reset.txt'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('line1\nline2\n')
        
        iterable = TxtIterable(test_file)
        line1 = iterable.read()
        iterable.reset()
        line1_again = iterable.read()
        assert line1 == line1_again
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

