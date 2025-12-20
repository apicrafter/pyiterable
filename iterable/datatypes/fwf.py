from __future__ import annotations
import typing
import chardet

from ..base import BaseFileIterable, BaseCodec
from ..helpers.utils import rowincount

DEFAULT_ENCODING = 'utf8'


class FixedWidthIterable(BaseFileIterable):
    def __init__(self, filename:str = None, stream:typing.IO = None, codec: BaseCodec = None, widths:list[int] = None, names:list[str] = None, encoding:str = None, mode:str='r', options:dict={}):
        self.widths = widths
        self.names = names
        self.encoding = encoding or DEFAULT_ENCODING
        
        if 'widths' in options:
            self.widths = options['widths']
        if 'names' in options:
            self.names = options['names']
        if 'encoding' in options:
            self.encoding = options['encoding']
            
        super(FixedWidthIterable, self).__init__(filename, stream, codec=codec, binary=False, mode=mode, encoding=self.encoding, options=options)
        self.reset()
        pass

    def reset(self):
        """Reset iterable"""
        super(FixedWidthIterable, self).reset()
        self.pos = 0
        if self.mode == 'r':
            if self.widths is None or self.names is None:
                raise ValueError("Fixed-width files require 'widths' and 'names' parameters")
            if len(self.widths) != len(self.names):
                raise ValueError("Length of 'widths' must match length of 'names'")

    @staticmethod
    def id() -> str:
        return 'fwf'

    @staticmethod
    def is_flatonly() -> bool:
        return True

    @staticmethod
    def has_totals():
        """Has totals indicator"""
        return True

    def totals(self):
        """Returns file totals"""
        return rowincount(self.filename, self.fobj)

    def read(self, skip_empty:bool = True) -> dict:
        """Read single fixed-width record"""
        line = self.fobj.readline()
        if not line:
            raise StopIteration
        if skip_empty and len(line.strip()) == 0:
            return self.read(skip_empty)
        
        self.pos += 1
        record = {}
        start = 0
        for i, (name, width) in enumerate(zip(self.names, self.widths)):
            end = start + width
            value = line[start:end].strip()
            record[name] = value
            start = end
        return record

    def read_bulk(self, num:int = 10) -> list[dict]:
        """Read bulk fixed-width records"""
        chunk = []
        for n in range(0, num):
            try:
                chunk.append(self.read())
            except StopIteration:
                break
        return chunk

    def write(self, record:dict):
        """Write single fixed-width record"""
        if self.widths is None or self.names is None:
            raise ValueError("Fixed-width files require 'widths' and 'names' parameters")
        
        line_parts = []
        for name, width in zip(self.names, self.widths):
            value = str(record.get(name, ''))
            # Pad or truncate to fit width
            formatted = value[:width].ljust(width)
            line_parts.append(formatted)
        
        self.fobj.write(''.join(line_parts) + '\n')

    def write_bulk(self, records:list[dict]):
        """Write bulk fixed-width records"""
        for record in records:
            self.write(record)
