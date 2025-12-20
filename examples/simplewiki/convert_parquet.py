import os
import sys
from iterable.datatypes import JSONLinesIterable, ParquetIterable
from iterable.codecs import ZSTDCodec

BATCH_SIZE = 10000

def run():
        RAW_FILE = sys.argv[1]
        RESULT_PARQUET_FILE = sys.argv[2]
        codec_obj = ZSTDCodec(RAW_FILE, mode='r')
        iterable = JSONLinesIterable(codec=codec_obj)        
        writerable = ParquetIterable(RESULT_PARQUET_FILE, mode='w', use_pandas=False, adapt_schema=True, batch_size=BATCH_SIZE)
      
        n = 0
        rows = []
        for row in iterable:
                n += 1     
                rows.append(row)
                if n % BATCH_SIZE == 0:
                        writerable.write_bulk(rows)
                        rows = []
        if len(rows) > 0:
                writerable.write_bulk(rows)
        iterable.close()
        writerable.close()

if __name__ == "__main__":
        run()