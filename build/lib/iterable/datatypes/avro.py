import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter

from ..base import BaseFileIterable


class AVROIterable(BaseFileIterable):
    def __init__(self, filename=None, stream=None, codec=None):
        super(AVROIterable, self).__init__(filename, stream, codec=codec, binary=True)
        self.reset()
        pass

    def reset(self):
        """Reset iterable"""
        super(AVROIterable, self).reset()
        self.pos = 0
        self.cursor = DataFileReader(self.fobj, DatumReader())


    @staticmethod
    def id():
        return 'avro'

    @staticmethod
    def is_flatonly():
        return True


    def read(self):
        """Read single record"""
        row = next(self.cursor)
        self.pos += 1
        return row

    def read_bulk(self, num=10):
        """Read bulk records"""
        chunk = []
        for n in range(0, num):
            chunk.append(self.read())
        return chunk

