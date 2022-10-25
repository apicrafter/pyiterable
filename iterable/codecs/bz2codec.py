from ..base import BaseCodec

import bz2

class BZIP2Codec(BaseCodec):
    def __init__(self, filename, compression_level=5, mode='r', open_it=False):
        self.compression_level = compression_level
        super(BZIP2Codec, self).__init__(filename, mode=mode, open_it=open_it)

    def open(self):
        self._fileobj = bz2.open(self.filename, self.mode, compresslevel=self.compression_level)
        return self._fileobj

    def close(self):
        self._fileobj.close()

    @staticmethod
    def fileexts():
        return ['bz2',]
