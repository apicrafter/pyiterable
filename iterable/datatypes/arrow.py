from __future__ import annotations
import typing
try:
    import pyarrow
    import pyarrow.feather
    HAS_PYARROW = True
except ImportError:
    HAS_PYARROW = False

from ..base import BaseFileIterable, BaseCodec

DEFAULT_BATCH_SIZE = 1024


class ArrowIterable(BaseFileIterable):
    datamode = 'binary'
    def __init__(self, filename:str = None, stream:typing.IO = None, mode: str = 'r', codec: BaseCodec = None, batch_size:int = DEFAULT_BATCH_SIZE, options:dict={}):
        if not HAS_PYARROW:
            raise ImportError("Arrow/Feather support requires 'pyarrow' package")
        self.batch_size = batch_size
        self.__buffer = []
        self.is_data_written = False
        super(ArrowIterable, self).__init__(filename, stream, codec=codec, mode=mode, binary=True, options=options)
        self.reset()
        pass

    def reset(self):
        """Reset iterable"""
        super(ArrowIterable, self).reset()
        self.pos = 0
        self.reader = None
        if self.mode == 'r':
            self.table = pyarrow.feather.read_table(self.fobj)
            self.iterator = self.__iterator()
        self.writer = None
        if self.mode == 'w':
            self.writer = None  # Will be created on first write

    @staticmethod
    def id() -> str:
        return 'arrow'

    @staticmethod
    def is_flatonly() -> bool:
        return True

    @staticmethod
    def has_totals():
        """Has totals indicator"""
        return True

    def totals(self):
        """Returns file totals"""
        if self.mode == 'r':
            return len(self.table)
        return 0

    def flush(self):
        """Flush all data"""
        if len(self.__buffer) > 0:
            batch = pyarrow.RecordBatch.from_pylist(self.__buffer)
            table = pyarrow.Table.from_batches([batch])
            # For writing, we need to write to the file object
            # Feather format requires a file path or file-like object
            pyarrow.feather.write_feather(table, self.fobj)
            self.__buffer = []

    def close(self):
        """Close iterable"""
        if self.mode == 'w' and len(self.__buffer) > 0:
            self.flush()
        super(ArrowIterable, self).close()

    def __iterator(self):
        """Iterator for reading records"""
        for batch in self.table.to_batches(max_chunksize=self.batch_size):
            yield from batch.to_pylist()

    def read(self) -> dict:
        """Read single record"""
        row = next(self.iterator)
        self.pos += 1
        return row

    def read_bulk(self, num:int = 10) -> list[dict]:
        """Read bulk Arrow records"""
        chunk = []
        for n in range(0, num):
            chunk.append(self.read())
        return chunk

    def write(self, record: dict):
        """Write single record"""
        self.write_bulk([record, ])

    def write_bulk(self, records: list[dict]):
        """Write bulk records"""
        self.__buffer.extend(records)
