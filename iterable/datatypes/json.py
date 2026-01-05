from __future__ import annotations

import json
import typing

from ..base import BaseCodec, BaseFileIterable


class JSONIterable(BaseFileIterable):
    def __init__(self, filename:str = None, stream:typing.IO = None, codec: BaseCodec = None, mode='r', tagname:str= None, options:dict=None):
        if options is None:
            options = {}
        self.tagname = tagname or options.get('tagname')
        super().__init__(filename, stream, codec=codec, mode=mode, binary=False, options=options)
        self.reset()
        pass

    def reset(self):
        super().reset()
        self.pos = 0
        if self.mode in ['w', 'wr']:
            # Re-initialize output (truncate if needed) and prepare streaming JSON writing.
            if hasattr(self.fobj, "seek") and hasattr(self.fobj, "truncate"):
                try:
                    self.fobj.seek(0)
                    self.fobj.truncate(0)
                except Exception:
                    # Best-effort; some streams may not support truncation.
                    pass
            self._write_started = True
            self._first_item = True
            # Support optional wrapper object with a list under tagname.
            if self.tagname:
                self.fobj.write('{"' + str(self.tagname) + '":[')
            else:
                self.fobj.write('[')
            self.total = 0
            self.data = None
        else:
            self.data = json.load(self.fobj)
            if self.tagname:
                self.data = self.data[self.tagname]
            self.total = len(self.data)

    @staticmethod
    def id() -> str:
        return 'json'

    @staticmethod
    def has_totals():
        """Has totals indicator"""
        return True        

    def totals(self):
        """Returns file totals"""
        return self.total

    @staticmethod
    def is_flatonly() -> bool:
        return False

    def read(self, skip_empty:bool = False) -> dict:
        """Read single JSON record"""
        if self.pos >= self.total:
            raise StopIteration

        row = self.data[self.pos]
        self.pos += 1
        return row

    def read_bulk(self, num:int = 10) -> list[dict]:
        """Read bulk JSON records"""
        chunk = []
        for _n in range(0, num):
            chunk.append(self.read())
        return chunk

    def write(self, record: dict):
        """Write single JSON record (array item)."""
        self.write_bulk([record])

    def write_bulk(self, records: list[dict]):
        """Write bulk JSON records (array items)."""
        if self.mode not in ['w', 'wr']:
            raise ValueError("Write mode not enabled")
        if not records:
            return
        for record in records:
            if not getattr(self, "_first_item", True):
                self.fobj.write(",")
            self.fobj.write(json.dumps(record, ensure_ascii=False, default=str))
            self._first_item = False
            self.total += 1

    def close(self):
        """Close iterable and finalize JSON output if writing."""
        if self.mode in ['w', 'wr'] and getattr(self, "_write_started", False):
            if self.tagname:
                self.fobj.write("]}")
            else:
                self.fobj.write("]")
        super().close()
