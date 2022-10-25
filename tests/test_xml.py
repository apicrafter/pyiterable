# -*- coding: utf-8 -*- 
import pytest
from iterable.datatypes import XMLIterable

from fixdata import FIXTURES_BOOKS

class TestXML:
    def test_id(self):
        datatype_id = XMLIterable.id()
        assert datatype_id == 'xml'

    def test_flatonly(self):
        flag = XMLIterable.is_flatonly()
        assert flag == False

    def test_openclose(self):
        iterable = XMLIterable('fixtures/books.xml', tagname='book')        
        iterable.close()
                
    def test_parsesimple_readone(self):
        iterable = XMLIterable('fixtures/books.xml', tagname='book')        
        row = iterable.read()
        assert row == FIXTURES_BOOKS[0]
        iterable.close()
           
    def test_parsesimple_reset(self):
        iterable = XMLIterable('fixtures/books.xml', tagname='book')        
        row = iterable.read()
        assert row == FIXTURES_BOOKS[0]
        iterable.reset() 
        row_reset = iterable.read()
        assert row_reset == FIXTURES_BOOKS[0]
        iterable.close()
           
    def test_parsesimple_next(self):
        iterable = XMLIterable('fixtures/books.xml', tagname='book')        
        row = next(iterable)
        assert row == FIXTURES_BOOKS[0]
        iterable.reset() 
        row_reset = next(iterable)
        assert row_reset == FIXTURES_BOOKS[0]
        iterable.close()

    def test_parsesimple_count(self):
        iterable = XMLIterable('fixtures/books.xml', tagname='book')        
        n = 0
        for row in iterable:
            n += 1
        assert n == len(FIXTURES_BOOKS)
        iterable.close()

    def test_parsesimple_iterateall(self):
        iterable = XMLIterable('fixtures/books.xml', tagname='book')        
        n = 0
        for row in iterable:
            assert row == FIXTURES_BOOKS[n]
            n += 1
        iterable.close()
