import pytest

from iterable.codecs import BZIP2Codec, GZIPCodec, LZMACodec

# Optional codecs - may not be available
try:
    from iterable.codecs import BrotliCodec
except (ImportError, NameError):
    BrotliCodec = None

try:
    from iterable.codecs import ZSTDCodec
except (ImportError, NameError):
    ZSTDCodec = None
from iterable.datatypes import (
    CSVIterable,
    JSONIterable,
    JSONLinesIterable,
    PickleIterable,
)

# Optional datatypes - may not be available
try:
    from iterable.datatypes import AVROIterable
except (ImportError, NameError):
    AVROIterable = None

try:
    from iterable.datatypes import BSONIterable
except (ImportError, NameError):
    BSONIterable = None

try:
    from iterable.datatypes import DBFIterable
except (ImportError, NameError):
    DBFIterable = None

try:
    from iterable.datatypes import DuckDBIterable
except (ImportError, NameError):
    DuckDBIterable = None

try:
    from iterable.datatypes import ORCIterable
except (ImportError, NameError):
    ORCIterable = None

try:
    from iterable.datatypes import ParquetIterable
except (ImportError, NameError):
    ParquetIterable = None

try:
    from iterable.datatypes import XLSIterable
except (ImportError, NameError):
    XLSIterable = None

try:
    from iterable.datatypes import XLSXIterable
except (ImportError, NameError):
    XLSXIterable = None

try:
    from iterable.datatypes import XMLIterable
except (ImportError, NameError):
    XMLIterable = None
