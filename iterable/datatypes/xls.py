from __future__ import annotations
import typing
from xlrd import open_workbook
import xlrd
from ..base import BaseFileIterable, BaseCodec
import datetime

def read_row_keys(rownum, ncols, sheet):
    """Read single row by row num"""
    tmp = list()
    for i in range(0, ncols):
        ct = sheet.cell_type(rownum, i)
        cell_value = sheet.cell_value(rownum, i)
        get_col = str(cell_value)
        tmp.append(get_col)    
    return tmp


def read_single_row(rownum, ncols, datemode, keys, sheet):
    """Read single row by row num"""
    tmp = list()
    for i in range(0, ncols):
        ct = sheet.cell_type(rownum, i)
        cell_value = sheet.cell_value(rownum, i)
        if ct == xlrd.XL_CELL_DATE:
            # Returns a tuple.
            dt_tuple = xlrd.xldate_as_tuple(cell_value, datemode)
            # Create datetime object from this tuple.
            get_col = str(datetime.datetime(             
                dt_tuple[0], dt_tuple[1], dt_tuple[2],
                dt_tuple[3], dt_tuple[4], dt_tuple[5]
            ))
        elif ct == xlrd.XL_CELL_NUMBER:
            get_col = int(cell_value)
        else:
            get_col = str(cell_value)
        tmp.append(get_col)
    row = dict(zip(keys, tmp))
    return row



class XLSIterable(BaseFileIterable):
    datamode = 'binary'
    def __init__(self, filename:str = None, stream:typing.IO = None, codec: BaseCodec = None, mode='r', keys: list[str] = None, page:int = 0, start_line:int = 0, options:dict={}):
        super(XLSIterable, self).__init__(filename, stream, codec=codec, binary=True, mode=mode, noopen=True, options=options)
        self.page = page
        self.start_line = start_line
        self.pos = start_line
        self.keys = keys
        self.extracted_keys = keys is None
        self.reset()
        pass

    def reset(self):
        """Reopen file and open sheet"""
        super(XLSIterable, self).reset()
        self.pos = self.start_line
        self.workbook = open_workbook(self.filename)
        self.sheet = self.workbook.sheet_by_index(self.page)
        if self.extracted_keys:
            self.keys = read_row_keys(self.pos, self.sheet.ncols, self.sheet)
            self.pos += 1

    @staticmethod
    def id() -> str:
        """ID of the data source type"""
        return 'xls'

    @staticmethod
    def is_flatonly() -> bool:
        """Flag that data is flat"""
        return True

    @staticmethod
    def has_totals():
        """Has totals indicator"""
        return True        

    def totals(self):
        """Returns file totals"""
        return self.sheet.nrows

    def read(self) -> dict:
        """Read single XLS record"""
        if self.pos >= self.sheet.nrows:
            raise StopIteration
        row = read_single_row(self.pos, self.sheet.ncols, self.workbook.datemode, self.keys, self.sheet)
        self.pos += 1
        return row

    def read_bulk(self, num:int = 10) -> list[dict]:
        """Read bulk XLS records"""
        chunk = []
        ncols = self.sheet.ncols
        datemode = self.workbook.datemode
        for n in range(0, num):
            if self.pos >= self.sheet.nrows:
                raise StopIteration
            row = read_single_row(self.pos, ncols, datemode, self.keys, self.sheet)
            chunk.append(row)
            self.pos += 1
        return chunk
