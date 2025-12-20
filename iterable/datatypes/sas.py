from __future__ import annotations
import typing
try:
    import pyreadstat
    HAS_PYREADSTAT = True
except ImportError:
    HAS_PYREADSTAT = False
    try:
        import sas7bdat
        HAS_SAS7BDAT = True
    except ImportError:
        HAS_SAS7BDAT = False

from ..base import BaseFileIterable, BaseCodec


class SASIterable(BaseFileIterable):
    datamode = 'binary'
    def __init__(self, filename:str = None, stream:typing.IO = None, codec: BaseCodec = None, mode:str='r', options:dict={}):
        if not HAS_PYREADSTAT and not HAS_SAS7BDAT:
            raise ImportError("SAS file support requires either 'pyreadstat' or 'sas7bdat' package")
        super(SASIterable, self).__init__(filename, stream, codec=codec, binary=True, mode=mode, options=options)
        self.reset()
        pass

    def reset(self):
        """Reset iterable"""
        super(SASIterable, self).reset()
        self.pos = 0
        if self.mode == 'r':
            if HAS_PYREADSTAT:
                # pyreadstat requires file path, not file object
                if self.filename:
                    df, meta = pyreadstat.read_sas7bdat(self.filename)
                    self.data = df.to_dict('records')
                    self.iterator = iter(self.data)
                else:
                    raise ValueError("SAS file reading requires filename, not stream")
            elif HAS_SAS7BDAT:
                self.reader = sas7bdat.SAS7BDAT(self.fobj)
                self.iterator = iter(self.reader)
        else:
            raise NotImplementedError("SAS file writing is not yet supported")

    @staticmethod
    def id() -> str:
        return 'sas7bdat'

    @staticmethod
    def is_flatonly() -> bool:
        return True

    @staticmethod
    def has_totals():
        """Has totals indicator"""
        return True

    def totals(self):
        """Returns file totals"""
        if HAS_PYREADSTAT and self.filename:
            df, meta = pyreadstat.read_sas7bdat(self.filename)
            return len(df)
        elif hasattr(self, 'data'):
            return len(self.data)
        return 0

    def read(self) -> dict:
        """Read single SAS record"""
        if HAS_PYREADSTAT:
            row = next(self.iterator)
            self.pos += 1
            # Convert numpy types to Python types
            return {k: (v.item() if hasattr(v, 'item') else v) for k, v in row.items()}
        else:
            row = next(self.iterator)
            self.pos += 1
            return row

    def read_bulk(self, num:int = 10) -> list[dict]:
        """Read bulk SAS records"""
        chunk = []
        for n in range(0, num):
            try:
                chunk.append(self.read())
            except StopIteration:
                break
        return chunk

    def write(self, record:dict):
        """Write single SAS record - not supported"""
        raise NotImplementedError("SAS file writing is not yet supported")

    def write_bulk(self, records:list[dict]):
        """Write bulk SAS records - not supported"""
        raise NotImplementedError("SAS file writing is not yet supported")
