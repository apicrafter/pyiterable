from __future__ import annotations
import typing
try:
    import flexbuffers
    HAS_FLEXBUFFERS = True
except ImportError:
    HAS_FLEXBUFFERS = False

from ..base import BaseFileIterable, BaseCodec


class FlexBuffersIterable(BaseFileIterable):
    datamode = 'binary'
    def __init__(self, filename:str = None, stream:typing.IO = None, codec: BaseCodec = None, mode:str='r', options:dict={}):
        if not HAS_FLEXBUFFERS:
            raise ImportError("FlexBuffers support requires 'flexbuffers' package")
        super(FlexBuffersIterable, self).__init__(filename, stream, codec=codec, mode=mode, binary=True, options=options)
        self.reset()
        pass

    def reset(self):
        """Reset iterable"""
        super(FlexBuffersIterable, self).reset()
        self.pos = 0
        if self.mode == 'r':
            content = self.fobj.read()
            
            try:
                # Try to decode as single document
                data = flexbuffers.load(content)
                if isinstance(data, list):
                    self.items = data
                elif isinstance(data, dict):
                    self.items = [data]
                else:
                    self.items = [{'value': data}]
            except:
                # If single document fails, try to parse as array
                self.items = []
                try:
                    data = flexbuffers.load(content)
                    if isinstance(data, list):
                        self.items = data
                    else:
                        self.items = [{'value': data}]
                except:
                    # If all parsing fails, create empty list
                    self.items = []
            
            self.iterator = iter(self.items)
        else:
            self.items = []

    @staticmethod
    def id() -> str:
        return 'flexbuffers'

    @staticmethod
    def is_flatonly() -> bool:
        return False

    def read(self) -> dict:
        """Read single FlexBuffers record"""
        row = next(self.iterator)
        self.pos += 1
        
        if isinstance(row, dict):
            return row
        else:
            return {'value': row}

    def read_bulk(self, num:int = 10) -> list[dict]:
        """Read bulk FlexBuffers records"""
        chunk = []
        for n in range(0, num):
            try:
                chunk.append(self.read())
            except StopIteration:
                break
        return chunk

    def write(self, record:dict):
        """Write single FlexBuffers record"""
        flexbuffers_data = flexbuffers.dump(record)
        self.fobj.write(flexbuffers_data)

    def write_bulk(self, records:list[dict]):
        """Write bulk FlexBuffers records"""
        for record in records:
            self.write(record)
