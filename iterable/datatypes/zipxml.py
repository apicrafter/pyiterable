from __future__ import annotations
import typing
import lxml.etree as etree

from .zipped import ZIPSourceWrapper
from .xml import etree_to_dict


class ZIPXMLSource(ZIPSourceWrapper):
    def __init__(self, filename:str = None, tagname:str = None, prefix_strip:bool = True):
        super(ZIPXMLSource, self).__init__(filename)
        self.tagname = tagname
        self.prefix_strip = prefix_strip
        self.reader = etree.iterparse(self.current_file, recover=True)
        pass

    def id(self) -> str:
        return 'zip-xml'

    def is_flat(self) -> bool:
        return False

    def iterfile(self) -> dict:
        res = super(ZIPXMLSource, self).iterfile()
        if res:
            self.reader = etree.iterparse(self.current_file, recover=True)
        return res

    def read_single(self) -> dict:
        """Read single XML record"""
        row = None
        while not row:
            event, elem = next(self.reader)
            shorttag = elem.tag.rsplit('}', 1)[-1]
            if shorttag == self.tagname:
                if self.prefix_strip:
                    row = etree_to_dict(elem, self.prefix_strip)
                else:
                    row = etree_to_dict(elem)
        self.filepos += 1
        self.globalpos += 1
        return row[self.tagname]
