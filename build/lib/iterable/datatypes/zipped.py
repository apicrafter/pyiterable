from zipfile import ZipFile

from .base import BaseSource


class ZIPSourceWrapper(BaseSource):
    def __init__(self, filename, binary=False):
        super(ZIPSourceWrapper, self).__init__()
        self.fobj = ZipFile(filename, mode='r')
        self.filenames = self.fobj.namelist()
        self.filenum = 0
        self.filepos = 0
        self.globalpos = 0
        self.mode = 'rb' if binary else 'r'
        self.current_file = self.fobj.open(self.filenames[self.filenum], mode=self.mode)
        pass

    def close(self):
        if self.current_file:
            self.current_file.close()
            self.current_file = None
        self.fobj.close()

    def iterfile(self):
        if self.current_file:
            self.current_file.close()
        if self.filenum < len(self.filenames) - 1:
            self.filenum += 1
            filename = self.filenames[self.filenum]
            self.current_file = self.fobj.open(filename, mode=self.mode)
            self.filepos = 0
            return True
        else:
            return False

    def read(self):
        """Read single record"""
        try:
            row = self.read_single()
            return row
        except StopIteration as e:
            if self.iterfile():
                row = self.read_single()
                return row
            else:
                raise StopIteration

    def __iter__(self):
        self.filenum = 0
        filename = self.filenames[self.filenum]
        self.current_file = self.fobj.open(filename, mode=self.mode)
        return self

    def read_single(self):
        """Not implemented single record read"""
        raise NotImplementedError

    def read_bulk(self, num):
        """Read bulk records"""
        chunk = []
        n = 0
        while n < num:
            n += 1
            try:
                chunk.append(self.read())
            except StopIteration:
                return chunk
        return chunk
