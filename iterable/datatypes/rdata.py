from __future__ import annotations
import typing
try:
    import pyreadr
    HAS_PYREADR = True
except ImportError:
    HAS_PYREADR = False

from ..base import BaseFileIterable, BaseCodec


class RDataIterable(BaseFileIterable):
    datamode = 'binary'
    def __init__(self, filename:str = None, stream:typing.IO = None, codec: BaseCodec = None, mode:str='r', options:dict={}):
        if not HAS_PYREADR:
            raise ImportError("RData file support requires 'pyreadr' package")
        super(RDataIterable, self).__init__(filename, stream, codec=codec, binary=True, mode=mode, options=options)
        self.reset()
        pass

    def reset(self):
        """Reset iterable"""
        super(RDataIterable, self).reset()
        self.pos = 0
        if self.mode == 'r':
            # pyreadr requires file path, not file object
            if self.filename:
                result = pyreadr.read_r(self.filename)
                # RData can contain multiple objects, iterate through all
                self.data = []
                for obj_name, df in result.items():
                    if df is not None:
                        # Convert each dataframe to dict records
                        records = df.to_dict('records')
                        # Add object name as metadata if multiple objects
                        if len(result) > 1:
                            for record in records:
                                record['_r_object_name'] = obj_name
                        self.data.extend(records)
                self.iterator = iter(self.data)
            else:
                raise ValueError("RData file reading requires filename, not stream")
        else:
            raise NotImplementedError("RData file writing is not yet supported")

    @staticmethod
    def id() -> str:
        return 'rdata'

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
            total = 0
            for df in result.values():
                if df is not None:
                    total += len(df)
            return total
        elif hasattr(self, 'data'):
            return len(self.data)
        return 0

    def read(self) -> dict:
        """Read single RData record"""
        row = next(self.iterator)
        self.pos += 1
        # Convert numpy types to Python types
        return {k: (v.item() if hasattr(v, 'item') else v) for k, v in row.items()}

    def read_bulk(self, num:int = 10) -> list[dict]:
        """Read bulk RData records"""
        chunk = []
        for n in range(0, num):
            try:
                chunk.append(self.read())
            except StopIteration:
                break
        return chunk

    def write(self, record:dict):
        """Write single RData record - not supported"""
        raise NotImplementedError("RData file writing is not yet supported")

    def write_bulk(self, records:list[dict]):
        """Write bulk RData records - not supported"""
        raise NotImplementedError("RData file writing is not yet supported")
