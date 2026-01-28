import os

import pytest
from fixdata import FIXTURES_TYPES

from iterable.datatypes import HDF5Iterable

# Create fixture file if it doesn't exist
FIXTURE_FILE = "fixtures/2cols6rows.h5"


def setup_module():
    """Create fixture file if it doesn't exist"""
    try:
        import h5py
        import numpy as np

        if not os.path.exists(FIXTURE_FILE):
            with h5py.File(FIXTURE_FILE, "w") as f:
                # Create structured array
                dtype = [("id", "i4"), ("name", "S20")]
                data = np.array([(int(r["id"]), r["name"].encode()) for r in FIXTURES_TYPES], dtype=dtype)
                f.create_dataset("/data", data=data)
    except ImportError:
        pass  # Skip if h5py not available


class TestHDF5:
    def test_id(self):
        try:
            datatype_id = HDF5Iterable.id()
            assert datatype_id == "hdf5"
        except ImportError:
            pytest.skip("HDF5 support requires h5py package")

    def test_flatonly(self):
        try:
            flag = HDF5Iterable.is_flatonly()
            assert flag
        except ImportError:
            pytest.skip("HDF5 support requires h5py package")

    def test_openclose(self):
        try:
            if os.path.exists(FIXTURE_FILE):
                iterable = HDF5Iterable(FIXTURE_FILE, dataset_path="/data")
                iterable.close()
        except ImportError:
            pytest.skip("HDF5 support requires h5py package")

    def test_has_totals(self):
        try:
            if os.path.exists(FIXTURE_FILE):
                iterable = HDF5Iterable(FIXTURE_FILE, dataset_path="/data")
                assert HDF5Iterable.has_totals()
                total = iterable.totals()
                assert total > 0
                iterable.close()
        except ImportError:
            pytest.skip("HDF5 support requires h5py package")

    def test_read(self):
        try:
            if os.path.exists(FIXTURE_FILE):
                iterable = HDF5Iterable(FIXTURE_FILE, dataset_path="/data")
                row = iterable.read()
                assert isinstance(row, dict)
                iterable.close()
        except ImportError:
            pytest.skip("HDF5 support requires h5py package")

    def test_has_tables(self):
        try:
            flag = HDF5Iterable.has_tables()
            assert flag is True
        except ImportError:
            pytest.skip("HDF5 support requires h5py package")

    def test_list_tables_instance_method(self):
        """Test list_tables on an already-opened instance"""
        try:
            if os.path.exists(FIXTURE_FILE):
                iterable = HDF5Iterable(FIXTURE_FILE, dataset_path="/data")
                # Read a row to ensure file is open
                _ = iterable.read()
                # Now list tables - should reuse file handle
                datasets = iterable.list_tables()
                assert isinstance(datasets, list)
                assert len(datasets) > 0
                assert "/data" in datasets
                iterable.close()
        except ImportError:
            pytest.skip("HDF5 support requires h5py package")

    def test_list_tables_with_filename(self):
        """Test list_tables with filename parameter (class-like usage)"""
        try:
            if os.path.exists(FIXTURE_FILE):
                iterable = HDF5Iterable(FIXTURE_FILE, dataset_path="/data")
                datasets = iterable.list_tables(FIXTURE_FILE)
                assert isinstance(datasets, list)
                assert len(datasets) > 0
                assert "/data" in datasets
                iterable.close()
        except ImportError:
            pytest.skip("HDF5 support requires h5py package")

    def test_list_tables_reuses_file_handle(self):
        """Test that list_tables reuses open file handle"""
        try:
            if os.path.exists(FIXTURE_FILE):
                iterable = HDF5Iterable(FIXTURE_FILE, dataset_path="/data")
                # Read a row to ensure file is open
                _ = iterable.read()
                # Now list tables - should reuse file handle
                datasets1 = iterable.list_tables()
                datasets2 = iterable.list_tables()
                assert datasets1 == datasets2
                iterable.close()
        except ImportError:
            pytest.skip("HDF5 support requires h5py package")
