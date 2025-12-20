# -*- coding: utf-8 -*- 
import pytest
import os
from iterable.datatypes import TOMLIterable
from fixdata import FIXTURES

# Create fixture file if it doesn't exist
FIXTURE_FILE = 'fixtures/2cols6rows.toml'

def setup_module():
    """Create fixture file if it doesn't exist"""
    try:
        import tomli_w
        if not os.path.exists(FIXTURE_FILE):
            with open(FIXTURE_FILE, 'w', encoding='utf-8') as f:
                # Create TOML with array of tables
                for record in FIXTURES:
                    f.write(f"[[item]]\n")
                    f.write(f"id = \"{record['id']}\"\n")
                    f.write(f"name = \"{record['name']}\"\n")
                    f.write("\n")
    except ImportError:
        try:
            import toml
            if not os.path.exists(FIXTURE_FILE):
                data = {'item': FIXTURES}
                with open(FIXTURE_FILE, 'w', encoding='utf-8') as f:
                    toml.dump(data, f)
        except ImportError:
            pass  # Skip if toml packages not available

class TestTOML:
    def test_id(self):
        try:
            datatype_id = TOMLIterable.id()
            assert datatype_id == 'toml'
        except ImportError:
            pytest.skip("TOML support requires tomli/tomli-w or toml package")

    def test_flatonly(self):
        try:
            flag = TOMLIterable.is_flatonly()
            assert flag == False
        except ImportError:
            pytest.skip("TOML support requires tomli/tomli-w or toml package")

    def test_openclose(self):
        try:
            if os.path.exists(FIXTURE_FILE):
                iterable = TOMLIterable(FIXTURE_FILE)        
                iterable.close()
        except ImportError:
            pytest.skip("TOML support requires tomli/tomli-w or toml package")

    def test_read(self):
        try:
            if os.path.exists(FIXTURE_FILE):
                iterable = TOMLIterable(FIXTURE_FILE)
                row = iterable.read()
                assert isinstance(row, dict)
                iterable.close()
        except ImportError:
            pytest.skip("TOML support requires tomli/tomli-w or toml package")
