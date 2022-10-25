import parquet

from ..base import BaseFileIterable


class ParquetIterable(BaseFileIterable):
    datamode = 'binary'
    def __init__(self, filename=None, stream=None, codec=None):
        super(ParquetIterable, self).__init__(filename, stream, codec=codec, binary=True)
        self.reset()
        pass

    def reset(self):
        """Reset iterable"""
        super(ParquetIterable, self).reset()
        self.pos = 0
        self.cursor = parquet.DictReader(self.fobj)


    @staticmethod
    def id():
        return 'parquet'

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

