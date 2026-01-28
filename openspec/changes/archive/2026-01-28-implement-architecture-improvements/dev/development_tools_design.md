# Development Tools and Utilities Design

> **⚠️ OBSOLETE**: This design document is no longer applicable. Instead, iterabledata will be used to rewrite the existing undatum command line tool. This document is kept for historical reference only.

## Executive Summary

This document designs a comprehensive set of development tools and utilities for IterableData, including CLI tools, format inspection utilities, performance profiling tools, schema inference tools, test data generators, and other developer-focused utilities. These tools will improve developer productivity and make it easier to work with IterableData.

## Current State

### Existing Tools

1. **Benchmark Scripts** (`dev/benchmarks/`)
   - `bench_memory_usage.py` - Memory usage benchmarks
   - `bench_import_open.py` - Import and open performance benchmarks

2. **Development Scripts** (`dev/scripts/`)
   - `find_missing_fixtures.py` - Find missing test fixture combinations
   - `inspect_zip.py` - Inspect ZIP file contents
   - `verify_output.py` - Verify output files

3. **Examples** (`examples/`)
   - Various example scripts for different use cases
   - MongoDB, Elasticsearch examples
   - Format conversion examples

### Limitations

1. **No CLI Tools**: No command-line interface for common operations
2. **No Format Inspection Tools**: No tools to inspect file formats, schemas, etc.
3. **No Performance Profiling Tools**: Limited performance analysis tools
4. **No Test Data Generators**: No utilities to generate test data
5. **No Documentation Generators**: No tools to generate documentation from code
6. **Scattered Tools**: Tools are in different locations, not unified

## Use Cases

### 1. Format Inspection and Analysis

**Problem**: Need to quickly inspect file format, schema, structure, sample data.

**Benefit**: CLI tool for quick file inspection without writing code.

**Example**:
```bash
# Inspect file format and schema
iterabledata inspect data.csv

# Show sample records
iterabledata inspect data.csv --sample 10

# Show schema information
iterabledata inspect data.csv --schema
```

### 2. Format Conversion (CLI)

**Problem**: Need to convert files from command line without writing Python scripts.

**Benefit**: CLI tool for quick format conversion.

**Example**:
```bash
# Convert CSV to Parquet
iterabledata convert data.csv output.parquet

# Convert with options
iterabledata convert data.csv output.jsonl --batch-size 10000
```

### 3. Performance Profiling

**Problem**: Need to profile operations, identify bottlenecks, measure performance.

**Benefit**: Tools for performance analysis and optimization.

**Example**:
```bash
# Profile file reading
iterabledata profile read data.csv

# Profile conversion
iterabledata profile convert data.csv output.parquet
```

### 4. Schema Inference and Validation

**Problem**: Need to infer schemas, validate data against schemas.

**Benefit**: Tools for schema analysis and validation.

**Example**:
```bash
# Infer schema
iterabledata schema infer data.csv

# Validate against schema
iterabledata schema validate data.csv schema.json
```

### 5. Test Data Generation

**Problem**: Need to generate test data for testing and development.

**Benefit**: Tools to generate realistic test data.

**Example**:
```bash
# Generate test CSV
iterabledata generate csv --rows 1000 --columns name,age,email

# Generate test JSONL
iterabledata generate jsonl --rows 1000 --schema schema.json
```

## Design Options

### Option 1: Single CLI Tool with Subcommands (Recommended)

**Approach**: Create `iterabledata` CLI tool with subcommands (inspect, convert, profile, etc.).

**Pros**:
- Unified interface
- Easy to discover commands
- Consistent UX
- Can use `click` or `argparse`

**Cons**:
- Single entry point
- May become large

**Implementation**:
```bash
iterabledata inspect <file>
iterabledata convert <input> <output>
iterabledata profile <operation>
iterabledata schema <command>
iterabledata generate <format>
```

### Option 2: Separate CLI Tools

**Approach**: Create separate CLI tools for each function (`iterabledata-inspect`, `iterabledata-convert`, etc.).

