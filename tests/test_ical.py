# -*- coding: utf-8 -*-
import pytest
import os
from iterable.datatypes import ICALIterable

try:
    from icalendar import Calendar, Event
    HAS_ICALENDAR = True
except ImportError:
    HAS_ICALENDAR = False

try:
    import ics
    HAS_ICS = True
except ImportError:
    HAS_ICS = False


@pytest.mark.skipif(not HAS_ICALENDAR and not HAS_ICS, reason="iCal support requires 'icalendar' or 'ics' package")
class TestICAL:
    def test_id(self):
        datatype_id = ICALIterable.id()
        assert datatype_id == 'ical'

    def test_flatonly(self):
        flag = ICALIterable.is_flatonly()
        assert flag == False

    def test_openclose(self):
        """Test basic open/close"""
        test_file = 'testdata/test_ical.ics'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('BEGIN:VCALENDAR\nVERSION:2.0\nBEGIN:VEVENT\nSUMMARY:Test Event\nEND:VEVENT\nEND:VCALENDAR\n')
        
        iterable = ICALIterable(test_file)
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_one(self):
        """Test reading single event"""
        test_file = 'testdata/test_ical_read.ics'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('BEGIN:VCALENDAR\nVERSION:2.0\nBEGIN:VEVENT\nSUMMARY:Test Event\nEND:VEVENT\nEND:VCALENDAR\n')
        
        iterable = ICALIterable(test_file)
        record = iterable.read()
        assert isinstance(record, dict)
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_read_bulk(self):
        """Test reading bulk events"""
        test_file = 'testdata/test_ical_bulk.ics'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('BEGIN:VCALENDAR\nVERSION:2.0\n')
            f.write('BEGIN:VEVENT\nSUMMARY:Event 1\nEND:VEVENT\n')
            f.write('BEGIN:VEVENT\nSUMMARY:Event 2\nEND:VEVENT\n')
            f.write('END:VCALENDAR\n')
        
        iterable = ICALIterable(test_file)
        chunk = iterable.read_bulk(2)
        assert isinstance(chunk, list)
        assert len(chunk) > 0
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

    def test_reset(self):
        """Test reset functionality"""
        test_file = 'testdata/test_ical_reset.ics'
        os.makedirs('testdata', exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('BEGIN:VCALENDAR\nVERSION:2.0\nBEGIN:VEVENT\nSUMMARY:Test\nEND:VEVENT\nEND:VCALENDAR\n')
        
        iterable = ICALIterable(test_file)
        record1 = iterable.read()
        iterable.reset()
        record2 = iterable.read()
        assert record1 == record2
        iterable.close()
        
        if os.path.exists(test_file):
            os.unlink(test_file)

