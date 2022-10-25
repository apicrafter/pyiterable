import pyorc

from ..base import BaseFileIterable


class ORCIterable(BaseFileIterable):
    def __init__(self, filename=None, stream=None, codec=None):
        super(ORCIterable, self).__init__(filename, stream, codec=codec, binary=True)
        self.reset()
        pass

    def reset(self):
        """Reset iterable"""
        super(ORCIterable, self).reset()
        self.pos = 0
        self.cursor = pyorc.Reader(self.fobj, struct_repr=pyorc.StructRepr.DICT)


    @staticmethod
    def id():
        return 'orc'

    @staticmethod
    def is_flatonly():
        return True


    def read(self):
        """Read single JSON lines record"""
        row = next(self.cursor)
        self.pos += 1
        return row

    def read_bulk(self, num=10):
        """Read bulk JSON lines records"""
        chunk = []
        for n in range(0, num):
            chunk.append(self.read())
        return chunk