**Pros**:
- Modular
- Can install separately
- Smaller tools

**Cons**:
- Multiple entry points
- Harder to discover
- Inconsistent UX

### Option 3: Python API + CLI Wrappers

**Approach**: Create Python API for tools, then CLI wrappers.

**Pros**:
- Programmatic access
- CLI convenience
- Reusable components

**Cons**:
- More complex
- Need to maintain both

**Recommendation**: Option 1 (Single CLI Tool with Subcommands) - provides unified interface while maintaining modularity.

## Implementation Design

### 1. CLI Tool Structure

#### Main CLI Entry Point

```python
# In iterable/cli/__init__.py or iterable/cli/main.py
import click
from typing import Optional

@click.group()
@click.version_option()
def cli():
    """IterableData - Unified interface for data file operations."""
    pass

@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--sample', '-n', default=10, help='Number of sample records to show')
@click.option('--schema', is_flag=True, help='Show schema information')
@click.option('--format', help='Override format detection')
@click.option('--json', is_flag=True, help='Output as JSON')
def inspect(file: str, sample: int, schema: bool, format: Optional[str], json: bool):
    """Inspect file format, schema, and sample data."""
    from .commands.inspect import inspect_file
    inspect_file(file, sample=sample, schema=schema, format=format, json=json)

@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
@click.option('--batch-size', default=50000, help='Batch size for conversion')
@click.option('--progress', is_flag=True, help='Show progress bar')
@click.option('--atomic', is_flag=True, help='Use atomic writes')
def convert(input_file: str, output_file: str, batch_size: int, progress: bool, atomic: bool):
    """Convert data between formats."""
    from .commands.convert import convert_file
    convert_file(input_file, output_file, batch_size=batch_size, progress=progress, atomic=atomic)

# ... more commands ...
```

#### Entry Point Configuration

```python
# In pyproject.toml
[project.scripts]
iterabledata = "iterable.cli.main:cli"
```

### 2. Format Inspection Tool

#### Implementation

```python
# In iterable/cli/commands/inspect.py
from iterable.helpers.detect import open_iterable, detect_file_type
from iterable.helpers.capabilities import get_format_capabilities
import json

def inspect_file(
    filename: str,
    sample: int = 10,
    schema: bool = False,
    format: str | None = None,
    json_output: bool = False
):
    """Inspect file format, schema, and sample data."""
    # Detect format
    if format:
        format_id = format
    else:
        result = detect_file_type(filename)
        format_id = result.format_id
    
    # Get format capabilities
    capabilities = get_format_capabilities(format_id)
    
    # Collect information
    info = {
        "filename": filename,
        "format": format_id,
        "capabilities": {
            "read": capabilities.get("read", False),
            "write": capabilities.get("write", False),
            "streaming": capabilities.get("streaming", False),
            "bulk": capabilities.get("bulk", False),
        }
    }
    
    # Read sample data
    sample_records = []
    with open_iterable(filename, iterableargs={"format": format_id} if format else None) as source:
        for i, row in enumerate(source):
            if i >= sample:
                break
            sample_records.append(row)
        info["total_records"] = source.totals() if hasattr(source, "totals") else None
    
    info["sample_records"] = sample_records[:sample]
    
    # Infer schema if requested
    if schema:
        from iterable.helpers.schema import infer_schema
        info["schema"] = infer_schema(sample_records)
    
    # Output
    if json_output:
        print(json.dumps(info, indent=2, default=str))
    else:
        _print_inspect_info(info)

def _print_inspect_info(info: dict):
    """Print inspection information in human-readable format."""
    print(f"File: {info['filename']}")
    print(f"Format: {info['format']}")
    print(f"\nCapabilities:")
    print(f"  Read: {'✓' if info['capabilities']['read'] else '✗'}")
    print(f"  Write: {'✓' if info['capabilities']['write'] else '✗'}")
    print(f"  Streaming: {'✓' if info['capabilities']['streaming'] else '✗'}")
    print(f"  Bulk Operations: {'✓' if info['capabilities']['bulk'] else '✗'}")
    
    if info.get("total_records") is not None:
        print(f"\nTotal Records: {info['total_records']}")
    
    if info.get("schema"):
        print(f"\nSchema:")
        schema = info["schema"]
        for field, field_type in schema.items():
            print(f"  {field}: {field_type}")
    
    print(f"\nSample Records ({len(info['sample_records'])}):")
    for i, record in enumerate(info["sample_records"], 1):
        print(f"\n  Record {i}:")
        for key, value in record.items():
            print(f"    {key}: {value}")
```

