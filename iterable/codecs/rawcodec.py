from __future__ import annotations
import typing
from ..base import BaseCodec


class RAWCodec(BaseCodec):
    def __init__(self, filename:str, mode:str = 'r', open_it:bool = False, options:dict = {}):
        super(RAWCodec, self).__init__(filename, mode=mode, open_it=open_it, options=options)

    def open(self) -> typing.IO:
        self._fileobj = open(self.filename, self.mode)
        return self._fileobj

    def close(self):
        self._fileobj.close()

    @staticmethod
    def id():
        return 'raw'

    @staticmethod
    def fileexts() -> list[str]:
        return None
