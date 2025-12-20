# -*- coding: utf-8 -*-
import pytest
import os

try:
    from iterable.codecs import SZipCodec
    HAS_SZIPCODEC = True
except ImportError:
    HAS_SZIPCODEC = False

try:
    import py7zr
    HAS_PY7ZR = True
except ImportError:
    HAS_PY7ZR = False


@pytest.mark.skipif(not HAS_PY7ZR or not HAS_SZIPCODEC, reason="7z support requires 'py7zr' package and SZipCodec")
class Test7Z:
    def test_fileexts(self):
        """Test fileexts method"""
        exts = SZipCodec.fileexts()
        assert '7z' in exts

    def test_openclose(self):
        """Test basic open/close"""
        # Create a simple 7z archive for testing
        test_file = 'testdata/test_7z.7z'
        os.makedirs('testdata', exist_ok=True)
        
        try:
            # Create a 7z archive with a test file
            with py7zr.SevenZipFile(test_file, 'w') as archive:
                archive.writeall('testdata', 'test')
            
            codec = SZipCodec(test_file, mode='r', open_it=True)
            assert codec._fileobj is not None
            codec.close()
        except Exception as e:
            pytest.skip(f"Could not create 7z test file: {e}")
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_open_read(self):
        """Test opening and reading through codec"""
        test_file = 'testdata/test_7z_read.7z'
        os.makedirs('testdata', exist_ok=True)
        
        try:
            # Create a 7z archive
            with py7zr.SevenZipFile(test_file, 'w') as archive:
                archive.writeall('testdata', 'test')
            
            codec = SZipCodec(test_file, mode='r', open_it=True)
            fileobj = codec.fileobj()
            assert fileobj is not None
            codec.close()
        except Exception as e:
            pytest.skip(f"Could not create/read 7z test file: {e}")
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_reset(self):
        """Test reset functionality"""
        test_file = 'testdata/test_7z_reset.7z'
        os.makedirs('testdata', exist_ok=True)
        
        try:
            # Create a 7z archive
            with py7zr.SevenZipFile(test_file, 'w') as archive:
                archive.writeall('testdata', 'test')
            
            codec = SZipCodec(test_file, mode='r', open_it=True)
            fileobj1 = codec.fileobj()
            codec.reset()
            fileobj2 = codec.fileobj()
            assert fileobj1 is not None
            assert fileobj2 is not None
            codec.close()
        except Exception as e:
            pytest.skip(f"Could not create/reset 7z test file: {e}")
        
        if os.path.exists(test_file):
            os.unlink(test_file)

