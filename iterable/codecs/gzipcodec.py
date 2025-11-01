from __future__ import annotations
import typing
from ..base import BaseCodec

import gzip

class GZIPCodec(BaseCodec):
    def __init__(self, filename:str, compression_level:int = 5, mode:str = 'r', open_it:bool = False, options:dict = {}):
        self.compression_level = compression_level
        super(GZIPCodec, self).__init__(filename, mode=mode, open_it=open_it, options=options)

    def open(self) -> gzip.GzipFile:         
        self._fileobj = gzip.GzipFile(filename=self.filename, mode=self.mode, compresslevel=self.compression_level)
        return self._fileobj
 
    def close(self):
        self._fileobj.close()

    @staticmethod
    def id():
        return 'gzip'


    @staticmethod
    def fileexts() -> list[str]:
        return ['gz',]
