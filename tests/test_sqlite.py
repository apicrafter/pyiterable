import pytest
import os
import tempfile
import sqlite3
from iterable.datatypes.sqlite import SQLiteIterable


def test_sqlite_read_write():
    """Test SQLite read and write"""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.sqlite') as tmp:
        tmp_path = tmp.name
    
    try:
        # Create a test database with data
        conn = sqlite3.connect(tmp_path)
        conn.execute("CREATE TABLE test_table (name TEXT, age INTEGER, city TEXT)")
        conn.execute("INSERT INTO test_table VALUES ('Alice', 30, 'New York')")
        conn.execute("INSERT INTO test_table VALUES ('Bob', 25, 'London')")
        conn.execute("INSERT INTO test_table VALUES ('Charlie', 35, 'Tokyo')")
        conn.commit()
        conn.close()
        
        # Read data
        reader = SQLiteIterable(tmp_path, mode='r', table='test_table')
        results = []
        for record in reader:
            results.append(record)
        reader.close()
        
        assert len(results) == 3
        assert results[0]['name'] == 'Alice'
        assert results[0]['age'] == 30
        
        # Test totals
        reader2 = SQLiteIterable(tmp_path, mode='r', table='test_table')
        total = reader2.totals()
        reader2.close()
        assert total == 3
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def test_sqlite_write():
    """Test SQLite write"""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.sqlite') as tmp:
        tmp_path = tmp.name
    
    try:
        # Write data
        writer = SQLiteIterable(tmp_path, mode='w', table='test_table')
        writer.write({'name': 'Alice', 'age': 30, 'city': 'New York'})
        writer.write({'name': 'Bob', 'age': 25, 'city': 'London'})
        writer.close()
        
        # Read back
        reader = SQLiteIterable(tmp_path, mode='r', table='test_table')
        results = list(reader)
        reader.close()
        
        assert len(results) == 2
        assert results[0]['name'] == 'Alice'
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def test_sqlite_write_bulk():
    """Test SQLite bulk write"""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.sqlite') as tmp:
        tmp_path = tmp.name
    
    try:
        test_data = [
            {'name': 'Alice', 'age': 30, 'city': 'New York'},
            {'name': 'Bob', 'age': 25, 'city': 'London'},
            {'name': 'Charlie', 'age': 35, 'city': 'Tokyo'}
        ]
        
        # Write bulk
        writer = SQLiteIterable(tmp_path, mode='w', table='test_table')
        writer.write_bulk(test_data)
        writer.close()
        
        # Read back
        reader = SQLiteIterable(tmp_path, mode='r', table='test_table')
        results = list(reader)
        reader.close()
        
        assert len(results) == 3
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def test_sqlite_query():
    """Test SQLite with custom query"""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.sqlite') as tmp:
        tmp_path = tmp.name
    
    try:
        # Create test data
        conn = sqlite3.connect(tmp_path)
        conn.execute("CREATE TABLE test_table (name TEXT, age INTEGER)")
        conn.execute("INSERT INTO test_table VALUES ('Alice', 30)")
        conn.execute("INSERT INTO test_table VALUES ('Bob', 25)")
        conn.commit()
        conn.close()
        
        # Read with query
        reader = SQLiteIterable(tmp_path, mode='r', query='SELECT name FROM test_table WHERE age > 26')
        results = list(reader)
        reader.close()
        
        assert len(results) == 1
        assert results[0]['name'] == 'Alice'
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def test_sqlite_id():
    """Test SQLite ID"""
    assert SQLiteIterable.id() == 'sqlite'


def test_sqlite_flatonly():
    """Test SQLite is flat only"""
    assert SQLiteIterable.is_flatonly() == True
