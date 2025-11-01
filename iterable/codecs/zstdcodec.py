from __future__ import annotations
import typing
from ..base import BaseCodec

import zstandard as zstd


# Zstandard file object doesn't support file seek so reset rewritten to close and open file

class ZSTDCodec(BaseCodec):
    def __init__(self, filename:str, compression_level:int = 0, mode:str = 'rb', open_it:bool = False, options:dict={}):
        self.compression_level = compression_level
        rmode = 'rb' if mode in ['r', 'rb'] else 'wb'
        super(ZSTDCodec, self).__init__(filename, mode=rmode , open_it=open_it, options=options)

    def open(self) -> zstd.ZstdDecompressionReader:
        self._fileobj = zstd.open(self.filename, mode=self.mode)
        return self._fileobj

    def reset(self):
        self.close()
        self._fileobj = self.open()

    def close(self):
        self._fileobj.close()

    @staticmethod
    def id():
        return 'zst'


    @staticmethod
    def fileexts() -> list[str]:
        return ['zstd', 'zst']
