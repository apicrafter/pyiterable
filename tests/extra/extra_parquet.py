from iterable.datatypes import ParquetIterable

# -*- coding: utf-8 -*- 
FIXTURES = [
{"id": "1", "name": "John"},
{"id": "2", "name": "Mary"},
{"id": "3", "name": "Michael"},
{"id": "4", "name": "Anna"},
{"id": "5", "name": "Orban"},
{"id": "6", "name": "Lucy"}
]

FIXTURES_TYPES = [
{"id": 1, "name": "John"},
{"id": 2, "name": "Mary"},
{"id": 3, "name": "Michael"},
{"id": 4, "name": "Anna"},
{"id": 5, "name": "Orban"},
{"id": 6, "name": "Lucy"}
]


FIXTURES_BOOKS = [
{"title":{"@lang":"en","#text":"Everyday Italian"},"author":"Giada De Laurentiis","year":"2005","price":"30.00","@category":"cooking"},
{"title":{"@lang":"en","#text":"Harry Potter"},"author":"J K. Rowling","year":"2005","price":"29.99","@category":"children"},
{"title":{"@lang":"en","#text":"Learning XML"},"author":"Erik T. Ray","year":"2003","price":"39.95","@category":"web"}
]

iterable = ParquetIterable('../testdata/2cols6rows.parquet', mode='w', keys=['id', 'name'], use_pandas=False, compression=None)
iterable.write_bulk(FIXTURES)
iterable.close()
iterable = ParquetIterable('../testdata/2cols6rows.parquet', mode='r')
n = 0
for row in iterable:
    n += 1
    print(n, row)
iterable.close()

iterable = ParquetIterable('../testdata/2cols6rows_pd.parquet', mode='w', keys=['id', 'name'], use_pandas=True, compression=None)
iterable.write_bulk(FIXTURES)
iterable.close()

iterable = ParquetIterable('../testdata/2cols6rows.parquet', mode='r')
n = 0
for row in iterable:
    n += 1
    print(n, row)
iterable.close()
