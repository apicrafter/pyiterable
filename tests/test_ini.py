# -*- coding: utf-8 -*-
import pytest
import os
from iterable.datatypes import INIIterable


class TestINI:
    def test_id(self):
        datatype_id = INIIterable.id()
        assert datatype_id == 'ini'

    def test_flatonly(self):
        flag = INIIterable.is_flatonly()
        assert flag == True

    def test_openclose(self):
        # Create a simple INI file for testing
        test_file = 'testdata/test_ini.ini'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('[section1]\nkey1=value1\nkey2=value2\n')
        
        iterable = INIIterable(test_file)
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_ini_sections(self):
        """Test reading INI file with sections"""
        test_file = 'testdata/test_ini_sections.ini'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('[section1]\nkey1=value1\nkey2=value2\n[section2]\nkey3=value3\n')
        
        iterable = INIIterable(test_file)
        records = list(iterable)
        iterable.close()
        
        assert len(records) >= 2
        # Check that sections are present
        sections = [r.get('_section') for r in records]
        assert 'section1' in sections or 'section2' in sections
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_ini_properties(self):
        """Test reading properties-style file"""
        test_file = 'testdata/test_ini_properties.ini'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('key1=value1\nkey2=value2\n')
        
        iterable = INIIterable(test_file)
        records = list(iterable)
        iterable.close()
        
        assert len(records) > 0
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_one(self):
        """Test reading single record"""
        test_file = 'testdata/test_ini_read.ini'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('[section1]\nkey1=value1\n')
        
        iterable = INIIterable(test_file)
        record = iterable.read()
        assert isinstance(record, dict)
        assert 'key1' in record or '_section' in record
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_bulk(self):
        """Test reading bulk records"""
        test_file = 'testdata/test_ini_bulk.ini'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('[section1]\nkey1=value1\n[section2]\nkey2=value2\n')
        
        iterable = INIIterable(test_file)
        chunk = iterable.read_bulk(2)
        assert isinstance(chunk, list)
        assert len(chunk) > 0
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_reset(self):
        """Test reset functionality"""
        test_file = 'testdata/test_ini_reset.ini'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('[section1]\nkey1=value1\n')
        
        iterable = INIIterable(test_file)
        record1 = iterable.read()
        iterable.reset()
        record2 = iterable.read()
        # After reset, should read the first record again
        assert record1.get('_section') == record2.get('_section')
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_write(self):
        """Test writing INI record"""
        test_file = 'testdata/test_ini_write.ini'
        os.makedirs('testdata', exist_ok=True)
        
        iterable = INIIterable(test_file, mode='w')
        record = {'_section': 'test_section', 'key1': 'value1', 'key2': 'value2'}
        iterable.write(record)
        iterable.close()
        
        # Verify file was created
        assert os.path.exists(test_file)
        
        # Read it back
        reader = INIIterable(test_file)
        records = list(reader)
        reader.close()
        
        # Should be able to read what we wrote
        assert len(records) > 0
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_write_bulk(self):
        """Test writing bulk INI records"""
        test_file = 'testdata/test_ini_write_bulk.ini'
        os.makedirs('testdata', exist_ok=True)
        
        iterable = INIIterable(test_file, mode='w')
        records = [
            {'_section': 'section1', 'key1': 'value1'},
            {'_section': 'section2', 'key2': 'value2'}
        ]
        iterable.write_bulk(records)
        iterable.close()
        
        assert os.path.exists(test_file)
        
        if os.path.exists(test_file):
            os.unlink(test_file)

