from __future__ import annotations
import typing
from json import loads, dumps
import datetime

from ..base import BaseFileIterable, BaseCodec
from ..helpers.utils import rowincount


date_handler = lambda obj: (
    obj.isoformat()
    if isinstance(obj, (datetime.datetime, datetime.date))
    else None
)


class JSONLinesIterable(BaseFileIterable):
    def __init__(self, filename:str = None, stream:typing.IO = None, codec: BaseCodec = None, mode:str = 'r', encoding:str = 'utf8', options:dict={}):
        self.pos = 0
        super(JSONLinesIterable, self).__init__(filename, stream, codec=codec, binary=False, mode=mode, encoding=encoding, options=options)
        pass

    @staticmethod
    def id() -> str:
        return 'jsonl'

    @staticmethod
    def is_flatonly() -> bool:
        return False

    @staticmethod
    def has_totals():
        """Has totals indicator"""
        return True        

    def totals(self):
        """Returns file totals"""
        if self.codec is not None:
            fobj = self.codec.fileobj()
        else:
            fobj = self.fobj
        return rowincount(self.filename, fobj)


    def read(self, skip_empty:bool = False) -> dict:
        """Read single JSON lines record"""
        line = next(self.fobj)
        if skip_empty and len(line) == 0:
            return self.read(skip_empty)
        self.pos += 1
        if line:
            return loads(line)
        return None

    def read_bulk(self, num:int = 10) -> list[dict]:
        """Read bulk JSON lines records"""
        chunk = []
        for n in range(0, num):
            chunk.append(loads(self.fobj.readline()))
        return chunk

    def write(self, record: dict):
        """Write single JSON lines record"""
        self.fobj.write(dumps(record, ensure_ascii=False, default=date_handler) + '\n')

    def write_bulk(self, records: list[dict]):
        """Write bulk JSON lines records"""
        for record in records:
            self.fobj.write(dumps(record, ensure_ascii=False, default=date_handler) + '\n')
