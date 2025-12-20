import pytest
from iterable.datatypes.capnp import CapnpIterable

try:
    import capnp
    HAS_CAPNP = True
except ImportError:
    HAS_CAPNP = False


@pytest.mark.skipif(not HAS_CAPNP, reason="Cap'n Proto library not available")
def test_capnp_id():
    """Test Cap'n Proto ID"""
    assert CapnpIterable.id() == 'capnp'


@pytest.mark.skipif(not HAS_CAPNP, reason="Cap'n Proto library not available")
def test_capnp_flatonly():
    """Test Cap'n Proto is not flat only"""
    assert CapnpIterable.is_flatonly() == False


@pytest.mark.skipif(not HAS_CAPNP, reason="Cap'n Proto library not available")
def test_capnp_requires_schema():
    """Test that Cap'n Proto requires schema"""
    with pytest.raises(ValueError):
        CapnpIterable('test.capnp', mode='r')
