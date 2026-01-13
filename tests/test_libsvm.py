"""Tests for LIBSVM format"""

import os
import tempfile

import pytest

from iterable.datatypes.libsvm import LIBSVMIterable
from iterable.helpers.detect import open_iterable


class TestLIBSVM:
    """Test LIBSVM format reading and writing"""

    def test_read_libsvm(self):
        """Test reading LIBSVM format"""
        # Create test data
        test_data = """1 1:0.5 3:0.8 5:1.0
-1 2:0.3 4:0.9
1 1:0.2 3:0.6
0 1:0.1 2:0.2 3:0.3"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".libsvm", delete=False) as f:
            f.write(test_data)
            temp_file = f.name

        try:
            source = open_iterable(temp_file)
            records = list(source)
            source.close()

            assert len(records) == 4
            assert records[0]["label"] == 1
            assert records[0]["features"] == {1: 0.5, 3: 0.8, 5: 1.0}
            assert records[1]["label"] == -1
            assert records[1]["features"] == {2: 0.3, 4: 0.9}
            assert records[2]["label"] == 1
            assert records[2]["features"] == {1: 0.2, 3: 0.6}
            assert records[3]["label"] == 0
            assert records[3]["features"] == {1: 0.1, 2: 0.2, 3: 0.3}
        finally:
            os.unlink(temp_file)

    def test_write_libsvm(self):
        """Test writing LIBSVM format"""
        records = [
            {"label": 1, "features": {1: 0.5, 3: 0.8, 5: 1.0}},
            {"label": -1, "features": {2: 0.3, 4: 0.9}},
            {"label": 1, "features": {1: 0.2, 3: 0.6}},
        ]

        with tempfile.NamedTemporaryFile(mode="w", suffix=".libsvm", delete=False) as f:
            temp_file = f.name

        try:
            source = open_iterable(temp_file, mode="w")
            for record in records:
                source.write(record)
            source.close()

            # Read back
            source = open_iterable(temp_file)
            read_records = list(source)
            source.close()

            assert len(read_records) == 3
            assert read_records[0]["label"] == 1
            assert read_records[0]["features"] == {1: 0.5, 3: 0.8, 5: 1.0}
        finally:
            os.unlink(temp_file)

    def test_write_bulk_libsvm(self):
        """Test bulk writing LIBSVM format"""
        records = [
            {"label": 1, "features": {1: 0.5, 3: 0.8}},
            {"label": -1, "features": {2: 0.3}},
            {"label": 0, "features": {1: 0.1, 2: 0.2}},
        ]

        with tempfile.NamedTemporaryFile(mode="w", suffix=".libsvm", delete=False) as f:
            temp_file = f.name

        try:
            source = open_iterable(temp_file, mode="w")
            source.write_bulk(records)
            source.close()

            # Read back
            source = open_iterable(temp_file)
            read_records = list(source)
            source.close()

            assert len(read_records) == 3
        finally:
            os.unlink(temp_file)

    def test_read_bulk_libsvm(self):
        """Test bulk reading LIBSVM format"""
        test_data = """1 1:0.5 3:0.8
-1 2:0.3
0 1:0.1 2:0.2"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".libsvm", delete=False) as f:
            f.write(test_data)
            temp_file = f.name

        try:
            source = open_iterable(temp_file)
            chunk = source.read_bulk(2)
            assert len(chunk) == 2
            chunk2 = source.read_bulk(2)
            assert len(chunk2) == 1
            source.close()
        finally:
            os.unlink(temp_file)

    def test_custom_keys(self):
        """Test custom label and features keys"""
        test_data = """1 1:0.5 3:0.8
-1 2:0.3"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".libsvm", delete=False) as f:
            f.write(test_data)
            temp_file = f.name

        try:
            source = LIBSVMIterable(temp_file, label_key="target", features_key="attrs")
            records = list(source)
            source.close()

            assert "target" in records[0]
            assert "attrs" in records[0]
            assert records[0]["target"] == 1
            assert records[0]["attrs"] == {1: 0.5, 3: 0.8}
        finally:
            os.unlink(temp_file)

    def test_float_labels(self):
        """Test float labels"""
        test_data = """1.5 1:0.5 2:0.8
-0.5 1:0.3"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".libsvm", delete=False) as f:
            f.write(test_data)
            temp_file = f.name

        try:
            source = open_iterable(temp_file)
            records = list(source)
            source.close()

            assert records[0]["label"] == 1.5
            assert records[1]["label"] == -0.5
        finally:
            os.unlink(temp_file)

    def test_totals(self):
        """Test totals count"""
        test_data = """1 1:0.5
-1 2:0.3
0 1:0.1
"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".libsvm", delete=False) as f:
            f.write(test_data)
            temp_file = f.name

        try:
            source = open_iterable(temp_file)
            total = source.totals()
            source.close()

            assert total == 3
        finally:
            os.unlink(temp_file)

    def test_empty_file(self):
        """Test empty file"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".libsvm", delete=False) as f:
            temp_file = f.name

        try:
            source = open_iterable(temp_file)
            records = list(source)
            source.close()

            assert len(records) == 0
        finally:
            os.unlink(temp_file)

    def test_invalid_format(self):
        """Test invalid format handling"""
        test_data = """invalid line
1 1:0.5"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".libsvm", delete=False) as f:
            f.write(test_data)
            temp_file = f.name

        try:
            source = open_iterable(temp_file)
            with pytest.raises(ValueError):
                list(source)
            source.close()
        finally:
            os.unlink(temp_file)
