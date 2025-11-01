from __future__ import annotations
import typing
from json import loads, dumps
import datetime
import duckdb
from ..base import BaseFileIterable, BaseCodec

DUCKDB_USE_CACHE = True
DUCKDB_CACHE_SIZE = 1000


class DuckDBIterable(BaseFileIterable):
    def __init__(self, filename:str = None, stream:typing.IO = None, codec: BaseCodec = None, engine:str="duckdb", mode:str = 'r', encoding:str = 'utf8', options:dict={}):
        self.pos = 0
        super(DuckDBIterable, self).__init__(filename, stream, codec=codec, binary=False, mode=mode, encoding=encoding, options=options)                
        self.slice = [0, DUCKDB_CACHE_SIZE]
        self.cached_batch = None
        pass

    @staticmethod
    def id() -> str:
        return 'duckdb'

    @staticmethod
    def is_flatonly() -> bool:
        return False

    def open(self):
        """No need to open iterable for DuckDB """
        pass

    def close(self):
        """No needto close iterable for DuckDB"""

    def totals(self):
        """Returns total number of records"""       
        return duckdb.sql(f"select count(*) from '{self.filename}'").fetchone()[0]

    def reset(self):
        """Resets counter"""
        self.pos = 0 

    def read(self) -> dict:
        """Read single cached record"""
        if self.cached_batch is None : 
            self.cached_batch = duckdb.sql(f"select * from '{self.filename}' offset {self.slice[0]} limit {self.slice[1]}").df().to_dict('records')
            realpos = self.pos % DUCKDB_CACHE_SIZE
            if realpos < len(self.cached_batch):
                self.pos += 1
                item = self.cached_batch[realpos]
                return item
            else:
                raise StopIteration
        elif self.slice[0] <= self.pos < self.slice[1]:
            realpos = self.pos % DUCKDB_CACHE_SIZE
            if realpos < len(self.cached_batch):
                self.pos += 1
                item = self.cached_batch[realpos]
                return item
            else:
                raise StopIteration
        else:
            self.slice = [int(self.pos / DUCKDB_CACHE_SIZE) * DUCKDB_CACHE_SIZE, int(self.pos / DUCKDB_CACHE_SIZE) * DUCKDB_CACHE_SIZE + DUCKDB_CACHE_SIZE]
            self.cached_batch = duckdb.sql(f"select * from '{self.filename}' offset {self.slice[0]} limit {self.slice[1]}").df().to_dict('records')
            realpos = self.pos % DUCKDB_CACHE_SIZE
            if realpos < len(self.cached_batch):
                self.pos += 1
                item = self.cached_batch[realpos]
                return item
            else:
                raise StopIteration
        return None

    def read_bulk(self, num:int = 100) -> list[dict]:
        """Read bulk records"""
        chunk = duckdb.sql(f"select * from '{self.filename}' offset {self.pos} limit {num}").df().to_dict('records')
        return chunk

