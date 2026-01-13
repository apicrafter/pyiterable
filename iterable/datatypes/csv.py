from __future__ import annotations

import logging
import typing
from csv import DictReader, DictWriter

import chardet

from ..base import BaseCodec, BaseFileIterable
from ..helpers.utils import rowincount

DEFAULT_ENCODING = "utf8"
DEFAULT_DELIMITER = ","


def detect_encoding_raw(filename=None, stream=None, limit=1000000):
    if filename is not None:
        f = open(filename, "rb")
        chunk = f.read(limit)
        f.close()
    else:
        chunk = stream.read(limit)
        stream.reset()
    detected = chardet.detect(chunk)
    logging.debug("Detected encoding {}".format(detected["encoding"]))
    return detected


def detect_delimiter(filename=None, stream=None, encoding="utf8"):
    if filename is not None:
        f = open(filename, encoding=encoding)
        line = f.readline()
        f.close()
    else:
        line = stream.readline()
        #        stream.seek(0,0)
        stream.reset()
    dict1 = {",": line.count(","), ";": line.count(";"), "\t": line.count("\t"), "|": line.count("|")}
    delimiter = max(dict1, key=dict1.get)
    logging.debug(f"Detected delimiter {delimiter}")
    return delimiter


class CSVIterable(BaseFileIterable):
    def __init__(
        self,
        filename: str = None,
        stream: typing.IO = None,
        codec: BaseCodec = None,
        keys: list[str] = None,
        delimiter: str = None,
        quotechar: str = '"',
        mode: str = "r",
        encoding: str = None,
        autodetect: bool = False,
        options: dict = None,
    ):
        if options is None:
            options = {}
        logging.debug(f"Params: encoding: {encoding}, options {options}")
        self.encoding = None
        self.fileobj = stream
        if encoding is not None:
            self.encoding = encoding
        elif "encoding" in options.keys() and options["encoding"] is not None:
            self.encoding = options["encoding"]
        if mode == "r":
            if filename is not None and self.encoding is None:
                self.encoding = detect_encoding_raw(filename=filename)["encoding"]
            elif stream is not None and self.encoding is None:
                self.encoding = detect_encoding_raw(stream=stream)["encoding"]
            elif self.encoding is None:
                self.encoding = DEFAULT_ENCODING
        elif self.encoding is None:
            self.encoding = DEFAULT_ENCODING
        logging.debug(f"Final encoding {self.encoding}")
        self.keys = keys

        super().__init__(
            filename, stream, codec=codec, binary=False, encoding=self.encoding, mode=mode, options=options
        )
        if not delimiter:
            if autodetect and mode == "r":
                #                print(filename, stream)
                self.delimiter = detect_delimiter(filename, self.fobj, encoding=self.encoding)
            else:
                self.delimiter = DEFAULT_DELIMITER
        else:
            self.delimiter = delimiter
        self.quotechar = quotechar
        logging.debug(f"Detected delimiter {self.delimiter}")
        self.reset()
        pass

    @staticmethod
    def has_totals():
        """Has totals indicator"""
        return True

    def totals(self):
        """Returns file totals"""
        return rowincount(self.filename, self.fobj)

    def reset(self):
        super().reset()
        if self.fobj is None and self.codec is not None:
            fobj = self.codec.textIO(self.encoding)
        else:
            fobj = self.fobj
        logging.debug(f"Detected delimiter {self.delimiter}")
        self.reader = None
        if self.mode == "r":
            if self.keys is not None:
                self.reader = DictReader(fobj, fieldnames=self.keys, delimiter=self.delimiter, quotechar=self.quotechar)
            else:
                self.reader = DictReader(fobj, delimiter=self.delimiter, quotechar=self.quotechar)
        if self.mode in ["w", "wr"] and self.keys is not None:
            self.writer = DictWriter(fobj, fieldnames=self.keys, delimiter=self.delimiter, quotechar=self.quotechar)
            self.writer.writeheader()
        else:
            self.writer = None

        #            self.reader = reader(self.fobj, delimiter=self.delimiter, quotechar=self.quotechar)
        self.pos = 0

    @staticmethod
    def id() -> str:
        return "csv"

    @staticmethod
    def is_flatonly() -> bool:
        return True

    def read(self, skip_empty: bool = True):
        """Read single CSV record"""
        row = next(self.reader)
        if skip_empty and len(row) == 0:
            return self.read(skip_empty)
        self.pos += 1
        return row

    def read_bulk(self, num: int = 10) -> list[dict]:
        """Read bulk CSV records efficiently"""
        chunk = []
        for _n in range(0, num):
            try:
                chunk.append(next(self.reader))
                self.pos += 1
            except StopIteration:
                break
        return chunk

    def is_streaming(self) -> bool:
        """Returns True - CSV always streams row by row"""
        return True

    def write(self, record: dict):
        """Write single CSV record"""
        self.writer.writerow(record)

    def write_bulk(self, records: list[dict]):
        """Write bulk CSV records"""
        self.writer.writerows(records)
