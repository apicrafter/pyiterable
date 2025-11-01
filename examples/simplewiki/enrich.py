from itertools import (takewhile, repeat)
from iterable.datatypes import JSONLinesIterable
from iterable.codecs import ZSTDCodec
import json
from tqdm import tqdm
import csv
import wikitextparser as wtp

CATEGORY_TEXT = 'Category'

def clean_text(s):
    """Cleans up wikitext"""
    s = wtp.remove_markup(s.replace('<br/>', ' ')).strip()
    return s

def rawincount(filename):
    f = open(filename, 'rb')
    bufgen = takewhile(lambda x: x, (f.raw.read(1024*1024) for _ in repeat(None)))
    return sum(buf.count(b'\n') for buf in bufgen)

RAW_INDEX = 'data/raw/simplewiki-latest-pages-articles-multistream-index.txt'
RESULT_ZSTD_JSONL_FILE = 'data/raw/simplewiki.jsonl.zst'
ENRICHED_ZSTD_JSONL_FILE = 'data/raw/simplewiki_prepared.jsonl.zst'

def run():
    total = rawincount(RAW_INDEX)
    in_codec = ZSTDCodec(RESULT_ZSTD_JSONL_FILE, mode='r')
    out_codec = ZSTDCodec(ENRICHED_ZSTD_JSONL_FILE, mode='w')
    in_iterable = JSONLinesIterable(codec=in_codec, mode='w')
    out_iterable = JSONLinesIterable(codec=out_codec, mode='w')

    for data in tqdm(in_iterable, total=total):        
        if data['revision']['text'] is not None and '#text' in data['revision']['text'].keys():            
            p = wtp.parse(data['revision']['text']['#text'])
            tn = 0 
            categories = []
            for w in p.wikilinks:
                if w.title.find(CATEGORY_TEXT + ':') > -1:
                    categories.append(w.title.split(CATEGORY_TEXT + ':')[1])
            data['categories'] = categories
            out_iterable.write(data)
    in_iterable.close()        
    out_iterable.close()
    pass


if __name__ == "__main__":
    run()