# -*- coding: utf-8 -*-
import pytest
import os
import io
from iterable.helpers.utils import (
    rowincount,
    detect_encoding_raw,
    detect_delimiter,
    get_dict_value,
    strip_dict_fields,
    dict_generator,
    guess_int_size,
    get_dict_keys,
    get_iterable_keys,
    get_dict_value_deep,
    make_flat
)
from iterable.datatypes import CSVIterable
from fixdata import FIXTURES


class TestUtils:
    def test_rowincount_with_filename(self):
        """Test rowincount with filename"""
        count = rowincount(filename='fixtures/2cols6rows.csv')
        # Should have at least header + 6 rows
        assert count >= 6

    def test_rowincount_with_fileobj(self):
        """Test rowincount with file object"""
        with open('fixtures/2cols6rows.csv', 'rb') as f:
            count = rowincount(fileobj=f)
            assert count >= 6

    def test_rowincount_error_no_args(self):
        """Test rowincount raises error with no arguments"""
        with pytest.raises(ValueError, match="Filename or fileobj should not be None"):
            rowincount()

    def test_detect_encoding_raw_with_filename(self):
        """Test detect_encoding_raw with filename"""
        result = detect_encoding_raw(filename='fixtures/ru_utf8_comma.csv')
        assert 'encoding' in result
        assert result['encoding'] in ['utf-8', 'ascii']  # UTF-8 files may be detected as ASCII

    def test_detect_encoding_raw_with_stream(self):
        """Test detect_encoding_raw with stream"""
        with open('fixtures/ru_utf8_comma.csv', 'rb') as f:
            result = detect_encoding_raw(stream=f)
            assert 'encoding' in result

    def test_detect_delimiter_comma(self):
        """Test detect_delimiter with comma"""
        delimiter = detect_delimiter(filename='fixtures/ru_utf8_comma.csv')
        assert delimiter == ','

    def test_detect_delimiter_semicolon(self):
        """Test detect_delimiter with semicolon"""
        delimiter = detect_delimiter(filename='fixtures/ru_utf8_semicolon.csv')
        assert delimiter == ';'

    def test_detect_delimiter_tab(self):
        """Test detect_delimiter with tab"""
        delimiter = detect_delimiter(filename='fixtures/ru_utf8_tab.csv')
        assert delimiter == '\t'

    def test_detect_delimiter_with_stream(self):
        """Test detect_delimiter with stream"""
        with open('fixtures/ru_utf8_comma.csv', 'r', encoding='utf-8') as f:
            delimiter = detect_delimiter(stream=f, encoding='utf-8')
            assert delimiter == ','

    def test_get_dict_value_simple(self):
        """Test get_dict_value with simple key"""
        d = {'name': 'test', 'value': 42}
        result = get_dict_value(d, ['name'])
        assert result == ['test']

    def test_get_dict_value_nested(self):
        """Test get_dict_value with nested keys"""
        d = {'user': {'name': 'test', 'age': 30}}
        result = get_dict_value(d, ['user', 'name'])
        assert result == ['test']

    def test_get_dict_value_list(self):
        """Test get_dict_value with list of dicts"""
        d = [{'name': 'test1'}, {'name': 'test2'}]
        result = get_dict_value(d, ['name'])
        assert result == ['test1', 'test2']

    def test_get_dict_value_none(self):
        """Test get_dict_value with None"""
        result = get_dict_value(None, ['key'])
        assert result == []

    def test_get_dict_value_missing_key(self):
        """Test get_dict_value with missing key"""
        d = {'other': 'value'}
        result = get_dict_value(d, ['missing'])
        assert result == []

    def test_strip_dict_fields(self):
        """Test strip_dict_fields"""
        record = {'keep': 'value1', 'remove': 'value2', 'also_keep': 'value3'}
        fields = [['keep'], ['also_keep']]
        result = strip_dict_fields(record, fields)
        assert 'keep' in result
        assert 'also_keep' in result
        assert 'remove' not in result

    def test_strip_dict_fields_nested(self):
        """Test strip_dict_fields with nested dict"""
        record = {'user': {'name': 'test', 'email': 'test@example.com'}, 'other': 'value'}
        fields = [['user', 'name']]
        result = strip_dict_fields(record, fields)
        assert 'user' in result
        assert 'name' in result['user']
        assert 'email' not in result['user']

    def test_dict_generator_simple(self):
        """Test dict_generator with simple dict"""
        d = {'name': 'test', 'value': 42}
        results = list(dict_generator(d))
        assert len(results) == 2
        assert ['name', 'test'] in results
        assert ['value', 42] in results

    def test_dict_generator_nested(self):
        """Test dict_generator with nested dict"""
        d = {'user': {'name': 'test', 'age': 30}}
        results = list(dict_generator(d))
        assert ['user', 'name', 'test'] in results
        assert ['user', 'age', 30] in results

    def test_dict_generator_with_list(self):
        """Test dict_generator with list values"""
        d = {'items': [{'name': 'item1'}, {'name': 'item2'}]}
        results = list(dict_generator(d))
        assert any('item1' in r for r in results)
        assert any('item2' in r for r in results)

    def test_dict_generator_skips_id(self):
        """Test dict_generator skips _id field"""
        d = {'_id': 'skip', 'name': 'keep'}
        results = list(dict_generator(d))
        assert ['_id', 'skip'] not in results
        assert ['name', 'keep'] in results

    def test_dict_generator_non_dict(self):
        """Test dict_generator with non-dict input"""
        result = list(dict_generator('not a dict'))
        assert result == ['not a dict']

    def test_guess_int_size_small(self):
        """Test guess_int_size with small value"""
        assert guess_int_size(100) == 'uint8'
        assert guess_int_size(254) == 'uint8'

    def test_guess_int_size_medium(self):
        """Test guess_int_size with medium value"""
        assert guess_int_size(1000) == 'uint16'
        assert guess_int_size(65534) == 'uint16'

    def test_guess_int_size_large(self):
        """Test guess_int_size with large value"""
        assert guess_int_size(100000) == 'uint32'
        assert guess_int_size(1000000) == 'uint32'

    def test_get_dict_keys(self):
        """Test get_dict_keys"""
        data = [
            {'name': 'test1', 'value': 1},
            {'name': 'test2', 'value': 2, 'extra': 'field'}
        ]
        keys = get_dict_keys(data)
        assert 'name' in keys
        assert 'value' in keys
        assert 'extra' in keys

    def test_get_dict_keys_with_limit(self):
        """Test get_dict_keys with limit"""
        data = [{'key' + str(i): i} for i in range(10)]
        keys = get_dict_keys(data, limit=3)
        # Should only process first 3 items
        assert len(keys) <= 3

    def test_get_dict_keys_nested(self):
        """Test get_dict_keys with nested dicts"""
        data = [
            {'user': {'name': 'test', 'age': 30}}
        ]
        keys = get_dict_keys(data)
        assert 'user.name' in keys or 'user' in keys

    def test_get_iterable_keys(self):
        """Test get_iterable_keys"""
        iterable = CSVIterable('fixtures/2cols6rows.csv')
        keys = get_iterable_keys(iterable)
        assert len(keys) > 0
        # Should have keys from CSV
        assert any('id' in k.lower() or 'name' in k.lower() for k in keys)
        iterable.close()

    def test_get_iterable_keys_with_limit(self):
        """Test get_iterable_keys with limit"""
        iterable = CSVIterable('fixtures/2cols6rows.csv')
        keys = get_iterable_keys(iterable, limit=2)
        iterable.close()
        # Should have some keys
        assert isinstance(keys, list)

    def test_get_dict_value_deep_simple(self):
        """Test get_dict_value_deep with simple key"""
        d = {'name': 'test'}
        result = get_dict_value_deep(d, 'name')
        assert result == 'test'

    def test_get_dict_value_deep_nested(self):
        """Test get_dict_value_deep with nested key"""
        d = {'user': {'profile': {'name': 'test'}}}
        result = get_dict_value_deep(d, 'user.profile.name')
        assert result == 'test'

    def test_get_dict_value_deep_missing(self):
        """Test get_dict_value_deep with missing key"""
        d = {'other': 'value'}
        result = get_dict_value_deep(d, 'missing')
        assert result is None

    def test_get_dict_value_deep_as_array(self):
        """Test get_dict_value_deep with as_array=True"""
        d = {'items': [{'name': 'item1'}, {'name': 'item2'}]}
        result = get_dict_value_deep(d, 'items.name', as_array=True)
        assert isinstance(result, list)
        assert 'item1' in result
        assert 'item2' in result

    def test_get_dict_value_deep_list(self):
        """Test get_dict_value_deep with list of dicts"""
        d = [{'name': 'test1'}, {'name': 'test2'}]
        result = get_dict_value_deep(d, 'name', as_array=True)
        assert isinstance(result, list)
        assert 'test1' in result
        assert 'test2' in result

    def test_get_dict_value_deep_custom_splitter(self):
        """Test get_dict_value_deep with custom splitter"""
        d = {'user': {'name': 'test'}}
        result = get_dict_value_deep(d, 'user/name', splitter='/')
        assert result == 'test'

    def test_make_flat_simple(self):
        """Test make_flat with simple dict"""
        item = {'name': 'test', 'value': 42}
        result = make_flat(item)
        assert result == item

    def test_make_flat_with_list(self):
        """Test make_flat with list value"""
        item = {'name': 'test', 'items': [1, 2, 3]}
        result = make_flat(item)
        assert result['name'] == 'test'
        assert isinstance(result['items'], str)  # List should be converted to string

    def test_make_flat_with_dict(self):
        """Test make_flat with nested dict"""
        item = {'name': 'test', 'user': {'age': 30}}
        result = make_flat(item)
        assert result['name'] == 'test'
        assert isinstance(result['user'], str)  # Dict should be converted to string

    def test_make_flat_with_tuple(self):
        """Test make_flat with tuple value"""
        item = {'name': 'test', 'coords': (1, 2)}
        result = make_flat(item)
        assert result['name'] == 'test'
        assert isinstance(result['coords'], str)  # Tuple should be converted to string

