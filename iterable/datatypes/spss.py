from __future__ import annotations
import typing
try:
    import pyreadstat
    HAS_PYREADSTAT = True
except ImportError:
    HAS_PYREADSTAT = False

from ..base import BaseFileIterable, BaseCodec


class SPSSIterable(BaseFileIterable):
    datamode = 'binary'
    def __init__(self, filename:str = None, stream:typing.IO = None, codec: BaseCodec = None, mode:str='r', options:dict={}):
        if not HAS_PYREADSTAT:
            raise ImportError("SPSS file support requires 'pyreadstat' package")
        super(SPSSIterable, self).__init__(filename, stream, codec=codec, binary=True, mode=mode, options=options)
        self.reset()
        pass

    def reset(self):
        """Reset iterable"""
        super(SPSSIterable, self).reset()
        self.pos = 0
        if self.mode == 'r':
            # pyreadstat requires file path, not file object
            if self.filename:
                df, meta = pyreadstat.read_sav(self.filename)
                self.data = df.to_dict('records')
                self.iterator = iter(self.data)
            else:
                raise ValueError("SPSS file reading requires filename, not stream")
        else:
            raise NotImplementedError("SPSS file writing is not yet supported")

    @staticmethod
    def id() -> str:
        return 'sav'

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
            df, meta = pyreadstat.read_sav(self.filename)
            return len(df)
        elif hasattr(self, 'data'):
            return len(self.data)
        return 0

    def read(self) -> dict:
        """Read single SPSS record"""
        row = next(self.iterator)
        self.pos += 1
        # Convert numpy types to Python types
        return {k: (v.item() if hasattr(v, 'item') else v) for k, v in row.items()}

    def read_bulk(self, num:int = 10) -> list[dict]:
        """Read bulk SPSS records"""
        chunk = []
        for n in range(0, num):
            try:
                chunk.append(self.read())
            except StopIteration:
                break
        return chunk

    def write(self, record:dict):
        """Write single SPSS record - not supported"""
        raise NotImplementedError("SPSS file writing is not yet supported")

    def write_bulk(self, records:list[dict]):
        """Write bulk SPSS records - not supported"""
        raise NotImplementedError("SPSS file writing is not yet supported")
