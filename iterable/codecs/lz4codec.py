from __future__ import annotations
import typing
from ..base import BaseCodec

import lz4.frame

class LZ4Codec(BaseCodec):
    def __init__(self, filename:str, compression_level:int = lz4.frame.COMPRESSIONLEVEL_MINHC, mode:str = 'r', open_it:bool = False):
        self.compression_level = compression_level
        super(LZ4Codec, self).__init__(filename, mode=mode, open_it=open_it)

    def open(self) -> bz2.BZ2File:
        self._fileobj = lz4.frame.open(self.filename, mode=self.mode, compression_level=self.compression_level)
        return self._fileobj

    def close(self):
        self._fileobj.close()

    @staticmethod
    def fileexts() -> list[str]:
        return ['lz4',]
