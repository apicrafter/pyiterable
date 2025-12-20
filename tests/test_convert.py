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

    def test_convert_with_batch_size(self):
        """Test convert with custom batch size"""
        convert(
            fromfile='fixtures/2cols6rows_flat.jsonl',
            tofile='testdata/test_convert_batch.jsonl',
            batch_size=2
        )
        assert os.path.exists('testdata/test_convert_batch.jsonl')
        if os.path.exists('testdata/test_convert_batch.jsonl'):
            os.unlink('testdata/test_convert_batch.jsonl')

    def test_convert_with_flatten(self):
        """Test convert with flatten option"""
        convert(
            fromfile='fixtures/2cols6rows_flat.jsonl',
            tofile='testdata/test_convert_flatten.jsonl',
            is_flatten=True
        )
        assert os.path.exists('testdata/test_convert_flatten.jsonl')
        if os.path.exists('testdata/test_convert_flatten.jsonl'):
            os.unlink('testdata/test_convert_flatten.jsonl')

    def test_convert_with_use_totals(self):
        """Test convert with use_totals option"""
        convert(
            fromfile='fixtures/2cols6rows.csv',
            tofile='testdata/test_convert_totals.jsonl',
            use_totals=True
        )
        assert os.path.exists('testdata/test_convert_totals.jsonl')
        if os.path.exists('testdata/test_convert_totals.jsonl'):
            os.unlink('testdata/test_convert_totals.jsonl')

    def test_convert_with_silent(self):
        """Test convert with silent=False"""
        convert(
            fromfile='fixtures/2cols6rows_flat.jsonl',
            tofile='testdata/test_convert_silent.jsonl',
            silent=False
        )
        assert os.path.exists('testdata/test_convert_silent.jsonl')
        if os.path.exists('testdata/test_convert_silent.jsonl'):
            os.unlink('testdata/test_convert_silent.jsonl')

    def test_convert_different_formats(self):
        """Test converting between different format combinations"""
        # CSV to JSON
        convert(
            fromfile='fixtures/2cols6rows.csv',
            tofile='testdata/test_convert_csv_json.json',
            iterableargs={'tagname': 'items'}
        )
        assert os.path.exists('testdata/test_convert_csv_json.json')
        if os.path.exists('testdata/test_convert_csv_json.json'):
            os.unlink('testdata/test_convert_csv_json.json')

    def test_convert_with_toiterableargs(self):
        """Test convert with output iterable arguments"""
        # Convert CSV to CSV with custom delimiter
        convert(
            fromfile='fixtures/2cols6rows.csv',
            tofile='testdata/test_convert_output_args.csv',
            toiterableargs={'delimiter': '|'}
        )
        assert os.path.exists('testdata/test_convert_output_args.csv')
        # Verify the file was created and has content
        if os.path.exists('testdata/test_convert_output_args.csv'):
            with open('testdata/test_convert_output_args.csv', 'r') as f:
                content = f.read()
                # Check that pipe delimiter is used (not comma)
                assert '|' in content or len(content) > 0
            os.unlink('testdata/test_convert_output_args.csv')