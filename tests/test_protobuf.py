# -*- coding: utf-8 -*- 
import pytest
import os
from iterable.datatypes import ProtobufIterable
from fixdata import FIXTURES

# Note: Protocol Buffers requires a message class definition
# This test will be skipped if protobuf is not available

class TestProtobuf:
    def test_id(self):
        try:
            datatype_id = ProtobufIterable.id()
            assert datatype_id == 'protobuf'
        except ImportError:
            pytest.skip("Protocol Buffers support requires protobuf package")

    def test_flatonly(self):
        try:
            flag = ProtobufIterable.is_flatonly()
            assert flag == False
        except ImportError:
            pytest.skip("Protocol Buffers support requires protobuf package")

    def test_requires_message_class(self):
        try:
            with pytest.raises(ValueError):
                iterable = ProtobufIterable('test.pb', mode='r')
        except ImportError:
            pytest.skip("Protocol Buffers support requires protobuf package")
