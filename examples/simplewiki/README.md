## Wiki dumps processing example

This example show how quickly convert wiki dump to jsonl.zst file which could be queried with duckdb.

## Steps to use
0. Install 'iterable' lib ```pip install iterabledata```
1. Download latest files https://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-pages-articles-multistream.xml.bz2 and https://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-pages-articles-multistream-index.txt.bz2 to the data/raw
2. Go to 'data/raw' directory.
3. Run 'bunzip2 simplewiki-latest-pages-articles-multistream-index.txt.bz2'
4. Go back to 'examples/simplewiki'
5. Run 'convert.py'
6. Make sure that 'data/raw/simplewiki/simplewiki.jsonl.zst' generated
7. Run 'enrich.py' . This script will add 'categories' column with categories names in wiki pages
8. Make sure that 'data/raw/simplewiki/simplewiki_prepared.jsonl.zst' generated
9. Test results with duckdb. Run 'duckdb' and use query "select * from 'simplewiki_prepared.jsonl.zst' where list_contains(categories, 'Argentina');" as example
