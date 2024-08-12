# -*- coding: utf-8 -*- 
import pytest
from iterable.datatypes import CSVIterable, BSONIterable, JSONLinesIterable, ParquetIterable, ORCIterable, AVROIterable, XLSXIterable, XLSIterable, XMLIterable
from iterable.codecs import GZIPCodec, BZIP2Codec

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

    def test_jsonl_to_csv(self):
        iterable = JSONLinesIterable('fixtures/2cols6rows_flat.jsonl')        
        csv_iterable = CSVIterable('testdata/2cols6rows_csv.csv', mode='w', keys=['id', 'name'])        
        n = 0
        for row in iterable:
            assert row == FIXTURES[n]
            n += 1
            csv_iterable.write(row)
        iterable.close()
        csv_iterable.close()

       
    def test_parquet_to_jsonl(self):
        iterable = ParquetIterable('fixtures/2cols6rows.parquet')        
        write_iterable = JSONLinesIterable('testdata/2cols6rows_parquet.jsonl', mode='w')        
        n = 0
        for row in iterable:
            n += 1
            write_iterable.write(row)
        iterable.close()
        write_iterable.close()


    def test_orc_to_bson(self):
        iterable = ORCIterable('fixtures/2cols6rows.orc')        
        write_iterable = BSONIterable('testdata/2cols6rows_orc.bson', mode='w')        
        n = 0
        for row in iterable:
            n += 1
            write_iterable.write(row)
        iterable.close()
        write_iterable.close()


    def test_orc_to_csv(self):
        iterable = ORCIterable('fixtures/2cols6rows.orc')        
        write_iterable = CSVIterable('testdata/2cols6rows_orc.csv', mode='w', keys=['id', 'name'])        
        n = 0
        for row in iterable:
            n += 1
            write_iterable.write(row)
        iterable.close()
        write_iterable.close()


    def test_csv_to_orc(self):
        iterable = CSVIterable('fixtures/2cols6rows.csv')        
        write_iterable = ORCIterable('testdata/2cols6rows_csv.orc', mode='w', keys=['id', 'name'])        
        n = 0
        for row in iterable:
            n += 1
            write_iterable.write(row)
        iterable.close()
        write_iterable.close()

    def test_jsonl_to_orc(self):
        iterable = JSONLinesIterable('fixtures/2cols6rows_flat.jsonl')        
        write_iterable = ORCIterable('testdata/2cols6rows_jsonl.orc', mode='w', keys=['id', 'name'])        
        n = 0
        for row in iterable:
            n += 1
            write_iterable.write(row)
        iterable.close()
        write_iterable.close()


    def test_avro_to_jsonl(self):
        iterable = AVROIterable('fixtures/2cols6rows.avro')        
        write_iterable = JSONLinesIterable('testdata/2cols6rows_avro.jsonl', mode='w')
        n = 0
        for row in iterable:
            n += 1
            write_iterable.write(row)
        iterable.close()
        write_iterable.close()

    def test_avro_to_jsonl_gzip(self):
        iterable = AVROIterable('fixtures/2cols6rows.avro')        
        write_iterable = JSONLinesIterable(codec=GZIPCodec('testdata/2cols6rows_avro.jsonl.gz', mode='w', open_it=True), mode='w')
        n = 0
        for row in iterable:
            n += 1
            write_iterable.write(row)
        iterable.close()
        write_iterable.close()


    def test_xlsx_to_jsonl(self):
        iterable = XLSXIterable('fixtures/2cols6rows.xlsx')        
        write_iterable = JSONLinesIterable('testdata/2cols6rows_xlsx.jsonl', mode='w')
        n = 0
        for row in iterable:
            n += 1
            write_iterable.write(row)
        iterable.close()
        write_iterable.close()

    def test_xlsx_to_jsonl_bzip2(self):
        iterable = XLSXIterable('fixtures/2cols6rows.xlsx')        
        write_iterable = JSONLinesIterable(codec=BZIP2Codec('testdata/2cols6rows_xlsx.jsonl.bz2', mode='w', open_it=True), mode='w')
        n = 0
        for row in iterable:
            n += 1
            write_iterable.write(row)
        iterable.close()
        write_iterable.close()


    def test_xls_to_jsonl(self):
        iterable = XLSIterable('fixtures/2cols6rows.xls')        
        write_iterable = JSONLinesIterable('testdata/2cols6rows_xls.jsonl', mode='w')
        n = 0
        for row in iterable:
            n += 1
            write_iterable.write(row)
        iterable.close()
        write_iterable.close()