from iterable.helpers.detect import detect_encoding_any, detect_file_type
from iterable.helpers.utils import detect_delimiter, detect_encoding_raw


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
        assert result['success']
        assert result['datatype'] == CSVIterable
        assert result['codec'] is None
           
    def test_filetype_plain_csv(self):
        result =  detect_file_type('fixtures/ru_utf8_comma.csv')
        assert result['success']
        assert result['datatype'] == CSVIterable
        assert result['codec'] is None

    def test_filetype_bson(self):
        result =  detect_file_type('fixtures/2cols6rows_flat.bson')
        assert result['success']
        assert result['datatype'] == BSONIterable
        assert result['codec'] is None

    def test_filetype_pickle(self):
        result =  detect_file_type('fixtures/2cols6rows_flat.pickle')
        assert result['success']
        assert result['datatype'] == PickleIterable
        assert result['codec'] is None

    def test_filetype_json(self):
        result =  detect_file_type('fixtures/2cols6rows_array.json')
        assert result['success']
        assert result['datatype'] == JSONIterable
        assert result['codec'] is None

    def test_filetype_jsonl(self):
        result =  detect_file_type('fixtures/2cols6rows_flat.jsonl')
        assert result['success']
        assert result['datatype'] == JSONLinesIterable
        assert result['codec'] is None

    def test_filetype_ndjson(self):
        result =  detect_file_type('fixtures/2cols6rows_flat.ndjson')
        assert result['success']
        assert result['datatype'] == JSONLinesIterable
        assert result['codec'] is None

    def test_filetype_avro(self):
        result =  detect_file_type('fixtures/2cols6rows.avro')
        assert result['success']
        assert result['datatype'] == AVROIterable
        assert result['codec'] is None        

    def test_filetype_orc(self):
        result =  detect_file_type('fixtures/2cols6rows.orc')
        assert result['success']
        assert result['datatype'] == ORCIterable
        assert result['codec'] is None   

    def test_filetype_xml(self):
        result =  detect_file_type('fixtures/books.xml')
        assert result['success']
        assert result['datatype'] == XMLIterable
        assert result['codec'] is None   

    def test_filetype_zstd_csv(self):
        if ZSTDCodec is None:
            pytest.skip("ZSTDCodec not available")
        result =  detect_file_type('fixtures/2cols6rows.csv.zst')
        assert result['success']
        assert result['datatype'] == CSVIterable
        assert result['codec'] == ZSTDCodec

    def test_filetype_brotli_csv(self):
        if BrotliCodec is None:
            pytest.skip("BrotliCodec not available")
        result =  detect_file_type('fixtures/2cols6rows.csv.br')
        assert result['success']
        assert result['datatype'] == CSVIterable
        assert result['codec'] == BrotliCodec

    def test_filetype_bzip2_csv(self):
        result =  detect_file_type('fixtures/2cols6rows.csv.bz2')
        assert result['success']
        assert result['datatype'] == CSVIterable
        assert result['codec'] == BZIP2Codec

    def test_filetype_lzma_csv(self):
        result =  detect_file_type('fixtures/2cols6rows.csv.xz')
        assert result['success']
        assert result['datatype'] == CSVIterable
        assert result['codec'] == LZMACodec

    def test_filetype_gzip_csv(self):
        result =  detect_file_type('fixtures/2cols6rows.csv.gz')
        assert result['success']
        assert result['datatype'] == CSVIterable
        assert result['codec'] == GZIPCodec


    def test_filetype_plain_parquet(self):
        result =  detect_file_type('fixtures/2cols6rows.parquet')
        assert result['success']
        assert result['datatype'] == ParquetIterable
        assert result['codec'] is None

    def test_filetype_plain_xls(self):
        result =  detect_file_type('fixtures/2cols6rows.xls')
        assert result['success']
        assert result['datatype'] == XLSIterable
        assert result['codec'] is None

    def test_filetype_plain_xlsx(self):
        result =  detect_file_type('fixtures/2cols6rows.xlsx')
        assert result['success']
        assert result['datatype'] == XLSXIterable
        assert result['codec'] is None

    def test_filetype_plain_dbf(self):
        result =  detect_file_type('fixtures/2cols6rows.dbf')
        assert result['success']
        assert result['datatype'] == DBFIterable
        assert result['codec'] is None

    def test_filetype_duckdb(self):
        """Test DuckDB format detection"""
        import tempfile

        import duckdb
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.duckdb') as tmp:
            tmp_path = tmp.name
        # DuckDB may error if the file already exists but is empty/not a valid DB.
        # Ensure the path does not exist before connecting so DuckDB can create it.
        import os
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        
        try:
            # Create a minimal DuckDB database file
            conn = duckdb.connect(tmp_path)
            conn.execute("CREATE TABLE test (id INTEGER)")
            if hasattr(conn, 'commit'):
                conn.commit()
            conn.close()
            
            result = detect_file_type(tmp_path)
            assert result['success']
            assert result['datatype'] == DuckDBIterable
            assert result['codec'] is None
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
        # DuckDB may error if the file already exists but is empty/not a valid DB.
        # Ensure the path does not exist before connecting so DuckDB can create it.
        import os
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        
        try:
            # Create a minimal DuckDB database file
            conn = duckdb.connect(tmp_path)
            conn.execute("CREATE TABLE test (id INTEGER)")
            if hasattr(conn, 'commit'):
                conn.commit()
            conn.close()
            
            result = detect_file_type(tmp_path)
            assert result['success']
            assert result['datatype'] == DuckDBIterable
            assert result['codec'] is None
        finally:
            import os
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_detect_file_type_empty_filename(self):
        """Test detect_file_type with empty filename raises ValueError"""
        with pytest.raises(ValueError, match="Filename cannot be empty"):
            detect_file_type("")

    def test_detect_file_type_unknown_format(self):
        """Test detect_file_type with unknown format"""
        result = detect_file_type("test.unknown")
        assert result["success"] is False
        assert result["datatype"] is None
        assert result["codec"] is None

    def test_detect_file_type_no_extension(self):
        """Test detect_file_type with no extension"""
        result = detect_file_type("test")
        assert result["success"] is False

    def test_detect_compression_empty_filename(self):
        """Test detect_compression with empty filename raises ValueError"""
        from iterable.helpers.detect import detect_compression
        with pytest.raises(ValueError, match="Filename cannot be empty"):
            detect_compression("")

    def test_detect_compression_gzip(self):
        """Test detect_compression with gzip file"""
        from iterable.helpers.detect import detect_compression
        result = detect_compression("test.csv.gz")
        assert result["success"] is True
        assert result["compression"] == GZIPCodec
        assert result["codec"] is None
        assert result["datatype"] is None

    def test_detect_compression_bz2(self):
        """Test detect_compression with bz2 file"""
        from iterable.helpers.detect import detect_compression
        result = detect_compression("test.bz2")
        assert result["success"] is True
        assert result["compression"] == BZIP2Codec

    def test_detect_compression_no_compression(self):
        """Test detect_compression with no compression"""
        from iterable.helpers.detect import detect_compression
        result = detect_compression("test.csv")
        assert result["success"] is False
        assert result["compression"] is None

    def test_detect_encoding_any_empty_filename(self):
        """Test detect_encoding_any with empty filename raises ValueError"""
        with pytest.raises(ValueError, match="Filename cannot be empty"):
            detect_encoding_any("")

    def test_detect_encoding_any_file_not_found(self):
        """Test detect_encoding_any with non-existent file raises FileNotFoundError"""
        import os
        non_existent = "this_file_does_not_exist_12345.txt"
        assert not os.path.exists(non_existent)
        with pytest.raises(FileNotFoundError):
            detect_encoding_any(non_existent)

    def test_detect_encoding_any_empty_file(self, tmp_path):
        """Test detect_encoding_any with empty file raises ValueError"""
        empty_file = tmp_path / "empty.txt"
        empty_file.write_text("")
        with pytest.raises(ValueError, match="appears to be empty"):
            detect_encoding_any(str(empty_file))

    def test_open_iterable_empty_filename(self):
        """Test open_iterable with empty filename raises ValueError"""
        from iterable.helpers.detect import open_iterable
        with pytest.raises(ValueError, match="Filename cannot be empty"):
            open_iterable("")

    def test_open_iterable_invalid_engine(self):
        """Test open_iterable with invalid engine raises ValueError"""
        from iterable.helpers.detect import open_iterable
        with pytest.raises(ValueError, match="Engine must be 'internal' or 'duckdb'"):
            open_iterable("test.csv", engine="invalid")

    def test_open_iterable_file_not_found(self):
        """Test open_iterable with non-existent file raises FileNotFoundError"""
        from iterable.helpers.detect import open_iterable
        import os
        non_existent = "this_file_does_not_exist_12345.csv"
        assert not os.path.exists(non_existent)
        with pytest.raises(FileNotFoundError):
            open_iterable(non_existent)

    def test_open_iterable_unknown_format(self, tmp_path):
        """Test open_iterable with unknown format raises RuntimeError"""
        from iterable.helpers.detect import open_iterable
        unknown_file = tmp_path / "test.unknown"
        unknown_file.write_text("test data")
        
        with pytest.raises(RuntimeError, match="Could not detect file type"):
            open_iterable(str(unknown_file))

    def test_open_iterable_duckdb_unsupported_format(self, tmp_path):
        """Test open_iterable with DuckDB engine and unsupported format"""
        from iterable.helpers.detect import open_iterable
        xml_file = tmp_path / "test.xml"
        xml_file.write_text("<root><item>test</item></root>")
        
        with pytest.raises(ValueError, match="DuckDB engine does not support file type"):
            open_iterable(str(xml_file), engine="duckdb")

    def test_is_flat_function(self):
        """Test is_flat function"""
        from iterable.helpers.detect import is_flat
        # Test with filename
        assert is_flat(filename="test.csv") is True
        assert is_flat(filename="test.json") is False
        # Test with filetype
        assert is_flat(filetype="csv") is True
        assert is_flat(filetype="json") is False
        # Test with None
        assert is_flat() is False

    def test_is_flat_with_compressed(self):
        """Test is_flat with compressed file"""
        from iterable.helpers.detect import is_flat
        assert is_flat(filename="test.csv.gz") is True
        assert is_flat(filename="test.json.gz") is False
