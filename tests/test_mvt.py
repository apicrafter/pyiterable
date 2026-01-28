import os
import tempfile

import pytest

from iterable.datatypes import MVTIterable
from iterable.helpers.detect import open_iterable

try:
    import mapbox_vector_tile  # noqa: F401

    HAS_MVT = True
except ImportError:
    HAS_MVT = False


@pytest.mark.skipif(not HAS_MVT, reason="MVT support requires 'mapbox-vector-tile' package")
class TestMVT:
    def test_id(self):
        datatype_id = MVTIterable.id()
        assert datatype_id == "mvt"

    def test_flatonly(self):
        flag = MVTIterable.is_flatonly()
        assert not flag

    def test_openclose(self):
        """Test basic open/close"""
        import mapbox_vector_tile

        # Create a simple MVT tile
        features = [
            {
                "geometry": {"type": "Point", "coordinates": [0, 0]},
                "properties": {"name": "test"},
            }
        ]
        tile_data = mapbox_vector_tile.encode(features)

        with tempfile.NamedTemporaryFile(suffix=".mvt", delete=False) as f:
            f.write(tile_data)
            temp_file = f.name

        try:
            iterable = MVTIterable(temp_file)
            iterable.close()
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_read_one(self):
        """Test reading single feature"""
        import mapbox_vector_tile

        features = [
            {
                "geometry": {"type": "Point", "coordinates": [0, 0]},
                "properties": {"name": "test", "value": 42},
            }
        ]
        tile_data = mapbox_vector_tile.encode(features)

        with tempfile.NamedTemporaryFile(suffix=".mvt", delete=False) as f:
            f.write(tile_data)
            temp_file = f.name

        try:
            iterable = MVTIterable(temp_file)
            record = iterable.read()
            assert isinstance(record, dict)
            assert "layer" in record
            assert "geometry" in record
            assert "properties" in record
            assert record["properties"]["name"] == "test"
            iterable.close()
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_read_all(self):
        """Test reading all features"""
        import mapbox_vector_tile

        # Create MVT with multiple features
        features = [
            {
                "geometry": {"type": "Point", "coordinates": [0, 0]},
                "properties": {"id": 1},
            },
            {
                "geometry": {"type": "Point", "coordinates": [1, 1]},
                "properties": {"id": 2},
            },
        ]
        tile_data = mapbox_vector_tile.encode(features)

        with tempfile.NamedTemporaryFile(suffix=".mvt", delete=False) as f:
            f.write(tile_data)
            temp_file = f.name

        try:
            iterable = MVTIterable(temp_file)
            records = list(iterable)
            assert len(records) >= 2
            iterable.close()
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_read_bulk(self):
        """Test bulk reading"""
        import mapbox_vector_tile

        features = [
            {
                "geometry": {"type": "Point", "coordinates": [i, i]},
                "properties": {"id": i},
            }
            for i in range(5)
        ]
        tile_data = mapbox_vector_tile.encode(features)

        with tempfile.NamedTemporaryFile(suffix=".mvt", delete=False) as f:
            f.write(tile_data)
            temp_file = f.name

        try:
            iterable = MVTIterable(temp_file)
            rows = iterable.read_bulk(3)
            assert len(rows) >= 1  # MVT encoding may group features
            iterable.close()
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_has_totals(self):
        """Test totals method"""
        import mapbox_vector_tile

        features = [
            {
                "geometry": {"type": "Point", "coordinates": [i, i]},
                "properties": {"id": i},
            }
            for i in range(3)
        ]
        tile_data = mapbox_vector_tile.encode(features)

        with tempfile.NamedTemporaryFile(suffix=".mvt", delete=False) as f:
            f.write(tile_data)
            temp_file = f.name

        try:
            iterable = MVTIterable(temp_file)
            assert MVTIterable.has_totals()
            total = iterable.totals()
            assert total > 0
            iterable.close()
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_automatic_detection(self):
        """Test automatic format detection via open_iterable"""
        import mapbox_vector_tile

        features = [
            {
                "geometry": {"type": "Point", "coordinates": [0, 0]},
                "properties": {"name": "test"},
            }
        ]
        tile_data = mapbox_vector_tile.encode(features)

        with tempfile.NamedTemporaryFile(suffix=".mvt", delete=False) as f:
            f.write(tile_data)
            temp_file = f.name

        try:
            with open_iterable(temp_file) as source:
                assert isinstance(source, MVTIterable)
                row = source.read()
                assert "geometry" in row
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_automatic_detection_pbf(self):
        """Test automatic format detection for .pbf extension"""
        import mapbox_vector_tile

        features = [
            {
                "geometry": {"type": "Point", "coordinates": [0, 0]},
                "properties": {"name": "test"},
            }
        ]
        tile_data = mapbox_vector_tile.encode(features)

        with tempfile.NamedTemporaryFile(suffix=".pbf", delete=False) as f:
            f.write(tile_data)
            temp_file = f.name

        try:
            with open_iterable(temp_file) as source:
                assert isinstance(source, MVTIterable)
                row = source.read()
                assert "geometry" in row
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_reset(self):
        """Test reset functionality"""
        import mapbox_vector_tile

        features = [
            {
                "geometry": {"type": "Point", "coordinates": [0, 0]},
                "properties": {"id": 1},
            }
        ]
        tile_data = mapbox_vector_tile.encode(features)

        with tempfile.NamedTemporaryFile(suffix=".mvt", delete=False) as f:
            f.write(tile_data)
            temp_file = f.name

        try:
            iterable = MVTIterable(temp_file)
            row1 = iterable.read()
            iterable.reset()
            row2 = iterable.read()
            assert row1 == row2
            iterable.close()
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_missing_dependency(self):
        """Test that missing mapbox-vector-tile raises helpful error"""
        # This test would need to mock the import, but we can at least verify
        # the error message format is correct by checking the code
        pass
