from __future__ import annotations
import typing
try:
    import pyreadr
    HAS_PYREADR = True
except ImportError:
    HAS_PYREADR = False

from ..base import BaseFileIterable, BaseCodec


class RDSIterable(BaseFileIterable):
    datamode = 'binary'
    def __init__(self, filename:str = None, stream:typing.IO = None, codec: BaseCodec = None, mode:str='r', options:dict={}):
        if not HAS_PYREADR:
            raise ImportError("RDS file support requires 'pyreadr' package")
        super(RDSIterable, self).__init__(filename, stream, codec=codec, binary=True, mode=mode, options=options)
        self.reset()
        pass

    def reset(self):
        """Reset iterable"""
        super(RDSIterable, self).reset()
        self.pos = 0
        if self.mode == 'r':
            # pyreadr requires file path, not file object
            if self.filename:
                result = pyreadr.read_r(self.filename)
                # RDS contains a single object, typically stored under None key
                df = result.get(None) or list(result.values())[0] if result else None
                if df is not None:
                    self.data = df.to_dict('records')
                    self.iterator = iter(self.data)
                else:
                    self.data = []
                    self.iterator = iter(self.data)
            else:
                raise ValueError("RDS file reading requires filename, not stream")
        else:
            raise NotImplementedError("RDS file writing is not yet supported")

    @staticmethod
    def id() -> str:
        return 'rds'

    @staticmethod
    def is_flatonly() -> bool:
        return True

    @staticmethod
    def has_totals():
        """Has totals indicator"""
        return True

    def totals(self):
        """Returns file totals"""
        if self.filename:
            result = pyreadr.read_r(self.filename)
            df = result.get(None) or list(result.values())[0] if result else None
            if df is not None:
                return len(df)
            return 0
        elif hasattr(self, 'data'):
            return len(self.data)
        return 0

    def read(self) -> dict:
        """Read single RDS record"""
        row = next(self.iterator)
        self.pos += 1
        # Convert numpy types to Python types
        return {k: (v.item() if hasattr(v, 'item') else v) for k, v in row.items()}

    def read_bulk(self, num:int = 10) -> list[dict]:
        """Read bulk RDS records"""
        chunk = []
        for n in range(0, num):
            try:
                chunk.append(self.read())
            except StopIteration:
                break
        return chunk

    def write(self, record:dict):
        """Write single RDS record - not supported"""
        raise NotImplementedError("RDS file writing is not yet supported")

    def write_bulk(self, records:list[dict]):
        """Write bulk RDS records - not supported"""
        raise NotImplementedError("RDS file writing is not yet supported")
