from json import loads, dumps
import datetime

from ..base import BaseFileIterable

date_handler = lambda obj: (
    obj.isoformat()
    if isinstance(obj, (datetime.datetime, datetime.date))
    else None
)


class JSONLinesIterable(BaseFileIterable):
    def __init__(self, filename=None, stream=None, codec=None, mode='r', encoding='utf8'):
        super(JSONLinesIterable, self).__init__(filename, stream, codec=codec, binary=False, mode=mode, encoding=encoding)
        self.pos = 0
        pass

    @staticmethod
    def id():
        return 'jsonl'

    @staticmethod
    def is_flatonly():
        return False


    def read(self, skip_empty=False):
        """Read single JSON lines record"""
        line = next(self.fobj)
        if skip_empty and len(line) == 0:
            return self.read(skip_empty)
        self.pos += 1
        if line:
            return loads(line)
        return None

    def read_bulk(self, num):
        """Read bulk JSON lines records"""
        chunk = []
        for n in range(0, num):
            chunk.append(loads(self.fobj.readline()))
        return chunk

    def write(self, record):
        """Write single JSON lines record"""
        self.fobj.write(dumps(record, ensure_ascii=False, default=date_handler) + '\n')

    def write_bulk(self, records):
        """Write bulk JSON lines records"""
        for record in records:
            self.fobj.write(dumps(record, ensure_ascii=False, default=date_handler) + '\n')
