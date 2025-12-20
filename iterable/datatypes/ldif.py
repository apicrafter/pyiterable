from __future__ import annotations
import typing
try:
    import ldif3
    HAS_LDIF3 = True
except ImportError:
    try:
        import ldif
        HAS_LDIF = True
        HAS_LDIF3 = False
    except ImportError:
        HAS_LDIF = False
        HAS_LDIF3 = False

from ..base import BaseFileIterable, BaseCodec


class LDIFIterable(BaseFileIterable):
    def __init__(self, filename:str = None, stream:typing.IO = None, codec: BaseCodec = None, mode:str='r', encoding:str = 'utf8', options:dict={}):
        if not HAS_LDIF3 and not HAS_LDIF:
            raise ImportError("LDIF support requires 'ldif3' or 'ldif' package")
        super(LDIFIterable, self).__init__(filename, stream, codec=codec, binary=False, mode=mode, encoding=encoding, options=options)
        self.reset()
        pass

    def reset(self):
        """Reset iterable"""
        super(LDIFIterable, self).reset()
        self.pos = 0
        if self.mode == 'r':
            self.entries = []
            current_entry = {}
            current_dn = None
            
            for line in self.fobj:
                line = line.rstrip('\n\r')
                
                if line == '':
                    # Empty line indicates end of entry
                    if current_dn and current_entry:
                        current_entry['dn'] = current_dn
                        self.entries.append(current_entry)
                    current_entry = {}
                    current_dn = None
                    continue
                
                if line.startswith(' ') or line.startswith('\t'):
                    # Continuation line
                    if current_entry and current_entry.get('_last_attr'):
                        current_entry[current_entry['_last_attr']] += line[1:]
                    continue
                
                if ':' in line:
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        attr_name = parts[0].strip()
                        attr_value = parts[1].strip()
                        
                        if attr_name.lower() == 'dn':
                            current_dn = attr_value
                        else:
                            # Handle multi-valued attributes
                            if attr_name in current_entry:
                                if not isinstance(current_entry[attr_name], list):
                                    current_entry[attr_name] = [current_entry[attr_name]]
                                current_entry[attr_name].append(attr_value)
                            else:
                                current_entry[attr_name] = attr_value
                            current_entry['_last_attr'] = attr_name
            
            # Add last entry if file doesn't end with newline
            if current_dn and current_entry:
                current_entry['dn'] = current_dn
                self.entries.append(current_entry)
            
            # Clean up temporary keys
            for entry in self.entries:
                entry.pop('_last_attr', None)
            
            self.iterator = iter(self.entries)
        else:
            self.entries = []

    @staticmethod
    def id() -> str:
        return 'ldif'

    @staticmethod
    def is_flatonly() -> bool:
        return False

    def read(self) -> dict:
        """Read single LDIF record"""
        row = next(self.iterator)
        self.pos += 1
        return row

    def read_bulk(self, num:int = 10) -> list[dict]:
        """Read bulk LDIF records"""
        chunk = []
        for n in range(0, num):
            try:
                chunk.append(self.read())
            except StopIteration:
                break
        return chunk

    def write(self, record:dict):
        """Write single LDIF record"""
        if 'dn' not in record:
            raise ValueError("LDIF entry must have 'dn' field")
        
        self.fobj.write(f"dn: {record['dn']}\n")
        for key, value in record.items():
            if key == 'dn':
                continue
            if isinstance(value, list):
                for v in value:
                    self.fobj.write(f"{key}: {v}\n")
            else:
                self.fobj.write(f"{key}: {value}\n")
        self.fobj.write("\n")

    def write_bulk(self, records:list[dict]):
        """Write bulk LDIF records"""
        for record in records:
            self.write(record)
