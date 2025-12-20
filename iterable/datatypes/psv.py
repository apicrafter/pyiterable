from __future__ import annotations
import typing
from .csv import CSVIterable

from ..base import BaseCodec


class PSVIterable(CSVIterable):
    """Pipe-Separated Values iterable - extends CSV with pipe delimiter"""
    def __init__(self, filename:str = None, stream:typing.IO = None, codec: BaseCodec = None, keys: list[str] = None, quotechar:str='"', mode:str='r', encoding:str = None, autodetect:bool=False, options:dict={}):
        # Force delimiter to pipe
        options['delimiter'] = '|'
        super(PSVIterable, self).__init__(filename, stream, codec=codec, keys=keys, delimiter='|', quotechar=quotechar, mode=mode, encoding=encoding, autodetect=False, options=options)

    @staticmethod
    def id() -> str:
        return 'psv'

    @staticmethod
    def is_flatonly() -> bool:
        return True


class SSVIterable(CSVIterable):
    """Semicolon-Separated Values iterable - extends CSV with semicolon delimiter"""
    def __init__(self, filename:str = None, stream:typing.IO = None, codec: BaseCodec = None, keys: list[str] = None, quotechar:str='"', mode:str='r', encoding:str = None, autodetect:bool=False, options:dict={}):
        # Force delimiter to semicolon
        options['delimiter'] = ';'
        super(SSVIterable, self).__init__(filename, stream, codec=codec, keys=keys, delimiter=';', quotechar=quotechar, mode=mode, encoding=encoding, autodetect=False, options=options)

    @staticmethod
    def id() -> str:
        return 'ssv'

    @staticmethod
    def is_flatonly() -> bool:
        return True
