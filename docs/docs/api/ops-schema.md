---
sidebar_position: 13
title: Schema Operations
description: Schema inference and generation in multiple formats
---

# Schema Operations

The `iterable.ops.schema` module provides functions for inferring schemas from data and converting them to various schema formats.

## Overview

Schema operations help you understand and document data structure:
- **Infer schemas** from datasets automatically
- **Convert to multiple formats** (JSON Schema, Avro, Parquet, Cerberus, YAML)
- **Detect constraints** (min/max, length, enums)
- **Validate data** against schemas

## Functions

### `infer()`

Infer schema from an iterable dataset.

Detects field names, types, nullability, and optionally constraints.

```python
from iterable.ops import schema

# Basic schema inference
sch = schema.infer("data.csv")
print(sch["fields"]["price"]["type"])

# With date detection and constraints
sch = schema.infer("data.csv", detect_dates=True, detect_constraints=True)
```

**Parameters:**
- `iterable`: An iterable of row dictionaries, or a file path/stream
- `detect_dates`: Whether to detect date and datetime fields (default: False)
- `detect_constraints`: Whether to detect constraints (min/max, length, etc.) (default: False)
- `sample_size`: Number of rows to sample for inference (default: 10000)

**Returns:** Dictionary containing:
- `fields`: Dictionary mapping field names to metadata:
  - `type`: Inferred type (string, integer, float, boolean, etc.)
  - `nullable`: Whether field contains null values
  - `sample_values`: Sample values from the dataset
- `constraints`: Dictionary of detected constraints (if `detect_constraints=True`):
  - `min`, `max`: Minimum and maximum values (for numeric fields)
  - `min_length`, `max_length`: String length constraints
  - `possible_values`: Enum-like value sets

### `to_jsonschema()`

Convert inferred schema to JSON Schema format.

```python
from iterable.ops import schema

sch = schema.infer("data.csv")
json_schema = schema.to_jsonschema(sch)
print(json.dumps(json_schema, indent=2))
```

**Parameters:**
- `schema`: Schema dictionary from `infer()`

**Returns:** JSON Schema document (compatible with JSON Schema validators)

### `to_yaml()`

Convert inferred schema to YAML format.

```python
from iterable.ops import schema

sch = schema.infer("data.csv")
yaml_str = schema.to_yaml(sch)
print(yaml_str)
```

**Parameters:**
- `schema`: Schema dictionary from `infer()`

**Returns:** YAML string (requires `pyyaml` for full support, falls back to JSON-like format)

### `to_cerberus()`

Convert inferred schema to Cerberus validation schema format.

```python
from iterable.ops import schema
from cerberus import Validator

sch = schema.infer("data.csv")
cerberus_schema = schema.to_cerberus(sch)

validator = Validator(cerberus_schema)
is_valid = validator.validate({"name": "John", "age": 30})
```

**Parameters:**
- `schema`: Schema dictionary from `infer()`

**Returns:** Cerberus-compatible schema dictionary

### `to_avro()`

Convert inferred schema to Avro schema format.

```python
from iterable.ops import schema

sch = schema.infer("data.csv")
avro_schema = schema.to_avro(sch, namespace="com.example")
print(json.dumps(avro_schema, indent=2))
```

**Parameters:**
- `schema`: Schema dictionary from `infer()`
- `namespace`: Avro namespace (default: "iterabledata")

**Returns:** Avro schema JSON

### `to_parquet_metadata()`

Convert inferred schema to Parquet metadata format.

```python
from iterable.ops import schema

sch = schema.infer("data.csv")
parquet_meta = schema.to_parquet_metadata(sch)
```

**Parameters:**
- `schema`: Schema dictionary from `infer()`

**Returns:** Parquet-compatible schema metadata dictionary

### `validate()`

Validate data against an inferred or provided schema.

```python
from iterable.ops import schema

sch = schema.infer("data.csv")
result = schema.validate("data.csv", sch)
print(f"Valid: {len(result['valid_rows'])}, Invalid: {len(result['invalid_rows'])}")
```

**Parameters:**
- `iterable`: An iterable of row dictionaries, or a file path/stream
- `schema`: Schema dictionary from `infer()` or manually created
- `strict`: If True, enforce strict type checking and flag extra/missing fields

**Returns:** Dictionary containing:
- `valid_rows`: List of valid rows
- `invalid_rows`: List of (row, errors) tuples
- `stats`: Validation statistics

## Examples

### Basic Schema Inference

```python
from iterable.ops import schema

# Infer schema from file
sch = schema.infer("data.csv")

# Access field information
for field_name, field_info in sch["fields"].items():
    print(f"{field_name}: {field_info['type']} (nullable: {field_info['nullable']})")
```

### Schema with Constraints

