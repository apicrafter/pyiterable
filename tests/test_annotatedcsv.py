# -*- coding: utf-8 -*-
import pytest
from iterable.datatypes import AnnotatedCSVIterable


class TestAnnotatedCSV:
    def test_id(self):
        datatype_id = AnnotatedCSVIterable.id()
        assert datatype_id == 'annotatedcsv'
    
    def test_flatonly(self):
        flag = AnnotatedCSVIterable.is_flatonly()
        assert flag == True
    
    def test_read_simple_annotated_csv(self):
        """Test reading a simple annotated CSV file"""
        # Create test file
        content = """#datatype,string,long,dateTime:RFC3339
#group,false,false,false
#default,_result,,
,result,table,_time,_value
,,0,2025-12-19T15:12:51Z,42
,,0,2025-12-19T15:13:51Z,43
"""
        with open('testdata/test_annotated.csv', 'w') as f:
            f.write(content)
        
        iterable = AnnotatedCSVIterable('testdata/test_annotated.csv')
        records = list(iterable)
        iterable.close()
        
        assert len(records) == 2
        assert records[0]['_value'] == 42
        assert records[1]['_value'] == 43
    
    def test_read_with_datatypes(self):
        """Test reading annotated CSV with type conversion"""
        content = """#datatype,string,long,double,boolean
#group,false,false,false,false
,name,count,price,active
,Item1,10,19.99,true
,Item2,20,29.99,false
"""
        with open('testdata/test_annotated_types.csv', 'w') as f:
            f.write(content)
        
        iterable = AnnotatedCSVIterable('testdata/test_annotated_types.csv')
        records = list(iterable)
        iterable.close()
        
        assert len(records) == 2
        assert isinstance(records[0]['count'], int)
        assert records[0]['count'] == 10
        assert isinstance(records[0]['price'], float)
        assert records[0]['price'] == 19.99
        assert isinstance(records[0]['active'], bool)
        assert records[0]['active'] == True
    
    def test_read_with_defaults(self):
        """Test reading annotated CSV with default values"""
        content = """#datatype,string,long
#group,false,false
#default,_result,0
,name,count
,Item1,10
,Item2,
"""
        with open('testdata/test_annotated_defaults.csv', 'w') as f:
            f.write(content)
        
        iterable = AnnotatedCSVIterable('testdata/test_annotated_defaults.csv')
        records = list(iterable)
        iterable.close()
        
        assert len(records) == 2
        assert records[0]['count'] == 10
        assert records[1]['count'] == 0  # Should use default
    
    def test_write_annotated_csv(self):
        """Test writing annotated CSV file"""
        records = [
            {'name': 'Item1', 'count': 10, 'price': 19.99},
            {'name': 'Item2', 'count': 20, 'price': 29.99}
        ]
        
        iterable = AnnotatedCSVIterable(
            'testdata/test_write_annotated.csv',
            mode='w',
            keys=['name', 'count', 'price'],
            options={
                'datatypes': ['string', 'long', 'double'],
                'group': [False, False, False]
            }
        )
        
        for record in records:
            iterable.write(record)
        iterable.close()
        
        # Read it back
        iterable = AnnotatedCSVIterable('testdata/test_write_annotated.csv')
        read_records = list(iterable)
        iterable.close()
        
        assert len(read_records) == 2
        assert read_records[0]['name'] == 'Item1'
        assert read_records[0]['count'] == 10
    
    def test_read_bulk(self):
        """Test reading bulk records"""
        content = """#datatype,string,long
#group,false,false
,name,count
,Item1,10
,Item2,20
,Item3,30
,Item4,40
"""
        with open('testdata/test_annotated_bulk.csv', 'w') as f:
            f.write(content)
        
        iterable = AnnotatedCSVIterable('testdata/test_annotated_bulk.csv')
        chunk = iterable.read_bulk(2)
        assert len(chunk) == 2
        
        # Read next
        record = iterable.read()
        assert record['name'] == 'Item3'
        iterable.close()
