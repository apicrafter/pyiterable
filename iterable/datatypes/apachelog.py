from __future__ import annotations
import typing
import re
from ..base import BaseFileIterable, BaseCodec


class ApacheLogIterable(BaseFileIterable):
    datamode = 'text'
    def __init__(self, filename:str = None, stream:typing.IO = None, codec: BaseCodec = None, mode:str='r', log_format:str = 'common', options:dict={}):
        # Check log format before opening file
        self.log_format = log_format
        if 'log_format' in options:
            self.log_format = options['log_format']
        
        # Define log format patterns
        self.patterns = {
            'common': r'(\S+) (\S+) (\S+) \[([^\]]+)\] "(\S+) (\S+) (\S+)" (\d+) (\S+)',
            'combined': r'(\S+) (\S+) (\S+) \[([^\]]+)\] "(\S+) (\S+) (\S+)" (\d+) (\S+) "([^"]*)" "([^"]*)"',
            'vhost_common': r'(\S+) (\S+) \[([^\]]+)\] "(\S+) (\S+) (\S+)" (\d+) (\S+)',
        }
        
        self.field_names = {
            'common': ['remote_host', 'remote_logname', 'remote_user', 'time', 'method', 'request', 'protocol', 'status', 'size'],
            'combined': ['remote_host', 'remote_logname', 'remote_user', 'time', 'method', 'request', 'protocol', 'status', 'size', 'referer', 'user_agent'],
            'vhost_common': ['remote_host', 'remote_logname', 'time', 'method', 'request', 'protocol', 'status', 'size'],
        }
        
        if self.log_format not in self.patterns:
            raise ValueError(f"Unknown log format: {self.log_format}. Supported: {', '.join(self.patterns.keys())}")
        
        super(ApacheLogIterable, self).__init__(filename, stream, codec=codec, binary=False, mode=mode, options=options)
        
        self.pattern = re.compile(self.patterns[self.log_format])
        self.keys = self.field_names[self.log_format]
        self.reset()
        pass

    def reset(self):
        """Reset iterable"""
        super(ApacheLogIterable, self).reset()
        self.pos = 0
        # File is already opened by parent class

    @staticmethod
    def has_totals():
        """Has totals indicator"""
        return True        

    def totals(self):
        """Returns file totals"""
        from ..helpers.utils import rowincount
        return rowincount(self.filename, self.fobj)

    @staticmethod
    def id() -> str:
        return 'apachelog'

    @staticmethod
    def is_flatonly() -> bool:
        return True

    def read(self, skip_empty:bool = True) -> dict:
        """Read single Apache log record"""
        while True:
            line = self.fobj.readline()
            if not line:
                raise StopIteration
            
            line = line.strip()
            if skip_empty and len(line) == 0:
                continue
            
            # Parse log line
            match = self.pattern.match(line)
            if match:
                values = match.groups()
                result = dict(zip(self.keys, values))
                self.pos += 1
                return result
            else:
                # If line doesn't match, return as raw line
                if not skip_empty:
                    return {'raw_line': line}
                # Otherwise skip and continue
                continue

    def read_bulk(self, num:int = 10) -> list[dict]:
        """Read bulk Apache log records"""
        chunk = []
        for n in range(0, num):
            try:
                chunk.append(self.read())
            except StopIteration:
                break
        return chunk

    def write(self, record:dict):
        """Write single Apache log record"""
        # Reconstruct log line from dict
        if self.log_format == 'common':
            line = f'{record.get("remote_host", "-")} {record.get("remote_logname", "-")} {record.get("remote_user", "-")} [{record.get("time", "-")}] "{record.get("method", "-")} {record.get("request", "-")} {record.get("protocol", "-")}" {record.get("status", "-")} {record.get("size", "-")}\n'
        elif self.log_format == 'combined':
            line = f'{record.get("remote_host", "-")} {record.get("remote_logname", "-")} {record.get("remote_user", "-")} [{record.get("time", "-")}] "{record.get("method", "-")} {record.get("request", "-")} {record.get("protocol", "-")}" {record.get("status", "-")} {record.get("size", "-")} "{record.get("referer", "-")}" "{record.get("user_agent", "-")}"\n'
        else:
            # Generic format
            line = ' '.join([str(record.get(key, '-')) for key in self.keys]) + '\n'
        self.fobj.write(line)

    def write_bulk(self, records: list[dict]):
        """Write bulk Apache log records"""
        for record in records:
            self.write(record)
