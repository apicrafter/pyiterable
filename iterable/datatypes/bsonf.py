# from bson import BSON
from __future__ import annotations
import typing
import bson

from ..base import BaseFileIterable, BaseCodec


class BSONIterable(BaseFileIterable):
    datamode = 'binary'
    def __init__(self, filename:str = None, stream:typing.IO = None, codec: BaseCodec = None, mode:str='r', options:dict={}):
        super(BSONIterable, self).__init__(filename, stream, codec=codec, binary=True, mode=mode, options=options)
        self.reset()
        pass

    def reset(self):
        super(BSONIterable, self).reset()
        self.reader = bson.decode_file_iter(self.fobj)

    @staticmethod
    def id() -> str:
        return 'bson'


    @staticmethod
    def is_flatonly() -> bool:
        return False

    def read(self) -> dict:
        """Write single bson record"""
        return next(self.reader)

    def read_bulk(self, num:int = 10) -> list[dict]:
        """Read bulk bson record"""
        chunk = []
        for n in range(0, num):
            chunk.append(next(self.reader))
        return chunk

    def write(self, record:dict):
        """Write single bson record"""
        self.fobj.write(bson.BSON.encode(record))

    def write_bulk(self, records:list[dict]):
        """Write bulk bson record"""
        for record in records:
            self.fobj.write(bson.BSON.encode(record))
