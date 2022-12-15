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

Supported file compression: GZip, BZip2, LZMA (.xz)


## Requirements

Python 3.8+

## Documentation

In progress

## Usage and examples

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



## Examples

See [tests](tests/) for example usage