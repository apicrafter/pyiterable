from __future__ import annotations

import typing

try:
    import msgpack

    HAS_MSGPACK = True
except ImportError:
    HAS_MSGPACK = False

from ..base import BaseCodec, BaseFileIterable, DEFAULT_BULK_NUMBER
from typing import Any


class MessagePackIterable(BaseFileIterable):
    datamode = "binary"

    def __init__(
        self,
        filename: str = None,
        stream: typing.IO[Any] | None = None,
        codec: BaseCodec | None = None,
        mode: str = "r",
        options: dict[str, Any] | None = None,
    ):
        if options is None:
            options = {}
        if not HAS_MSGPACK:
            raise ImportError("MessagePack support requires 'msgpack' package")
        super().__init__(filename, stream, codec=codec, binary=True, mode=mode, options=options)
        self.reset()
        pass

    def reset(self):
        """Reset iterable"""
        super().reset()
        self.pos = 0
        if self.mode == "r":
            self.unpacker = msgpack.Unpacker(self.fobj, raw=False, use_list=True)
        else:
            self.packer = msgpack.Packer(use_bin_type=True)

    @staticmethod
    def id() -> str:
        return "msgpack"

    @staticmethod
    def is_flatonly() -> bool:
        return False

    def read(self, skip_empty: bool = True) -> dict:
        """Read single MessagePack record"""
        try:
            row = next(self.unpacker)
            self.pos += 1
            return row
        except StopIteration:
            raise StopIteration from None

    def read_bulk(self, num: int = DEFAULT_BULK_NUMBER) -> list[dict]:
        """Read bulk MessagePack records"""
        chunk = []
        for _n in range(0, num):
            try:
                chunk.append(self.read())
            except StopIteration:
                break
        return chunk

    def write(self, record: Row) -> None:
        """Write single MessagePack record"""
        self.fobj.write(self.packer.pack(record))

    def write_bulk(self, records: list[Row]) -> None:
        """Write bulk MessagePack records"""
        for record in records:
            self.fobj.write(self.packer.pack(record))
