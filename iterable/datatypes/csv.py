from __future__ import annotations
import typing
from csv import DictReader, DictWriter

from ..base import BaseFileIterable, BaseCodec


class CSVIterable(BaseFileIterable):
    def __init__(self, filename:str = None, stream:typing.IO = None, codec: BaseCodec = None, keys: list[str] = None, delimiter:str = ',', quotechar:str='"', mode:str='r', encoding:str = 'utf8', options:dict={}):
        self.delimiter = delimiter
        self.quotechar = quotechar
        self.keys = keys
        super(CSVIterable, self).__init__(filename, stream, codec=codec, binary=False, encoding=encoding, mode=mode, options=options)
        self.reset()
        pass

    def reset(self):
        super(CSVIterable, self).reset()
        if self.fobj is None and self.codec is not None:
            fobj = self.codec.textIO(self.encoding)
        else:
            fobj = self.fobj

        self.reader = None
        if self.mode == 'r':
            if self.keys is not None:
                 self.reader = DictReader(fobj, fieldnames=self.keys, delimiter=self.delimiter,
                                     quotechar=self.quotechar)                
            else:
                 self.reader = DictReader(fobj, delimiter=self.delimiter, quotechar=self.quotechar)
        if self.mode in ['w', 'wr'] and self.keys:
            self.writer = DictWriter(fobj, fieldnames=self.keys, delimiter=self.delimiter, quotechar=self.quotechar)
            self.writer.writeheader()
        else:
            self.writer = None

        #            self.reader = reader(self.fobj, delimiter=self.delimiter, quotechar=self.quotechar)
        self.pos = 0

    @staticmethod
    def id() -> str:
        return 'csv'

    @staticmethod
    def is_flatonly() -> bool:
        return True

    def read(self, skip_empty:bool = True):
        """Read single CSV record"""
        row = next(self.reader)
        if skip_empty and len(row) == 0:
            return self.read(skip_empty)
        self.pos += 1
        return row

    def read_bulk(self, num:int = 10) -> list[dict]:
        """Read bulk CSV records"""
        chunk = []
        for n in range(0, num):
            chunk.append(next(self.reader))
            self.pos += 1
        return chunk

    def write(self, record:dict):
        """Write single CSV record"""
        self.writer.writerow(record)

    def write_bulk(self, records: list[dict]):
        """Write bulk CSV records"""
        self.writer.writerows(records)
