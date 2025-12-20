import pytest
from iterable.datatypes.thrift import ThriftIterable

try:
    from thrift.transport import TTransport
    HAS_THRIFT = True
except ImportError:
    HAS_THRIFT = False


@pytest.mark.skipif(not HAS_THRIFT, reason="Thrift library not available")
def test_thrift_id():
    """Test Thrift ID"""
    assert ThriftIterable.id() == 'thrift'


@pytest.mark.skipif(not HAS_THRIFT, reason="Thrift library not available")
def test_thrift_flatonly():
    """Test Thrift is not flat only"""
    assert ThriftIterable.is_flatonly() == False


@pytest.mark.skipif(not HAS_THRIFT, reason="Thrift library not available")
def test_thrift_requires_struct_class():
    """Test that Thrift requires struct_class"""
    with pytest.raises(ValueError):
        ThriftIterable('test.thrift', mode='r')
