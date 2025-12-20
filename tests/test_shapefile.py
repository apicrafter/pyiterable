# -*- coding: utf-8 -*- 
import pytest
import os
from iterable.datatypes import ShapefileIterable
from fixdata import FIXTURES

# Create fixture file if it doesn't exist
FIXTURE_FILE = 'fixtures/2cols6rows.shp'

def setup_module():
    """Create fixture file if it doesn't exist"""
    try:
        import shapefile
    except ImportError:
        pytest.skip("pyshp library not available")
    
    if not os.path.exists(FIXTURE_FILE):
        # Create a simple shapefile
        w = shapefile.Writer(FIXTURE_FILE.replace('.shp', ''))
        w.field('id', 'C', 10)
        w.field('name', 'C', 50)
        
        for i, record in enumerate(FIXTURES):
            w.point(i, i)
            w.record(record['id'], record['name'])
        
        w.close()

class TestShapefile:
    def test_id(self):
        datatype_id = ShapefileIterable.id()
        assert datatype_id == 'shapefile'

    def test_flatonly(self):
        flag = ShapefileIterable.is_flatonly()
        assert flag == False

    def test_openclose(self):
        try:
            iterable = ShapefileIterable(FIXTURE_FILE)        
            iterable.close()
        except ImportError:
            pytest.skip("pyshp library not available")

    def test_has_totals(self):
        try:
            iterable = ShapefileIterable(FIXTURE_FILE)
            assert ShapefileIterable.has_totals() == True
            total = iterable.totals()
            assert total == len(FIXTURES)
            iterable.close()
        except ImportError:
            pytest.skip("pyshp library not available")

    def test_read(self):
        try:
            iterable = ShapefileIterable(FIXTURE_FILE)
            row = iterable.read()
            assert isinstance(row, dict)
            assert 'type' in row
            assert row['type'] == 'Feature'
            assert 'geometry' in row
            iterable.close()
        except ImportError:
            pytest.skip("pyshp library not available")

    def test_read_all(self):
        try:
            iterable = ShapefileIterable(FIXTURE_FILE)
            n = 0
            for row in iterable:
                assert isinstance(row, dict)
                assert 'geometry' in row
                n += 1
            assert n == len(FIXTURES)
            iterable.close()
        except ImportError:
            pytest.skip("pyshp library not available")

    def test_write_read(self):
        try:
            iterable = ShapefileIterable('testdata/2cols6rows_test.shp', mode='w')
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
            
            iterable = ShapefileIterable('testdata/2cols6rows_test.shp')
            n = 0
            for row in iterable:
                assert isinstance(row, dict)
                assert 'geometry' in row
                n += 1
            assert n == len(FIXTURES)
            iterable.close()
        except ImportError:
            pytest.skip("pyshp library not available")
