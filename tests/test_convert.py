# -*- coding: utf-8 -*- 
import pytest
import os
from iterable.convert import convert
from fixdata import FIXTURES

class TestConvert:
    def test_convert_csv_to_jsonl(self):
        convert(fromfile='fixtures/ru_cp1251_comma.csv', tofile='testdata/ru_cp1251_comma_converted.jsonl')
        assert os.path.exists('testdata/ru_cp1251_comma_converted.jsonl')

    def test_convert_csv_to_parquet(self):
        convert(fromfile='fixtures/ru_cp1251_comma.csv', tofile='testdata/ru_cp1251_comma_converted.parquet')
        assert os.path.exists('testdata/ru_cp1251_comma_converted.parquet')

    def test_convert_csv_to_csv_gz(self):
        convert(fromfile='fixtures/ru_cp1251_comma.csv', tofile='testdata/ru_cp1251_comma_converted.csv.gz')
        assert os.path.exists('testdata/ru_cp1251_comma_converted.csv.gz')


    def test_convert_jsonl_to_csv_xz(self):
        convert(fromfile='fixtures/2cols6rows_flat.jsonl', tofile='testdata/2cols6rows_flat_converted.csv.gz')
        assert os.path.exists('testdata/2cols6rows_flat_converted.csv.gz')
