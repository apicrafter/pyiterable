from __future__ import annotations

import zstandard as zstd

from ..base import BaseCodec

# Zstandard file object doesn't support file seek so reset rewritten to close and open file


class ZSTDCodec(BaseCodec):
    def __init__(
        self, filename: str, compression_level: int = 0, mode: str = "rb", open_it: bool = False, options: dict = None
    ):
        if options is None:
            options = {}
        self.compression_level = compression_level
        rmode = "rb" if mode in ["r", "rb"] else "wb"
        super().__init__(filename, mode=rmode, open_it=open_it, options=options)

    def open(self) -> zstd.ZstdDecompressionReader:
        # If fileobj was provided (e.g., from cloud storage), use it
        if self._fileobj is not None:
            # fileobj provided, use zstd to wrap it
            # Store original for potential reset operations
            if not hasattr(self, "_original_fileobj"):
                self._original_fileobj = self._fileobj
            if "r" in self.mode or "rb" in self.mode:
                # Reading: create decompression reader
                dctx = zstd.ZstdDecompressor()
                self._fileobj = dctx.stream_reader(self._original_fileobj)
            else:
                # Writing: create compression writer
                cctx = zstd.ZstdCompressor(level=self.compression_level)
                self._fileobj = cctx.stream_writer(self._original_fileobj)
        elif self.filename is not None:
            # Open from filename as usual
            self._fileobj = zstd.open(self.filename, mode=self.mode)
        else:
            raise ValueError("ZSTDCodec requires either filename or fileobj")
        return self._fileobj

    def reset(self):
        self.close()
        self._fileobj = self.open()

    def close(self):
        self._fileobj.close()

    @staticmethod
    def id():
        return "zst"

    @staticmethod
    def fileexts() -> list[str]:
        return ["zstd", "zst"]
