import json

from ..base import BaseFileIterable


class JSONIterable(BaseFileIterable):
    def __init__(self, filename=None, stream=None, codec=None, tagname=None):
        super(JSONIterable, self).__init__(filename, stream, codec=codec, binary=False)
        self.tagname = tagname
        self.reset()
        pass

    def reset(self):
        super(JSONIterable, self).reset()
        self.pos = 0
        self.data = json.load(self.fobj)
        if self.tagname:
            self.data = self.data[self.tagname]
        self.total = len(self.data)

    @staticmethod
    def id():
        return 'json'

    @staticmethod
    def is_flatonly():
        return False

    def read(self, skip_empty=False):
        """Read single JSON record"""
        if self.pos >= self.total:
            raise StopIteration

        row = self.data[self.pos]
        self.pos += 1
        return row

    def read_bulk(self, num=10):
        """Read bulk JSON records"""
        chunk = []
        for n in range(0, num):
            chunk.append(self.read())
        return chunk
