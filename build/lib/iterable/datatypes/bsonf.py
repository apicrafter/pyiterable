# from bson import BSON
import bson

from ..base import BaseFileIterable


class BSONIterable(BaseFileIterable):
    datamode = 'binary'
    def __init__(self, filename=None, stream=None, codec=None, mode='r'):
        super(BSONIterable, self).__init__(filename, stream, codec=codec, binary=True, mode=mode)
        self.reset()
        pass

    def reset(self):
        super(BSONIterable, self).reset()
        self.reader = bson.decode_file_iter(self.fobj)

    @staticmethod
    def id():
        return 'bson'


    @staticmethod
    def is_flatonly():
        return False

    def read(self):
        """Write single bson record"""
        return next(self.reader)

    def read_bulk(self, num):
        """Read bulk bson record"""
        chunk = []
        for n in range(0, num):
            chunk.append(next(self.reader))
        return chunk

    def write(self, record):
        """Write single bson record"""
        self.fobj.write(bson.BSON.encode(record))

    def write_bulk(self, records):
        """Write bulk bson record"""
        for record in records:
            self.fobj.write(bson.BSON.encode(record))
