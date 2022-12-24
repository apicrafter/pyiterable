# -*- coding: utf-8 -*- 
import pytest
from iterable.datatypes import CSVIterable, BSONIterable, JSONLinesIterable, ParquetIterable, ORCIterable, AVROIterable, XLSXIterable, XLSIterable, XMLIterable
from iterable.codecs import GZIPCodec, BZIP2Codec, LZMACodec
from iterable.helpers.utils import detect_encoding, detect_delimiter
from iterable.helpers.detect import detect_file_type

from fixdata import FIXTURES

class TestDetectors:
    def test_encoding(self):
        assert 'utf-8' == detect_encoding(filename='fixtures/ru_utf8_comma.csv')['encoding'] 
        assert 'windows-1251' == detect_encoding(filename='fixtures/ru_cp1251_comma.csv')['encoding'] 


    def test_delimiters(self):
        assert ',' == detect_delimiter(filename='fixtures/ru_utf8_comma.csv') 
        assert ';' == detect_delimiter(filename='fixtures/ru_utf8_semicolon.csv') 
        assert '\t' == detect_delimiter(filename='fixtures/ru_utf8_tab.csv') 
       
    def test_filetype_plain_csv(self):
        result =  detect_file_type('fixtures/ru_utf8_comma.csv')
        assert result['success'] == True
        assert result['datatype'] == CSVIterable
        assert result['codec'] == None

    def test_filetype_bzip2_csv(self):
        result =  detect_file_type('fixtures/2cols6rows.csv.bz2')
        assert result['success'] == True
        assert result['datatype'] == CSVIterable
        assert result['codec'] == BZIP2Codec

    def test_filetype_lzma_csv(self):
        result =  detect_file_type('fixtures/2cols6rows.csv.xz')
        assert result['success'] == True
        assert result['datatype'] == CSVIterable
        assert result['codec'] == LZMACodec

    def test_filetype_gzip_csv(self):
        result =  detect_file_type('fixtures/2cols6rows.csv.gz')
        assert result['success'] == True
        assert result['datatype'] == CSVIterable
        assert result['codec'] == GZIPCodec


    def test_filetype_plain_parquet(self):
        result =  detect_file_type('fixtures/2cols6rows.parquet')
        assert result['success'] == True
        assert result['datatype'] == ParquetIterable
        assert result['codec'] == None

    def test_filetype_plain_xls(self):
        result =  detect_file_type('fixtures/2cols6rows.xls')
        assert result['success'] == True
        assert result['datatype'] == XLSIterable
        assert result['codec'] == None

    def test_filetype_plain_xlsx(self):
        result =  detect_file_type('fixtures/2cols6rows.xlsx')
        assert result['success'] == True
        assert result['datatype'] == XLSXIterable
        assert result['codec'] == None

