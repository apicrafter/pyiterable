# TOML Format

## Description

TOML (Tom's Obvious, Minimal Language) is a configuration file format designed to be easy to read and write. It's used by many modern tools and projects for configuration files. TOML supports nested data structures, arrays, and tables.

## File Extensions

- `.toml` - TOML files

## Implementation Details

### Reading

The TOML implementation:
- Uses `tomli` (or `toml`) library for parsing
- Supports array of tables (common TOML pattern)
- Converts TOML structures to Python dictionaries
- Handles nested tables and arrays

### Writing

Writing support:
- Uses `tomli-w` (or `toml`) for writing
- Writes TOML format
- Supports nested structures

### Key Features

- **Nested data**: Supports complex nested structures
- **Array of tables**: Handles TOML's array of tables pattern
- **Human-readable**: Easy to read and edit
- **Configuration format**: Designed for configuration files

## Usage

```python
from iterable.helpers.detect import open_iterable

# Basic reading
source = open_iterable('config.toml')
for row in source:
    print(row)
source.close()

# Writing
dest = open_iterable('output.toml', mode='w')
dest.write({'name': 'John', 'age': 30})
dest.close()
```

## Parameters

- `encoding` (str): File encoding (default: `utf8`)

## Limitations

1. **Dependency**: Requires `tomli`/`tomli-w` or `toml` package
2. **Memory usage**: Entire file is loaded into memory
3. **Structure complexity**: Complex nested structures may be difficult to iterate
4. **Array of tables**: TOML's array of tables pattern may require specific structure

## Compression Support

TOML files can be compressed with all supported codecs:
- GZip (`.toml.gz`)
- BZip2 (`.toml.bz2`)
- LZMA (`.toml.xz`)
- LZ4 (`.toml.lz4`)
- ZIP (`.toml.zip`)
- Brotli (`.toml.br`)
- ZStandard (`.toml.zst`)

## Use Cases

- **Configuration files**: Application and tool configuration
- **Project settings**: Project configuration files
- **Data exchange**: Human-readable data format

## Related Formats

- [YAML](yaml.md) - Another configuration format
- [INI](ini.md) - Simpler configuration format
- [JSON](json.md) - Similar structure, less readable