### 3. Format Conversion CLI

#### Implementation

```python
# In iterable/cli/commands/convert.py
from iterable.convert.core import convert
from tqdm import tqdm

def convert_file(
    input_file: str,
    output_file: str,
    batch_size: int = 50000,
    progress: bool = False,
    atomic: bool = False
):
    """Convert file between formats."""
    if progress:
        def progress_callback(stats):
            tqdm.write(f"Progress: {stats['rows_read']} rows read, {stats['rows_written']} rows written")
        
        result = convert(
            input_file,
            output_file,
            batch_size=batch_size,
            progress=progress_callback,
            show_progress=True,
            atomic=atomic
        )
    else:
        result = convert(
            input_file,
            output_file,
            batch_size=batch_size,
            atomic=atomic
        )
    
    print(f"Conversion complete:")
    print(f"  Input rows: {result.rows_in}")
    print(f"  Output rows: {result.rows_out}")
    print(f"  Elapsed time: {result.elapsed_seconds:.2f}s")
    print(f"  Throughput: {result.throughput:.0f} rows/sec")
```

### 4. Performance Profiling Tool

#### Implementation

```python
# In iterable/cli/commands/profile.py
import cProfile
import pstats
import io
from contextlib import contextmanager

@contextmanager
def profile_context():
    """Context manager for profiling."""
    profiler = cProfile.Profile()
    profiler.enable()
    try:
        yield profiler
    finally:
        profiler.disable()

def profile_read(filename: str, format: str | None = None, limit: int | None = None):
    """Profile file reading operation."""
    with profile_context() as profiler:
        with open_iterable(filename, iterableargs={"format": format} if format else None) as source:
            count = 0
            for row in source:
                count += 1
                if limit and count >= limit:
                    break
    
    # Print profiling results
    s = io.StringIO()
    stats = pstats.Stats(profiler, stream=s)
    stats.sort_stats('cumulative')
    stats.print_stats(20)  # Top 20 functions
    print(s.getvalue())

def profile_convert(input_file: str, output_file: str):
    """Profile conversion operation."""
    with profile_context() as profiler:
        convert(input_file, output_file)
    
    # Print profiling results
    s = io.StringIO()
    stats = pstats.Stats(profiler, stream=s)
    stats.sort_stats('cumulative')
    stats.print_stats(20)
    print(s.getvalue())
```

### 5. Schema Inference and Validation Tool

#### Implementation

```python
# In iterable/cli/commands/schema.py
from iterable.helpers.schema import infer_schema, validate_schema
import json

def infer_schema_command(filename: str, output: str | None = None, sample: int = 1000):
    """Infer schema from file."""
    with open_iterable(filename) as source:
        sample_records = []
        for i, row in enumerate(source):
            if i >= sample:
                break
            sample_records.append(row)
    
    schema = infer_schema(sample_records)
    
    if output:
        with open(output, 'w') as f:
            json.dump(schema, f, indent=2)
        print(f"Schema saved to {output}")
    else:
        print(json.dumps(schema, indent=2))

def validate_schema_command(filename: str, schema_file: str):
    """Validate file against schema."""
    with open(schema_file) as f:
        schema = json.load(f)
    
    errors = []
    with open_iterable(filename) as source:
        for i, row in enumerate(source):
            try:
                validate_schema(row, schema)
            except Exception as e:
                errors.append({
                    "row": i + 1,
                    "error": str(e),
                    "data": row
                })
    
    if errors:
        print(f"Validation failed: {len(errors)} errors found")
        for error in errors[:10]:  # Show first 10 errors
            print(f"  Row {error['row']}: {error['error']}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more errors")
    else:
        print("Validation passed: All records match schema")
```

