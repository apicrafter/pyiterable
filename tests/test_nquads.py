# -*- coding: utf-8 -*-
import pytest
import os
from iterable.datatypes import NQuadsIterable


class TestNQuads:
    def test_id(self):
        datatype_id = NQuadsIterable.id()
        assert datatype_id == 'nquads'

    def test_flatonly(self):
        flag = NQuadsIterable.is_flatonly()
        assert flag == True

    def test_has_totals(self):
        flag = NQuadsIterable.has_totals()
        assert flag == True

    def test_openclose(self):
        """Test basic open/close"""
        test_file = 'testdata/test_nquads.nq'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('<http://example.com/subject> <http://example.com/predicate> <http://example.com/object> <http://example.com/graph> .\n')
        
        iterable = NQuadsIterable(test_file)
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_one(self):
        """Test reading single N-Quads record"""
        test_file = 'testdata/test_nquads_read.nq'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('<http://example.com/subject> <http://example.com/predicate> <http://example.com/object> <http://example.com/graph> .\n')
        
        iterable = NQuadsIterable(test_file)
        record = iterable.read()
        assert isinstance(record, dict)
        assert 'subject' in record or 'graph' in record
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_bulk(self):
        """Test reading bulk N-Quads records"""
        test_file = 'testdata/test_nquads_bulk.nq'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('<http://example.com/subject1> <http://example.com/predicate> <http://example.com/object1> <http://example.com/graph> .\n')
            f.write('<http://example.com/subject2> <http://example.com/predicate> <http://example.com/object2> <http://example.com/graph> .\n')
        
        iterable = NQuadsIterable(test_file)
        chunk = iterable.read_bulk(2)
        assert isinstance(chunk, list)
        assert len(chunk) == 2
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_totals(self):
        """Test totals() method"""
        test_file = 'testdata/test_nquads_totals.nq'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('<http://example.com/subject1> <http://example.com/predicate> <http://example.com/object1> <http://example.com/graph> .\n')
            f.write('<http://example.com/subject2> <http://example.com/predicate> <http://example.com/object2> <http://example.com/graph> .\n')
        
        iterable = NQuadsIterable(test_file)
        total = iterable.totals()
        assert total >= 2
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_reset(self):
        """Test reset functionality"""
        test_file = 'testdata/test_nquads_reset.nq'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('<http://example.com/subject> <http://example.com/predicate> <http://example.com/object> <http://example.com/graph> .\n')
        
        iterable = NQuadsIterable(test_file)
        record1 = iterable.read()
        iterable.reset()
        record2 = iterable.read()
        assert record1 == record2
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_write(self):
        """Test writing N-Quads record"""
        test_file = 'testdata/test_nquads_write.nq'
        os.makedirs('testdata', exist_ok=True)
        
        iterable = NQuadsIterable(test_file, mode='w')
        record = {
            'subject': 'http://example.com/subject',
            'predicate': 'http://example.com/predicate',
            'object': 'http://example.com/object',
            'graph': 'http://example.com/graph'
        }
        iterable.write(record)
        iterable.close()
        
        assert os.path.exists(test_file)
        
        if os.path.exists(test_file):
            os.unlink(test_file)

