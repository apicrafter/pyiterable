# -*- coding: utf-8 -*- 
import pytest
from iterable.helpers.detect import open_iterable
from fixdata import FIXTURES, FIXTURES_TYPES

class TestOpenIterable:
    def test_iterate_plain_csv(self):
        iterable = open_iterable('fixtures/2cols6rows.csv')
        n = 0
        for row in iterable:
            assert row == FIXTURES[n]
            n += 1
        iterable.close()

    def test_iterate_gzip_csv(self):
        iterable = open_iterable('fixtures/2cols6rows.csv.gz')
        n = 0
        for row in iterable:
            assert row == FIXTURES[n]
            n += 1
        iterable.close()

    def test_iterate_lzma_csv(self):
        iterable = open_iterable('fixtures/2cols6rows.csv.xz')
        n = 0
        for row in iterable:
            assert row == FIXTURES[n]
            n += 1
        iterable.close()

    def test_iterate_bzip2_csv(self):
        iterable = open_iterable('fixtures/2cols6rows.csv.bz2')
        n = 0
        for row in iterable:
            assert row == FIXTURES[n]
            n += 1
        iterable.close()

    def test_iterate_lz4_csv(self):
        iterable = open_iterable('fixtures/2cols6rows.csv.lz4')
        n = 0
        for row in iterable:
            assert row == FIXTURES[n]
            n += 1
        iterable.close()

    def test_iterate_plain_xls(self):
        iterable = open_iterable('fixtures/2cols6rows.xls')
        n = 0
        for row in iterable:
            assert row == FIXTURES_TYPES[n]
            n += 1
        iterable.close()

    def test_iterate_plain_xlsx(self):
        iterable = open_iterable('fixtures/2cols6rows.xlsx')
        n = 0
        for row in iterable:
            assert row == FIXTURES[n]
            n += 1
        iterable.close()

    def test_iterate_plain_parquet(self):
        iterable = open_iterable('fixtures/2cols6rows.parquet')
        n = 0
        for row in iterable:
            assert row == FIXTURES_TYPES[n]
            n += 1
        iterable.close()

    def test_iterate_plain_orc(self):
        iterable = open_iterable('fixtures/2cols6rows.orc')
        n = 0
        for row in iterable:
            assert row == FIXTURES[n]
            n += 1
        iterable.close()

    def test_iterate_plain_avro(self):
        iterable = open_iterable('fixtures/2cols6rows.avro')
        n = 0
        for row in iterable:
            assert row == FIXTURES[n]
            n += 1
        iterable.close()

    def test_iterate_plain_bson(self):
        iterable = open_iterable('fixtures/2cols6rows_flat.bson')
        n = 0
        for row in iterable:
            assert row == FIXTURES[n]
            n += 1
        iterable.close()

    def test_iterate_plain_json(self):
        iterable = open_iterable('fixtures/2cols6rows_array.json')
        n = 0
        for row in iterable:
            assert row == FIXTURES[n]
            n += 1
        iterable.close()

    def test_iterate_plain_jsonl(self):
        iterable = open_iterable('fixtures/2cols6rows_flat.jsonl')
        n = 0
        for row in iterable:
            assert row == FIXTURES[n]
            n += 1
        iterable.close()

    def test_iterate_plain_xml(self):
        iterable = open_iterable('fixtures/books.xml', iterableargs={'tagname' : 'book'})
        n = 0
        years = [2005, 2005, 2003]
        for row in iterable:
            assert int(row['year']) == years[n]
            n += 1
        iterable.close()
