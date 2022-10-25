from ..base import BaseCodec

import lzma

LZMA_FILTERS = [
    {"id": lzma.FILTER_DELTA, "dist": 5},
    {"id": lzma.FILTER_LZMA2, "preset": 7 | lzma.PRESET_EXTREME},
]

class LZMACodec(BaseCodec):
    def __init__(self, filename, compression_level=5, mode='r', open_it=False):
        super(LZMACodec, self).__init__(filename, mode=mode, open_it=open_it)
        self.compression_level = compression_level

    def open(self):
        filters = LZMA_FILTERS
        filters[0]['dist'] = self.compression_level
        self._fileobj = lzma.LZMAFile(self.filename, mode=self.mode, format=lzma.FORMAT_XZ)#, filters=filters)
        return self._fileobj

    def close(self):
        self._fileobj.close()



    @staticmethod
    def fileexts():
        return ['xz', 'lzma']
