# -*- coding: utf-8 -*-
import pytest
import os
from iterable.datatypes import LDIFIterable

try:
    import ldif3
    HAS_LDIF3 = True
except ImportError:
    HAS_LDIF3 = False

try:
    import ldif
    HAS_LDIF = True
except ImportError:
    HAS_LDIF = False


@pytest.mark.skipif(not HAS_LDIF3 and not HAS_LDIF, reason="LDIF support requires 'ldif3' or 'ldif' package")
class TestLDIF:
    def test_id(self):
        datatype_id = LDIFIterable.id()
        assert datatype_id == 'ldif'

    def test_flatonly(self):
        flag = LDIFIterable.is_flatonly()
        assert flag == False

    def test_openclose(self):
        """Test basic open/close"""
        test_file = 'testdata/test_ldif.ldif'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('dn: cn=test,dc=example,dc=com\ncn: test\nobjectClass: person\n\n')
        
        iterable = LDIFIterable(test_file)
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_one(self):
        """Test reading single LDIF entry"""
        test_file = 'testdata/test_ldif_read.ldif'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('dn: cn=test,dc=example,dc=com\ncn: test\nobjectClass: person\n\n')
        
        iterable = LDIFIterable(test_file)
        record = iterable.read()
        assert isinstance(record, dict)
        assert 'dn' in record
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_bulk(self):
        """Test reading bulk LDIF entries"""
        test_file = 'testdata/test_ldif_bulk.ldif'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('dn: cn=test1,dc=example,dc=com\ncn: test1\n\n')
            f.write('dn: cn=test2,dc=example,dc=com\ncn: test2\n\n')
        
        iterable = LDIFIterable(test_file)
        chunk = iterable.read_bulk(2)
        assert isinstance(chunk, list)
        assert len(chunk) == 2
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_reset(self):
        """Test reset functionality"""
        test_file = 'testdata/test_ldif_reset.ldif'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('dn: cn=test,dc=example,dc=com\ncn: test\n\n')
        
        iterable = LDIFIterable(test_file)
        record1 = iterable.read()
        iterable.reset()
        record2 = iterable.read()
        assert record1 == record2
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