```python
from iterable.ops import schema

# Infer schema with constraints
sch = schema.infer("products.csv", detect_constraints=True)

# Check constraints
if "price" in sch.get("constraints", {}):
    constraints = sch["constraints"]["price"]
    print(f"Price range: ${constraints['min']} - ${constraints['max']}")
    print(f"Possible values: {constraints.get('possible_values', 'N/A')}")
```

### Generate JSON Schema

```python
from iterable.ops import schema
import json

# Infer and convert to JSON Schema
sch = schema.infer("data.csv")
json_schema = schema.to_jsonschema(sch)

# Save to file
with open("schema.json", "w") as f:
    json.dump(json_schema, f, indent=2)

# Use with JSON Schema validators
from jsonschema import validate as jsonschema_validate
jsonschema_validate({"name": "John", "age": 30}, json_schema)
```

### Generate Avro Schema

```python
from iterable.ops import schema
import json

# Infer and convert to Avro
sch = schema.infer("data.csv")
avro_schema = schema.to_avro(sch, namespace="com.example")

# Save to file
with open("schema.avsc", "w") as f:
    json.dump(avro_schema, f, indent=2)
```

### Generate Cerberus Schema

```python
from iterable.ops import schema
from cerberus import Validator

# Infer and convert to Cerberus
sch = schema.infer("data.csv")
cerberus_schema = schema.to_cerberus(sch)

# Use with Cerberus validator
validator = Validator(cerberus_schema)
for row in data:
    if validator.validate(row):
        process(row)
    else:
        print(f"Validation errors: {validator.errors}")
```

### Validate Against Schema

```python
from iterable.ops import schema

# Infer schema
sch = schema.infer("data.csv")

# Validate new data against schema
result = schema.validate("new_data.csv", sch)

print(f"Validation results:")
print(f"  Valid rows: {len(result['valid_rows'])}")
print(f"  Invalid rows: {len(result['invalid_rows'])}")

# Process invalid rows
for row, errors in result["invalid_rows"]:
    print(f"  Row errors: {errors}")
```

### Strict Schema Validation

```python
from iterable.ops import schema

sch = schema.infer("data.csv")

# Strict validation flags extra/missing fields
result = schema.validate("data.csv", sch, strict=True)

for row, errors in result["invalid_rows"]:
    if "Extra fields" in str(errors):
        print(f"Row has extra fields: {row}")
```

### Schema for Documentation

```python
from iterable.ops import schema

# Generate schema documentation
sch = schema.infer("data.csv", detect_constraints=True)

print("Dataset Schema:")
print("=" * 50)
for field_name, field_info in sch["fields"].items():
    print(f"\n{field_name}:")
    print(f"  Type: {field_info['type']}")
    print(f"  Nullable: {field_info['nullable']}")
    if field_name in sch.get("constraints", {}):
        constraints = sch["constraints"][field_name]
        if "min" in constraints:
            print(f"  Range: {constraints['min']} - {constraints['max']}")
        if "possible_values" in constraints:
            print(f"  Possible values: {constraints['possible_values']}")
```

### Combining with Other Operations

```python
from iterable.ops import schema, stats, inspect

# Analyze dataset structure
analysis = inspect.analyze("data.csv")

# Infer detailed schema
sch = schema.infer("data.csv", detect_constraints=True)

# Generate JSON Schema for API documentation
json_schema = schema.to_jsonschema(sch)

# Validate data quality
result = schema.validate("data.csv", sch)
print(f"Data quality: {result['stats']['valid']}/{result['stats']['total']} valid")
```

## Schema Format Details

### JSON Schema

JSON Schema is widely used for API validation and documentation:

```python
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "name": {"type": "string"},
    "age": {"type": "integer", "minimum": 0}
  },
  "required": ["name"]
}
```

### Avro Schema

Avro schemas are used for data serialization:

```python
{
  "type": "record",
  "name": "Record",
  "namespace": "iterabledata",
  "fields": [
    {"name": "name", "type": "string"},
    {"name": "age", "type": ["null", "long"], "default": null}
  ]
}
```

### Cerberus Schema

Cerberus schemas are used for Python data validation:

```python
{
  "name": {"type": "string", "required": True},
  "age": {"type": "integer", "min": 0}
}
```

## Performance Notes

- **Sampling**: Schema inference uses sampling (default 10,000 rows) for performance
- **Large datasets**: Inference remains fast even on very large files
- **Constraint detection**: May be slower when `detect_constraints=True` due to value analysis

## Integration with Validation

Schemas can be used with the validation framework:

```python
from iterable.ops import schema
from iterable import validate

# Infer schema
sch = schema.infer("data.csv")

# Validate against schema
result = schema.validate("data.csv", sch)

# Or use validation rules based on schema
rules = {}
for field_name, field_info in sch["fields"].items():
    if not field_info.get("nullable", True):
        rules[field_name] = ["required"]

validate_results = validate.iterable("data.csv", rules)
```
