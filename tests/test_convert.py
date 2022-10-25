# -*- coding: utf-8 -*- 
import pytest
from iterable.datatypes import CSVIterable, BSONIterable, JSONLinesIterable, ParquetIterable

from fixdata import FIXTURES

class TestConvert:
    def test_csv_to_bson(self):
        iterable = CSVIterable('fixtures/2cols6rows.csv')        
        bson_iterable = BSONIterable('testdata/2cols6rows.bson', mode='w')        
        n = 0
        for row in iterable:
            assert row == FIXTURES[n]
            n += 1
            bson_iterable.write(row)
        iterable.close()
        bson_iterable.close()
       
    def test_jsonl_to_bson(self):
        iterable = JSONLinesIterable('fixtures/2cols6rows_flat.jsonl')        
        bson_iterable = BSONIterable('testdata/2cols6rows_jsonl.bson', mode='w')        
        n = 0
        for row in iterable:
            assert row == FIXTURES[n]
            n += 1
            bson_iterable.write(row)
        iterable.close()
        bson_iterable.close()
       
    def test_parquet_to_jsonl(self):
        iterable = ParquetIterable('fixtures/2cols6rows.parquet')        
        write_iterable = JSONLinesIterable('testdata/2cols6rows_parquet.jsonl', mode='w')        
        n = 0
        for row in iterable:
            n += 1
            write_iterable.write(row)
        iterable.close()
        write_iterable.close()


