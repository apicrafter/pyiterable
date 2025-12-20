# XLSX Format (Excel 2007+)

## Description

XLSX is the modern XML-based file format used by Microsoft Excel 2007 and later. It's an open standard (ECMA-376, ISO/IEC 29500) that stores spreadsheet data including formulas, formatting, and multiple sheets.

## File Extensions

- `.xlsx` - Excel 2007+ files

## Implementation Details

### Reading

The XLSX implementation:
- Uses `openpyxl` library for reading
- Supports multiple sheets (by index or name)
- Extracts column headers from first row (if not specified)
- Iterates rows efficiently
- Converts each row to a dictionary

### Writing

Writing support:
- Uses `openpyxl` for writing
- Creates new Excel files
- Writes data row by row
- Supports multiple sheets

### Key Features

- **Multiple sheets**: Can read/write specific sheet by index or name
- **Header detection**: Automatically extracts headers from first row
- **Efficient iteration**: Uses row iterators for large files
- **Totals support**: Can count total rows
- **Write support**: Can create new Excel files

## Usage

```python
from iterable.helpers.detect import open_iterable

# Basic reading (first sheet, headers from first row)
source = open_iterable('data.xlsx')
for row in source:
    print(row)
source.close()

# Read specific sheet by index
source = open_iterable('data.xlsx', iterableargs={
    'page': 1  # Second sheet (0-indexed)
})

# Read specific sheet by name
source = open_iterable('data.xlsx', iterableargs={
    'page': 'Sheet2'  # Sheet name
})

# Writing
dest = open_iterable('output.xlsx', mode='w')
dest.write({'id': 1, 'name': 'John', 'age': 30})
dest.close()
```

## Parameters

- `page` (int or str): Sheet index (int) or name (str) to read/write (default: `0`)
- `keys` (list[str]): Column names (default: extracted from first row when reading)
- `start_line` (int): Row to start reading from (default: `0`)

## Limitations

1. **openpyxl dependency**: Requires `openpyxl` package
2. **Flat data only**: Only supports tabular data
3. **File path required**: Requires filename, not stream
4. **Memory usage**: Large files may use significant memory
5. **Formatting**: Basic writing doesn't preserve Excel formatting
6. **Formulas**: Formulas are not evaluated, only values are read

## Compression Support

XLSX files are already ZIP archives internally, so additional compression may not provide much benefit. However, they can still be compressed:
- GZip (`.xlsx.gz`)
- BZip2 (`.xlsx.bz2`)
- LZMA (`.xlsx.xz`)
- LZ4 (`.xlsx.lz4`)
- ZIP (`.xlsx.zip`)
- Brotli (`.xlsx.br`)
- ZStandard (`.xlsx.zst`)

## Use Cases

- **Data analysis**: Processing Excel data
- **Reporting**: Generating Excel reports
- **Data migration**: Converting between formats
- **Business data**: Working with business spreadsheets

## Related Formats

- [XLS](xls.md) - Legacy Excel format (read-only)
- [ODS](ods.md) - OpenDocument Spreadsheet format
- [CSV](csv.md) - Simple text format
