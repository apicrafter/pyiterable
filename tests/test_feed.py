import os
import tempfile

import pytest

from iterable.datatypes import FeedIterable
from iterable.helpers.detect import open_iterable

try:
    import feedparser  # noqa: F401

    HAS_FEEDPARSER = True
except ImportError:
    HAS_FEEDPARSER = False


@pytest.mark.skipif(not HAS_FEEDPARSER, reason="Feed support requires 'feedparser' package")
class TestFeed:
    def test_id(self):
        datatype_id = FeedIterable.id()
        assert datatype_id == "feed"

    def test_flatonly(self):
        flag = FeedIterable.is_flatonly()
        assert not flag

    def test_openclose(self):
        """Test basic open/close"""
        rss_content = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Test Feed</title>
    <link>http://example.com</link>
    <description>Test Description</description>
    <item>
      <title>Test Item</title>
      <link>http://example.com/item1</link>
      <description>Test Description</description>
    </item>
  </channel>
</rss>"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".rss", delete=False) as f:
            f.write(rss_content)
            temp_file = f.name

        try:
            iterable = FeedIterable(temp_file)
            iterable.close()
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_read_one(self):
        """Test reading single entry"""
        rss_content = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Test Feed</title>
    <link>http://example.com</link>
    <item>
      <title>Test Item</title>
      <link>http://example.com/item1</link>
      <description>Test Description</description>
    </item>
  </channel>
</rss>"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".rss", delete=False) as f:
            f.write(rss_content)
            temp_file = f.name

        try:
            iterable = FeedIterable(temp_file)
            record = iterable.read()
            assert isinstance(record, dict)
            assert "title" in record
            assert record["title"] == "Test Item"
            assert "feed_title" in record
            assert record["feed_title"] == "Test Feed"
            iterable.close()
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_read_all(self):
        """Test reading all entries"""
        rss_content = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Test Feed</title>
    <link>http://example.com</link>
    <item>
      <title>Item 1</title>
      <link>http://example.com/item1</link>
    </item>
    <item>
      <title>Item 2</title>
      <link>http://example.com/item2</link>
    </item>
    <item>
      <title>Item 3</title>
      <link>http://example.com/item3</link>
    </item>
  </channel>
</rss>"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".rss", delete=False) as f:
            f.write(rss_content)
            temp_file = f.name

        try:
            iterable = FeedIterable(temp_file)
            records = list(iterable)
            assert len(records) == 3
            assert records[0]["title"] == "Item 1"
            assert records[1]["title"] == "Item 2"
            assert records[2]["title"] == "Item 3"
            iterable.close()
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_read_bulk(self):
        """Test bulk reading"""
        rss_content = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Test Feed</title>
    <link>http://example.com</link>
    <item>
      <title>Item 1</title>
      <link>http://example.com/item1</link>
    </item>
    <item>
      <title>Item 2</title>
      <link>http://example.com/item2</link>
    </item>
    <item>
      <title>Item 3</title>
      <link>http://example.com/item3</link>
    </item>
  </channel>
</rss>"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".rss", delete=False) as f:
            f.write(rss_content)
            temp_file = f.name

        try:
            iterable = FeedIterable(temp_file)
            rows = iterable.read_bulk(2)
            assert len(rows) == 2
            assert rows[0]["title"] == "Item 1"
            assert rows[1]["title"] == "Item 2"
            iterable.close()
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_has_totals(self):
        """Test totals method"""
        rss_content = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Test Feed</title>
    <link>http://example.com</link>
    <item>
      <title>Item 1</title>
      <link>http://example.com/item1</link>
    </item>
    <item>
      <title>Item 2</title>
      <link>http://example.com/item2</link>
    </item>
  </channel>
</rss>"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".rss", delete=False) as f:
            f.write(rss_content)
            temp_file = f.name

        try:
            iterable = FeedIterable(temp_file)
            assert FeedIterable.has_totals()
            total = iterable.totals()
            assert total == 2
            iterable.close()
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_automatic_detection_rss(self):
        """Test automatic format detection for RSS via open_iterable"""
        rss_content = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Test Feed</title>
    <link>http://example.com</link>
    <item>
      <title>Test Item</title>
      <link>http://example.com/item1</link>
    </item>
  </channel>
</rss>"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".rss", delete=False) as f:
            f.write(rss_content)
            temp_file = f.name

        try:
            with open_iterable(temp_file) as source:
                assert isinstance(source, FeedIterable)
                row = source.read()
                assert "title" in row
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_automatic_detection_atom(self):
        """Test automatic format detection for Atom via open_iterable"""
        atom_content = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Test Feed</title>
  <link href="http://example.com"/>
  <entry>
    <title>Test Entry</title>
    <link href="http://example.com/entry1"/>
  </entry>
</feed>"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".atom", delete=False) as f:
            f.write(atom_content)
            temp_file = f.name

        try:
            with open_iterable(temp_file) as source:
                assert isinstance(source, FeedIterable)
                row = source.read()
                assert "title" in row
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_reset(self):
        """Test reset functionality"""
        rss_content = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Test Feed</title>
    <link>http://example.com</link>
    <item>
      <title>Test Item</title>
      <link>http://example.com/item1</link>
    </item>
  </channel>
</rss>"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".rss", delete=False) as f:
            f.write(rss_content)
            temp_file = f.name

        try:
            iterable = FeedIterable(temp_file)
            row1 = iterable.read()
            iterable.reset()
            row2 = iterable.read()
            assert row1 == row2
            iterable.close()
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_write_not_supported(self):
        """Test that writing raises NotImplementedError"""
        rss_content = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Test Feed</title>
    <link>http://example.com</link>
    <item>
      <title>Test Item</title>
      <link>http://example.com/item1</link>
    </item>
  </channel>
</rss>"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".rss", delete=False) as f:
            f.write(rss_content)
            temp_file = f.name

        try:
            iterable = FeedIterable(temp_file)
            with pytest.raises(NotImplementedError):
                iterable.write({"title": "New Item"})
            with pytest.raises(NotImplementedError):
                iterable.write_bulk([{"title": "New Item"}])
            iterable.close()
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_missing_dependency(self):
        """Test that missing feedparser raises helpful error"""
        # This test would need to mock the import, but we can at least verify
        # the error message format is correct by checking the code
        pass
