import pytest
from iterable.datatypes.iceberg import IcebergIterable

try:
    import pyiceberg
    HAS_PYICEBERG = True
except ImportError:
    HAS_PYICEBERG = False


@pytest.mark.skipif(not HAS_PYICEBERG, reason="PyIceberg library not available")
def test_iceberg_id():
    """Test Iceberg ID"""
    assert IcebergIterable.id() == 'iceberg'


@pytest.mark.skipif(not HAS_PYICEBERG, reason="PyIceberg library not available")
def test_iceberg_flatonly():
    """Test Iceberg is flat only"""
    assert IcebergIterable.is_flatonly() == True


@pytest.mark.skipif(not HAS_PYICEBERG, reason="PyIceberg library not available")
def test_iceberg_requires_params():
    """Test that Iceberg requires catalog and table names"""
    with pytest.raises(ValueError):
        IcebergIterable('test.iceberg', mode='r')
