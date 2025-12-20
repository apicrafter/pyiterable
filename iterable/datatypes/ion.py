from __future__ import annotations
import typing
try:
    import ion
    HAS_ION = True
except ImportError:
    HAS_ION = False

from ..base import BaseFileIterable, BaseCodec


class IonIterable(BaseFileIterable):
    datamode = 'binary'
    def __init__(self, filename:str = None, stream:typing.IO = None, codec: BaseCodec = None, mode:str='r', options:dict={}):
        if not HAS_ION:
            raise ImportError("Ion format support requires 'ion-python' package")
        super(IonIterable, self).__init__(filename, stream, codec=codec, binary=True, mode=mode, options=options)
        self.reset()
        pass

    def reset(self):
        """Reset iterable"""
        super(IonIterable, self).reset()
        self.pos = 0
        if self.mode == 'r':
            # Read Ion data
            data = self.fobj.read()
            self.iterator = iter(ion.loads(data, single_value=False))
        else:
            self.buffer = []

    @staticmethod
    def id() -> str:
        return 'ion'

    @staticmethod
    def is_flatonly() -> bool:
        return False

    def read(self) -> dict:
        """Read single Ion record"""
        value = next(self.iterator)
        self.pos += 1
        # Convert Ion value to dict
        if isinstance(value, dict):
            return value
        elif isinstance(value, list):
            # If it's a list, convert to dict with index
            return {str(i): v for i, v in enumerate(value)}
        else:
            return {'value': value}

    def read_bulk(self, num:int = 10) -> list[dict]:
        """Read bulk Ion records"""
        chunk = []
        for n in range(0, num):
            try:
                chunk.append(self.read())
            except StopIteration:
                break
        return chunk

    def write(self, record:dict):
        """Write single Ion record"""
        self.write_bulk([record, ])

    def write_bulk(self, records:list[dict]):
        """Write bulk Ion records"""
        for record in records:
            ion_data = ion.dumps(record)
            self.fobj.write(ion_data)
