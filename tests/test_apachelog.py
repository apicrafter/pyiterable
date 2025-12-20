import pytest
import os
import tempfile
from iterable.datatypes.apachelog import ApacheLogIterable


def test_apachelog_read_common():
    """Test Apache Common Log Format reading"""
    log_content = """127.0.0.1 - - [25/Dec/2023:10:00:00 +0000] "GET /index.html HTTP/1.1" 200 1234
192.168.1.1 - - [25/Dec/2023:10:01:00 +0000] "POST /api/data HTTP/1.1" 404 567"""
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log', encoding='utf-8') as tmp:
        tmp_path = tmp.name
        tmp.write(log_content)
    
    try:
        reader = ApacheLogIterable(tmp_path, mode='r', log_format='common')
        results = []
        for record in reader:
            results.append(record)
        reader.close()
        
        assert len(results) == 2
        assert results[0]['remote_host'] == '127.0.0.1'
        assert results[0]['method'] == 'GET'
        assert results[0]['status'] == '200'
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def test_apachelog_read_combined():
    """Test Apache Combined Log Format reading"""
    log_content = """127.0.0.1 - - [25/Dec/2023:10:00:00 +0000] "GET /index.html HTTP/1.1" 200 1234 "http://example.com" "Mozilla/5.0"
192.168.1.1 - - [25/Dec/2023:10:01:00 +0000] "POST /api/data HTTP/1.1" 404 567 "-" "curl/7.0" """
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log', encoding='utf-8') as tmp:
        tmp_path = tmp.name
        tmp.write(log_content)
    
    try:
        reader = ApacheLogIterable(tmp_path, mode='r', log_format='combined')
        results = []
        for record in reader:
            results.append(record)
        reader.close()
        
        assert len(results) == 2
        assert 'referer' in results[0]
        assert 'user_agent' in results[0]
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def test_apachelog_write():
    """Test Apache log writing"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log', encoding='utf-8') as tmp:
        tmp_path = tmp.name
    
    try:
        writer = ApacheLogIterable(tmp_path, mode='w', log_format='common')
        writer.write({
            'remote_host': '127.0.0.1',
            'remote_logname': '-',
            'remote_user': '-',
            'time': '25/Dec/2023:10:00:00 +0000',
            'method': 'GET',
            'request': '/index.html',
            'protocol': 'HTTP/1.1',
            'status': '200',
            'size': '1234'
        })
        writer.close()
        
        # Verify written data
        with open(tmp_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert '127.0.0.1' in content
            assert 'GET' in content
            assert '200' in content
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def test_apachelog_id():
    """Test Apache Log ID"""
    assert ApacheLogIterable.id() == 'apachelog'


def test_apachelog_flatonly():
    """Test Apache Log is flat only"""
    assert ApacheLogIterable.is_flatonly() == True


def test_apachelog_unknown_format():
    """Test Apache Log with unknown format"""
    with pytest.raises(ValueError):
        ApacheLogIterable('test.log', mode='r', log_format='unknown')
