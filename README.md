# Iterable Data

*Work in progress. Documentation in progress*

Iterable data is a Python lib to read data files row by row and write data files.
Iterable classes are similar to files or csv.DictReader or reading parquet files row by row. 

This library was written to simplify data processing and conversion between formats.
 
Supported file types:
* BSON
* JSON
* NDJSON (JSON lines)
* XML
* XLS
* XLSX
* Parquet
* ORC
* Avro
* Pickle

Supported file compression: GZip, BZip2, LZMA (.xz), LZ4, ZIP

## Why writing this lib? 

Python has many high-quality data processing tools and libraries, especially pandas and other data frames lib. The only issue with most of them is flat data. Data frames don't support complex data types, and you must *flatten* data each time. 

pyiterable helps you read any data as a Python dictionary instead of flattening data.
It makes it much easier to work with such data sources as JSON, NDJSON, or BSON files.

This code is used in several tools written by its author. It's command line tool [undatum](https://github.com/datacoon/undatum) and data processing ETL engine [datacrafter](https://github.com/apicrafter/datacrafter)


## Requirements

Python 3.8+


## Installation

```pip install iterabledata``` or use this repository

## Documentation

In progress. Please see usage and examples.

## Usage and examples


### Read compressed CSV file 

Read compressed csv.xz file

```{python}

from iterable.helpers.detect import open_iterable

source = open_iterable('data.csv.xz')
n = 0
for row in iterable:
    n += 1
    # Add data processing code here
    if n % 1000 == 0: print('Processing %d' % (n))
```

### Detect encoding and file delimiter

Detects encoding and delimiter of the selected CSV file and use it to open as iterable

```{python}

from iterable.helpers.detect import open_iterable
from iterable.helpers.utils import detect_encoding, detect_delimiter

delimiter = detect_delimiter('data.csv')
encoding = detect_encoding('data.csv')

source = open_iterable('data.csv', iterableargs={'encoding' : encoding['encoding'], 'delimiter' : delimiter)
n = 0
for row in iterable:
    n += 1
    # Add data processing code here
    if n % 1000 == 0: print('Processing %d' % (n))
```


### Convert Parquet file to BSON compressed with LZMA using pipeline

Uses pipeline class to iterate through parquet file and convert its selected fields to JSON lines (NDJSON)

```{python}

from iterable.helpers.detect import open_iterable
from iterable.pipeline import pipeline

source = open_iterable('data/data.parquet')
destination = open_iterable('data/data.jsonl.xz', mode='w')

def extract_fields(record, state):
    out = {}
    record = dict(record)
    print(record)
    for k in ['name',]:
        out[k] = record[k]
    return out

def print_process(stats, state):
    print(stats)

pipeline(source, destination=destination, process_func=extract_fields, trigger_on=2, trigger_func=print_process, final_func=print_process, start_state={})

```

### Convert gzipped JSON lines (NDJSON) file to BSON compressed with LZMA 

Reads each row from JSON lines file using Gzip codec and writes BSON data using LZMA codec

```{python}

from iterable.datatypes import JSONLinesIterable, BSONIterable
from iterable.codecs import GZIPCodec, LZMACodec


codecobj = GZIPCodec('data.jsonl.gz', mode='r', open_it=True)
iterable = JSONLinesIterable(codec=codecobj)        
codecobj = LZMACodec('data.bson.xz', mode='wb', open_it=False)
write_iterable = BSONIterable(codec=codecobj, mode='w')
n = 0
for row in iterable:
    n += 1
    if n % 10000 == 0: print('Processing %d' % (n))
    write_iterable.write(row)
```



## More examples and tests

See [tests](tests/) for example usage and tests