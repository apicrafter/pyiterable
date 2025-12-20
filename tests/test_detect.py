# -*- coding: utf-8 -*- 
import pytest
from iterable.datatypes import CSVIterable, BSONIterable, JSONLinesIterable, ParquetIterable, ORCIterable, AVROIterable, XLSXIterable, XLSIterable, XMLIterable, PickleIterable, JSONIterable, DBFIterable, DuckDBIterable
from iterable.codecs import GZIPCodec, BZIP2Codec, LZMACodec, ZSTDCodec, BrotliCodec
from iterable.helpers.utils import detect_encoding_raw, detect_delimiter
from iterable.helpers.detect import detect_file_type, detect_encoding_any

from fixdata import FIXTURES

class TestDetectors:
    def test_encoding(self):
        assert 'utf-8' == detect_encoding_raw(filename='fixtures/ru_utf8_comma.csv')['encoding'] 
        assert 'windows-1251' == detect_encoding_raw(filename='fixtures/ru_cp1251_comma.csv')['encoding'] 

    def test_encoding_any_raw(self):
        assert 'utf-8' == detect_encoding_any(filename='fixtures/ru_utf8_comma.csv')['encoding'] 
        assert 'windows-1251' == detect_encoding_any(filename='fixtures/ru_cp1251_comma.csv')['encoding'] 

    def test_encoding_any_compressed(self):
#        assert 'utf-8' == detect_encoding_any(filename='fixtures/ru_utf8_comma.csv.zst')['encoding'] 
        assert 'windows-1251' == detect_encoding_any(filename='fixtures/ru_cp1251_comma.csv.gz')['encoding'] 


    def test_delimiters(self):
        assert ',' == detect_delimiter(filename='fixtures/ru_utf8_comma.csv') 
        assert ';' == detect_delimiter(filename='fixtures/ru_utf8_semicolon.csv') 
        assert '\t' == detect_delimiter(filename='fixtures/ru_utf8_tab.csv') 
       

    def test_filetype_csv_utf8(e):
        result =  detect_file_type('fixtures/9_25.24.28.712_2014.csv')
        assert result['success'] == True
        assert result['datatype'] == CSVIterable
        assert result['codec'] == None
           
    def test_filetype_plain_csv(self):
        result =  detect_file_type('fixtures/ru_utf8_comma.csv')
        assert result['success'] == True
        assert result['datatype'] == CSVIterable
        assert result['codec'] == None

    def test_filetype_bson(self):
        result =  detect_file_type('fixtures/2cols6rows_flat.bson')
        assert result['success'] == True
        assert result['datatype'] == BSONIterable
        assert result['codec'] == None

    def test_filetype_pickle(self):
        result =  detect_file_type('fixtures/2cols6rows_flat.pickle')
        assert result['success'] == True
        assert result['datatype'] == PickleIterable
        assert result['codec'] == None

    def test_filetype_json(self):
        result =  detect_file_type('fixtures/2cols6rows_array.json')
        assert result['success'] == True
        assert result['datatype'] == JSONIterable
        assert result['codec'] == None

    def test_filetype_jsonl(self):
        result =  detect_file_type('fixtures/2cols6rows_flat.jsonl')
        assert result['success'] == True
        assert result['datatype'] == JSONLinesIterable
        assert result['codec'] == None

    def test_filetype_ndjson(self):
        result =  detect_file_type('fixtures/2cols6rows_flat.ndjson')
        assert result['success'] == True
        assert result['datatype'] == JSONLinesIterable
        assert result['codec'] == None

    def test_filetype_avro(self):
        result =  detect_file_type('fixtures/2cols6rows.avro')
        assert result['success'] == True
        assert result['datatype'] == AVROIterable
        assert result['codec'] == None        

    def test_filetype_orc(self):
        result =  detect_file_type('fixtures/2cols6rows.orc')
        assert result['success'] == True
        assert result['datatype'] == ORCIterable
        assert result['codec'] == None   

    def test_filetype_xml(self):
        result =  detect_file_type('fixtures/books.xml')
        assert result['success'] == True
        assert result['datatype'] == XMLIterable
        assert result['codec'] == None   

    def test_filetype_zstd_csv(self):
        result =  detect_file_type('fixtures/2cols6rows.csv.zst')
        assert result['success'] == True
        assert result['datatype'] == CSVIterable
        assert result['codec'] == ZSTDCodec

    def test_filetype_brotli_csv(self):
        result =  detect_file_type('fixtures/2cols6rows.csv.br')
        assert result['success'] == True
        assert result['datatype'] == CSVIterable
        assert result['codec'] == BrotliCodec

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

    def test_filetype_plain_dbf(self):
        result =  detect_file_type('fixtures/2cols6rows.dbf')
        assert result['success'] == True
        assert result['datatype'] == DBFIterable
        assert result['codec'] == None

    def test_filetype_duckdb(self):
        """Test DuckDB format detection"""
        import tempfile
        import duckdb
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.duckdb') as tmp:
            tmp_path = tmp.name
        
        try:
            # Create a minimal DuckDB database file
            conn = duckdb.connect(tmp_path)
            conn.execute("CREATE TABLE test (id INTEGER)")
            if hasattr(conn, 'commit'):
                conn.commit()
            conn.close()
            
            result = detect_file_type(tmp_path)
            assert result['success'] == True
            assert result['datatype'] == DuckDBIterable
            assert result['codec'] == None
        finally:
            import os
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_filetype_ddb(self):
        """Test DuckDB format detection with .ddb extension"""
        import tempfile
        import duckdb
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.ddb') as tmp:
            tmp_path = tmp.name
        
        try:
            # Create a minimal DuckDB database file
            conn = duckdb.connect(tmp_path)
            conn.execute("CREATE TABLE test (id INTEGER)")
            if hasattr(conn, 'commit'):
                conn.commit()
            conn.close()
            
            result = detect_file_type(tmp_path)
            assert result['success'] == True
            assert result['datatype'] == DuckDBIterable
            assert result['codec'] == None
        finally:
            import os
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

