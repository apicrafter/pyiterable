from __future__ import annotations

import zipfile

import lxml.etree as etree

from .xml import etree_to_dict
from .zipped import ZIPSourceWrapper


class ZIPXMLSource(ZIPSourceWrapper):
    def __init__(self, filename: str | None = None, tagname: str = None, prefix_strip: bool = True):
        super().__init__(filename)
        self.tagname = tagname
        self.prefix_strip = prefix_strip
        self.reader = etree.iterparse(self.current_file, recover=True)
        pass

    def id(self) -> str:
        return "zip-xml"

    def is_flat(self) -> bool:
        return False

    @staticmethod
    def has_tables() -> bool:
        """Indicates if this format supports multiple tables/files."""
        return True

    def list_tables(self, filename: str | None = None) -> list[str] | None:
        """List available XML filenames in the ZIP archive.

        Can be called as:
        - Instance method: `iterable.list_tables()` - reuses open ZIP if available
        - With filename: `iterable.list_tables(filename)` - opens ZIP temporarily

        Args:
            filename: Optional filename. If None, uses instance's filename.

        Returns:
            list[str]: List of XML filenames within the ZIP archive, or empty list if no XML files.
        """
        target_filename = filename if filename is not None else self.filename
        if target_filename is None:
            # Try to use open ZIP if available (from ZIPSourceWrapper parent)
            if hasattr(self, "fobj") and self.fobj is not None:
                try:
                    xml_files = [name for name in self.fobj.namelist() if name.lower().endswith(".xml")]
                    return sorted(xml_files) if xml_files else []
                except (AttributeError, OSError):
                    return None
            return None

        # Open ZIP and list XML files
        try:
            with zipfile.ZipFile(target_filename, "r") as zf:
                xml_files = [name for name in zf.namelist() if name.lower().endswith(".xml")]
                return sorted(xml_files) if xml_files else []
        except Exception:
            return None

    def iterfile(self) -> dict:
        res = super().iterfile()
        if res:
            self.reader = etree.iterparse(self.current_file, recover=True)
        return res

    def read_single(self) -> dict:
        """Read single XML record"""
        row = None
        while not row:
            event, elem = next(self.reader)
            shorttag = elem.tag.rsplit("}", 1)[-1]
            if shorttag == self.tagname:
                if self.prefix_strip:
                    row = etree_to_dict(elem, self.prefix_strip)
                else:
                    row = etree_to_dict(elem)
        self.filepos += 1
        self.globalpos += 1
        return row[self.tagname]