### 6. Test Data Generation Tool

#### Implementation

```python
# In iterable/cli/commands/generate.py
from iterable.helpers.detect import open_iterable
import random
import string

def generate_csv(rows: int, columns: list[str], output: str):
    """Generate test CSV file."""
    with open_iterable(output, mode='w') as dest:
        # Write header
        dest.write({col: col for col in columns})
        
        # Generate rows
        for _ in range(rows):
            row = {}
            for col in columns:
                # Generate random data based on column name
                if 'email' in col.lower():
                    row[col] = f"user{random.randint(1, 10000)}@example.com"
                elif 'age' in col.lower():
                    row[col] = random.randint(18, 80)
                elif 'name' in col.lower():
                    row[col] = ''.join(random.choices(string.ascii_letters, k=10))
                else:
                    row[col] = f"value{random.randint(1, 1000)}"
            dest.write(row)
    
    print(f"Generated {rows} rows to {output}")

def generate_jsonl(rows: int, schema_file: str | None, output: str):
    """Generate test JSONL file."""
    if schema_file:
        with open(schema_file) as f:
            schema = json.load(f)
    else:
        schema = None
    
    with open_iterable(output, mode='w') as dest:
        for _ in range(rows):
            if schema:
                row = _generate_from_schema(schema)
            else:
                row = {"id": random.randint(1, 10000), "value": f"data{random.randint(1, 1000)}"}
            dest.write(row)
    
    print(f"Generated {rows} rows to {output}")
```

### 7. Format Validation Tool

#### Implementation

```python
# In iterable/cli/commands/validate.py
def validate_file(filename: str, format: str | None = None, strict: bool = False):
    """Validate file format and data integrity."""
    errors = []
    warnings = []
    
    try:
        with open_iterable(filename, iterableargs={"format": format} if format else None) as source:
            count = 0
            for row in source:
                count += 1
                # Basic validation
                if not isinstance(row, dict):
                    errors.append(f"Row {count}: Expected dict, got {type(row)}")
    except Exception as e:
        errors.append(f"Failed to read file: {e}")
    
    # Report results
    if errors:
        print(f"Validation failed: {len(errors)} errors")
        for error in errors[:10]:
            print(f"  {error}")
        return 1
    else:
        print(f"Validation passed: {count} records processed")
        return 0
```

### 8. Documentation Generation Tool

#### Implementation

```python
# In iterable/cli/commands/docs.py
def generate_format_docs(output_dir: str):
    """Generate format documentation from code."""
    from iterable.helpers.detect import DATATYPE_REGISTRY
    
    for format_id, (module_path, class_name) in DATATYPE_REGISTRY.items():
        # Extract docstring and metadata
        # Generate markdown documentation
        # Save to output_dir
        pass
```

### 9. Benchmark Tool

#### Implementation

```python
# In iterable/cli/commands/benchmark.py
import time
from iterable.helpers.detect import open_iterable

def benchmark_read(filename: str, format: str | None = None, iterations: int = 5):
    """Benchmark file reading performance."""
    times = []
    
    for i in range(iterations):
        start = time.perf_counter()
        with open_iterable(filename, iterableargs={"format": format} if format else None) as source:
            count = sum(1 for _ in source)
        elapsed = time.perf_counter() - start
        times.append(elapsed)
        print(f"Iteration {i+1}: {elapsed:.3f}s ({count} records, {count/elapsed:.0f} records/sec)")
    
    avg_time = sum(times) / len(times)
    print(f"\nAverage: {avg_time:.3f}s ({count/avg_time:.0f} records/sec)")
```

### 10. Utility Functions

#### Helper Utilities

