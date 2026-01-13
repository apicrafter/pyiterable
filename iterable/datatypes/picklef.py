from __future__ import annotations

import datetime
import pickle
import typing

from ..base import BaseCodec, BaseFileIterable


def date_handler(obj):
    return obj.isoformat() if isinstance(obj, (datetime.datetime, datetime.date)) else None


class PickleIterable(BaseFileIterable):
    datamode = "binary"

    def __init__(
        self,
        filename: str = None,
        stream: typing.IO = None,
        codec: BaseCodec = None,
        mode: str = "r",
        options: dict = None,
    ):
        if options is None:
            options = {}
        super().__init__(filename, stream, codec=codec, binary=True, mode=mode, options=options)
        self.pos = 0
        pass

    @staticmethod
    def id() -> str:
        return "pickle"

    @staticmethod
    def is_flatonly() -> bool:
        return False

    def read(self) -> dict:
        """Read single record"""
        try:
            return pickle.load(self.fobj)
        except EOFError:
            raise StopIteration from None

    def read_bulk(self, num: int = 10) -> list[dict]:
        """Read bulk records"""
        chunk = []
        for _n in range(0, num):
            try:
                obj = pickle.load(self.fobj)
                chunk.append(obj)
            except Exception:
                if len(chunk) > 0:
                    return chunk
                raise StopIteration from None
        return chunk

    def write(self, record: dict):
        """Write single record into file"""
        pickle.dump(record, self.fobj)

    def write_bulk(self, records: list[dict]):
        """Write bulk records"""
        for record in records:
            pickle.dump(record, self.fobj)
