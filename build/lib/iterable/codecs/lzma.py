from ..base import BaseCodec

from lzma import LZMAFile

LZMA_FILTERS = [
    {"id": lzma.FILTER_DELTA, "dist": 5},
    {"id": lzma.FILTER_LZMA2, "preset": 7 | lzma.PRESET_EXTREME},
]

class LZMACodec(BaseCodec):
    def __init__(self, filename, compression_level=5, mode='r'):
        super(XZCodec, self).__init__(filename)
        self.compression_level = compression_level
        self.mode = mode

    def open(self):
        filters = LZMA_FILTERS
        filters[0]['dist'] = compression_level
        self._fileobj = LZMAFile(self.filename, self.mode, filters=filters)

    def close(self):
        self._fileobj.close()

    @staticmethod
    def fileexts():
        return ['xz', 'lzma']
