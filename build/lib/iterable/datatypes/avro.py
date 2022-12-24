from __future__ import annotations
import typing
import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter

from ..base import BaseFileIterable, BaseCodec


class AVROIterable(BaseFileIterable):
    def __init__(self, filename:str = None, stream:typing.IO = None, codec: BaseCodec = None, mode='r'):
        super(AVROIterable, self).__init__(filename, stream, codec=codec, mode=mode, binary=True)
        self.reset()
        pass

    def reset(self):
        """Reset iterable"""
        super(AVROIterable, self).reset()
        self.pos = 0
        self.cursor = DataFileReader(self.fobj, DatumReader())


    @staticmethod
    def id() -> str:
        return 'avro'


    @staticmethod
    def is_flatonly() -> bool:
        return True


    def read(self) -> dict:
        """Read single record"""
        row = next(self.cursor)
        self.pos += 1
        return row

    def read_bulk(self, num:int = 10) -> list[dict]:
        """Read bulk records"""
        chunk = []
        for n in range(0, num):
            chunk.append(self.read())
        return chunk

