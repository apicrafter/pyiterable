from __future__ import annotations

import bz2

from ..base import BaseCodec


class BZIP2Codec(BaseCodec):
    def __init__(
        self, filename: str, compression_level: int = 5, mode: str = "r", open_it: bool = False, options: dict = None
    ):
        if options is None:
            options = {}
        self.compression_level = compression_level
        super().__init__(filename, mode=mode, open_it=open_it, options=options)

    def open(self) -> bz2.BZ2File:
        # If fileobj was provided (e.g., from cloud storage), wrap it with BZ2File
        if self._fileobj is not None and not isinstance(self._fileobj, bz2.BZ2File):
            # fileobj provided, wrap it with BZ2File
            # Store original for potential reset operations
            if not hasattr(self, "_original_fileobj"):
                self._original_fileobj = self._fileobj
            self._fileobj = bz2.BZ2File(self._original_fileobj, mode=self.mode, compresslevel=self.compression_level)
        elif self.filename is not None:
            # Open from filename as usual
            self._fileobj = bz2.open(self.filename, self.mode, compresslevel=self.compression_level)
        else:
            raise ValueError("BZIP2Codec requires either filename or fileobj")
        return self._fileobj

    def close(self):
        self._fileobj.close()

    @staticmethod
    def fileexts() -> list[str]:
        return [
            "bz2",
        ]
