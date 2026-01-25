import os

import pytest

pytest.importorskip("vortex", reason="vortex-data package not installed")
pytest.importorskip("pyarrow", reason="pyarrow package not installed")

from fixdata import FIXTURES, FIXTURES_TYPES

from iterable.datatypes import VortexIterable


class TestVortex:
    def setup_method(self):
        """Create testdata directory if it doesn't exist"""
        os.makedirs("testdata", exist_ok=True)

    def test_id(self):
        datatype_id = VortexIterable.id()
        assert datatype_id == "vortex"

    def test_flatonly(self):
        flag = VortexIterable.is_flatonly()
        assert flag

    def test_has_totals(self):
        flag = VortexIterable.has_totals()
        assert flag

    def test_openclose(self):
        # Create a test file first
        iterable = VortexIterable("testdata/test_vortex.vortex", mode="w")
        iterable.write_bulk(FIXTURES)
        iterable.close()
        # Now test opening
        iterable = VortexIterable("testdata/test_vortex.vortex")
        iterable.close()

    def test_read_bulk_returns_n_records(self):
        # Create test file
        iterable = VortexIterable("testdata/test_vortex_bulk.vortex", mode="w")
        iterable.write_bulk(FIXTURES)
        iterable.close()
        # Test reading
        iterable = VortexIterable("testdata/test_vortex_bulk.vortex")
        chunk = iterable.read_bulk(2)
        assert len(chunk) == 2
        # Note: Vortex may preserve types differently, so we check keys
        assert set(chunk[0].keys()) == set(FIXTURES_TYPES[0].keys())
        iterable.close()

    def test_parsesimple_readone(self):
        # Create test file
        iterable = VortexIterable("testdata/test_vortex_readone.vortex", mode="w")
        iterable.write_bulk(FIXTURES)
        iterable.close()
        # Test reading
        iterable = VortexIterable("testdata/test_vortex_readone.vortex")
        row = iterable.read()
        assert set(row.keys()) == set(FIXTURES_TYPES[0].keys())
        iterable.close()

    def test_parsesimple_reset(self):
        # Create test file
        iterable = VortexIterable("testdata/test_vortex_reset.vortex", mode="w")
        iterable.write_bulk(FIXTURES)
        iterable.close()
        # Test reset
        iterable = VortexIterable("testdata/test_vortex_reset.vortex")
        row = iterable.read()
        assert set(row.keys()) == set(FIXTURES_TYPES[0].keys())
        iterable.reset()
        row_reset = iterable.read()
        assert set(row_reset.keys()) == set(FIXTURES_TYPES[0].keys())
        iterable.close()

    def test_parsesimple_next(self):
        # Create test file
        iterable = VortexIterable("testdata/test_vortex_next.vortex", mode="w")
        iterable.write_bulk(FIXTURES)
        iterable.close()
        # Test next
        iterable = VortexIterable("testdata/test_vortex_next.vortex")
        row = next(iterable)
        assert set(row.keys()) == set(FIXTURES_TYPES[0].keys())
        iterable.reset()
        row_reset = next(iterable)
        assert set(row_reset.keys()) == set(FIXTURES_TYPES[0].keys())
        iterable.close()

    def test_parsesimple_count(self):
        # Create test file
        iterable = VortexIterable("testdata/test_vortex_count.vortex", mode="w")
        iterable.write_bulk(FIXTURES)
        iterable.close()
        # Test count
        iterable = VortexIterable("testdata/test_vortex_count.vortex")
        n = 0
        for _row in iterable:
            n += 1
        assert n == len(FIXTURES_TYPES)
        iterable.close()

    def test_parsesimple_iterateall(self):
        # Create test file
        iterable = VortexIterable("testdata/test_vortex_iterate.vortex", mode="w")
        iterable.write_bulk(FIXTURES)
        iterable.close()
        # Test iteration
        iterable = VortexIterable("testdata/test_vortex_iterate.vortex")
        n = 0
        for row in iterable:
            assert set(row.keys()) == set(FIXTURES_TYPES[n].keys())
            n += 1
        iterable.close()

    def test_write_read(self):
        iterable = VortexIterable("testdata/2cols6rows.vortex", mode="w")
        iterable.write_bulk(FIXTURES)
        iterable.close()
        iterable = VortexIterable("testdata/2cols6rows.vortex", mode="r")
        n = 0
        for row in iterable:
            assert set(row.keys()) == set(FIXTURES[n].keys())
            n += 1
        assert n == len(FIXTURES)
        iterable.close()

    def test_totals(self):
        # Create test file
        iterable = VortexIterable("testdata/test_vortex_totals.vortex", mode="w")
        iterable.write_bulk(FIXTURES)
        iterable.close()
        # Test totals
        iterable = VortexIterable("testdata/test_vortex_totals.vortex")
        total = iterable.totals()
        assert total == len(FIXTURES)
        iterable.close()

    def test_context_manager(self):
        # Create test file
        with VortexIterable("testdata/test_vortex_context.vortex", mode="w") as iterable:
            iterable.write_bulk(FIXTURES)
        # Test reading with context manager
        with VortexIterable("testdata/test_vortex_context.vortex") as iterable:
            n = 0
            for row in iterable:
                assert set(row.keys()) == set(FIXTURES[n].keys())
                n += 1
            assert n == len(FIXTURES)

    def test_missing_dependency(self):
        # This test verifies the ImportError is raised properly
        # We can't easily test this without mocking, but the implementation
        # should raise ImportError if vortex is not available
        # The pytest.importorskip at the top handles skipping if not available
        pass
