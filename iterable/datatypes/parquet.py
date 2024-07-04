from __future__ import annotations
import typing
import pyarrow
import pyarrow.parquet

from ..base import BaseFileIterable, BaseCodec

DEFAULT_BATCH_SIZE = 1024

def fields_to_pyarrow_schema(keys):
    fields = []
    for key in keys:
        fields.append((key, pyarrow.string()))
    return pyarrow.schema(fields)
                                                                                                                                                                                        

class ParquetIterable(BaseFileIterable):
    datamode = 'binary'
    def __init__(self, filename:str = None, stream:typing.IO = None, mode: str = 'r', codec: BaseCodec = None, keys:list[str] = None, schema:list[str] = None, compression:str  = None, batch_size:int = DEFAULT_BATCH_SIZE, options:dict={}):
        self.keys = keys
        self.schema = schema
        self.compression = compression
        self.batch_size = batch_size          
        super(ParquetIterable, self).__init__(filename, stream, codec=codec, mode=mode, binary=True, options=options)
        self.reset()
        pass

    def reset(self):
        """Reset iterable"""
        super(ParquetIterable, self).reset()
        self.pos = 0
        self.reader = None
        if self.mode == 'r':
            self.reader = pyarrow.parquet.ParquetFile(self.fobj)    
            self.iterator = self.__iterator()              
 #           self.tbl = self.reader.to_table()
        self.writer = None
        if self.mode == 'w':
            if self.schema is not None:
               struct_schema = self.schema
            else:
               struct_schema = fields_to_pyarrow_schema(self.keys)
            self.writer = pyarrow.parquet.ParquetWriter(self.fobj, struct_schema, compression=self.compression, use_dictionary=False)          
#            self.writer = pyorc.Writer(self.fobj, "struct<%s>" % (','.join(struct_schema)), struct_repr = pyorc.StructRepr.DICT, compression=self.compression, compression_strategy=1)  


    @staticmethod
    def id() -> str:
        return 'parquet'

    @staticmethod
    def is_flatonly() -> bool:
        return True

    def close(self):
        """Close iterable"""
        if self.writer is not None: self.writer.close()
        super(ParquetIterable, self).close()

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
        for n in range(0, num):
            chunk.append(self.read())
        return chunk

    def write(self, record: dict):
        """Write single record"""
        batch = pyarrow.RecordBatch.from_pylist([record, ])
        self.writer.write_batch(batch)

    def write_bulk(self, records: list[dict]):
        """Write bulk records"""
        batch = pyarrow.RecordBatch.from_pylist(records)
        self.writer.write_batch(batch)

