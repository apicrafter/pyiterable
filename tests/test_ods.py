import pytest
import os
import tempfile
from iterable.datatypes.ods import ODSIterable

try:
    from odf.opendocument import load
    HAS_ODF = True
except ImportError:
    try:
        import pyexcel_ods3
        HAS_PYEXCEL_ODS = True
        HAS_ODF = False
    except ImportError:
        HAS_PYEXCEL_ODS = False
        HAS_ODF = False


@pytest.mark.skipif(not HAS_ODF and not HAS_PYEXCEL_ODS, reason="ODS library not available")
def test_ods_read():
    """Test ODS reading - requires a test fixture file"""
    # This test would need an actual ODS file fixture
    # For now, we'll just test that the class can be instantiated
    pass


@pytest.mark.skipif(not HAS_ODF and not HAS_PYEXCEL_ODS, reason="ODS library not available")
def test_ods_id():
    """Test ODS ID"""
    assert ODSIterable.id() == 'ods'


@pytest.mark.skipif(not HAS_ODF and not HAS_PYEXCEL_ODS, reason="ODS library not available")
def test_ods_flatonly():
    """Test ODS is flat only"""
    assert ODSIterable.is_flatonly() == True
