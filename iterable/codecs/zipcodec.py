from __future__ import annotations
import typing
from ..base import BaseCodec

import zipfile

class ZIPCodec(BaseCodec):
    def __init__(self, filename:str, compression_level:int = 5, mode:str = 'r', open_it:bool = False):
        self.compression_level = compression_level
        super(ZIPCodec, self).__init__(filename, mode=mode, open_it=open_it)

    def open(self) -> zipfile.ZipFile:
        self._archiveobj = zipfile.ZipFile(self.filename, mode=self.mode)
        fnames = self._archiveobj.namelist()
        self._fileobj = self._archiveobj.open(fnames[0], self.mode)
        return self._fileobj

    def close(self):
        self._fileobj.close()
        self._archiveobj.close()

    @staticmethod
    def fileexts() -> list[str]:
        return ['zip',]
