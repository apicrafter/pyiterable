# -*- coding: utf-8 -*- 
import pytest
import os
from iterable.datatypes import YAMLIterable
from fixdata import FIXTURES

# Create fixture file if it doesn't exist
FIXTURE_FILE = 'fixtures/2cols6rows_flat.yaml'

def setup_module():
    """Create fixture file if it doesn't exist"""
    try:
        import yaml
        if not os.path.exists(FIXTURE_FILE):
            with open(FIXTURE_FILE, 'w', encoding='utf-8') as f:
                for record in FIXTURES:
                    yaml.dump(record, f, default_flow_style=False, allow_unicode=True)
                    f.write('---\n')
    except ImportError:
        pass  # Skip if yaml not available

class TestYAML:
    def test_id(self):
        datatype_id = YAMLIterable.id()
        assert datatype_id == 'yaml'

    def test_flatonly(self):
        flag = YAMLIterable.is_flatonly()
        assert flag == False

    def test_openclose(self):
        iterable = YAMLIterable(FIXTURE_FILE)        
        iterable.close()

    def test_read_bulk_returns_n_records(self):
        iterable = YAMLIterable(FIXTURE_FILE)
        chunk = iterable.read_bulk(3)
        assert len(chunk) == 3
        assert chunk == FIXTURES[:3]
        iterable.close()
                
    def test_parsesimple_readone(self):
        iterable = YAMLIterable(FIXTURE_FILE)        
        row = iterable.read()
        assert row == FIXTURES[0]
        iterable.close()
           
    def test_parsesimple_reset(self):
        iterable = YAMLIterable(FIXTURE_FILE)        
        row = iterable.read()
        assert row == FIXTURES[0]
        iterable.reset() 
        row_reset = iterable.read()
        assert row_reset == FIXTURES[0]
        iterable.close()
           
    def test_parsesimple_next(self):
        iterable = YAMLIterable(FIXTURE_FILE)        
        row = next(iterable)
        assert row == FIXTURES[0]
        iterable.reset() 
        row_reset = next(iterable)
        assert row_reset == FIXTURES[0]
        iterable.close()

    def test_parsesimple_count(self):
        iterable = YAMLIterable(FIXTURE_FILE)        
        n = 0
        for row in iterable:
            n += 1
        assert n == len(FIXTURES)
        iterable.close()

    def test_parsesimple_iterateall(self):
        iterable = YAMLIterable(FIXTURE_FILE)        
        n = 0
        for row in iterable:
            assert row == FIXTURES[n]
            n += 1
        iterable.close()

    def test_write_read(self):
        iterable = YAMLIterable('testdata/2cols6rows_test.yaml', mode='w')        
        for row in FIXTURES:
            iterable.write(row)
        iterable.close()
        iterable = YAMLIterable('testdata/2cols6rows_test.yaml')        
        n = 0
        for row in iterable:
            assert row == FIXTURES[n]
            n += 1
        iterable.close()
