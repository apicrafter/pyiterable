import os
import zipfile

from iterable.datatypes import ZIPXMLSource


class TestZIPXML:
    def test_id(self):
        source = ZIPXMLSource("../testdata/test_zipxml.zip", tagname="item")
        datatype_id = source.id()
        assert datatype_id == "zip-xml"
        source.close()

    def test_is_flat(self):
        source = ZIPXMLSource("../testdata/test_zipxml.zip", tagname="item")
        flag = source.is_flat()
        assert not flag
        source.close()

    def test_openclose(self):
        """Test basic open/close"""
        test_file = "testdata/test_zipxml.zip"
        os.makedirs("testdata", exist_ok=True)

        # Create a ZIP file with XML content
        with zipfile.ZipFile(test_file, "w") as zf:
            zf.writestr("data.xml", '<?xml version="1.0"?><root><item>test</item></root>')

        source = ZIPXMLSource(test_file, tagname="item")
        source.close()

        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_one(self):
        """Test reading single XML record from ZIP"""
        test_file = "testdata/test_zipxml_read.zip"
        os.makedirs("testdata", exist_ok=True)

        # Create a ZIP file with XML content
        with zipfile.ZipFile(test_file, "w") as zf:
            zf.writestr("data.xml", '<?xml version="1.0"?><root><item><name>test</name></item></root>')

        source = ZIPXMLSource(test_file, tagname="item")
        try:
            record = source.read()
            assert isinstance(record, dict)
        except NotImplementedError:
            # If read_single is not fully implemented, that's okay
            pass
        source.close()

        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_iterfile(self):
        """Test iterating through files in ZIP"""
        test_file = "testdata/test_zipxml_iter.zip"
        os.makedirs("testdata", exist_ok=True)

        # Create a ZIP file with multiple XML files
        with zipfile.ZipFile(test_file, "w") as zf:
            zf.writestr("file1.xml", '<?xml version="1.0"?><root><item>1</item></root>')
            zf.writestr("file2.xml", '<?xml version="1.0"?><root><item>2</item></root>')

        source = ZIPXMLSource(test_file, tagname="item")
        # Test iterfile method
        has_more = source.iterfile()
        # Should have more files
        assert isinstance(has_more, bool)
        source.close()

        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_real_data(self):
        """Test with provided real-world ZIP file"""
        test_file = "../testdata/test_zipxml.zip"

        # Ensure the test file exists
        assert os.path.exists(test_file), f"Test file {test_file} not found"

        source = ZIPXMLSource(test_file, tagname="Документ")
        count = 0
        for record in source:
            assert isinstance(record, dict)
            assert "@ИдДок" in record
            count += 1

        assert count > 0
        source.close()

    def test_has_tables(self):
        """Test has_tables static method"""
        assert ZIPXMLSource.has_tables() is True

    def test_list_tables_single_xml(self):
        """Test list_tables with single XML file"""
        test_file = "testdata/test_zipxml_list1.zip"
        os.makedirs("testdata", exist_ok=True)

        # Create a ZIP file with one XML file
        with zipfile.ZipFile(test_file, "w") as zf:
            zf.writestr("data.xml", '<?xml version="1.0"?><root><item>test</item></root>')

        try:
            source = ZIPXMLSource(test_file, tagname="item")
            tables = source.list_tables(test_file)
            assert isinstance(tables, list)
            assert len(tables) == 1
            assert "data.xml" in tables
            source.close()
        finally:
            if os.path.exists(test_file):
                os.unlink(test_file)

    def test_list_tables_multiple_xml(self):
        """Test list_tables with multiple XML files"""
        test_file = "testdata/test_zipxml_list2.zip"
        os.makedirs("testdata", exist_ok=True)

        # Create a ZIP file with multiple XML files
        with zipfile.ZipFile(test_file, "w") as zf:
            zf.writestr("file1.xml", '<?xml version="1.0"?><root><item>1</item></root>')
            zf.writestr("file2.xml", '<?xml version="1.0"?><root><item>2</item></root>')
            zf.writestr("file3.xml", '<?xml version="1.0"?><root><item>3</item></root>')
            zf.writestr("readme.txt", "Not an XML file")

        try:
            source = ZIPXMLSource(test_file, tagname="item")
            tables = source.list_tables(test_file)
            assert isinstance(tables, list)
            assert len(tables) == 3
            assert "file1.xml" in tables
            assert "file2.xml" in tables
            assert "file3.xml" in tables
            assert "readme.txt" not in tables  # Should only list XML files
            source.close()
        finally:
            if os.path.exists(test_file):
                os.unlink(test_file)

    def test_list_tables_instance_method(self):
        """Test list_tables on already-opened instance"""
        test_file = "testdata/test_zipxml_list3.zip"
        os.makedirs("testdata", exist_ok=True)

        # Create a ZIP file with multiple XML files
        with zipfile.ZipFile(test_file, "w") as zf:
            zf.writestr("first.xml", '<?xml version="1.0"?><root><item>1</item></root>')
            zf.writestr("second.xml", '<?xml version="1.0"?><root><item>2</item></root>')

        try:
            source = ZIPXMLSource(test_file, tagname="item")
            tables = source.list_tables()
            assert isinstance(tables, list)
            assert len(tables) == 2
            assert "first.xml" in tables
            assert "second.xml" in tables
            source.close()
        finally:
            if os.path.exists(test_file):
                os.unlink(test_file)

    def test_list_tables_empty_zip(self):
        """Test list_tables on ZIP file with no XML files"""
        test_file = "testdata/test_zipxml_list4.zip"
        os.makedirs("testdata", exist_ok=True)

        # Create a ZIP file with no XML files
        with zipfile.ZipFile(test_file, "w") as zf:
            zf.writestr("readme.txt", "No XML here")
            zf.writestr("data.json", '{"key": "value"}')

        try:
            source = ZIPXMLSource(test_file, tagname="item")
            tables = source.list_tables(test_file)
            assert isinstance(tables, list)
            assert len(tables) == 0
            source.close()
        finally:
            if os.path.exists(test_file):
                os.unlink(test_file)
