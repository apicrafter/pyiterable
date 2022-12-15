from __future__ import annotations
import typing
import parquet

from ..base import BaseFileIterable


class ParquetIterable(BaseFileIterable):
    datamode = 'binary'
    def __init__(self, filename:str = None, stream:typing.IO = None, codec: BaseCodec = None):
        super(ParquetIterable, self).__init__(filename, stream, codec=codec, binary=True)
        self.reset()
        pass

    def reset(self):
        """Reset iterable"""
        super(ParquetIterable, self).reset()
        self.pos = 0
        self.cursor = parquet.DictReader(self.fobj)


    @staticmethod
    def id() -> str:
        return 'parquet'

    @staticmethod
    def is_flatonly() -> bool:
        return True


    def read(self) -> dict:
        """Read single JSON lines record"""
        row = next(self.cursor)
        self.pos += 1
        return row

    def read_bulk(self, num:int = 10) -> list[dict]:
        """Read bulk JSON lines records"""
        chunk = []
        for n in range(0, num):
            chunk.append(self.read())
        return chunk

