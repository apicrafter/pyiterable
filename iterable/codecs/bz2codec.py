from __future__ import annotations
import typing
from ..base import BaseCodec

import bz2

class BZIP2Codec(BaseCodec):
    def __init__(self, filename:str, compression_level:int = 5, mode:str = 'r', open_it:bool = False, options:dict = {}):
        self.compression_level = compression_level
        super(BZIP2Codec, self).__init__(filename, mode=mode, open_it=open_it, options=options)

    def open(self) -> bz2.BZ2File:
        self._fileobj = bz2.open(self.filename, self.mode, compresslevel=self.compression_level)
        return self._fileobj

    def close(self):
        self._fileobj.close()

    @staticmethod
    def fileexts() -> list[str]:
        return ['bz2',]
