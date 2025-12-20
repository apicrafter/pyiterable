# -*- coding: utf-8 -*-
from ..helpers.detect import open_iterable, is_flat
from ..helpers.utils import dict_generator, make_flat
from tqdm import tqdm
import logging
from typing import Dict, Any, Optional


DEFAULT_BATCH_SIZE = 50000
DEFAULT_HEADERS_DETECT_LIMIT = 1000


def convert(
    fromfile: str,
    tofile: str,
    iterableargs: Dict[str, Any] = None,
    toiterableargs: Dict[str, Any] = None,
    scan_limit: int = DEFAULT_HEADERS_DETECT_LIMIT,
    batch_size: int = DEFAULT_BATCH_SIZE,
    silent: bool = True,
    is_flatten: bool = False,
    use_totals: bool = False
) -> None:
    """
    Convert data between different file formats.
    
    Args:
        fromfile: Path to the source file
        tofile: Path to the destination file
        iterableargs: Format-specific arguments for reading the source file
                     (e.g., {'delimiter': ';', 'encoding': 'utf-8'})
        toiterableargs: Format-specific arguments for writing the destination file
                       (e.g., {'delimiter': '|', 'quotechar': "'", 'page': 0})
        scan_limit: Number of records to scan for schema detection (for flat formats)
        batch_size: Number of records to process in each batch
        silent: If False, shows progress bars during conversion
        is_flatten: If True, flattens nested structures when converting to flat formats
        use_totals: If True, uses total count for progress tracking (if available)
    
    Raises:
        FileNotFoundError: If source file doesn't exist
        ValueError: If scan_limit or batch_size are invalid
        Exception: Various exceptions from file I/O operations
    
    Examples:
        # Convert CSV with custom output delimiter
        convert('input.csv', 'output.csv', 
                toiterableargs={'delimiter': '|', 'quotechar': "'"})
        
        # Convert to Excel with specific sheet
        convert('input.jsonl', 'output.xlsx',
                toiterableargs={'page': 0})
        
        # Convert to JSON with tagname
        convert('input.csv', 'output.json',
                toiterableargs={'tagname': 'items'})
    """
    if iterableargs is None:
        iterableargs = {}
    if toiterableargs is None:
        toiterableargs = {}
    
    # Input validation
    if scan_limit is not None and scan_limit < 0:
        raise ValueError(f"scan_limit must be non-negative, got {scan_limit}")
    if batch_size <= 0:
        raise ValueError(f"batch_size must be positive, got {batch_size}")
    
    it_in = None
    it_out = None
    
    try:
        it_in = open_iterable(fromfile, mode='r', iterableargs=iterableargs)
        keys = set()  # Use set for O(1) lookups instead of O(n) with list
        n = 0
        is_flat_output = is_flat(tofile)
        
        # Schema extraction for flat output formats
        if is_flat_output:
            if not silent:
                logging.debug('Extracting schema')
            it = tqdm(it_in, total=scan_limit, desc='Schema analysis') if not silent else it_in
            for item in it:
                if scan_limit is not None and n >= scan_limit:
                    break
                n += 1
                if not is_flatten:
                    dk = dict_generator(item)
                    for i in dk:
                        k = ".".join(i[:-1])
                        keys.add(k)
                else:
                    item = make_flat(item)
                    keys.update(item.keys())
            
            # Reset after schema extraction (moved outside the loop - was a critical bug)
            it_in.reset()
            keys = sorted(keys)  # Convert to sorted list for consistent ordering
        
        # Prepare output iterable arguments
        # Merge auto-generated args (like 'keys' for flat formats) with user-provided args
        if is_flat_output:
            args = {'keys': keys}
            # Merge user-provided args (user args can override 'keys' if needed, though not recommended)
            args.update(toiterableargs)
        else:
            args = toiterableargs.copy()
        it_out = open_iterable(tofile, mode='w', iterableargs=args)

        logging.debug('Converting data')
        n = 0
        
        # Setup progress tracking
        if use_totals and it_in.has_totals():
            totals = it_in.totals()
            if totals is not None and totals > 0:
                logging.debug(f'Total rows: {totals}')
                it_in.reset()
                it = tqdm(it_in, total=totals, desc='Converting') if not silent else it_in
            else:
                # Fallback if totals() returns None or invalid value
                it_in.reset()
                it = tqdm(it_in, desc='Converting') if not silent else it_in
        else:
            it = tqdm(it_in, desc='Converting') if not silent else it_in
        
        # Process data in batches
        batch = []
        for row in it:
            n += 1
            if is_flatten:
                # Ensure all keys are present (fill missing with None)
                for k in keys:
                    if k not in row:
                        row[k] = None
                batch.append(make_flat(row))
            else:
                batch.append(row)
            
            if n % batch_size == 0:
                it_out.write_bulk(batch)
                batch = []
        
        # Write remaining batch
        if len(batch) > 0:
            it_out.write_bulk(batch)
    
    finally:
        # Ensure resources are always cleaned up, even if an error occurs
        if it_in is not None:
            try:
                it_in.close()
            except Exception as e:
                logging.warning(f"Error closing input file: {e}")
        if it_out is not None:
            try:
                it_out.close()
            except Exception as e:
                logging.warning(f"Error closing output file: {e}")
