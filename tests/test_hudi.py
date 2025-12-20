import pytest
from iterable.datatypes.hudi import HudiIterable

try:
    from pyhudi import HudiCatalog
    HAS_PYHUDI = True
except ImportError:
    try:
        import hudi
        HAS_HUDI = True
        HAS_PYHUDI = False
    except ImportError:
        HAS_HUDI = False
        HAS_PYHUDI = False


@pytest.mark.skipif(not HAS_PYHUDI and not HAS_HUDI, reason="Hudi library not available")
def test_hudi_id():
    """Test Hudi ID"""
    assert HudiIterable.id() == 'hudi'


@pytest.mark.skipif(not HAS_PYHUDI and not HAS_HUDI, reason="Hudi library not available")
def test_hudi_flatonly():
    """Test Hudi is flat only"""
    assert HudiIterable.is_flatonly() == True


@pytest.mark.skipif(not HAS_PYHUDI and not HAS_HUDI, reason="Hudi library not available")
def test_hudi_requires_table_path():
    """Test that Hudi requires table_path"""
    with pytest.raises(ValueError):
        HudiIterable(mode='r')
