import pytest
import os
import tempfile
from iterable.datatypes.ubjson import UBJSONIterable

try:
    import ubjson
    HAS_UBJSON = True
except ImportError:
    HAS_UBJSON = False


@pytest.mark.skipif(not HAS_UBJSON, reason="UBJSON library not available")
def test_ubjson_read_write():
    """Test UBJSON read and write"""
    test_data = [
        {'name': 'Alice', 'age': 30, 'city': 'New York'},
        {'name': 'Bob', 'age': 25, 'city': 'London'}
    ]
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.ubj') as tmp:
        tmp_path = tmp.name
    
    try:
        # Write data
        writer = UBJSONIterable(tmp_path, mode='w')
        writer.write_bulk(test_data)
        writer.close()
        
        # Read data back
        reader = UBJSONIterable(tmp_path, mode='r')
        results = []
        for record in reader:
            results.append(record)
        reader.close()
        
        assert len(results) > 0
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


@pytest.mark.skipif(not HAS_UBJSON, reason="UBJSON library not available")
def test_ubjson_id():
    """Test UBJSON ID"""
    assert UBJSONIterable.id() == 'ubjson'


@pytest.mark.skipif(not HAS_UBJSON, reason="UBJSON library not available")
def test_ubjson_flatonly():
    """Test UBJSON is not flat only"""
    assert UBJSONIterable.is_flatonly() == False
