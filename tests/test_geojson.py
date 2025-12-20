# -*- coding: utf-8 -*- 
import pytest
import os
import json
from iterable.datatypes import GeoJSONIterable
from fixdata import FIXTURES

# Create fixture file if it doesn't exist
FIXTURE_FILE = 'fixtures/2cols6rows.geojson'

def setup_module():
    """Create fixture file if it doesn't exist"""
    if not os.path.exists(FIXTURE_FILE):
        # Create a simple GeoJSON FeatureCollection
        features = []
        for i, record in enumerate(FIXTURES):
            feature = {
                'type': 'Feature',
                'properties': record,
                'geometry': {
                    'type': 'Point',
                    'coordinates': [i, i]  # Simple coordinates
                }
            }
            features.append(feature)
        
        fc = {
            'type': 'FeatureCollection',
            'features': features
        }
        
        with open(FIXTURE_FILE, 'w', encoding='utf-8') as f:
            json.dump(fc, f)

class TestGeoJSON:
    def test_id(self):
        datatype_id = GeoJSONIterable.id()
        assert datatype_id == 'geojson'

    def test_flatonly(self):
        flag = GeoJSONIterable.is_flatonly()
        assert flag == False

    def test_openclose(self):
        iterable = GeoJSONIterable(FIXTURE_FILE)        
        iterable.close()

    def test_has_totals(self):
        iterable = GeoJSONIterable(FIXTURE_FILE)
        assert GeoJSONIterable.has_totals() == True
        total = iterable.totals()
        assert total == len(FIXTURES)
        iterable.close()

    def test_read(self):
        iterable = GeoJSONIterable(FIXTURE_FILE)
        row = iterable.read()
        assert isinstance(row, dict)
        assert 'type' in row
        assert row['type'] == 'Feature'
        iterable.close()

    def test_read_all(self):
        iterable = GeoJSONIterable(FIXTURE_FILE)
        n = 0
        for row in iterable:
            assert isinstance(row, dict)
            n += 1
        assert n == len(FIXTURES)
        iterable.close()

    def test_write_read(self):
        iterable = GeoJSONIterable('testdata/2cols6rows_test.geojson', mode='w')
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
        
        iterable = GeoJSONIterable('testdata/2cols6rows_test.geojson')
        n = 0
        for row in iterable:
            assert isinstance(row, dict)
            n += 1
        assert n == len(FIXTURES)
        iterable.close()
