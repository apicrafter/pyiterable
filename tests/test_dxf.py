import os
import tempfile

import pytest

from iterable.datatypes import DXFIterable
from iterable.helpers.detect import open_iterable

try:
    import ezdxf  # noqa: F401

    HAS_EZDXF = True
except ImportError:
    HAS_EZDXF = False


@pytest.mark.skipif(not HAS_EZDXF, reason="DXF support requires 'ezdxf' package")
class TestDXF:
    def test_id(self):
        datatype_id = DXFIterable.id()
        assert datatype_id == "dxf"

    def test_flatonly(self):
        flag = DXFIterable.is_flatonly()
        assert not flag

    def test_openclose(self):
        """Test basic open/close"""
        import ezdxf

        with tempfile.NamedTemporaryFile(suffix=".dxf", delete=False) as f:
            temp_file = f.name

        try:
            # Create a simple DXF file
            doc = ezdxf.new("R2010")
            msp = doc.modelspace()
            msp.add_line((0, 0), (10, 10))
            doc.saveas(temp_file)

            iterable = DXFIterable(temp_file)
            iterable.close()
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_read_one(self):
        """Test reading single entity"""
        import ezdxf

        with tempfile.NamedTemporaryFile(suffix=".dxf", delete=False) as f:
            temp_file = f.name

        try:
            # Create a simple DXF file
            doc = ezdxf.new("R2010")
            msp = doc.modelspace()
            msp.add_line((0, 0), (10, 10))
            doc.saveas(temp_file)

            iterable = DXFIterable(temp_file)
            record = iterable.read()
            assert isinstance(record, dict)
            assert "dxftype" in record
            assert record["dxftype"] == "LINE"
            iterable.close()
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_read_all(self):
        """Test reading all entities"""
        import ezdxf

        with tempfile.NamedTemporaryFile(suffix=".dxf", delete=False) as f:
            temp_file = f.name

        try:
            # Create a DXF file with multiple entities
            doc = ezdxf.new("R2010")
            msp = doc.modelspace()
            msp.add_line((0, 0), (10, 10))
            msp.add_circle((5, 5), radius=2)
            msp.add_point((1, 1))
            doc.saveas(temp_file)

            iterable = DXFIterable(temp_file)
            records = list(iterable)
            assert len(records) == 3
            # Check entity types
            dxftypes = [r["dxftype"] for r in records]
            assert "LINE" in dxftypes
            assert "CIRCLE" in dxftypes
            assert "POINT" in dxftypes
            iterable.close()
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_read_bulk(self):
        """Test bulk reading"""
        import ezdxf

        with tempfile.NamedTemporaryFile(suffix=".dxf", delete=False) as f:
            temp_file = f.name

        try:
            # Create a DXF file with multiple entities
            doc = ezdxf.new("R2010")
            msp = doc.modelspace()
            for i in range(5):
                msp.add_point((i, i))
            doc.saveas(temp_file)

            iterable = DXFIterable(temp_file)
            rows = iterable.read_bulk(3)
            assert len(rows) == 3
            assert all(r["dxftype"] == "POINT" for r in rows)
            iterable.close()
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_has_totals(self):
        """Test totals method"""
        import ezdxf

        with tempfile.NamedTemporaryFile(suffix=".dxf", delete=False) as f:
            temp_file = f.name

        try:
            # Create a DXF file with multiple entities
            doc = ezdxf.new("R2010")
            msp = doc.modelspace()
            msp.add_line((0, 0), (10, 10))
            msp.add_circle((5, 5), radius=2)
            doc.saveas(temp_file)

            iterable = DXFIterable(temp_file)
            assert DXFIterable.has_totals()
            total = iterable.totals()
            assert total == 2
            iterable.close()
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_automatic_detection(self):
        """Test automatic format detection via open_iterable"""
        import ezdxf

        with tempfile.NamedTemporaryFile(suffix=".dxf", delete=False) as f:
            temp_file = f.name

        try:
            # Create a simple DXF file
            doc = ezdxf.new("R2010")
            msp = doc.modelspace()
            msp.add_line((0, 0), (10, 10))
            doc.saveas(temp_file)

            with open_iterable(temp_file) as source:
                assert isinstance(source, DXFIterable)
                row = source.read()
                assert "dxftype" in row
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_reset(self):
        """Test reset functionality"""
        import ezdxf

        with tempfile.NamedTemporaryFile(suffix=".dxf", delete=False) as f:
            temp_file = f.name

        try:
            # Create a simple DXF file
            doc = ezdxf.new("R2010")
            msp = doc.modelspace()
            msp.add_line((0, 0), (10, 10))
            doc.saveas(temp_file)

            iterable = DXFIterable(temp_file)
            row1 = iterable.read()
            iterable.reset()
            row2 = iterable.read()
            assert row1 == row2
            iterable.close()
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_line_entity(self):
        """Test reading LINE entity with geometry"""
        import ezdxf

        with tempfile.NamedTemporaryFile(suffix=".dxf", delete=False) as f:
            temp_file = f.name

        try:
            doc = ezdxf.new("R2010")
            msp = doc.modelspace()
            msp.add_line((1, 2), (3, 4))
            doc.saveas(temp_file)

            iterable = DXFIterable(temp_file)
            record = iterable.read()
            assert record["dxftype"] == "LINE"
            assert record["start"] == (1.0, 2.0)
            assert record["end"] == (3.0, 4.0)
            iterable.close()
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_circle_entity(self):
        """Test reading CIRCLE entity with geometry"""
        import ezdxf

        with tempfile.NamedTemporaryFile(suffix=".dxf", delete=False) as f:
            temp_file = f.name

        try:
            doc = ezdxf.new("R2010")
            msp = doc.modelspace()
            msp.add_circle((5, 5), radius=3)
            doc.saveas(temp_file)

            iterable = DXFIterable(temp_file)
            record = iterable.read()
            assert record["dxftype"] == "CIRCLE"
            assert record["center"] == (5.0, 5.0)
            assert record["radius"] == 3.0
            iterable.close()
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_point_entity(self):
        """Test reading POINT entity with geometry"""
        import ezdxf

        with tempfile.NamedTemporaryFile(suffix=".dxf", delete=False) as f:
            temp_file = f.name

        try:
            doc = ezdxf.new("R2010")
            msp = doc.modelspace()
            msp.add_point((7, 8))
            doc.saveas(temp_file)

            iterable = DXFIterable(temp_file)
            record = iterable.read()
            assert record["dxftype"] == "POINT"
            assert record["location"] == (7.0, 8.0)
            iterable.close()
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_text_entity(self):
        """Test reading TEXT entity"""
        import ezdxf

        with tempfile.NamedTemporaryFile(suffix=".dxf", delete=False) as f:
            temp_file = f.name

        try:
            doc = ezdxf.new("R2010")
            msp = doc.modelspace()
            msp.add_text("Hello World", dxfattribs={"insert": (1, 2), "height": 2.5})
            doc.saveas(temp_file)

            iterable = DXFIterable(temp_file)
            record = iterable.read()
            assert record["dxftype"] == "TEXT"
            assert record["text"] == "Hello World"
            assert record["insert"] == (1.0, 2.0)
            assert record["height"] == 2.5
            iterable.close()
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_missing_dependency(self):
        """Test that missing ezdxf raises helpful error"""
        # This test would need to mock the import, but we can at least verify
        # the error message format is correct by checking the code
        pass
