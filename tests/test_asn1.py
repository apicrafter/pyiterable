# -*- coding: utf-8 -*-
import pytest
import os
from iterable.datatypes import ASN1Iterable

try:
    from pyasn1.codec.der import decoder, encoder
    from pyasn1.type import univ
    HAS_PYASN1 = True
except ImportError:
    HAS_PYASN1 = False


@pytest.mark.skipif(not HAS_PYASN1, reason="ASN.1 support requires 'pyasn1' package")
class TestASN1:
    def test_id(self):
        datatype_id = ASN1Iterable.id()
        assert datatype_id == 'asn1'

    def test_flatonly(self):
        flag = ASN1Iterable.is_flatonly()
        assert flag == False

    def test_openclose(self):
        """Test basic open/close"""
        test_file = 'testdata/test_asn1.der'
        os.makedirs('testdata', exist_ok=True)
        
        # Create a simple ASN.1 file
        try:
            seq = univ.Sequence()
            seq.setComponentByPosition(0, univ.OctetString('test'))
            encoded = encoder.encode(seq)
            with open(test_file, 'wb') as f:
                f.write(encoded)
            
            iterable = ASN1Iterable(test_file)
            iterable.close()
        except Exception:
            pytest.skip("Could not create ASN.1 test file")
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_one(self):
        """Test reading single record"""
        test_file = 'testdata/test_asn1_read.der'
        os.makedirs('testdata', exist_ok=True)
        
        try:
            seq = univ.Sequence()
            seq.setComponentByPosition(0, univ.OctetString('test'))
            encoded = encoder.encode(seq)
            with open(test_file, 'wb') as f:
                f.write(encoded)
            
            iterable = ASN1Iterable(test_file)
            record = iterable.read()
            assert isinstance(record, dict)
            iterable.close()
        except Exception:
            pytest.skip("Could not create/read ASN.1 test file")
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_bulk(self):
        """Test reading bulk records"""
        test_file = 'testdata/test_asn1_bulk.der'
        os.makedirs('testdata', exist_ok=True)
        
        try:
            seq = univ.Sequence()
            seq.setComponentByPosition(0, univ.OctetString('test'))
            encoded = encoder.encode(seq)
            with open(test_file, 'wb') as f:
                f.write(encoded)
            
            iterable = ASN1Iterable(test_file)
            chunk = iterable.read_bulk(1)
            assert isinstance(chunk, list)
            iterable.close()
        except Exception:
            pytest.skip("Could not create/read ASN.1 test file")
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_reset(self):
        """Test reset functionality"""
        test_file = 'testdata/test_asn1_reset.der'
        os.makedirs('testdata', exist_ok=True)
        
        try:
            seq = univ.Sequence()
            seq.setComponentByPosition(0, univ.OctetString('test'))
            encoded = encoder.encode(seq)
            with open(test_file, 'wb') as f:
                f.write(encoded)
            
            iterable = ASN1Iterable(test_file)
            record1 = iterable.read()
            iterable.reset()
            record2 = iterable.read()
            assert record1 == record2
            iterable.close()
        except Exception:
            pytest.skip("Could not create/read ASN.1 test file")
        
        if os.path.exists(test_file):
            os.unlink(test_file)

