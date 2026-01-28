---
name: testing-patterns
description: Testing conventions, patterns, and best practices for IterableData. Use when writing tests, debugging test failures, or establishing test coverage.
---

# Testing Patterns

## Test Structure

### File Naming

- Test files: `test_*.py` in `tests/` directory
- One test file per format/feature: `test_csv.py`, `test_parquet.py`
- Test classes: `Test*` (e.g., `TestCSV`, `TestParquet`)
- Test functions: `test_*` (e.g., `test_read`, `test_write`)

### Running Tests

```bash
# All tests
pytest --verbose

# Specific test file
pytest tests/test_csv.py -v

# Specific test function
pytest tests/test_csv.py::TestCSV::test_read -v

# Parallel execution
pytest -n auto

# With coverage
pytest --cov=iterable --cov-report=html
```

## Test Patterns

### Basic Read Test

```python
def test_read(self):
    with open_iterable('testdata/test.csv') as source:
        rows = list(source)
        assert len(rows) > 0
        assert isinstance(rows[0], dict)
```

### Basic Write Test

```python
def test_write(self, tmp_path):
    output = tmp_path / 'output.csv'
    data = [{'col1': 'val1', 'col2': 'val2'}]
    
    with open_iterable(output, 'w') as dest:
        dest.write_bulk(data)
    
    # Verify written data
    with open_iterable(output) as source:
        rows = list(source)
        assert rows == data
```

### Compression Tests

```python
def test_gzip_compression(self):
    with open_iterable('testdata/test.csv.gz') as source:
        rows = list(source)
        assert len(rows) > 0
```

### Bulk Operations Test

```python
def test_read_bulk(self):
    with open_iterable('testdata/test.csv') as source:
        chunks = list(source.read_bulk(size=100))
        assert len(chunks) > 0
        assert all(isinstance(chunk, list) for chunk in chunks)
```

### Edge Cases

```python
def test_empty_file(self):
    with open_iterable('testdata/empty.csv') as source:
        rows = list(source)
        assert rows == []

def test_malformed_data(self):
    with pytest.raises(ValueError):
        with open_iterable('testdata/malformed.csv') as source:
            list(source)
```

### Missing Dependencies

```python
@pytest.mark.skipif(
    not HAS_OPTIONAL_DEPENDENCY,
    reason="Optional dependency not installed"
)
def test_optional_format(self):
    # Test format that requires optional dependency
    pass
```

## Test Data

- Store test files in `testdata/` directory
- Use descriptive names: `test_simple.csv`, `test_nested.json`
- Include edge cases: empty files, malformed data
- Test with various encodings for text formats
- Test with compression: `.gz`, `.bz2`, `.zst`, etc.

## Test Coverage

### Required Coverage

- All public methods
- Error handling paths
- Edge cases (empty files, malformed data)
- Compression variants
- Encoding variants (for text formats)

### Coverage Report

```bash
pytest --cov=iterable --cov-report=html
# Opens htmlcov/index.html
```

## Test Organization

### Class-Based Tests

```python
class TestCSV:
    def test_read(self):
        pass
    
    def test_write(self):
        pass
    
    def test_read_bulk(self):
        pass
```

### Fixtures

Use pytest fixtures for common setup:

```python
@pytest.fixture
def sample_data():
    return [{'col1': 'val1', 'col2': 'val2'}]

def test_write_with_fixture(sample_data, tmp_path):
    output = tmp_path / 'output.csv'
    with open_iterable(output, 'w') as dest:
        dest.write_bulk(sample_data)
```

## Python Version Support

Tests should pass for:
- Python 3.10
- Python 3.11
- Python 3.12

Use `pytest` markers if version-specific behavior needed:

```python
@pytest.mark.skipif(
    sys.version_info < (3, 11),
    reason="Requires Python 3.11+"
)
```

## Best Practices

1. **Always use context managers**: `with open_iterable(...) as source:`
2. **Use temporary directories**: `tmp_path` fixture for write tests
3. **Test both read and write**: Verify round-trip when possible
4. **Test compression**: Include compressed variants
5. **Test edge cases**: Empty files, single row, large files
6. **Skip optional dependencies**: Use `@pytest.mark.skipif` appropriately
7. **Clear assertions**: Use descriptive assert messages
8. **Isolated tests**: Each test should be independent

## Common Test Patterns

### Round-Trip Test

```python
def test_round_trip(self, tmp_path):
    original = [{'a': 1, 'b': 2}, {'a': 3, 'b': 4}]
    output = tmp_path / 'output.csv'
    
    # Write
    with open_iterable(output, 'w') as dest:
        dest.write_bulk(original)
    
    # Read back
    with open_iterable(output) as source:
        result = list(source)
    
    assert result == original
```

### Streaming Test

```python
def test_streaming(self):
    with open_iterable('large_file.csv') as source:
        count = 0
        for row in source:
            count += 1
            if count >= 100:
                break
        assert count == 100
```

## Debugging Tests

### Verbose Output

```bash
pytest -vv  # Very verbose
pytest -s   # Show print statements
```

### Run Last Failed

```bash
pytest --lf  # Last failed
pytest --ff  # Failed first
```

### Debug Specific Test

```bash
pytest tests/test_csv.py::TestCSV::test_read -v -s
```
