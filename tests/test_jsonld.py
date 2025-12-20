# -*- coding: utf-8 -*- 
import pytest
from iterable.datatypes import JSONLDIterable

from fixdata import FIXTURES
TESTING_DIR = 'testdata'

class TestJSONLD:
    def test_id(self):
        datatype_id = JSONLDIterable.id()
        assert datatype_id == 'jsonld'

    def test_flatonly(self):
        flag = JSONLDIterable.is_flatonly()
        assert flag == False

    def test_openclose(self):
        iterable = JSONLDIterable('fixtures/2cols6rows_flat.jsonld')        
        iterable.close()
                
    def test_parsesimple_readone(self):
        iterable = JSONLDIterable('fixtures/2cols6rows_flat.jsonld')        
        row = iterable.read()
        # JSON-LD adds @context and @id, so we check for the basic fields
        assert row['id'] == FIXTURES[0]['id']
        assert row['name'] == FIXTURES[0]['name']
        iterable.close()
           
    def test_parsesimple_reset(self):
        iterable = JSONLDIterable('fixtures/2cols6rows_flat.jsonld')        
        row = iterable.read()
        assert row['id'] == FIXTURES[0]['id']
        iterable.reset() 
        row_reset = iterable.read()
        assert row_reset['id'] == FIXTURES[0]['id']
        iterable.close()
           
    def test_parsesimple_next(self):
        iterable = JSONLDIterable('fixtures/2cols6rows_flat.jsonld')        
        row = next(iterable)
        assert row['id'] == FIXTURES[0]['id']
        iterable.reset() 
        row_reset = next(iterable)
        assert row_reset['id'] == FIXTURES[0]['id']
        iterable.close()

    def test_parsesimple_count(self):
        iterable = JSONLDIterable('fixtures/2cols6rows_flat.jsonld')        
        n = 0
        for row in iterable:
            n += 1
        assert n == len(FIXTURES)
        iterable.close()

    def test_parsesimple_iterateall(self):
        iterable = JSONLDIterable('fixtures/2cols6rows_flat.jsonld')        
        n = 0
        for row in iterable:
            assert row['id'] == FIXTURES[n]['id']
            assert row['name'] == FIXTURES[n]['name']
            n += 1
        iterable.close()

    def test_parse_array(self):
        """Test reading JSON-LD array format"""
        iterable = JSONLDIterable('fixtures/2cols6rows_array.jsonld')        
        n = 0
        for row in iterable:
            assert row['id'] == FIXTURES[n]['id']
            assert row['name'] == FIXTURES[n]['name']
            n += 1
        assert n == len(FIXTURES)
        iterable.close()

    def test_parse_graph(self):
        """Test reading JSON-LD @graph format"""
        iterable = JSONLDIterable('fixtures/2cols6rows_graph.jsonld')        
        n = 0
        for row in iterable:
            assert row['id'] == FIXTURES[n]['id']
            assert row['name'] == FIXTURES[n]['name']
            # Check that context is added back
            assert '@context' in row
            n += 1
        assert n == len(FIXTURES)
        iterable.close()

    def test_write_read(self):
        iterable = JSONLDIterable('testdata/2cols6rows_test.jsonld', mode='w')        
        for row in FIXTURES:
            # Add JSON-LD context
            jsonld_row = {
                '@context': {'@vocab': 'http://example.org/'},
                '@id': row['id'],
                **row
            }
            iterable.write(jsonld_row)
        iterable.close()
        iterable = JSONLDIterable('testdata/2cols6rows_test.jsonld')        
        n = 0
        for row in iterable:
            assert row['id'] == FIXTURES[n]['id']
            assert row['name'] == FIXTURES[n]['name']
            n += 1
        iterable.close()
