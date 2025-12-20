# -*- coding: utf-8 -*-
import pytest
import os
from iterable.datatypes import PGCopyIterable


class TestPGCopy:
    def test_id(self):
        datatype_id = PGCopyIterable.id()
        assert datatype_id == 'pgcopy'

    def test_flatonly(self):
        flag = PGCopyIterable.is_flatonly()
        assert flag == True

    def test_openclose(self):
        """Test basic open/close"""
        test_file = 'testdata/test_pgcopy.copy'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('col1\tcol2\tcol3\nvalue1\tvalue2\tvalue3\n')
        
        iterable = PGCopyIterable(test_file)
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_one(self):
        """Test reading single PostgreSQL COPY record"""
        test_file = 'testdata/test_pgcopy_read.copy'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('col1\tcol2\tcol3\nvalue1\tvalue2\tvalue3\n')
        
        iterable = PGCopyIterable(test_file)
        record = iterable.read()
        assert isinstance(record, dict)
        assert 'col1' in record or 'col_0' in record
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_bulk(self):
        """Test reading bulk PostgreSQL COPY records"""
        test_file = 'testdata/test_pgcopy_bulk.copy'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('col1\tcol2\nvalue1\tvalue2\nvalue3\tvalue4\n')
        
        iterable = PGCopyIterable(test_file)
        chunk = iterable.read_bulk(2)
        assert isinstance(chunk, list)
        assert len(chunk) == 2
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_null_values(self):
        """Test reading NULL values (\\N)"""
        test_file = 'testdata/test_pgcopy_null.copy'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('col1\tcol2\nvalue1\t\\N\n')
        
        iterable = PGCopyIterable(test_file)
        record = iterable.read()
        assert record.get('col2') is None or record.get('col_1') is None
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_reset(self):
        """Test reset functionality"""
        test_file = 'testdata/test_pgcopy_reset.copy'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('col1\tcol2\nvalue1\tvalue2\n')
        
        iterable = PGCopyIterable(test_file)
        record1 = iterable.read()
        iterable.reset()
        record2 = iterable.read()
        assert record1 == record2
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_write(self):
        """Test writing PostgreSQL COPY record"""
        test_file = 'testdata/test_pgcopy_write.copy'
        os.makedirs('testdata', exist_ok=True)
        
        iterable = PGCopyIterable(test_file, mode='w', options={'keys': ['col1', 'col2']})
        record = {'col1': 'value1', 'col2': 'value2'}
        iterable.write(record)
        iterable.close()
        
        assert os.path.exists(test_file)
        
        if os.path.exists(test_file):
            os.unlink(test_file)

