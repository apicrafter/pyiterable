from __future__ import annotations

import typing

import pyarrow
import pyarrow.parquet

from ..base import BaseCodec, BaseFileIterable

DEFAULT_BATCH_SIZE = 1024

def fields_to_pyarrow_schema(keys):
    fields = []
    for key in keys:
        fields.append((key, pyarrow.string()))
    return pyarrow.schema(fields)
                                                                                                                                                                                        

class ParquetIterable(BaseFileIterable):
    datamode = 'binary'
    def __init__(self, filename:str = None, stream:typing.IO = None, mode: str = 'r', codec: BaseCodec = None, keys:list[str] = None, schema:list[str] = None, compression:str  = 'snappy', adapt_schema:bool = True, use_pandas:bool = True, batch_size:int = DEFAULT_BATCH_SIZE, options:dict=None):
        if options is None:
            options = {}
        self.use_pandas = use_pandas
        self.__buffer = []
        self.adapt_schema = adapt_schema
        self.keys = keys
        self.schema = schema
        self.compression = compression
        self.batch_size = batch_size          
        super().__init__(filename, stream, codec=codec, mode=mode, binary=True, options=options)
        self.reset()
        self.is_data_written = False
        pass

    def reset(self):
        """Reset iterable"""
        super().reset()
        self.pos = 0
        self.reader = None
        if self.mode == 'r':
            self.reader = pyarrow.parquet.ParquetFile(self.fobj)    
            self.iterator = self.__iterator()              
 #           self.tbl = self.reader.to_table()
        self.writer = None
        if self.mode == 'w':
            # Reset write state for streaming writes
            self.__buffer = []
            self.is_data_written = False
            if not self.adapt_schema:
                if self.schema is not None:
                    struct_schema = self.schema
                else:
                    struct_schema = fields_to_pyarrow_schema(self.keys)
                self.writer = pyarrow.parquet.ParquetWriter(
                    self.fobj, struct_schema, compression=self.compression, use_dictionary=False
                )
                self.is_data_written = True

#            self.writer = pyorc.Writer(self.fobj, "struct<%s>" % (','.join(struct_schema)), struct_repr = pyorc.StructRepr.DICT, compression=self.compression, compression_strategy=1)  


    @staticmethod
    def id() -> str:
        return 'parquet'

    @staticmethod
    def is_flatonly() -> bool:
        return True

    @staticmethod
    def has_totals():
        """Has totals indicator"""
        return True        

    def totals(self):
        """Returns file totals"""
        if self.reader is None:
            return 0
        try:
            meta = self.reader.metadata
            return meta.num_rows if meta is not None else 0
        except Exception:
            return self.reader.scan_contents()        

    def flush(self):
        """Flush all data"""
        if not self.__buffer:
            return
        table = pyarrow.Table.from_pylist(self.__buffer)
        if self.writer is None:
            self.writer = pyarrow.parquet.ParquetWriter(
                self.fobj, table.schema, compression=self.compression, use_dictionary=False
            )
        self.writer.write_table(table)
        self.__buffer = []
        

    def close(self):
        """Close iterable"""          
        if self.mode == 'w':
            self.flush()
        if self.writer is not None:
            self.writer.close()
        super().close()

    def __iterator(self):
        for batch in self.reader.iter_batches(batch_size=self.batch_size):
            yield from batch.to_pylist()


    def read(self) -> dict:
        """Read single record"""
        row = next(self.iterator)
        self.pos += 1
        return row


    def read_bulk(self, num:int = 10) -> list[dict]:
        """Read bulk Parquet records"""
        chunk = []
        for _n in range(0, num):
            chunk.append(self.read())
        return chunk

    def write(self, record: dict):
        """Write single record"""
        self.write_bulk([record, ])

    def write_bulk(self, records: list[dict]):
        """Write bulk records"""
        if not records:
            return

        # If we already have a writer, write immediately (bounded memory).
        if self.writer is not None:
            self.writer.write_table(pyarrow.Table.from_pylist(records))
            return

        # Schema-adaptive streaming: buffer up to batch_size, then flush (writer created on first flush).
        self.__buffer.extend(records)
        if len(self.__buffer) >= self.batch_size:
            self.flush()

