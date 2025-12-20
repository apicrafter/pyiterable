from __future__ import annotations
import typing
try:
    import ubjson
    HAS_UBJSON = True
except ImportError:
    HAS_UBJSON = False

from ..base import BaseFileIterable, BaseCodec


class UBJSONIterable(BaseFileIterable):
    datamode = 'binary'
    def __init__(self, filename:str = None, stream:typing.IO = None, codec: BaseCodec = None, mode:str='r', options:dict={}):
        if not HAS_UBJSON:
            raise ImportError("UBJSON support requires 'py-ubjson' package")
        super(UBJSONIterable, self).__init__(filename, stream, codec=codec, binary=True, mode=mode, options=options)
        self.reset()
        pass

    def reset(self):
        """Reset iterable"""
        super(UBJSONIterable, self).reset()
        self.pos = 0
        if self.mode == 'r':
            try:
                if hasattr(self.fobj, 'seek'):
                    self.fobj.seek(0)
                # Read all data
                data = self.fobj.read()
                if len(data) == 0:
                    self.iterator = iter([])
                else:
                    # Decode UBJSON data
                    self.data = ubjson.loadb(data)
                    if isinstance(self.data, list):
                        self.iterator = iter(self.data)
                    else:
                        # Single object, wrap in list
                        self.iterator = iter([self.data])
            except Exception:
                self.iterator = iter([])
        else:
            # Write mode - no initialization needed
            pass

    @staticmethod
    def id() -> str:
        return 'ubjson'

    @staticmethod
    def is_flatonly() -> bool:
        return False

    def read(self) -> dict:
        """Read single UBJSON record"""
        try:
            row = next(self.iterator)
            self.pos += 1
            return row
        except (StopIteration, EOFError, ValueError):
            raise StopIteration

    def read_bulk(self, num:int = 10) -> list[dict]:
        """Read bulk UBJSON records"""
        chunk = []
        for n in range(0, num):
            try:
                chunk.append(self.read())
            except StopIteration:
                break
        return chunk

    def write(self, record:dict):
        """Write single UBJSON record"""
        encoded = ubjson.dumpb(record)
        self.fobj.write(encoded)

    def write_bulk(self, records:list[dict]):
        """Write bulk UBJSON records"""
        for record in records:
            self.write(record)
