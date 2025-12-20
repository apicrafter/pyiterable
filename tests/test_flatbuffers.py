import pytest
from iterable.datatypes.flatbuffers import FlatBuffersIterable

try:
    import flatbuffers
    HAS_FLATBUFFERS = True
except ImportError:
    HAS_FLATBUFFERS = False


@pytest.mark.skipif(not HAS_FLATBUFFERS, reason="FlatBuffers library not available")
def test_flatbuffers_id():
    """Test FlatBuffers ID"""
    assert FlatBuffersIterable.id() == 'flatbuffers'


@pytest.mark.skipif(not HAS_FLATBUFFERS, reason="FlatBuffers library not available")
def test_flatbuffers_flatonly():
    """Test FlatBuffers is not flat only"""
    assert FlatBuffersIterable.is_flatonly() == False
