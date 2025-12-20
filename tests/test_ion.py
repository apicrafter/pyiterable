# -*- coding: utf-8 -*- 
import pytest
import os
from iterable.datatypes import IonIterable
from fixdata import FIXTURES

# Create fixture file if it doesn't exist
FIXTURE_FILE = 'fixtures/2cols6rows_flat.ion'

def setup_module():
    """Create fixture file if it doesn't exist"""
    try:
        import ion
        if not os.path.exists(FIXTURE_FILE):
            with open(FIXTURE_FILE, 'wb') as f:
                for record in FIXTURES:
                    ion_data = ion.dumps(record)
                    f.write(ion_data)
    except ImportError:
        pass  # Skip if ion-python not available

class TestIon:
    def test_id(self):
        try:
            datatype_id = IonIterable.id()
            assert datatype_id == 'ion'
        except ImportError:
            pytest.skip("Ion support requires ion-python package")

    def test_flatonly(self):
        try:
            flag = IonIterable.is_flatonly()
            assert flag == False
        except ImportError:
            pytest.skip("Ion support requires ion-python package")

    def test_openclose(self):
        try:
            if os.path.exists(FIXTURE_FILE):
                iterable = IonIterable(FIXTURE_FILE)        
                iterable.close()
        except ImportError:
            pytest.skip("Ion support requires ion-python package")

    def test_read(self):
        try:
            if os.path.exists(FIXTURE_FILE):
                iterable = IonIterable(FIXTURE_FILE)
                row = iterable.read()
                assert isinstance(row, dict)
                iterable.close()
        except ImportError:
            pytest.skip("Ion support requires ion-python package")
