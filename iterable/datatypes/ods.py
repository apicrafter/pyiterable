from __future__ import annotations
import typing
try:
    from odf.opendocument import load
    from odf.table import Table, TableRow, TableCell
    from odf.text import P
    HAS_ODF = True
except ImportError:
    try:
        import pyexcel_ods3
        HAS_PYEXCEL_ODS = True
        HAS_ODF = False
    except ImportError:
        HAS_PYEXCEL_ODS = False
        HAS_ODF = False

from ..base import BaseFileIterable, BaseCodec


class ODSIterable(BaseFileIterable):
    datamode = 'binary'
    def __init__(self, filename:str = None, stream:typing.IO = None, codec: BaseCodec = None, mode='r', keys: list[str] = None, page:int = 0, start_line:int = 0, options:dict={}):
        if not HAS_ODF and not HAS_PYEXCEL_ODS:
            raise ImportError("ODS file support requires 'odfpy' or 'pyexcel-ods3' package")
        super(ODSIterable, self).__init__(filename, stream, codec=codec, mode=mode, binary=True, noopen=True, options=options)
        self.keys = keys
        self.start_line = start_line + 1
        self.page = page
        if 'page' in options.keys():
            self.page = int(options['page'])
        self.pos = self.start_line
        self.extracted_keys = keys is None
        self.reset()
        pass

    def reset(self):
        """Reset iterable"""
        super(ODSIterable, self).reset()
        self.pos = self.start_line
        
        if HAS_ODF:
            # Using odfpy library
            self.doc = load(self.filename)
            self.sheets = [sheet for sheet in self.doc.spreadsheet.getElementsByType(Table)]
            if self.page >= len(self.sheets):
                raise ValueError(f"Sheet index {self.page} out of range. Available sheets: {len(self.sheets)}")
            self.sheet = self.sheets[self.page]
            self.rows = self.sheet.getElementsByType(TableRow)
            self.row_index = 0
            
            if self.extracted_keys and len(self.rows) > 0:
                # Extract keys from first row
                first_row = self.rows[0]
                cells = first_row.getElementsByType(TableCell)
                self.keys = []
                for cell in cells:
                    text_content = ""
                    paragraphs = cell.getElementsByType(P)
                    for p in paragraphs:
                        text_content += p.firstChild.data if p.firstChild else ""
                    self.keys.append(text_content if text_content else "")
                self.row_index = 1
                self.pos += 1
        else:
            # Using pyexcel_ods3 library
            self.data = pyexcel_ods3.get_data(self.filename)
            sheet_names = list(self.data.keys())
            if self.page >= len(sheet_names):
                raise ValueError(f"Sheet index {self.page} out of range. Available sheets: {len(sheet_names)}")
            self.sheet_name = sheet_names[self.page]
            self.rows = self.data[self.sheet_name]
            self.row_index = 0
            
            if self.extracted_keys and len(self.rows) > 0:
                # Extract keys from first row
                self.keys = [str(cell) for cell in self.rows[0]]
                self.row_index = 1
                self.pos += 1

    @staticmethod
    def has_totals():
        """Has totals indicator"""
        return True        

    def totals(self):
        """Returns file totals"""
        if HAS_ODF:
            return len(self.rows)
        else:
            return len(self.rows)

    @staticmethod
    def id() -> str:
        return 'ods'

    @staticmethod
    def is_flatonly() -> bool:
        return True

    def read(self) -> dict:
        """Read single ODS record"""
        if HAS_ODF:
            if self.row_index >= len(self.rows):
                raise StopIteration
            row = self.rows[self.row_index]
            cells = row.getElementsByType(TableCell)
            values = []
            for cell in cells:
                text_content = ""
                paragraphs = cell.getElementsByType(P)
                for p in paragraphs:
                    text_content += p.firstChild.data if p.firstChild else ""
                values.append(text_content)
            # Pad values if needed
            while len(values) < len(self.keys):
                values.append("")
            result = dict(zip(self.keys, values))
            self.row_index += 1
            self.pos += 1
            return result
        else:
            if self.row_index >= len(self.rows):
                raise StopIteration
            row = self.rows[self.row_index]
            # Convert to strings and pad if needed
            values = [str(cell) for cell in row]
            while len(values) < len(self.keys):
                values.append("")
            result = dict(zip(self.keys, values))
            self.row_index += 1
            self.pos += 1
            return result

    def read_bulk(self, num:int = 10) -> list[dict]:
        """Read bulk ODS records"""
        chunk = []
        for n in range(0, num):
            try:
                chunk.append(self.read())
            except StopIteration:
                break
        return chunk

    def write(self, record:dict):
        """Write single ODS record"""
        raise NotImplementedError("ODS writing is not yet supported")

    def write_bulk(self, records: list[dict]):
        """Write bulk ODS records"""
        raise NotImplementedError("ODS writing is not yet supported")
