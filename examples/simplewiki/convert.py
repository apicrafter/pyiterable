import os
from iterable.datatypes import XMLIterable, JSONLinesIterable
from iterable.codecs import BZIP2Codec, ZSTDCodec
from tqdm import tqdm

from itertools import (takewhile, repeat)

def rawincount(filename):
    f = open(filename, 'rb')
    bufgen = takewhile(lambda x: x, (f.raw.read(1024*1024) for _ in repeat(None)))
    return sum(buf.count(b'\n') for buf in bufgen)

RAW_FILE = 'data/raw/simplewiki-latest-pages-articles-multistream.xml.bz2'
RAW_INDEX = 'data/raw/simplewiki-latest-pages-articles-multistream-index.txt'
RESULT_ZSTD_JSONL_FILE = 'data/raw/simplewiki.jsonl.zst'

def run():
        codecobj = BZIP2Codec(RAW_FILE, mode='r')
        iterable = XMLIterable(codec=codecobj, tagname='page')        
        wrcodecobj = ZSTDCodec(RESULT_ZSTD_JSONL_FILE, mode='w')
        witerable = JSONLinesIterable(codec=wrcodecobj, mode='w')        
      
        num = rawincount(RAW_INDEX)
        n = 0
        for row in tqdm(iterable, total=num, desc='Converting data'):
                n += 1
                witerable.write(row)
        iterable.close()
        witerable.close()

if __name__ == "__main__":
        run()