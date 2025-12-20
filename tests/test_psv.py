import pytest
import os
import tempfile
from iterable.datatypes.psv import PSVIterable, SSVIterable


def test_psv_read_write():
    """Test PSV (pipe-separated values) read and write"""
    test_data = [
        {'name': 'Alice', 'age': '30', 'city': 'New York'},
        {'name': 'Bob', 'age': '25', 'city': 'London'},
        {'name': 'Charlie', 'age': '35', 'city': 'Tokyo'}
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.psv', encoding='utf-8') as tmp:
        tmp_path = tmp.name
        # Write header
        tmp.write('name|age|city\n')
        # Write data
        for record in test_data:
            tmp.write(f"{record['name']}|{record['age']}|{record['city']}\n")
    
    try:
        # Read data
        reader = PSVIterable(tmp_path, mode='r')
        results = []
        for record in reader:
            results.append(record)
        reader.close()
        
        assert len(results) == 3
        assert results[0]['name'] == 'Alice'
        assert results[0]['age'] == '30'
        
        # Write data
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.psv', encoding='utf-8') as tmp2:
            tmp2_path = tmp2.name
        
        writer = PSVIterable(tmp2_path, mode='w', keys=['name', 'age', 'city'])
        for record in test_data:
            writer.write(record)
        writer.close()
        
        # Verify written data
        with open(tmp2_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            assert 'name|age|city' in lines[0]
            assert 'Alice|30|New York' in lines[1]
        
        if os.path.exists(tmp2_path):
            os.unlink(tmp2_path)
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def test_ssv_read_write():
    """Test SSV (semicolon-separated values) read and write"""
    test_data = [
        {'name': 'Alice', 'age': '30', 'city': 'New York'},
        {'name': 'Bob', 'age': '25', 'city': 'London'}
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.ssv', encoding='utf-8') as tmp:
        tmp_path = tmp.name
        # Write header
        tmp.write('name;age;city\n')
        # Write data
        for record in test_data:
            tmp.write(f"{record['name']};{record['age']};{record['city']}\n")
    
    try:
        # Read data
        reader = SSVIterable(tmp_path, mode='r')
        results = []
        for record in reader:
            results.append(record)
        reader.close()
        
        assert len(results) == 2
        assert results[0]['name'] == 'Alice'
        
        # Write data
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.ssv', encoding='utf-8') as tmp2:
            tmp2_path = tmp2.name
        
        writer = SSVIterable(tmp2_path, mode='w', keys=['name', 'age', 'city'])
        for record in test_data:
            writer.write(record)
        writer.close()
        
        # Verify written data
        with open(tmp2_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            assert 'name;age;city' in lines[0]
            assert 'Alice;30;New York' in lines[1]
        
        if os.path.exists(tmp2_path):
            os.unlink(tmp2_path)
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def test_psv_id():
    """Test PSV ID"""
    assert PSVIterable.id() == 'psv'


def test_ssv_id():
    """Test SSV ID"""
    assert SSVIterable.id() == 'ssv'


def test_psv_flatonly():
    """Test PSV is flat only"""
    assert PSVIterable.is_flatonly() == True


def test_ssv_flatonly():
    """Test SSV is flat only"""
    assert SSVIterable.is_flatonly() == True
