from __future__ import annotations
import typing
try:
    import cbor2
    HAS_CBOR2 = True
except ImportError:
    try:
        import cbor
        HAS_CBOR = True
        HAS_CBOR2 = False
    except ImportError:
        HAS_CBOR = False
        HAS_CBOR2 = False

from ..base import BaseFileIterable, BaseCodec


class CBORIterable(BaseFileIterable):
    datamode = 'binary'
    def __init__(self, filename:str = None, stream:typing.IO = None, codec: BaseCodec = None, mode:str='r', options:dict={}):
        if not HAS_CBOR2 and not HAS_CBOR:
            raise ImportError("CBOR support requires 'cbor2' or 'cbor' package")
        super(CBORIterable, self).__init__(filename, stream, codec=codec, binary=True, mode=mode, options=options)
        self.reset()
        pass

    def reset(self):
        """Reset iterable"""
        super(CBORIterable, self).reset()
        self.pos = 0
        if self.mode == 'r':
            # For reading, CBOR files typically contain a single object or array
            # We'll read the entire file and iterate over it
            if HAS_CBOR2:
                try:
                    # Try to seek to beginning
                    if hasattr(self.fobj, 'seek'):
                        self.fobj.seek(0)
                    # Read all data
                    data = self.fobj.read()
                    if len(data) == 0:
                        self.iterator = iter([])
                    else:
                        # Decode CBOR data
                        self.data = cbor2.loads(data)
                        if isinstance(self.data, list):
                            self.iterator = iter(self.data)
                        else:
                            # Single object, wrap in list
                            self.iterator = iter([self.data])
                except Exception as e:
                    # If reading fails, create empty iterator
                    self.iterator = iter([])
            else:
                # cbor library doesn't have a streaming decoder, so we'll read all at once
                try:
                    if hasattr(self.fobj, 'seek'):
                        self.fobj.seek(0)
                    self.data = cbor.load(self.fobj)
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
        return 'cbor'

    @staticmethod
    def is_flatonly() -> bool:
        return False

    def read(self) -> dict:
        """Read single CBOR record"""
        try:
            row = next(self.iterator)
            self.pos += 1
            return row
        except (StopIteration, EOFError, ValueError):
            raise StopIteration

    def read_bulk(self, num:int = 10) -> list[dict]:
        """Read bulk CBOR records"""
        chunk = []
        for n in range(0, num):
            try:
                chunk.append(self.read())
            except StopIteration:
                break
        return chunk

    def write(self, record:dict):
        """Write single CBOR record"""
        if HAS_CBOR2:
            encoded = cbor2.dumps(record)
            self.fobj.write(encoded)
        else:
            cbor.dump(record, self.fobj)

    def write_bulk(self, records:list[dict]):
        """Write bulk CBOR records"""
        for record in records:
            self.write(record)
