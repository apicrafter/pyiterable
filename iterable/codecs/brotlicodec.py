from __future__ import annotations
import typing
from ..base import BaseCodec

import brotli_file

BROTLI_DEFAULT_COMPRESSION_LEVEL = 11

class BrotliCodec(BaseCodec):
    def __init__(self, filename:str, compression_level:int = BROTLI_DEFAULT_COMPRESSION_LEVEL, mode:str = 'r', open_it:bool = False, options:dict = {}):
        "Code to support Brotli compression"
        self.compression_level = compression_level
        super(BrotliCodec, self).__init__(filename, mode=mode, open_it=open_it, options=options)

    def open(self) -> brotli_file.BrotliFile:
        self._fileobj = brotli_file.open(self.filename, mode=self.mode, quality=self.compression_level)
        return self._fileobj

    def close(self):
        self._fileobj.close()

    @staticmethod
    def id():
        return 'brotli'

    @staticmethod
    def fileexts() -> list[str]:
        return ['br', 'brotli']
