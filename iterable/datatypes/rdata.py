from __future__ import annotations

import typing

try:
    import pyreadr

    HAS_PYREADR = True
except ImportError:
    HAS_PYREADR = False

from ..base import BaseCodec, BaseFileIterable


class RDataIterable(BaseFileIterable):
    datamode = "binary"

    def __init__(
        self,
        filename: str = None,
        stream: typing.IO = None,
        codec: BaseCodec = None,
        mode: str = "r",
        options: dict = None,
    ):
        if options is None:
            options = {}
        if not HAS_PYREADR:
            raise ImportError("RData file support requires 'pyreadr' package")
        super().__init__(filename, stream, codec=codec, binary=True, mode=mode, options=options)
        self.reset()
        pass

    def reset(self):
        """Reset iterable"""
        super().reset()
        self.pos = 0
        if self.mode == "r":
            # pyreadr requires file path, not file object
            if self.filename:
                result = pyreadr.read_r(self.filename)
                # RData can contain multiple objects, iterate through all
                self.data = []
                for obj_name, df in result.items():
                    if df is not None:
                        # Convert each dataframe to dict records
                        records = df.to_dict("records")
                        # Add object name as metadata if multiple objects
                        if len(result) > 1:
                            for record in records:
                                record["_r_object_name"] = obj_name
                        self.data.extend(records)
                self.iterator = iter(self.data)
            else:
                raise ValueError("RData file reading requires filename, not stream")
        else:
            raise NotImplementedError("RData file writing is not yet supported")

    @staticmethod
    def id() -> str:
        return "rdata"

    @staticmethod
    def is_flatonly() -> bool:
        return True

    @staticmethod
    def has_tables() -> bool:
        """Indicates if this format supports multiple tables/objects."""
        return True

    def list_tables(self, filename: str | None = None) -> list[str] | None:
        """List available R object names in the RData file.

        Args:
            filename: Optional filename. If None, uses instance's filename.

        Returns:
            list[str]: List of R object names, or empty list if no objects.
        """
        target_filename = filename if filename is not None else self.filename
        if target_filename is None:
            return None

        # If data is already loaded, reuse it
        if filename is None and hasattr(self, "data") and self.data is not None:
            # We need to reload to get object names, but we can check if we have the result
            # Actually, we need to read the file again to get object names
            # pyreadr.read_r returns a dict with object names as keys
            result = pyreadr.read_r(target_filename)
            return list(result.keys())

        # Read file to get object names
        result = pyreadr.read_r(target_filename)
        return list(result.keys())

    @staticmethod
    def has_totals():
        """Has totals indicator"""
        return True

    def totals(self):
        """Returns file totals"""
        if self.filename:
            result = pyreadr.read_r(self.filename)
            total = 0
            for df in result.values():
                if df is not None:
                    total += len(df)
            return total
        elif hasattr(self, "data"):
            return len(self.data)
        return 0

    def read(self) -> dict:
        """Read single RData record"""
        row = next(self.iterator)
        self.pos += 1
        # Convert numpy types to Python types
        return {k: (v.item() if hasattr(v, "item") else v) for k, v in row.items()}

    def read_bulk(self, num: int = 10) -> list[dict]:
        """Read bulk RData records"""
        chunk = []
        for _n in range(0, num):
            try:
                chunk.append(self.read())
            except StopIteration:
                break
        return chunk

    def write(self, record: dict):
        """Write single RData record - not supported"""
        raise NotImplementedError("RData file writing is not yet supported")

    def write_bulk(self, records: list[dict]):
        """Write bulk RData records - not supported"""
        raise NotImplementedError("RData file writing is not yet supported")
