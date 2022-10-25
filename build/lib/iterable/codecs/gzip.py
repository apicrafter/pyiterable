from ..base import BaseCodec

import gzip

class GZIPCodec(BaseCodec):
    def __init__(self, filename, compression_level=5, mode='r'):
        super(GZIPCodec, self).__init__(filename)
        self.compression_level = compression_level
        self.mode = mode

    def open(self):
        self._fileobj = gzip.open(self.filename, self.mode, compressLevel=self.compression_level)

    def close(self):
        self._fileobj.close()

    @staticmethod
    def fileexts():
        return ['gz',]
