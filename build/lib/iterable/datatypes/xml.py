from collections import defaultdict
import lxml.etree as etree

from ..base import BaseFileIterable


PREFIX_STRIP = False
PREFIX = ""


def etree_to_dict(t, prefix_strip=True):
    tag = t.tag if not prefix_strip else t.tag.rsplit('}', 1)[-1]
    d = {tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            #            print(dir(dc))
            for k, v in dc.items():
                if prefix_strip:
                    k = k.rsplit('}', 1)[-1]
                dd[k].append(v)
        d = {tag: {k: v[0] if len(v) == 1 else v for k, v in dd.items()}}
    if t.attrib:
        d[tag].update(('@' + k.rsplit('}', 1)[-1], v) for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            tag = tag.rsplit('}', 1)[-1]
            if text:
                d[tag]['#text'] = text
        else:
            d[tag] = text
    return d


class XMLIterable(BaseFileIterable):
    def __init__(self, filename=None, stream=None, codec=None, tagname=None, prefix_strip=True):
        super(XMLIterable, self).__init__(filename, stream, codec=codec, binary=True, encoding='utf8')
        self.tagname = tagname
        self.prefix_strip = prefix_strip
        self.reset()
        pass

    def reset(self):
        super(XMLIterable, self).reset()
        self.reader = etree.iterparse(self.fobj, recover=True)        
        self.pos = 0

    @staticmethod
    def id():
        return 'xml'


    @staticmethod
    def is_flatonly():
        return False

    def read(self):
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
        self.pos += 1
        return row[self.tagname]

    def read_bulk(self, num):
        """Read bulk XML records"""
        chunk = []
        for n in range(0, num):
            chunk.append(self.read())
        return chunk
