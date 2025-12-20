from __future__ import annotations
import typing
try:
    import edn_format
    HAS_EDN_FORMAT = True
except ImportError:
    try:
        import pyedn
        HAS_PYEDN = True
        HAS_EDN_FORMAT = False
    except ImportError:
        HAS_PYEDN = False
        HAS_EDN_FORMAT = False

from ..base import BaseFileIterable, BaseCodec


class EDNIterable(BaseFileIterable):
    def __init__(self, filename:str = None, stream:typing.IO = None, codec: BaseCodec = None, mode:str='r', encoding:str = 'utf8', options:dict={}):
        if not HAS_EDN_FORMAT and not HAS_PYEDN:
            raise ImportError("EDN support requires 'edn_format' or 'pyedn' package")
        super(EDNIterable, self).__init__(filename, stream, codec=codec, binary=False, mode=mode, encoding=encoding, options=options)
        self.reset()
        pass

    def reset(self):
        """Reset iterable"""
        super(EDNIterable, self).reset()
        self.pos = 0
        if self.mode == 'r':
            content = self.fobj.read()
            
            if HAS_EDN_FORMAT:
                # edn_format library
                try:
                    data = edn_format.loads(content)
                    if isinstance(data, list):
                        self.items = data
                    elif isinstance(data, dict):
                        self.items = [data]
                    else:
                        self.items = [{'value': data}]
                except:
                    # Try parsing multiple EDN values
                    self.items = []
                    for line in content.split('\n'):
                        line = line.strip()
                        if line:
                            try:
                                item = edn_format.loads(line)
                                if isinstance(item, dict):
                                    self.items.append(item)
                                else:
                                    self.items.append({'value': item})
                            except:
                                pass
            else:
                # pyedn library
                try:
                    data = pyedn.read(content)
                    if isinstance(data, list):
                        self.items = data
                    elif isinstance(data, dict):
                        self.items = [data]
                    else:
                        self.items = [{'value': data}]
                except:
                    # Try parsing multiple EDN values
                    self.items = []
                    for line in content.split('\n'):
                        line = line.strip()
                        if line:
                            try:
                                item = pyedn.read(line)
                                if isinstance(item, dict):
                                    self.items.append(item)
                                else:
                                    self.items.append({'value': item})
                            except:
                                pass
            
            self.iterator = iter(self.items)
        else:
            self.items = []

    @staticmethod
    def id() -> str:
        return 'edn'

    @staticmethod
    def is_flatonly() -> bool:
        return False

    def _convert_to_dict(self, obj):
        """Convert EDN object to Python dict"""
        if isinstance(obj, dict):
            return {str(k): self._convert_to_dict(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_to_dict(item) for item in obj]
        elif hasattr(obj, '__dict__'):
            return {str(k): self._convert_to_dict(v) for k, v in obj.__dict__.items()}
        else:
            return obj

    def read(self) -> dict:
        """Read single EDN record"""
        row = next(self.iterator)
        self.pos += 1
        
        # Convert to dict if needed
        if isinstance(row, dict):
            return row
        else:
            return self._convert_to_dict(row)

    def read_bulk(self, num:int = 10) -> list[dict]:
        """Read bulk EDN records"""
        chunk = []
        for n in range(0, num):
            try:
                chunk.append(self.read())
            except StopIteration:
                break
        return chunk

    def write(self, record:dict):
        """Write single EDN record"""
        if HAS_EDN_FORMAT:
            edn_str = edn_format.dumps(record)
        else:
            edn_str = pyedn.write(record)
        self.fobj.write(edn_str + '\n')

    def write_bulk(self, records:list[dict]):
        """Write bulk EDN records"""
        for record in records:
            self.write(record)
