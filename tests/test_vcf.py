# -*- coding: utf-8 -*-
import pytest
import os
from iterable.datatypes import VCFIterable

try:
    import vobject
    HAS_VOBJECT = True
except ImportError:
    HAS_VOBJECT = False

try:
    import vcard
    HAS_VCARD = True
except ImportError:
    HAS_VCARD = False


@pytest.mark.skipif(not HAS_VOBJECT and not HAS_VCARD, reason="VCF support requires 'vobject' or 'vcard' package")
class TestVCF:
    def test_id(self):
        datatype_id = VCFIterable.id()
        assert datatype_id == 'vcf'

    def test_flatonly(self):
        flag = VCFIterable.is_flatonly()
        assert flag == False

    def test_openclose(self):
        """Test basic open/close"""
        test_file = 'testdata/test_vcf.vcf'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('BEGIN:VCARD\nVERSION:3.0\nFN:Test User\nEND:VCARD\n')
        
        iterable = VCFIterable(test_file)
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_one(self):
        """Test reading single VCard"""
        test_file = 'testdata/test_vcf_read.vcf'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('BEGIN:VCARD\nVERSION:3.0\nFN:Test User\nEND:VCARD\n')
        
        iterable = VCFIterable(test_file)
        record = iterable.read()
        assert isinstance(record, dict)
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_bulk(self):
        """Test reading bulk VCards"""
        test_file = 'testdata/test_vcf_bulk.vcf'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('BEGIN:VCARD\nVERSION:3.0\nFN:User 1\nEND:VCARD\n')
            f.write('BEGIN:VCARD\nVERSION:3.0\nFN:User 2\nEND:VCARD\n')
        
        iterable = VCFIterable(test_file)
        chunk = iterable.read_bulk(2)
        assert isinstance(chunk, list)
        assert len(chunk) > 0
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_reset(self):
        """Test reset functionality"""
        test_file = 'testdata/test_vcf_reset.vcf'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('BEGIN:VCARD\nVERSION:3.0\nFN:Test User\nEND:VCARD\n')
        
        iterable = VCFIterable(test_file)
        record1 = iterable.read()
        iterable.reset()
        record2 = iterable.read()
        # After reset, should read the same record
        assert record1 == record2
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