```python
# In iterable/cli/utils.py
def format_bytes(bytes: int) -> str:
    """Format bytes as human-readable string."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.2f} PB"

def format_duration(seconds: float) -> str:
    """Format duration as human-readable string."""
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.2f}s"
    else:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.1f}s"
```

## CLI Tool Structure

### Command Organization

```
iterabledata
├── inspect      # File inspection
├── convert      # Format conversion
├── profile      # Performance profiling
├── schema       # Schema inference/validation
├── generate     # Test data generation
├── validate     # File validation
├── benchmark    # Performance benchmarking
└── docs         # Documentation generation
```

### Installation

```python
# In pyproject.toml
[project.scripts]
iterabledata = "iterable.cli.main:cli"

[project.optional-dependencies]
cli = [
    "click>=8.0.0",  # CLI framework
    "tqdm>=4.60.0",  # Progress bars
]
```

## Usage Examples

### Format Inspection

```bash
# Basic inspection
iterabledata inspect data.csv

# With schema
iterabledata inspect data.csv --schema

# JSON output
iterabledata inspect data.csv --json

# Show more samples
iterabledata inspect data.csv --sample 50
```

### Format Conversion

```bash
# Basic conversion
iterabledata convert data.csv output.parquet

# With progress bar
iterabledata convert data.csv output.parquet --progress

# With atomic writes
iterabledata convert data.csv output.parquet --atomic

# Custom batch size
iterabledata convert data.csv output.parquet --batch-size 10000
```

### Performance Profiling

```bash
# Profile reading
iterabledata profile read data.csv

# Profile conversion
iterabledata profile convert data.csv output.parquet
```

### Schema Operations

```bash
# Infer schema
iterabledata schema infer data.csv

# Save schema to file
iterabledata schema infer data.csv --output schema.json

# Validate against schema
iterabledata schema validate data.csv schema.json
```

### Test Data Generation

```bash
# Generate CSV
iterabledata generate csv --rows 1000 --columns name,age,email --output test.csv

# Generate JSONL
iterabledata generate jsonl --rows 1000 --output test.jsonl

# Generate from schema
iterabledata generate jsonl --rows 1000 --schema schema.json --output test.jsonl
```

## Testing Strategy

### Unit Tests

1. **CLI Command Tests**
   - Test each command independently
   - Test argument parsing
   - Test error handling

2. **Integration Tests**
   - Test CLI tools with real files
   - Test end-to-end workflows
   - Test output formats

## Migration Path

### Backward Compatibility

- **No Breaking Changes**: CLI tools are additive
- **Existing Code Works**: Python API continues to work
- **Optional Installation**: CLI tools can be installed separately

### Gradual Rollout

1. **Phase 1**: Core CLI tools (inspect, convert)
2. **Phase 2**: Advanced tools (profile, schema)
3. **Phase 3**: Utility tools (generate, validate, benchmark)
4. **Phase 4**: Documentation and polish

## Recommendations

### Immediate Implementation (Phase 1)

1. **Create CLI infrastructure**
   - Set up `click` or `argparse`
   - Create main CLI entry point
   - Add to `pyproject.toml`

2. **Implement core commands**
   - `inspect` - File inspection
   - `convert` - Format conversion

3. **Documentation**
   - CLI usage guide
   - Command reference
   - Examples

### Future Enhancements (Phase 2+)

1. **Advanced tools**
   - Performance profiling
   - Schema operations
   - Test data generation

2. **Integration**
   - IDE plugins
   - VS Code extension
   - Jupyter notebook integration

3. **Advanced features**
   - Interactive mode
   - Configuration files
   - Plugin system for custom commands

## Conclusion

Development tools and utilities significantly improve developer productivity by providing convenient CLI access to common operations, format inspection, performance profiling, and other development tasks. The recommended approach is to create a unified CLI tool with subcommands, maintaining modularity while providing a consistent user experience.

All tools are additive and optional, maintaining backward compatibility with the existing Python API. The system can be extended with additional tools and utilities as needed.
