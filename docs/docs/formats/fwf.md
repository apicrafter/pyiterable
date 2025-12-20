# Fixed Width Format (FWF)

## Description

Fixed Width Format (FWF) is a text format where each field has a fixed width in characters. This format is common in legacy systems and mainframe data exports. Fields are positioned at specific column positions, and values are padded or truncated to fit the specified width.

## File Extensions

- `.fwf` - Fixed width format files
- `.fixed` - Fixed width format files (alias)

## Implementation Details

### Reading

The FWF implementation:
- Requires `widths` and `names` parameters
- Reads line by line
- Extracts fields based on column positions
- Strips whitespace from field values

### Writing

Writing support:
- Requires `widths` and `names` parameters
- Pads or truncates values to fit field widths
- Writes fixed-width lines

### Key Features

- **Column-based**: Fields defined by column positions
- **Totals support**: Can count total rows
- **Encoding support**: Handles various text encodings
- **Simple format**: Easy to parse and generate

## Usage

```python
from iterable.helpers.detect import open_iterable

# Reading fixed-width file
source = open_iterable('data.fwf', iterableargs={
    'widths': [10, 20, 15],  # Width of each field
    'names': ['id', 'name', 'date'],  # Field names
    'encoding': 'utf-8'
})
for row in source:
    print(row)
source.close()

# Writing fixed-width file
dest = open_iterable('output.fwf', mode='w', iterableargs={
    'widths': [10, 20, 15],
    'names': ['id', 'name', 'date']
})
dest.write({'id': '1', 'name': 'John', 'date': '2024-01-01'})
dest.close()
```

## Parameters

- `widths` (list[int]): **Required** - Width of each field in characters
- `names` (list[str]): **Required** - Names of each field
- `encoding` (str): File encoding (default: `utf8`)

## Limitations

1. **Parameters required**: Must specify `widths` and `names` for both reading and writing
2. **No nested data**: Only supports flat, tabular data
3. **Fixed structure**: Field positions cannot vary
4. **Truncation**: Values longer than field width are truncated
5. **Padding**: Values shorter than field width are padded with spaces
6. **No type information**: All values are strings

## Compression Support

FWF files can be compressed with all supported codecs:
- GZip (`.fwf.gz`)
- BZip2 (`.fwf.bz2`)
- LZMA (`.fwf.xz`)
- LZ4 (`.fwf.lz4`)
- ZIP (`.fwf.zip`)
- Brotli (`.fwf.br`)
- ZStandard (`.fwf.zst`)

## Use Cases

- **Legacy systems**: Working with mainframe data exports
- **Banking**: Financial data formats
- **Government data**: Official data formats
- **Data migration**: Converting from legacy systems

## Related Formats

- [CSV](csv.md) - Delimiter-separated format
- [PSV](psv.md) - Pipe-separated format
