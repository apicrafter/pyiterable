from __future__ import annotations
import typing
try:
    from google.protobuf import message
    from google.protobuf import json_format
    HAS_PROTOBUF = True
except ImportError:
    HAS_PROTOBUF = False

from ..base import BaseFileIterable, BaseCodec


class ProtobufIterable(BaseFileIterable):
    datamode = 'binary'
    def __init__(self, filename:str = None, stream:typing.IO = None, codec: BaseCodec = None, mode:str='r', message_class=None, options:dict={}):
        if not HAS_PROTOBUF:
            raise ImportError("Protocol Buffers support requires 'protobuf' package")
        if message_class is None and 'message_class' in options:
            message_class = options['message_class']
        self.message_class = message_class
        if self.message_class is None:
            raise ValueError("Protocol Buffers requires 'message_class' parameter")
        super(ProtobufIterable, self).__init__(filename, stream, codec=codec, binary=True, mode=mode, options=options)
        self.reset()
        pass

    def reset(self):
        """Reset iterable"""
        super(ProtobufIterable, self).reset()
        self.pos = 0
        if self.mode == 'r':
            # Read messages sequentially from binary stream
            self.messages = []
            self.iterator = self.__iterator()
        else:
            self.messages = []

    def __iterator(self):
        """Iterator for reading protobuf messages"""
        while True:
            try:
                # Read message size (varint)
                size_bytes = bytearray()
                while True:
                    byte = self.fobj.read(1)
                    if not byte:
                        return
                    size_bytes.append(ord(byte))
                    if not (byte[0] & 0x80):
                        break
                
                # Parse size (simplified - protobuf uses varint encoding)
                size = int.from_bytes(size_bytes, byteorder='little')
                if size > 0:
                    # Read message data
                    message_data = self.fobj.read(size)
                    if len(message_data) < size:
                        return
                    
                    # Parse message
                    msg = self.message_class()
                    msg.ParseFromString(message_data)
                    # Convert to dict
                    yield json_format.MessageToDict(msg)
            except (EOFError, StopIteration):
                return

    @staticmethod
    def id() -> str:
        return 'protobuf'

    @staticmethod
    def is_flatonly() -> bool:
        return False

    def read(self) -> dict:
        """Read single protobuf record"""
        row = next(self.iterator)
        self.pos += 1
        return row

    def read_bulk(self, num:int = 10) -> list[dict]:
        """Read bulk protobuf records"""
        chunk = []
        for n in range(0, num):
            try:
                chunk.append(self.read())
            except StopIteration:
                break
        return chunk

    def write(self, record:dict):
        """Write single protobuf record"""
        msg = self.message_class()
        json_format.ParseDict(record, msg)
        serialized = msg.SerializeToString()
        # Write size as varint (simplified)
        size_bytes = len(serialized).to_bytes(4, byteorder='little')
        self.fobj.write(size_bytes)
        self.fobj.write(serialized)

    def write_bulk(self, records:list[dict]):
        """Write bulk protobuf records"""
        for record in records:
            self.write(record)
