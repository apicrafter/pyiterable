from __future__ import annotations
import typing
from ..base import BaseCodec

try:
    import py7zr
    HAS_PY7ZR = True
except ImportError:
    HAS_PY7ZR = False
    py7zr = None

class SZipCodec(BaseCodec):
    def __init__(self, filename:str, compression_level:int = 5, mode:str = 'r', open_it:bool = False):
        self.compression_level = compression_level            
        if mode == 'rb':
            mode = 'r'
            self.filemode = 'rb'        
        else:
            self.filemode = 'r'
        super(SZipCodec, self).__init__(filename, mode=mode, open_it=open_it)

    def open(self):        
        self._archiveobj = py7zr.SevenZipFile(self.filename, mode=self.mode)
        fnames = self._archiveobj.getnames()
       
        self._fileobj = self._archiveobj.open(fnames[0], self.filemode)
        return self._fileobj

    def close(self):
        self._fileobj.close()
        self._archiveobj.close()

    @staticmethod
    def fileexts() -> list[str]:
        return ['7z',]
