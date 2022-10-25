from ..base import BaseCodec

import gzip

class GZIPCodec(BaseCodec):
    def __init__(self, filename, compression_level=5, mode='r', open_it=False):
        self.compression_level = compression_level
        super(GZIPCodec, self).__init__(filename, mode=mode, open_it=open_it)

    def open(self):         
        self._fileobj = gzip.GzipFile(filename=self.filename, mode=self.mode, compresslevel=self.compression_level)
        return self._fileobj
 
    def close(self):
        self._fileobj.close()

    @staticmethod
    def fileexts():
        return ['gz',]
