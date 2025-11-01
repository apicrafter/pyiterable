# -*- coding: utf-8 -*- 
import pytest
from iterable.engines import DuckDBIterable
from fixdata import FIXTURES_TYPES, FIXTURES

class TestParquet:
    def test_id(self):
        datatype_id = DuckDBIterable.id()
        assert datatype_id == 'duckdb'


                
    def test_parsesimple_readone(self):
        iterable = DuckDBIterable('fixtures/2cols6rows.parquet')        
        row = iterable.read()
        assert row == FIXTURES_TYPES[0]
        iterable.close()
           
    def test_totals(self):
        iterable = DuckDBIterable('fixtures/2cols6rows.parquet')        
        totals = iterable.totals()
        assert totals == 6

           
    def test_parsesimple_next(self):
        iterable = DuckDBIterable('fixtures/2cols6rows.parquet')        
        row = next(iterable)
        assert row == FIXTURES_TYPES[0]
        iterable.reset() 
        row_reset = next(iterable)
        assert row_reset == FIXTURES_TYPES[0]
        iterable.close()

    def test_parsesimple_count(self):
        iterable = DuckDBIterable('fixtures/2cols6rows.parquet')        
        n = 0
        for row in iterable:
            n += 1
        assert n == len(FIXTURES_TYPES)
        iterable.close()

    def test_parsesimple_iterateall(self):
        iterable = DuckDBIterable('fixtures/2cols6rows.parquet')        
        n = 0
        for row in iterable:
            assert row == FIXTURES_TYPES[n]
            n += 1
        iterable.close()

    def test_is_flatonly_false(self):
        assert DuckDBIterable.is_flatonly() is False

    def test_open_close_noop(self):
        iterable = DuckDBIterable('fixtures/2cols6rows.parquet')
        totals_before = iterable.totals()
        iterable.open()
        iterable.close()
        # Should not affect ability to query totals
        iterable2 = DuckDBIterable('fixtures/2cols6rows.parquet')
        totals_after = iterable2.totals()
        assert totals_before == totals_after == 6

    def test_read_bulk_returns_n_records(self):
        iterable = DuckDBIterable('fixtures/2cols6rows.parquet')
        chunk = iterable.read_bulk(3)
        assert len(chunk) == 3
        assert chunk == FIXTURES_TYPES[:3]
        iterable.close()

    def test_read_bulk_does_not_advance_pos(self):
        iterable = DuckDBIterable('fixtures/2cols6rows.parquet')
        first_chunk = iterable.read_bulk(2)
        second_chunk = iterable.read_bulk(2)
        assert first_chunk == FIXTURES_TYPES[:2]
        assert second_chunk == FIXTURES_TYPES[:2]  # position not advanced by read_bulk
        # Now a single read should still return the first row
        row = iterable.read()
        assert row == FIXTURES_TYPES[0]
        iterable.close()

    def test_stop_iteration_after_exhaustion(self):
        iterable = DuckDBIterable('fixtures/2cols6rows.parquet')
        # Consume all rows
        for _ in range(6):
            _ = iterable.read()
        with pytest.raises(StopIteration):
            _ = iterable.read()
        iterable.close()