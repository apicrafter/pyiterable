from __future__ import annotations
import typing
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

from ..base import BaseFileIterable, BaseCodec


class YAMLIterable(BaseFileIterable):
    def __init__(self, filename:str = None, stream:typing.IO = None, codec: BaseCodec = None, mode:str='r', encoding:str = 'utf8', options:dict={}):
        if not HAS_YAML:
            raise ImportError("YAML support requires 'pyyaml' package")
        super(YAMLIterable, self).__init__(filename, stream, codec=codec, binary=False, mode=mode, encoding=encoding, options=options)
        self.reset()
        pass

    def reset(self):
        """Reset iterable"""
        super(YAMLIterable, self).reset()
        self.pos = 0
        if self.mode == 'r':
            # YAML can have multiple documents separated by ---
            self.documents = list(yaml.safe_load_all(self.fobj))
            self.current_doc = 0
            self.current_pos = 0
            # If documents are lists, iterate over items; otherwise treat as single-item lists
            self.data = []
            for doc in self.documents:
                if doc is None:
                    continue  # Skip empty documents
                if isinstance(doc, list):
                    self.data.extend(doc)
                elif isinstance(doc, dict):
                    self.data.append(doc)
                else:
                    self.data.append({'value': doc})
        else:
            self.data = []

    @staticmethod
    def id() -> str:
        return 'yaml'

    @staticmethod
    def is_flatonly() -> bool:
        return False

    def read(self) -> dict:
        """Read single YAML record"""
        if self.pos >= len(self.data):
            raise StopIteration
        row = self.data[self.pos]
        self.pos += 1
        return row

    def read_bulk(self, num:int = 10) -> list[dict]:
        """Read bulk YAML records"""
        chunk = []
        for n in range(0, num):
            try:
                chunk.append(self.read())
            except StopIteration:
                break
        return chunk

    def write(self, record:dict):
        """Write single YAML record"""
        yaml.dump(record, self.fobj, default_flow_style=False, allow_unicode=True)
        self.fobj.write('---\n')

    def write_bulk(self, records:list[dict]):
        """Write bulk YAML records"""
        for record in records:
            yaml.dump(record, self.fobj, default_flow_style=False, allow_unicode=True)
            self.fobj.write('---\n')
