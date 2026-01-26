from __future__ import annotations

import gzip

from ..base import BaseCodec


class GZIPCodec(BaseCodec):
    def __init__(
        self, filename: str, compression_level: int = 5, mode: str = "r", open_it: bool = False, options: dict = None
    ):
        if options is None:
            options = {}
        self.compression_level = compression_level
        super().__init__(filename, mode=mode, open_it=open_it, options=options)

    def open(self) -> gzip.GzipFile:
        # If fileobj was provided (e.g., from cloud storage), wrap it with GzipFile
        # Store original fileobj if it's a raw stream (not already a GzipFile)
        if self._fileobj is not None and not isinstance(self._fileobj, gzip.GzipFile):
            # fileobj provided, wrap it with GzipFile
            # Store original for potential reset operations
            if not hasattr(self, "_original_fileobj"):
                self._original_fileobj = self._fileobj
            self._fileobj = gzip.GzipFile(fileobj=self._original_fileobj, mode=self.mode, compresslevel=self.compression_level)
        elif self.filename is not None:
            # Open from filename as usual
            self._fileobj = gzip.GzipFile(filename=self.filename, mode=self.mode, compresslevel=self.compression_level)
        else:
            raise ValueError("GZIPCodec requires either filename or fileobj")
        return self._fileobj

    def close(self):
        self._fileobj.close()

    @staticmethod
    def id():
        return "gzip"

    @staticmethod
    def fileexts() -> list[str]:
        return [
            "gz",
        ]
