# -*- coding: utf-8 -*- 
import pytest
import os
from iterable.datatypes import FixedWidthIterable
from fixdata import FIXTURES

# Create fixture file if it doesn't exist
FIXTURE_FILE = 'fixtures/2cols6rows.fwf'

def setup_module():
    """Create fixture file if it doesn't exist"""
    if not os.path.exists(FIXTURE_FILE):
        # Fixed width: id (3 chars) + name (10 chars) = 13 chars per line
        with open(FIXTURE_FILE, 'w', encoding='utf-8') as f:
            for record in FIXTURES:
                id_str = str(record['id']).ljust(3)
                name_str = record['name'].ljust(10)
                f.write(id_str + name_str + '\n')

class TestFixedWidth:
    def test_id(self):
        datatype_id = FixedWidthIterable.id()
        assert datatype_id == 'fwf'

    def test_flatonly(self):
        flag = FixedWidthIterable.is_flatonly()
        assert flag == True

    def test_openclose(self):
        iterable = FixedWidthIterable(FIXTURE_FILE, widths=[3, 10], names=['id', 'name'])        
        iterable.close()

    def test_read_bulk_returns_n_records(self):
        iterable = FixedWidthIterable(FIXTURE_FILE, widths=[3, 10], names=['id', 'name'])
        chunk = iterable.read_bulk(3)
        assert len(chunk) == 3
        # Values are strings and may have trailing spaces
        assert chunk[0]['id'].strip() == FIXTURES[0]['id']
        assert chunk[0]['name'].strip() == FIXTURES[0]['name']
        iterable.close()
                
    def test_parsesimple_readone(self):
        iterable = FixedWidthIterable(FIXTURE_FILE, widths=[3, 10], names=['id', 'name'])        
        row = iterable.read()
        assert row['id'].strip() == FIXTURES[0]['id']
        assert row['name'].strip() == FIXTURES[0]['name']
        iterable.close()
           
    def test_parsesimple_reset(self):
        iterable = FixedWidthIterable(FIXTURE_FILE, widths=[3, 10], names=['id', 'name'])        
        row = iterable.read()
        assert row['id'].strip() == FIXTURES[0]['id']
        iterable.reset() 
        row_reset = iterable.read()
        assert row_reset['id'].strip() == FIXTURES[0]['id']
        iterable.close()
           
    def test_parsesimple_next(self):
        iterable = FixedWidthIterable(FIXTURE_FILE, widths=[3, 10], names=['id', 'name'])        
        row = next(iterable)
        assert row['id'].strip() == FIXTURES[0]['id']
        iterable.reset() 
        row_reset = next(iterable)
        assert row_reset['id'].strip() == FIXTURES[0]['id']
        iterable.close()

    def test_parsesimple_count(self):
        iterable = FixedWidthIterable(FIXTURE_FILE, widths=[3, 10], names=['id', 'name'])        
        n = 0
        for row in iterable:
            n += 1
        assert n == len(FIXTURES)
        iterable.close()

    def test_parsesimple_iterateall(self):
        iterable = FixedWidthIterable(FIXTURE_FILE, widths=[3, 10], names=['id', 'name'])        
        n = 0
        for row in iterable:
            assert row['id'].strip() == FIXTURES[n]['id']
            assert row['name'].strip() == FIXTURES[n]['name']
            n += 1
        iterable.close()

    def test_write_read(self):
        iterable = FixedWidthIterable('testdata/2cols6rows_test.fwf', mode='w', widths=[3, 10], names=['id', 'name'])        
        for row in FIXTURES:
            iterable.write(row)
        iterable.close()
        iterable = FixedWidthIterable('testdata/2cols6rows_test.fwf', widths=[3, 10], names=['id', 'name'])        
        n = 0
        for row in iterable:
            assert row['id'].strip() == FIXTURES[n]['id']
            assert row['name'].strip() == FIXTURES[n]['name']
            n += 1
        iterable.close()

    def test_has_totals(self):
        iterable = FixedWidthIterable(FIXTURE_FILE, widths=[3, 10], names=['id', 'name'])
        assert FixedWidthIterable.has_totals() == True
        total = iterable.totals()
        assert total == len(FIXTURES)
        iterable.close()

    def test_missing_widths_names(self):
        with pytest.raises(ValueError):
            iterable = FixedWidthIterable(FIXTURE_FILE)
            iterable.read()
