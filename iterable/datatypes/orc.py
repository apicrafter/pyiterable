from __future__ import annotations

import typing

import pyorc

from ..base import BaseCodec, BaseFileIterable


def df_to_pyorc_schema(df):
    """Extracts column information from pandas dataframe and generate pyorc schema"""
    struct_schema = []
    for k, v in df.dtypes.to_dict().items():
        v = str(v)
        if v == 'float64':
            struct_schema.append(f'{k}:float')
        elif v == 'float32':
            struct_schema.append(f'{k}:float')
        elif v == 'datetime64[ns]':
            struct_schema.append(f'{k}:timestamp')
        elif v == 'int32':
            struct_schema.append(f'{k}:int')
        elif v == 'int64':
            struct_schema.append(f'{k}:int')
        else:
            struct_schema.append(f'{k}:string')
    return struct_schema


def fields_to_pyorc_schema(fields):
    """Converts list of fields to pyorc schema array"""
    struct_schema = []
    for field in fields:
        struct_schema.append(f'{field}:string')    
    return struct_schema

class ORCIterable(BaseFileIterable):
    datamode = 'binary'
    def __init__(self, filename:str = None, stream:typing.IO = None, codec: BaseCodec = None, mode:str = 'r', keys:list[str] = None, schema:list[str] = None, compression:int = 5, options:dict=None):
        if options is None:
            options = {}
        self.keys = keys
        self.schema = schema
        self.compression = compression
        super().__init__(filename, stream, codec=codec, mode=mode, binary=True, options=options)
        self.reset()
        pass

    def reset(self):
        """Reset iterable"""
        super().reset()
        self.pos = 0
        self.reader = None
        if self.mode == 'r':
            self.reader = pyorc.Reader(self.fobj, struct_repr=pyorc.StructRepr.DICT)
        self.writer = None
        if self.mode == 'w':
            if self.schema is not None:
               struct_schema = self.schema
            else:
               struct_schema = fields_to_pyorc_schema(self.keys)
            self.writer = pyorc.Writer(self.fobj, "struct<{}>".format(','.join(struct_schema)), struct_repr = pyorc.StructRepr.DICT, compression=self.compression, compression_strategy=1)  
         

    @staticmethod
    def id() -> str:
        return 'orc'

    @staticmethod
    def is_flatonly() -> bool:
        return True


    @staticmethod
    def has_totals():
        """Has totals indicator"""
        return True        

    def totals(self):
        """Returns file totals"""
        return len(self.reader)

    def close(self):
        """Close iterable"""
        if self.writer is not None: self.writer.close()
        super().close()


    def read(self) -> dict:
        """Read single record"""
        row = next(self.reader)
        self.pos += 1
        return row

    def read_bulk(self, num:int = 10) -> list[dict]:
        """Read bulk records"""
        chunk = []
        for _n in range(0, num):
            chunk.append(self.read())
        return chunk

    def write(self, record: dict):
        """Write single record"""
        self.writer.write(record)

    def write_bulk(self, records: list[dict]):
        """Write bulk records"""
        self.writer.writerows(records)
