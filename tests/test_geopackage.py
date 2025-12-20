# -*- coding: utf-8 -*- 
import pytest
import os
from iterable.datatypes import GeoPackageIterable
from fixdata import FIXTURES

# Create fixture file if it doesn't exist
FIXTURE_FILE = 'fixtures/2cols6rows.gpkg'

def setup_module():
    """Create fixture file if it doesn't exist"""
    try:
        import fiona
    except ImportError:
        pytest.skip("fiona library not available")
    
    if not os.path.exists(FIXTURE_FILE):
        # Create a simple GeoPackage
        schema = {
            'geometry': 'Point',
            'properties': {
                'id': 'str',
                'name': 'str'
            }
        }
        
        with fiona.open(FIXTURE_FILE, 'w', driver='GPKG', schema=schema, crs='EPSG:4326') as f:
            for i, record in enumerate(FIXTURES):
                feature = {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Point',
                        'coordinates': (i, i)
                    },
                    'properties': record
                }
                f.write(feature)

class TestGeoPackage:
    def test_id(self):
        datatype_id = GeoPackageIterable.id()
        assert datatype_id == 'geopackage'

    def test_flatonly(self):
        flag = GeoPackageIterable.is_flatonly()
        assert flag == False

    def test_openclose(self):
        try:
            iterable = GeoPackageIterable(FIXTURE_FILE)        
            iterable.close()
        except ImportError:
            pytest.skip("fiona library not available")

    def test_has_totals(self):
        try:
            iterable = GeoPackageIterable(FIXTURE_FILE)
            assert GeoPackageIterable.has_totals() == True
            total = iterable.totals()
            assert total == len(FIXTURES)
            iterable.close()
        except ImportError:
            pytest.skip("fiona library not available")

    def test_read(self):
        try:
            iterable = GeoPackageIterable(FIXTURE_FILE)
            row = iterable.read()
            assert isinstance(row, dict)
            assert 'type' in row
            assert row['type'] == 'Feature'
            assert 'geometry' in row
            iterable.close()
        except ImportError:
            pytest.skip("fiona library not available")

    def test_read_all(self):
        try:
            iterable = GeoPackageIterable(FIXTURE_FILE)
            n = 0
            for row in iterable:
                assert isinstance(row, dict)
                assert 'geometry' in row
                n += 1
            assert n == len(FIXTURES)
            iterable.close()
        except ImportError:
            pytest.skip("fiona library not available")

    def test_write_read(self):
        try:
            iterable = GeoPackageIterable('testdata/2cols6rows_test.gpkg', mode='w')
            # Create features
            for i, record in enumerate(FIXTURES):
                feature = {
                    'type': 'Feature',
                    'properties': record,
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [i, i]
                    }
                }
                iterable.write(feature)
            iterable.close()
            
            iterable = GeoPackageIterable('testdata/2cols6rows_test.gpkg')
            n = 0
            for row in iterable:
                assert isinstance(row, dict)
                assert 'geometry' in row
                n += 1
            assert n == len(FIXTURES)
            iterable.close()
        except ImportError:
            pytest.skip("fiona library not available")
