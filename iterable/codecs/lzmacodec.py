from __future__ import annotations
import typing
from ..base import BaseCodec

import lzma

LZMA_FILTERS = [
    {"id": lzma.FILTER_DELTA, "dist": 5},
    {"id": lzma.FILTER_LZMA2, "preset": 7 | lzma.PRESET_EXTREME},
]

class LZMACodec(BaseCodec):
    def __init__(self, filename:str, compression_level:int = 5, mode:str = 'r', open_it:bool = False, options:dict = {}):
        self.compression_level = compression_level
        super(LZMACodec, self).__init__(filename, mode=mode, open_it=open_it, options=options)

    def open(self) -> lzma.LZMAFile:
        filters = LZMA_FILTERS
        filters[0]['dist'] = self.compression_level
        self._fileobj = lzma.LZMAFile(self.filename, mode=self.mode, format=lzma.FORMAT_XZ)#, filters=filters)
        return self._fileobj


    def reset(self):
        if self.mode in ['w', 'wb']:
            pass
        else:
            super(LZMACodec, self).reset()

    def close(self):
        self._fileobj.close()

    @staticmethod
    def id():
        return 'xz'
        
    @staticmethod
    def fileexts() -> list[str]:
        return ['xz', 'lzma']
