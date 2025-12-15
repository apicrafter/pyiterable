# -*- coding: utf-8 -*-
from ..helpers.detect import open_iterable, is_flat
from ..helpers.utils import dict_generator, make_flat
from tqdm import tqdm
import logging
import time


DEFAULT_BATCH_SIZE = 50000
DEFAULT_HEADERS_DETECT_LIMIT = 1000

ITERABLE_OPTIONS_KEYS = ['tagname', 'delimiter', 'encoding', 'start_line', 'page']

DEFAULT_BATCH_SIZE = 50000


def convert(fromfile:str, tofile:str, iterableargs:dict={}, scan_limit:int=DEFAULT_HEADERS_DETECT_LIMIT, batch_size:int=DEFAULT_BATCH_SIZE, silent:bool=True, is_flatten:bool=False, use_totals:bool=False):
    it_in = open_iterable(fromfile, mode='r', iterableargs=iterableargs)       
    keys = []
    n = 0 
    it = tqdm(it_in, total=scan_limit, desc='Schema analysis') if not silent else it_in
    is_flat_output = is_flat(tofile)
    if is_flat_output:
        if not silent: logging.debug('Extracting schema')
        for item in it:
            if scan_limit is not None and n > scan_limit:
                break
            n += 1                
            if not is_flatten:
                dk = dict_generator(item)
                for i in dk:
                    k = ".".join(i[:-1])
                    if k not in keys:
                        keys.append(k)
            else:
                item = make_flat(item)
                for k in item.keys():
                    if k not in keys:
                        keys.append(k)

            it_in.reset()
    if is_flat_output:
        args = {'keys' : keys}
    else:
        args = {}
    it_out = open_iterable(tofile, mode='w', iterableargs=args)

    logging.debug('Converting data')
    n = 0
    if use_totals and it_in.has_totals():
        totals = it_in.totals()
        logging.debug(f'Total rows: {totals}')
        it_in.reset()
        it = tqdm(it_in, total=totals, desc='Converting') if not silent else it_in
    else:
        it = tqdm(it_in, desc='Converting') if not silent else it_in
    batch = []
    for row in it:
        n += 1 
        if is_flatten:
            for k in keys:
                if k not in row.keys(): 
                    row[k] = None              
            batch.append(make_flat(row))
        else:
            batch.append(row)
        if n % batch_size == 0:
            it_out.write_bulk(batch)
            batch = []
    if len(batch) > 0: 
        it_out.write_bulk(batch)
    it_in.close()
    it_out.close()
