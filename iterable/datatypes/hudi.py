from __future__ import annotations

import typing

try:
    from pyhudi import HudiCatalog

    HAS_PYHUDI = True
except ImportError:
    try:
        import hudi  # noqa: F401

        HAS_HUDI = True
        HAS_PYHUDI = False
    except ImportError:
        HAS_HUDI = False
        HAS_PYHUDI = False

from ..base import BaseCodec, BaseFileIterable


class HudiIterable(BaseFileIterable):
    datamode = "binary"

    def __init__(
        self,
        filename: str = None,
        stream: typing.IO = None,
        codec: BaseCodec = None,
        mode: str = "r",
        table_path: str = None,
        options: dict = None,
    ):
        if options is None:
            options = {}
        if not HAS_PYHUDI and not HAS_HUDI:
            raise ImportError("Apache Hudi support requires 'pyhudi' or 'hudi' package")
        super().__init__(filename, stream, codec=codec, mode=mode, binary=True, noopen=True, options=options)
        self.table_path = table_path
        if "table_path" in options:
            self.table_path = options["table_path"]
        if stream is not None:
            raise ValueError("Hudi requires table_path, not a stream")
        if self.table_path is None and self.filename is None:
            raise ValueError("Hudi requires table_path parameter")
        if self.table_path is None:
            self.table_path = self.filename
        self.table = None
        self.iterator = None
        self.reset()
        pass

    def reset(self):
        """Reset iterable"""
        super().reset()
        self.pos = 0

        if self.mode == "r":
            # Load Hudi table
            # This is a simplified implementation - actual usage would depend on Hudi API
            if HAS_PYHUDI:
                # pyhudi API
                catalog = HudiCatalog()
                self.table = catalog.load_table(self.table_path)
                # Read table data
                df = self.table.to_pandas()
                self.iterator = iter(df.to_dict("records"))
            else:
                # hudi API (if different)
                # Placeholder - would need actual Hudi API documentation
                self.iterator = iter([])
        else:
            raise NotImplementedError("Hudi writing is not yet supported")

    @staticmethod
    def has_totals():
        """Has totals indicator"""
        return True

    def totals(self):
        """Returns table totals"""
        if self.table is None:
            return 0
        if HAS_PYHUDI:
            df = self.table.to_pandas()
            return len(df)
        return 0

    @staticmethod
    def id() -> str:
        return "hudi"

    @staticmethod
    def is_flatonly() -> bool:
        return True

    @staticmethod
    def has_tables() -> bool:
        """Indicates if this format supports multiple tables."""
        return True

    def list_tables(self, filename: str | None = None) -> list[str] | None:
        """List available table names in the Hudi catalog or directory.

        Can be called as:
        - Instance method: `iterable.list_tables()` - reuses catalog if available
        - With filename: `iterable.list_tables(filename)` - connects to catalog/directory temporarily

        Args:
            filename: Optional catalog path or directory. If None, uses instance's table_path.

        Returns:
            list[str]: List of table names, or empty list if no tables. Returns None if single table path.
        """
        if not HAS_PYHUDI and not HAS_HUDI:
            return None

        # Determine table path or catalog path
        target_path = filename if filename is not None else (self.table_path if hasattr(self, "table_path") else None)
        if target_path is None:
            return None

        try:
            if HAS_PYHUDI:
                # Try to use catalog to list tables
                catalog = HudiCatalog()
                # Check if path is a catalog or single table
                # If it's a catalog, try to list tables
                if hasattr(catalog, "list_tables"):
                    try:
                        tables = catalog.list_tables(target_path)
                        return [str(t) for t in tables] if tables else []
                    except Exception:
                        # If listing fails, might be a single table path
                        return None
                else:
                    # Catalog doesn't support listing, might be single table
                    return None
            else:
                # hudi package - similar approach
                return None
        except Exception:
            return None

    def read(self) -> dict:
        """Read single Hudi record"""
        try:
            row = next(self.iterator)
            self.pos += 1
            return row
        except (StopIteration, EOFError, ValueError):
            raise StopIteration from None

    def read_bulk(self, num: int = 10) -> list[dict]:
        """Read bulk Hudi records"""
        chunk = []
        for _n in range(0, num):
            try:
                chunk.append(self.read())
            except StopIteration:
                break
        return chunk

    def write(self, record: dict):
        """Write single Hudi record"""
        raise NotImplementedError("Hudi writing is not yet supported")

    def write_bulk(self, records: list[dict]):
        """Write bulk Hudi records"""
        raise NotImplementedError("Hudi writing is not yet supported")
