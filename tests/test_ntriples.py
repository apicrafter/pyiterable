# -*- coding: utf-8 -*-
import pytest
import os
from iterable.datatypes import NTriplesIterable


class TestNTriples:
    def test_id(self):
        datatype_id = NTriplesIterable.id()
        assert datatype_id == 'ntriples'

    def test_flatonly(self):
        flag = NTriplesIterable.is_flatonly()
        assert flag == True

    def test_has_totals(self):
        flag = NTriplesIterable.has_totals()
        assert flag == True

    def test_openclose(self):
        """Test basic open/close"""
        test_file = 'testdata/test_ntriples.nt'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('<http://example.com/subject> <http://example.com/predicate> <http://example.com/object> .\n')
        
        iterable = NTriplesIterable(test_file)
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_one(self):
        """Test reading single N-Triples record"""
        test_file = 'testdata/test_ntriples_read.nt'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('<http://example.com/subject> <http://example.com/predicate> <http://example.com/object> .\n')
        
        iterable = NTriplesIterable(test_file)
        record = iterable.read()
        assert isinstance(record, dict)
        assert 'subject' in record or 'predicate' in record
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_bulk(self):
        """Test reading bulk N-Triples records"""
        test_file = 'testdata/test_ntriples_bulk.nt'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('<http://example.com/subject1> <http://example.com/predicate> <http://example.com/object1> .\n')
            f.write('<http://example.com/subject2> <http://example.com/predicate> <http://example.com/object2> .\n')
        
        iterable = NTriplesIterable(test_file)
        chunk = iterable.read_bulk(2)
        assert isinstance(chunk, list)
        assert len(chunk) == 2
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_totals(self):
        """Test totals() method"""
        test_file = 'testdata/test_ntriples_totals.nt'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('<http://example.com/subject1> <http://example.com/predicate> <http://example.com/object1> .\n')
            f.write('<http://example.com/subject2> <http://example.com/predicate> <http://example.com/object2> .\n')
        
        iterable = NTriplesIterable(test_file)
        total = iterable.totals()
        assert total >= 2
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_reset(self):
        """Test reset functionality"""
        test_file = 'testdata/test_ntriples_reset.nt'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('<http://example.com/subject> <http://example.com/predicate> <http://example.com/object> .\n')
        
        iterable = NTriplesIterable(test_file)
        record1 = iterable.read()
        iterable.reset()
        record2 = iterable.read()
        assert record1 == record2
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_write(self):
        """Test writing N-Triples record"""
        test_file = 'testdata/test_ntriples_write.nt'
        os.makedirs('testdata', exist_ok=True)
        
        iterable = NTriplesIterable(test_file, mode='w')
        record = {
            'subject': 'http://example.com/subject',
            'predicate': 'http://example.com/predicate',
            'object': 'http://example.com/object'
        }
        iterable.write(record)
        iterable.close()
        
        assert os.path.exists(test_file)
        
        if os.path.exists(test_file):
            os.unlink(test_file)

