from __future__ import annotations

import typing

from dbfread import DBF

from ..base import BaseCodec, BaseFileIterable


class DBFIterable(BaseFileIterable):
    datamode = "binary"

    def __init__(
        self,
        filename: str = None,
        stream: typing.IO = None,
        codec: BaseCodec = None,
        mode="r",
        encoding: str = "utf-8",
        options: dict = None,
    ):
        if options is None:
            options = {}
        super().__init__(filename, stream, codec=codec, binary=True, mode=mode, noopen=True, options=options)
        self.encoding = encoding
        if "encoding" in options:
            self.encoding = options["encoding"]
        self.reset()
        pass

    def reset(self):
        """Reopen file and open DBF table"""
        super().reset()
        # DBF files need to be opened directly using filename
        # dbfread can accept filename or file-like object, but for codec support
        # we use the filename directly (codecs are typically not used with DBF files)
        self.table = DBF(self.filename, encoding=self.encoding)
        self.iterator = iter(self.table)

    @staticmethod
    def id() -> str:
        """ID of the data source type"""
        return "dbf"

    @staticmethod
    def is_flatonly() -> bool:
        """Flag that data is flat"""
        return True

    @staticmethod
    def has_totals():
        """Has totals indicator"""
        return True

    def totals(self):
        """Returns file totals"""
        return len(self.table)

    def read(self) -> dict:
        """Read single DBF record"""
        try:
            record = next(self.iterator)
            # Convert OrderedDict to regular dict
            return dict(record)
        except StopIteration:
            raise StopIteration from None

    def read_bulk(self, num: int = 10) -> list[dict]:
        """Read bulk DBF records"""
        chunk = []
        for _n in range(0, num):
            try:
                record = next(self.iterator)
                # Convert OrderedDict to regular dict
                chunk.append(dict(record))
            except StopIteration:
                if len(chunk) > 0:
                    return chunk
                raise StopIteration from None
        return chunk
