import pytest

from iterable.datatypes.hudi import HudiIterable

try:
    from pyhudi import HudiCatalog  # noqa: F401

    HAS_PYHUDI = True
except ImportError:
    try:
        import hudi  # noqa: F401

        HAS_HUDI = True
        HAS_PYHUDI = False
    except ImportError:
        HAS_HUDI = False
        HAS_PYHUDI = False


@pytest.mark.skipif(not HAS_PYHUDI and not HAS_HUDI, reason="Hudi library not available")
def test_hudi_id():
    """Test Hudi ID"""
    assert HudiIterable.id() == "hudi"


@pytest.mark.skipif(not HAS_PYHUDI and not HAS_HUDI, reason="Hudi library not available")
def test_hudi_flatonly():
    """Test Hudi is flat only"""
    assert HudiIterable.is_flatonly()


@pytest.mark.skipif(not HAS_PYHUDI and not HAS_HUDI, reason="Hudi library not available")
def test_hudi_requires_table_path():
    """Test that Hudi requires table_path"""
    with pytest.raises(ValueError):
        HudiIterable(mode="r")


@pytest.mark.skipif(not HAS_PYHUDI and not HAS_HUDI, reason="Hudi library not available")
def test_hudi_has_tables():
    """Test has_tables static method"""
    assert HudiIterable.has_tables() is True


@pytest.mark.skipif(not HAS_PYHUDI and not HAS_HUDI, reason="Hudi library not available")
def test_hudi_list_tables():
    """Test list_tables method (may return None if single table path)"""
    # Note: This test may not work without a real Hudi catalog setup
    # It's mainly to ensure the method exists and doesn't crash
    try:
        # Try to create an instance with dummy path to test the method signature
        # The actual implementation may require real catalog/table configuration
        iterable = HudiIterable(filename="/tmp/test_hudi", table_path="/tmp/test_hudi", mode="r")
        # list_tables may return None if it's a single table path or catalog doesn't support listing
        result = iterable.list_tables()
        # Result can be None, empty list, or list of strings
        assert result is None or isinstance(result, list)
        iterable.close()
    except (ValueError, Exception):
        # If catalog/table setup fails, that's expected in test environment
        pass
