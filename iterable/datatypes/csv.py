from csv import DictReader, DictWriter

from ..base import BaseFileIterable


class CSVIterable(BaseFileIterable):
    def __init__(self, filename=None, stream=None, codec=None, keys=None, delimiter=',', quotechar='"', mode='r', encoding=None):
        super(CSVIterable, self).__init__(filename, stream, codec=codec, binary=False, encoding=encoding, mode=mode)
        self.delimiter = delimiter
        self.quotechar = quotechar
        self.keys = keys
        self.reset()
        pass

    def reset(self):
        super(CSVIterable, self).reset()
        if self.fobj is None and self.codec is not None:
            fobj = self.codec.textIO(self.encoding)
        else:
            fobj = self.fobj

        self.reader = None
        if self.mode == 'r':
            if self.keys is not None:
                 self.reader = DictReader(fobj, fieldnames=self.keys, delimiter=self.delimiter,
                                     quotechar=self.quotechar)                
            else:
                 self.reader = DictReader(fobj, delimiter=self.delimiter, quotechar=self.quotechar)
        if self.mode in ['w', 'wr'] and self.keys:
            self.writer = DictWriter(fobj, fieldnames=self.keys, delimiter=self.delimiter, quotechar=self.quotechar)
            self.writer.writeheader()
        else:
            self.writer = None

        #            self.reader = reader(self.fobj, delimiter=self.delimiter, quotechar=self.quotechar)
        self.pos = 0

    @staticmethod
    def id():
        return 'csv'

    @staticmethod
    def is_flatonly():
        return True

    def read(self, skip_empty=True):
        """Read single CSV record"""
        row = next(self.reader)
        if skip_empty and len(row) == 0:
            return self.read(skip_empty)
        self.pos += 1
        return row

    def read_bulk(self, num=10):
        """Read bulk CSV records"""
        chunk = []
        for n in range(0, num):
            chunk.append(next(self.reader))
            self.pos += 1
        return chunk

    def write(self, record):
        """Write single CSV record"""
        self.writer.writerow(record)

    def write_bulk(self, records):
        """Write bulk CSV records"""
        self.writer.writerows(records)
