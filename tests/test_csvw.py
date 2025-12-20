# -*- coding: utf-8 -*- 
import pytest
import os
import json
from iterable.datatypes import CSVWIterable
from fixdata import FIXTURES

# Create fixture file if it doesn't exist
FIXTURE_FILE = 'fixtures/2cols6rows.csv'
METADATA_FILE = 'fixtures/2cols6rows.csv-metadata.json'

def setup_module():
    """Create fixture file if it doesn't exist"""
    if not os.path.exists(FIXTURE_FILE):
        import csv
        os.makedirs(os.path.dirname(FIXTURE_FILE), exist_ok=True)
        with open(FIXTURE_FILE, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'name'])
            writer.writeheader()
            for record in FIXTURES:
                writer.writerow(record)
    
    if not os.path.exists(METADATA_FILE):
        # Create CSVW metadata file
        metadata = {
            "@context": "http://www.w3.org/ns/csvw",
            "url": "2cols6rows.csv",
            "tableSchema": {
                "columns": [
                    {
                        "name": "id",
                        "titles": "id",
                        "datatype": {"base": "string"}
                    },
                    {
                        "name": "name",
                        "titles": "name",
                        "datatype": {"base": "string"}
                    }
                ]
            }
        }
        os.makedirs(os.path.dirname(METADATA_FILE), exist_ok=True)
        with open(METADATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)

class TestCSVW:
    def test_id(self):
        datatype_id = CSVWIterable.id()
        assert datatype_id == 'csvw'

    def test_flatonly(self):
        flag = CSVWIterable.is_flatonly()
        assert flag == True

    def test_openclose(self):
        iterable = CSVWIterable(FIXTURE_FILE, metadata_file=METADATA_FILE)        
        iterable.close()

    def test_has_totals(self):
        iterable = CSVWIterable(FIXTURE_FILE, metadata_file=METADATA_FILE)
        assert CSVWIterable.has_totals() == True
        total = iterable.totals()
        assert total == len(FIXTURES) + 1  # +1 for header
        iterable.close()

    def test_read(self):
        iterable = CSVWIterable(FIXTURE_FILE, metadata_file=METADATA_FILE)
        row = iterable.read()
        assert isinstance(row, dict)
        assert 'id' in row
        assert 'name' in row
        iterable.close()

    def test_read_all(self):
        iterable = CSVWIterable(FIXTURE_FILE, metadata_file=METADATA_FILE)
        n = 0
        for row in iterable:
            assert isinstance(row, dict)
            n += 1
        assert n == len(FIXTURES)
        iterable.close()

    def test_write_read(self):
        iterable = CSVWIterable('testdata/2cols6rows_test.csvw', mode='w', 
                               options={'keys': ['id', 'name']})
        # Write records
        for record in FIXTURES:
            iterable.write(record)
        iterable.close()
        
        iterable = CSVWIterable('testdata/2cols6rows_test.csvw')
        n = 0
        for row in iterable:
            assert isinstance(row, dict)
            n += 1
        assert n == len(FIXTURES)
        iterable.close()
