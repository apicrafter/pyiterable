# ODS Format (OpenDocument Spreadsheet)

## Description

ODS (OpenDocument Spreadsheet) is an open standard spreadsheet format used by LibreOffice, OpenOffice, and other office suites. It's an XML-based format stored in a ZIP archive, similar to XLSX but using open standards.

## File Extensions

- `.ods` - OpenDocument Spreadsheet files

## Implementation Details

### Reading

The ODS implementation:
- Uses `odfpy` library (preferred) or `pyexcel-ods3` library
- Supports multiple sheets (pages)
- Extracts column headers from first row (if not specified)
- Converts each row to a dictionary
- Requires file path (not stream)

### Writing

Writing support:
- Creates ODS files
- Writes data to sheets
- Supports multiple sheets

### Key Features

- **Multiple sheets**: Can read/write from specific sheet
- **Header detection**: Automatically extracts headers from first row
- **Open standard**: Open format, not proprietary
- **Totals support**: Can count total rows

## Usage

```python
from iterable.helpers.detect import open_iterable

# Basic reading (first sheet, headers from first row)
source = open_iterable('data.ods')
for row in source:
    print(row)
source.close()

# Read specific sheet
source = open_iterable('data.ods', iterableargs={
    'page': 1  # Second sheet (0-indexed)
})

# Writing
dest = open_iterable('output.ods', mode='w')
dest.write({'id': 1, 'name': 'John', 'age': 30})
dest.close()
```

## Parameters

- `page` (int): Sheet index to read/write (default: `0`)
- `keys` (list[str]): Column names (default: extracted from first row)
- `start_line` (int): Row to start reading from (default: `0`)

## Limitations

1. **Dependency**: Requires `odfpy` or `pyexcel-ods3` package
2. **File path required**: Requires filename, not stream
3. **Flat data only**: Only supports tabular data
4. **Memory usage**: Large files may use significant memory
5. **Formatting**: Basic writing doesn't preserve spreadsheet formatting

## Compression Support

ODS files are already ZIP archives internally, so additional compression may not provide much benefit. However, they can still be compressed:
- GZip (`.ods.gz`)
- BZip2 (`.ods.bz2`)
- LZMA (`.ods.xz`)
- LZ4 (`.ods.lz4`)
- ZIP (`.ods.zip`)
- Brotli (`.ods.br`)
- ZStandard (`.ods.zst`)

## Use Cases

- **OpenOffice/LibreOffice**: Working with open office suite files
- **Data migration**: Converting from proprietary formats
- **Open standards**: When you need open, non-proprietary format
- **Cross-platform**: Compatible across different office suites

## Related Formats

- [XLSX](xlsx.md) - Microsoft Excel format
- [XLS](xls.md) - Legacy Excel format
- [CSV](csv.md) - Simple text format
