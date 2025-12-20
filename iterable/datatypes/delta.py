from __future__ import annotations
import typing
try:
    import deltalake
    HAS_DELTALAKE = True
except ImportError:
    HAS_DELTALAKE = False

from ..base import BaseFileIterable, BaseCodec


class DeltaIterable(BaseFileIterable):
    datamode = 'binary'
    def __init__(self, filename:str = None, stream:typing.IO = None, codec: BaseCodec = None, mode:str='r', options:dict={}):
        if not HAS_DELTALAKE:
            raise ImportError("Delta Lake support requires 'deltalake' package")
        super(DeltaIterable, self).__init__(filename, stream, codec=codec, binary=True, mode=mode, options=options)
        self.reset()
        pass

    def reset(self):
        """Reset iterable"""
        super(DeltaIterable, self).reset()
        self.pos = 0
        if self.mode == 'r':
            # Delta Lake requires a path to the delta table directory
            if self.filename:
                self.delta_table = deltalake.DeltaTable(self.filename)
                # Convert to PyArrow table and iterate
                self.pyarrow_table = self.delta_table.to_pyarrow_table()
                self.iterator = self.__iterator()
            else:
                raise ValueError("Delta Lake reading requires filename (path to delta table)")
        else:
            raise NotImplementedError("Delta Lake writing is not yet supported")

    def __iterator(self):
        """Iterator for reading Delta table records"""
        # Convert PyArrow table to list of dicts
        for batch in self.pyarrow_table.to_batches():
            yield from batch.to_pylist()

    @staticmethod
    def id() -> str:
        return 'delta'

    @staticmethod
    def is_flatonly() -> bool:
        return True

    @staticmethod
    def has_totals():
        """Has totals indicator"""
        return True

    def totals(self):
        """Returns file totals"""
        if hasattr(self, 'pyarrow_table'):
            return len(self.pyarrow_table)
        return 0

    def read(self) -> dict:
        """Read single Delta record"""
        row = next(self.iterator)
        self.pos += 1
        return row

    def read_bulk(self, num:int = 10) -> list[dict]:
        """Read bulk Delta records"""
        chunk = []
        for n in range(0, num):
            try:
                chunk.append(self.read())
            except StopIteration:
                break
        return chunk

    def write(self, record:dict):
        """Write single Delta record - not supported"""
        raise NotImplementedError("Delta Lake writing is not yet supported")

    def write_bulk(self, records:list[dict]):
        """Write bulk Delta records - not supported"""
        raise NotImplementedError("Delta Lake writing is not yet supported")
