import pytest
import os
import tempfile
from iterable.datatypes.ltsv import LTSVIterable


def test_ltsv_read():
    """Test LTSV reading"""
    ltsv_content = """time:2023-01-01T00:00:00Z\thost:example.com\tstatus:200\tmethod:GET
time:2023-01-01T00:01:00Z\thost:example.com\tstatus:404\tmethod:GET\tpath:/notfound
time:2023-01-01T00:02:00Z\thost:api.example.com\tstatus:200\tmethod:POST\tpath:/api/data"""
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.ltsv', encoding='utf-8') as tmp:
        tmp_path = tmp.name
        tmp.write(ltsv_content)
    
    try:
        reader = LTSVIterable(tmp_path, mode='r')
        results = []
        for record in reader:
            results.append(record)
        reader.close()
        
        assert len(results) == 3
        assert results[0]['time'] == '2023-01-01T00:00:00Z'
        assert results[0]['host'] == 'example.com'
        assert results[0]['status'] == '200'
        assert results[0]['method'] == 'GET'
        assert results[1]['status'] == '404'
        assert results[1]['path'] == '/notfound'
        assert results[2]['path'] == '/api/data'
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def test_ltsv_read_empty_lines():
    """Test LTSV reading with empty lines"""
    ltsv_content = """time:2023-01-01T00:00:00Z\thost:example.com\tstatus:200

time:2023-01-01T00:01:00Z\thost:example.com\tstatus:404
"""
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.ltsv', encoding='utf-8') as tmp:
        tmp_path = tmp.name
        tmp.write(ltsv_content)
    
    try:
        reader = LTSVIterable(tmp_path, mode='r')
        results = []
        for record in reader:
            results.append(record)
        reader.close()
        
        assert len(results) == 2
        assert results[0]['status'] == '200'
        assert results[1]['status'] == '404'
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def test_ltsv_write():
    """Test LTSV writing"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.ltsv', encoding='utf-8') as tmp:
        tmp_path = tmp.name
    
    try:
        writer = LTSVIterable(tmp_path, mode='w')
        writer.write({
            'time': '2023-01-01T00:00:00Z',
            'host': 'example.com',
            'status': '200',
            'method': 'GET'
        })
        writer.write({
            'time': '2023-01-01T00:01:00Z',
            'host': 'example.com',
            'status': '404',
            'path': '/notfound'
        })
        writer.close()
        
        # Verify written data
        with open(tmp_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            assert len(lines) == 2
            assert 'time:2023-01-01T00:00:00Z' in lines[0]
            assert 'host:example.com' in lines[0]
            assert 'status:200' in lines[0]
            assert 'status:404' in lines[1]
            assert 'path:/notfound' in lines[1]
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def test_ltsv_write_bulk():
    """Test LTSV bulk writing"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.ltsv', encoding='utf-8') as tmp:
        tmp_path = tmp.name
    
    try:
        writer = LTSVIterable(tmp_path, mode='w')
        records = [
            {'time': '2023-01-01T00:00:00Z', 'host': 'example.com', 'status': '200'},
            {'time': '2023-01-01T00:01:00Z', 'host': 'example.com', 'status': '404'},
            {'time': '2023-01-01T00:02:00Z', 'host': 'api.example.com', 'status': '200'}
        ]
        writer.write_bulk(records)
        writer.close()
        
        # Verify written data
        reader = LTSVIterable(tmp_path, mode='r')
        results = []
        for record in reader:
            results.append(record)
        reader.close()
        
        assert len(results) == 3
        assert results[0]['status'] == '200'
        assert results[1]['status'] == '404'
        assert results[2]['host'] == 'api.example.com'
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def test_ltsv_read_bulk():
    """Test LTSV bulk reading"""
    ltsv_content = """time:2023-01-01T00:00:00Z\thost:example.com\tstatus:200
time:2023-01-01T00:01:00Z\thost:example.com\tstatus:404
time:2023-01-01T00:02:00Z\thost:api.example.com\tstatus:200"""
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.ltsv', encoding='utf-8') as tmp:
        tmp_path = tmp.name
        tmp.write(ltsv_content)
    
    try:
        reader = LTSVIterable(tmp_path, mode='r')
        results = reader.read_bulk(2)
        assert len(results) == 2
        assert results[0]['status'] == '200'
        assert results[1]['status'] == '404'
        
        results = reader.read_bulk(2)
        assert len(results) == 1
        assert results[0]['host'] == 'api.example.com'
        
        reader.close()
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def test_ltsv_id():
    """Test LTSV ID"""
    assert LTSVIterable.id() == 'ltsv'


def test_ltsv_flatonly():
    """Test LTSV is flat only"""
    assert LTSVIterable.is_flatonly() == True


def test_ltsv_has_totals():
    """Test LTSV has totals"""
    assert LTSVIterable.has_totals() == True


def test_ltsv_totals():
    """Test LTSV totals counting"""
    ltsv_content = """time:2023-01-01T00:00:00Z\thost:example.com\tstatus:200
time:2023-01-01T00:01:00Z\thost:example.com\tstatus:404
time:2023-01-01T00:02:00Z\thost:api.example.com\tstatus:200"""
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.ltsv', encoding='utf-8') as tmp:
        tmp_path = tmp.name
        tmp.write(ltsv_content)
    
    try:
        reader = LTSVIterable(tmp_path, mode='r')
        total = reader.totals()
        assert total == 3
        reader.close()
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def test_ltsv_none_values():
    """Test LTSV handling of None values"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.ltsv', encoding='utf-8') as tmp:
        tmp_path = tmp.name
    
    try:
        writer = LTSVIterable(tmp_path, mode='w')
        writer.write({
            'key1': 'value1',
            'key2': None,
            'key3': 'value3'
        })
        writer.close()
        
        reader = LTSVIterable(tmp_path, mode='r')
        result = reader.read()
        reader.close()
        
        assert result['key1'] == 'value1'
        assert result['key2'] == ''
        assert result['key3'] == 'value3'
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def test_ltsv_numeric_values():
    """Test LTSV handling of numeric values"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.ltsv', encoding='utf-8') as tmp:
        tmp_path = tmp.name
    
    try:
        writer = LTSVIterable(tmp_path, mode='w')
        writer.write({
            'status': 200,
            'count': 42,
            'ratio': 0.95
        })
        writer.close()
        
        reader = LTSVIterable(tmp_path, mode='r')
        result = reader.read()
        reader.close()
        
        assert result['status'] == '200'
        assert result['count'] == '42'
        assert result['ratio'] == '0.95'
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
