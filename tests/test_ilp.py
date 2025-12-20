# -*- coding: utf-8 -*-
import pytest
from iterable.datatypes import ILPIterable


class TestILP:
    def test_id(self):
        datatype_id = ILPIterable.id()
        assert datatype_id == 'ilp'
    
    def test_flatonly(self):
        flag = ILPIterable.is_flatonly()
        assert flag == False
    
    def test_parse_simple_line(self):
        """Test parsing a simple ILP line"""
        from iterable.datatypes.ilp import parse_line_protocol
        
        line = 'temperature value=23.5 1631022245000000000'
        result = parse_line_protocol(line)
        
        assert result['measurement'] == 'temperature'
        assert result['fields'] == {'value': 23.5}
        assert result['time'] == '1631022245000000000'
        assert 'tags' in result
        assert len(result['tags']) == 0
    
    def test_parse_with_tags(self):
        """Test parsing ILP line with tags"""
        from iterable.datatypes.ilp import parse_line_protocol
        
        line = 'temperature,sensor=abc123,location=room1 value=23.5 1631022245000000000'
        result = parse_line_protocol(line)
        
        assert result['measurement'] == 'temperature'
        assert result['tags'] == {'sensor': 'abc123', 'location': 'room1'}
        assert result['fields'] == {'value': 23.5}
    
    def test_parse_multiple_fields(self):
        """Test parsing ILP line with multiple fields"""
        from iterable.datatypes.ilp import parse_line_protocol
        
        line = 'weather,location=us-midwest temperature=82,humidity=71 1465839830100400200'
        result = parse_line_protocol(line)
        
        assert result['measurement'] == 'weather'
        assert result['tags'] == {'location': 'us-midwest'}
        assert result['fields']['temperature'] == 82.0
        assert result['fields']['humidity'] == 71.0
    
    def test_parse_string_field(self):
        """Test parsing ILP line with string field"""
        from iterable.datatypes.ilp import parse_line_protocol
        
        line = 'weather,location=us-midwest temperature=82,description="hot and humid"'
        result = parse_line_protocol(line)
        
        assert result['fields']['temperature'] == 82.0
        assert result['fields']['description'] == 'hot and humid'
    
    def test_parse_integer_field(self):
        """Test parsing ILP line with integer field"""
        from iterable.datatypes.ilp import parse_line_protocol
        
        line = 'weather,location=us-midwest count=42i'
        result = parse_line_protocol(line)
        
        assert result['fields']['count'] == 42
        assert isinstance(result['fields']['count'], int)
    
    def test_parse_boolean_field(self):
        """Test parsing ILP line with boolean field"""
        from iterable.datatypes.ilp import parse_line_protocol
        
        line = 'weather,location=us-midwest active=t'
        result = parse_line_protocol(line)
        
        assert result['fields']['active'] == True
    
    def test_format_line_protocol(self):
        """Test formatting a record to ILP"""
        from iterable.datatypes.ilp import format_line_protocol
        
        record = {
            'measurement': 'temperature',
            'tags': {'sensor': 'abc123'},
            'fields': {'value': 23.5},
            'time': '1631022245000000000'
        }
        
        line = format_line_protocol(record)
        assert 'temperature' in line
        assert 'sensor=abc123' in line
        assert 'value=23.5' in line
        assert '1631022245000000000' in line
    
    def test_write_read(self):
        """Test writing and reading ILP file"""
        records = [
            {
                'measurement': 'temperature',
                'tags': {'sensor': 'sensor1'},
                'fields': {'value': 23.5},
                'time': '1631022245000000000'
            },
            {
                'measurement': 'temperature',
                'tags': {'sensor': 'sensor2'},
                'fields': {'value': 24.0},
                'time': '1631022246000000000'
            }
        ]
        
        # Write
        iterable = ILPIterable('testdata/test_ilp.ilp', mode='w')
        for record in records:
            iterable.write(record)
        iterable.close()
        
        # Read
        iterable = ILPIterable('testdata/test_ilp.ilp')
        read_records = []
        for record in iterable:
            read_records.append(record)
        iterable.close()
        
        assert len(read_records) == 2
        assert read_records[0]['measurement'] == 'temperature'
        assert read_records[0]['tags']['sensor'] == 'sensor1'
        assert read_records[0]['fields']['value'] == 23.5
    
    def test_read_bulk(self):
        """Test reading bulk records"""
        # Create test file
        iterable = ILPIterable('testdata/test_ilp_bulk.ilp', mode='w')
        for i in range(5):
            iterable.write({
                'measurement': 'test',
                'fields': {'value': float(i)},
                'time': str(1631022245000000000 + i)
            })
        iterable.close()
        
        # Read bulk
        iterable = ILPIterable('testdata/test_ilp_bulk.ilp')
        chunk = iterable.read_bulk(3)
        assert len(chunk) == 3
        
        # Read next
        record = iterable.read()
        assert record['fields']['value'] == 3.0
        iterable.close()
