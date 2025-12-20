# YAML Format

## Description

YAML (YAML Ain't Markup Language) is a human-readable data serialization format. It's commonly used for configuration files and data exchange. YAML supports complex nested data structures and is more readable than JSON for human editing.

## File Extensions

- `.yaml` - YAML files
- `.yml` - YAML files (alias)

## Implementation Details

### Reading

The YAML implementation:
- Uses `pyyaml` library for parsing
- Supports multiple YAML documents (separated by `---`)
- Handles lists and dictionaries
- Converts YAML documents to Python objects

### Writing

Writing support:
- Writes each record as a separate YAML document
- Separates documents with `---`
- Supports Unicode characters
- Uses block style (not flow style) for readability

### Key Features

- **Multiple documents**: Supports YAML files with multiple documents
- **Nested data**: Supports complex nested structures
- **Human-readable**: Easy to read and edit
- **Unicode support**: Full Unicode character support

## Usage

```python
from iterable.helpers.detect import open_iterable

# Basic reading
source = open_iterable('data.yaml')
for row in source:
    print(row)
source.close()

# Writing
dest = open_iterable('output.yaml', mode='w')
dest.write({'name': 'John', 'age': 30})
dest.write({'name': 'Jane', 'age': 25})
dest.close()
```

## Parameters

- `encoding` (str): File encoding (default: `utf8`)

## Limitations

1. **pyyaml dependency**: Requires `pyyaml` package
2. **Memory usage**: Multiple documents are loaded into memory
3. **Performance**: Slower than binary formats
4. **Write format**: Each record written as separate document with `---` separator

## Compression Support

YAML files can be compressed with all supported codecs:
- GZip (`.yaml.gz`)
- BZip2 (`.yaml.bz2`)
- LZMA (`.yaml.xz`)
- LZ4 (`.yaml.lz4`)
- ZIP (`.yaml.zip`)
- Brotli (`.yaml.br`)
- ZStandard (`.yaml.zst`)

## Use Cases

- **Configuration files**: Application and system configuration
- **Data exchange**: Human-readable data format
- **Documentation**: Embedding data in documentation
- **DevOps**: Infrastructure as code (Ansible, Kubernetes)

## Related Formats

- [JSON](json.md) - Similar structure, less readable
- [TOML](toml.md) - Another configuration format
- [INI](ini.md) - Simpler configuration format
