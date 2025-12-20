from __future__ import annotations
import typing
import os
from pathlib import Path
try:
    import pyiceberg
    from pyiceberg.catalog import load_catalog
    from pyiceberg.table import Table
    HAS_PYICEBERG = True
except ImportError:
    HAS_PYICEBERG = False

from ..base import BaseFileIterable, BaseCodec


class IcebergIterable(BaseFileIterable):
    datamode = 'binary'
    def __init__(self, filename:str = None, stream:typing.IO = None, codec: BaseCodec = None, mode:str='r', catalog_name:str = None, table_name:str = None, options:dict={}):
        if not HAS_PYICEBERG:
            raise ImportError("Apache Iceberg support requires 'pyiceberg' package")
        super(IcebergIterable, self).__init__(filename, stream, codec=codec, mode=mode, binary=True, noopen=True, options=options)
        self.catalog_name = catalog_name
        self.table_name = table_name
        if 'catalog_name' in options:
            self.catalog_name = options['catalog_name']
        if 'table_name' in options:
            self.table_name = options['table_name']
        if stream is not None:
            raise ValueError("Iceberg requires catalog and table names, not a stream")
        if self.catalog_name is None or self.table_name is None:
            raise ValueError("Iceberg requires catalog_name and table_name parameters")
        self.table = None
        self.scan_result = None
        self.iterator = None
        self.reset()
        pass

    def reset(self):
        """Reset iterable"""
        super(IcebergIterable, self).reset()
        self.pos = 0
        
        # Load catalog and table
        # For file-based catalog, filename might be the catalog properties file
        if self.filename and os.path.exists(self.filename):
            # Assume filename is a catalog properties file
            catalog = load_catalog(self.catalog_name, **{"properties": self.filename})
        else:
            # Use default catalog configuration
            catalog = load_catalog(self.catalog_name)
        
        self.table = catalog.load_table(self.table_name)
        
        if self.mode == 'r':
            # Scan table
            self.scan_result = self.table.scan()
            # Convert to iterator of dicts
            self.iterator = iter(self.scan_result.to_arrow().to_pylist())
        else:
            raise NotImplementedError("Iceberg writing is not yet supported")

    @staticmethod
    def has_totals():
        """Has totals indicator"""
        return True        

    def totals(self):
        """Returns table totals"""
        if self.table is None:
            return 0
        # Count rows in table
        scan_result = self.table.scan()
        return len(scan_result.to_arrow())

    @staticmethod
    def id() -> str:
        return 'iceberg'

    @staticmethod
    def is_flatonly() -> bool:
        return True

    def read(self) -> dict:
        """Read single Iceberg record"""
        try:
            row = next(self.iterator)
            self.pos += 1
            return row
        except (StopIteration, EOFError, ValueError):
            raise StopIteration

    def read_bulk(self, num:int = 10) -> list[dict]:
        """Read bulk Iceberg records"""
        chunk = []
        for n in range(0, num):
            try:
                chunk.append(self.read())
            except StopIteration:
                break
        return chunk

    def write(self, record:dict):
        """Write single Iceberg record"""
        raise NotImplementedError("Iceberg writing is not yet supported")

    def write_bulk(self, records: list[dict]):
        """Write bulk Iceberg records"""
        raise NotImplementedError("Iceberg writing is not yet supported")
