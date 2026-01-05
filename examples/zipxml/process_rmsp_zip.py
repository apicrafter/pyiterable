
import os
import sys
import zipfile
import logging
from tqdm import tqdm

# Add parent directory to path to import iterabledata if not installed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from iterable import open_iterable
from iterable.datatypes.xml import XMLIterable

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def process_rmsp_zip(zip_path, output_path, limit=0):
    """
    Process RMSP ZIP file with XMLs and convert to JSONL.ZST
    
    Args:
        zip_path: Path to source ZIP file
        output_path: Path to output JSONL.ZST file
        limit: Max number of files to process
    """
    if not os.path.exists(zip_path):
        logger.error(f"Input file not found: {zip_path}")
        return

    logger.info(f"Processing {zip_path} -> {output_path}")

    # specific tag to extract from XMLs
    target_tag = 'Документ'

    # Open output file using iterabledata's smart opener
    # It automatically detects jsonl.zst and sets up ZSTD compression
    try:
        output = open_iterable(output_path, mode='w')
    except Exception as e:
        logger.error(f"Failed to open output file: {e}")
        return

    total_records = 0
    files_processed = 0

    try:
        with output:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                # get list of xml files
                xml_files = [f for f in zf.namelist() if f.endswith('.xml')]
                logger.info(f"Found {len(xml_files)} XML files in archive")

                for filename in tqdm(xml_files, desc="Processing files"):
                    try:
                        with zf.open(filename, 'r') as xml_file:
                            # Use XMLIterable to parse valid XML files
                            # We pass the stream directly from zip
                            source = XMLIterable(
                                stream=xml_file, 
                                tagname=target_tag
                            )
                            
                            batch = []
                            for record in source:
                                # Add filename to record for traceability
                                record['_source_file'] = filename
                                batch.append(record)
                                
                                if len(batch) >= 1000:
                                    output.write_bulk(batch)
                                    total_records += len(batch)
                                    batch = []
                            
                            # Write remaining records
                            if batch:
                                output.write_bulk(batch)
                                total_records += len(batch)
                            
                            files_processed += 1
                            
                            if limit > 0 and files_processed >= limit:
                                logger.info(f"Limit of {limit} files reached.")
                                break

                            
                    except Exception as e:
                        logger.warning(f"Error processing file {filename}: {e}")
                        continue
                        
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        # cleanup if needed
    
    logger.info(f"Completed. Processed {files_processed} files. Total records: {total_records}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Convert RMSP ZIP to JSONL.ZST")
    parser.add_argument("--input", default="/Users/ibegtin/workspace/data/rmsp/data-10122025-structure-10062025.zip", help="Input ZIP file")
    parser.add_argument("--output", default="rmsp_data_sample.jsonl.zst", help="Output JSONL.ZST file")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of files to process (0 for all)")
    
    args = parser.parse_args()
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if not os.path.isabs(args.output):
        output_path = os.path.join(current_dir, args.output)
    else:
        output_path = args.output
        
    process_rmsp_zip(args.input, output_path, limit=args.limit)
