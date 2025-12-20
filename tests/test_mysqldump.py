# -*- coding: utf-8 -*-
import pytest
import os
from iterable.datatypes import MySQLDumpIterable


class TestMySQLDump:
    def test_id(self):
        datatype_id = MySQLDumpIterable.id()
        assert datatype_id == 'mysqldump'

    def test_flatonly(self):
        flag = MySQLDumpIterable.is_flatonly()
        assert flag == True

    def test_openclose(self):
        """Test basic open/close"""
        test_file = 'testdata/test_mysqldump.sql'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('INSERT INTO `test_table` VALUES (1, "value1"), (2, "value2");\n')
        
        iterable = MySQLDumpIterable(test_file)
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_one(self):
        """Test reading single MySQL dump record"""
        test_file = 'testdata/test_mysqldump_read.sql'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('INSERT INTO `test_table` VALUES (1, "value1");\n')
        
        iterable = MySQLDumpIterable(test_file)
        record = iterable.read()
        assert isinstance(record, dict)
        assert '_table' in record
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_bulk(self):
        """Test reading bulk MySQL dump records"""
        test_file = 'testdata/test_mysqldump_bulk.sql'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('INSERT INTO `test_table` VALUES (1, "value1"), (2, "value2");\n')
        
        iterable = MySQLDumpIterable(test_file)
        chunk = iterable.read_bulk(2)
        assert isinstance(chunk, list)
        assert len(chunk) > 0
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_with_table_filter(self):
        """Test reading with table_name filter"""
        test_file = 'testdata/test_mysqldump_filter.sql'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('INSERT INTO `table1` VALUES (1, "value1");\n')
            f.write('INSERT INTO `table2` VALUES (2, "value2");\n')
        
        iterable = MySQLDumpIterable(test_file, table_name='table1')
        records = list(iterable)
        iterable.close()
        
        # Should only have records from table1
        assert all(r.get('_table') == 'table1' for r in records)
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_reset(self):
        """Test reset functionality"""
        test_file = 'testdata/test_mysqldump_reset.sql'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('INSERT INTO `test_table` VALUES (1, "value1");\n')
        
        iterable = MySQLDumpIterable(test_file)
        record1 = iterable.read()
        iterable.reset()
        record2 = iterable.read()
        assert record1 == record2
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

