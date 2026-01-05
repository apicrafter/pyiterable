# RMSP Data Converter Example

This example demonstrates how to process a large ZIP file containing thousands of XML files from the Russian Registry of Small and Medium Enterprises (RMSP). It converts these XML documents into a single, compressed JSONL file using the `iterabledata` library.

## What it does

1.  Reads a ZIP archive as a stream.
2.  Iterates through each XML file inside the archive without extracting it to disk.
3.  Parses the XML content, specifically extracting the `<Документ>` (Document) tag.
4.  Converts the XML structure into a JSON object.
5.  Writes the result to a `.jsonl.zst` file, which is a Zstandard-compressed JSON Lines format.

## Data Source

This example is designed to work with the RMSP open data dumps.
You can download the dataset used in this example from the Federal Tax Service (FTS) open data portal:

*   **Page URL:** [https://www.nalog.gov.ru/opendata/7707329152-rsmp/](https://www.nalog.gov.ru/opendata/7707329152-rsmp/)
*   **Direct File URL (Example):** [https://file.nalog.ru/opendata/7707329152-rsmp/data-10122025-structure-10062025.zip](https://file.nalog.ru/opendata/7707329152-rsmp/data-10122025-structure-10062025.zip)

**Note:** The file name changes with each update (dates in the filename).

## Usage

Run the script from the command line:

```bash
python3 process_rmsp_zip.py --input /path/to/data-10122025-structure-10062025.zip --output output_data.jsonl.zst
```

### Options

*   `--input`: Path to the source ZIP file (default: `/Users/ibegtin/workspace/data/rmsp/data-10122025-structure-10062025.zip`)
*   `--output`: Path to the output file (default: `rmsp_data_sample.jsonl.zst` in the current directory)
*   `--limit`: Number of files to process (useful for testing). Default is 0 (process all).

### Example (Test Run)

To process only the first 100 XML files:

```bash
python3 process_rmsp_zip.py --limit 100
```
