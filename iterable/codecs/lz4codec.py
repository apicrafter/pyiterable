from __future__ import annotations

import lz4.frame

from ..base import BaseCodec


class LZ4Codec(BaseCodec):
    def __init__(
        self,
        filename: str,
        compression_level: int = lz4.frame.COMPRESSIONLEVEL_MINHC,
        mode: str = "r",
        open_it: bool = False,
        options: dict = None,
    ):
        if options is None:
            options = {}
        self.compression_level = compression_level
        super().__init__(filename, mode=mode, open_it=open_it, options=options)

    def open(self) -> lz4.frame.LZ4FrameFile:
        self._fileobj = lz4.frame.open(self.filename, mode=self.mode, compression_level=self.compression_level)
        return self._fileobj

    def close(self):
        self._fileobj.close()

    @staticmethod
    def id():
        return "lz4"

    @staticmethod
    def fileexts() -> list[str]:
        return [
            "lz4",
        ]
