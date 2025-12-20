import pytest
import os
import tempfile
from iterable.datatypes.turtle import TurtleIterable

try:
    from rdflib import Graph
    HAS_RDFLIB = True
except ImportError:
    HAS_RDFLIB = False


@pytest.mark.skipif(not HAS_RDFLIB, reason="RDFLib library not available")
def test_turtle_read_write():
    """Test Turtle read and write"""
    turtle_content = """@prefix ex: <http://example.org/> .
    
ex:alice ex:name "Alice" ;
         ex:age 30 .
ex:bob ex:name "Bob" ;
       ex:age 25 ."""
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.ttl', encoding='utf-8') as tmp:
        tmp_path = tmp.name
        tmp.write(turtle_content)
    
    try:
        # Read data
        reader = TurtleIterable(tmp_path, mode='r')
        results = []
        for record in reader:
            results.append(record)
        reader.close()
        
        assert len(results) > 0
        
        # Write data
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.ttl', encoding='utf-8') as tmp2:
            tmp2_path = tmp2.name
        
        writer = TurtleIterable(tmp2_path, mode='w')
        writer.write({'subject': 'http://example.org/charlie', 'name': 'Charlie', 'age': '35'})
        writer.close()
        
        # Verify written data
        with open(tmp2_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert 'charlie' in content.lower()
        
        if os.path.exists(tmp2_path):
            os.unlink(tmp2_path)
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


@pytest.mark.skipif(not HAS_RDFLIB, reason="RDFLib library not available")
def test_turtle_id():
    """Test Turtle ID"""
    assert TurtleIterable.id() == 'turtle'


@pytest.mark.skipif(not HAS_RDFLIB, reason="RDFLib library not available")
def test_turtle_flatonly():
    """Test Turtle is not flat only"""
    assert TurtleIterable.is_flatonly() == False
