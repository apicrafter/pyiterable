from __future__ import annotations
import typing
import os
from pathlib import Path
try:
    from pyhudi import HudiCatalog
    HAS_PYHUDI = True
except ImportError:
    try:
        import hudi
        HAS_HUDI = True
        HAS_PYHUDI = False
    except ImportError:
        HAS_HUDI = False
        HAS_PYHUDI = False

from ..base import BaseFileIterable, BaseCodec


class HudiIterable(BaseFileIterable):
    datamode = 'binary'
    def __init__(self, filename:str = None, stream:typing.IO = None, codec: BaseCodec = None, mode:str='r', table_path:str = None, options:dict={}):
        if not HAS_PYHUDI and not HAS_HUDI:
            raise ImportError("Apache Hudi support requires 'pyhudi' or 'hudi' package")
        super(HudiIterable, self).__init__(filename, stream, codec=codec, mode=mode, binary=True, noopen=True, options=options)
        self.table_path = table_path
        if 'table_path' in options:
            self.table_path = options['table_path']
        if stream is not None:
            raise ValueError("Hudi requires table_path, not a stream")
        if self.table_path is None and self.filename is None:
            raise ValueError("Hudi requires table_path parameter")
        if self.table_path is None:
            self.table_path = self.filename
        self.table = None
        self.iterator = None
        self.reset()
        pass

    def reset(self):
        """Reset iterable"""
        super(HudiIterable, self).reset()
        self.pos = 0
        
        if self.mode == 'r':
            # Load Hudi table
            # This is a simplified implementation - actual usage would depend on Hudi API
            if HAS_PYHUDI:
                # pyhudi API
                catalog = HudiCatalog()
                self.table = catalog.load_table(self.table_path)
                # Read table data
                df = self.table.to_pandas()
                self.iterator = iter(df.to_dict('records'))
            else:
                # hudi API (if different)
                # Placeholder - would need actual Hudi API documentation
                self.iterator = iter([])
        else:
            raise NotImplementedError("Hudi writing is not yet supported")

    @staticmethod
    def has_totals():
        """Has totals indicator"""
        return True        

    def totals(self):
        """Returns table totals"""
        if self.table is None:
            return 0
        if HAS_PYHUDI:
            df = self.table.to_pandas()
            return len(df)
        return 0

    @staticmethod
    def id() -> str:
        return 'hudi'

    @staticmethod
    def is_flatonly() -> bool:
        return True

    def read(self) -> dict:
        """Read single Hudi record"""
        try:
            row = next(self.iterator)
            self.pos += 1
            return row
        except (StopIteration, EOFError, ValueError):
            raise StopIteration

    def read_bulk(self, num:int = 10) -> list[dict]:
        """Read bulk Hudi records"""
        chunk = []
        for n in range(0, num):
            try:
                chunk.append(self.read())
            except StopIteration:
                break
        return chunk

    def write(self, record:dict):
        """Write single Hudi record"""
        raise NotImplementedError("Hudi writing is not yet supported")

    def write_bulk(self, records: list[dict]):
        """Write bulk Hudi records"""
        raise NotImplementedError("Hudi writing is not yet supported")
