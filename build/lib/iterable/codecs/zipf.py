from ..base import BaseCodec

import zipfile

class ZIPCodec(BaseCodec):
    def __init__(self, filename, compression_level=5, mode='r'):
        super(ZIPCodec, self).__init__(filename)
        self.compression_level = compression_level
        self.mode = mode

    def open(self):
        self._archiveobj = ZipFile(filename, mode='r')
        fnames = self.archiveobj.namelist()
        self._fileobj = self._archiveobj.open(fnames[0], self.mode)

    def close(self):
        self._fileobj.close()
        self._archiveobj.close()


    @staticmethod
    def fileexts():
        return ['zip',]
