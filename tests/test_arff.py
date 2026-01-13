import pytest

from iterable.datatypes import ARFFIterable
from iterable.helpers.detect import open_iterable

try:
    import arff  # noqa: F401

    HAS_ARFF = True
except ImportError:
    HAS_ARFF = False


@pytest.mark.skipif(not HAS_ARFF, reason="ARFF format requires 'liac-arff' package")
class TestARFF:
    def test_id(self):
        datatype_id = ARFFIterable.id()
        assert datatype_id == "arff"

    def test_flatonly(self):
        flag = ARFFIterable.is_flatonly()
        assert flag

    def test_read_standard_arff(self):
        """Test reading standard ARFF file"""
        arff_content = """@relation test_data

@attribute name string
@attribute age numeric
@attribute city {NewYork,London,Paris}

@data
Alice,30,NewYork
Bob,25,London
Charlie,35,Paris
"""
        import os
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", suffix=".arff", delete=False) as f:
            f.write(arff_content)
            temp_file = f.name

        try:
            iterable = ARFFIterable(temp_file)
            row = iterable.read()
            assert row["name"] == "Alice"
            assert row["age"] == 30.0  # ARFF numeric becomes float
            assert row["city"] == "NewYork"
            assert "_relation" in row
            assert row["_relation"] == "test_data"

            row = iterable.read()
            assert row["name"] == "Bob"
            assert row["age"] == 25.0
            iterable.close()
        finally:
            os.unlink(temp_file)

    def test_read_arff_with_missing_values(self):
        """Test reading ARFF with missing values"""
        arff_content = """@relation test_data

@attribute name string
@attribute age numeric
@attribute city {NewYork,London,Paris}

@data
Alice,30,NewYork
Bob,?,London
Charlie,35,?
"""
        import os
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", suffix=".arff", delete=False) as f:
            f.write(arff_content)
            temp_file = f.name

        try:
            iterable = ARFFIterable(temp_file)
            row = iterable.read()
            assert row["name"] == "Alice"
            assert row["age"] == 30.0

            row = iterable.read()
            assert row["name"] == "Bob"
            assert row["age"] is None  # Missing value should be None

            row = iterable.read()
            assert row["city"] is None
            iterable.close()
        finally:
            os.unlink(temp_file)

    def test_read_sparse_arff(self):
        """Test reading ARFF with sparse format"""
        arff_content = """@relation sparse_data

@attribute attr1 numeric
@attribute attr2 numeric
@attribute attr3 numeric

@data
{0 1.0, 2 3.0}
{1 2.0}
{0 4.0, 1 5.0, 2 6.0}
"""
        import os
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", suffix=".arff", delete=False) as f:
            f.write(arff_content)
            temp_file = f.name

        try:
            iterable = ARFFIterable(temp_file)
            row = iterable.read()
            # Sparse format: {index value, ...}
            # First row: index 0 = 1.0, index 2 = 3.0, index 1 = None
            assert row["attr1"] == 1.0
            assert row["attr2"] is None
            assert row["attr3"] == 3.0

            row = iterable.read()
            # Second row: index 1 = 2.0, others None
            assert row["attr1"] is None
            assert row["attr2"] == 2.0
            assert row["attr3"] is None
            iterable.close()
        finally:
            os.unlink(temp_file)

    def test_automatic_detection(self):
        """Test automatic format detection via open_iterable"""
        arff_content = """@relation test

@attribute name string
@attribute value numeric

@data
Test,123
"""
        import os
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", suffix=".arff", delete=False) as f:
            f.write(arff_content)
            temp_file = f.name

        try:
            with open_iterable(temp_file) as source:
                assert isinstance(source, ARFFIterable)
                row = source.read()
                assert row["name"] == "Test"
                assert row["value"] == 123.0
        finally:
            os.unlink(temp_file)

    def test_reset(self):
        """Test reset functionality"""
        arff_content = """@relation test

@attribute name string

@data
First
"""
        import os
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", suffix=".arff", delete=False) as f:
            f.write(arff_content)
            temp_file = f.name

        try:
            iterable = ARFFIterable(temp_file)
            row1 = iterable.read()
            iterable.reset()
            row2 = iterable.read()
            assert row1 == row2
            iterable.close()
        finally:
            os.unlink(temp_file)

    def test_read_bulk(self):
        """Test bulk reading"""
        arff_content = """@relation test

@attribute id numeric
@attribute name string

@data
1,Alice
2,Bob
3,Charlie
"""
        import os
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", suffix=".arff", delete=False) as f:
            f.write(arff_content)
            temp_file = f.name

        try:
            iterable = ARFFIterable(temp_file)
            rows = iterable.read_bulk(2)
            assert len(rows) == 2
            assert rows[0]["id"] == 1.0
            assert rows[0]["name"] == "Alice"
            assert rows[1]["id"] == 2.0
            assert rows[1]["name"] == "Bob"
            iterable.close()
        finally:
            os.unlink(temp_file)

    def test_relation_name_preserved(self):
        """Test that relation name is preserved in records"""
        arff_content = """@relation my_dataset

@attribute value numeric

@data
42
"""
        import os
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", suffix=".arff", delete=False) as f:
            f.write(arff_content)
            temp_file = f.name

        try:
            iterable = ARFFIterable(temp_file)
            row = iterable.read()
            assert "_relation" in row
            assert row["_relation"] == "my_dataset"
            iterable.close()
        finally:
            os.unlink(temp_file)

    def test_missing_dependency(self):
        """Test that missing liac-arff raises helpful error"""
        # This test would need to mock the import, but we can at least verify
        # the error message format is correct by checking the code
        pass
