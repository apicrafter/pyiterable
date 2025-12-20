from __future__ import annotations
import typing
try:
    import tomli
    import tomli_w
    HAS_TOMLI = True
except ImportError:
    try:
        import toml
        HAS_TOML = True
        HAS_TOMLI = False
    except ImportError:
        HAS_TOML = False
        HAS_TOMLI = False

from ..base import BaseFileIterable, BaseCodec


class TOMLIterable(BaseFileIterable):
    def __init__(self, filename:str = None, stream:typing.IO = None, codec: BaseCodec = None, mode:str='r', encoding:str = 'utf8', options:dict={}):
        if not HAS_TOMLI and not HAS_TOML:
            raise ImportError("TOML support requires either 'tomli' and 'tomli-w' or 'toml' package")
        super(TOMLIterable, self).__init__(filename, stream, codec=codec, binary=False, mode=mode, encoding=encoding, options=options)
        self.reset()
        pass

    def reset(self):
        """Reset iterable"""
        super(TOMLIterable, self).reset()
        self.pos = 0
        if self.mode == 'r':
            data_str = self.fobj.read()
            if HAS_TOMLI:
                self.data = tomli.loads(data_str)
            else:
                self.data = toml.loads(data_str)
            
            # TOML files typically contain tables/arrays of tables
            # Try to find array of tables or convert top-level to list
            if isinstance(self.data, dict):
                # Look for array of tables (common pattern)
                self.items = []
                for key, value in self.data.items():
                    if isinstance(value, list):
                        # Array of tables
                        for item in value:
                            item_copy = item.copy()
                            item_copy['_table'] = key
                            self.items.append(item_copy)
                    elif isinstance(value, dict):
                        # Single table
                        value_copy = value.copy()
                        value_copy['_table'] = key
                        self.items.append(value_copy)
                    else:
                        # Scalar value
                        self.items.append({key: value})
            else:
                self.items = self.data if isinstance(self.data, list) else [self.data]
            
            self.iterator = iter(self.items)

    @staticmethod
    def id() -> str:
        return 'toml'

    @staticmethod
    def is_flatonly() -> bool:
        return False

    def read(self) -> dict:
        """Read single TOML record"""
        row = next(self.iterator)
        self.pos += 1
        return row

    def read_bulk(self, num:int = 10) -> list[dict]:
        """Read bulk TOML records"""
        chunk = []
        for n in range(0, num):
            try:
                chunk.append(self.read())
            except StopIteration:
                break
        return chunk

    def write(self, record:dict):
        """Write single TOML record"""
        self.write_bulk([record, ])

    def write_bulk(self, records:list[dict]):
        """Write bulk TOML records"""
        # Convert records to TOML format
        if HAS_TOMLI:
            toml_str = tomli_w.dumps(records)
        else:
            toml_str = toml.dumps(records)
        self.fobj.write(toml_str)
