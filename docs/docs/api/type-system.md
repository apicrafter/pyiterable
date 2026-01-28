---
sidebar_position: 20
title: Type System
description: Type hints and typed helper functions for type-safe data processing
---

# Type System

IterableData provides comprehensive type hints and typed helper functions for modern Python projects using static type checkers like mypy, pyright, or pyre.

## Overview

The type system includes:
- **Complete type annotations** across the public API
- **Type aliases** for common data structures (`Row`, `IterableArgs`, `CodecArgs`)
- **Typed helper functions** for converting dict-based rows to dataclasses or Pydantic models
- **Type marker file** (`py.typed`) to indicate package supports type checking

## Type Aliases

Import type aliases for use in your own type annotations:

```python
from iterable import Row, IterableArgs, CodecArgs

# Row represents a data row as a dictionary
def process_row(row: Row) -> None:
    name = row.get('name')
    age = row.get('age')

# IterableArgs for configuration dictionaries
def configure_csv(config: IterableArgs) -> None:
    delimiter = config.get('delimiter', ',')
    encoding = config.get('encoding', 'utf-8')

# CodecArgs for compression codec configuration
def configure_compression(codec_config: CodecArgs) -> None:
    level = codec_config.get('level', 6)
```

### Available Type Aliases

- **`Row`**: `dict[str, Any]` - A data row represented as a dictionary
- **`IterableArgs`**: `dict[str, Any]` - Iterable-specific configuration arguments
- **`CodecArgs`**: `dict[str, Any]` - Codec-specific configuration arguments

## Type Hints in API

All public API functions and methods have complete type annotations:

```python
from iterable import open_iterable
from iterable.base import BaseIterable

# open_iterable() has type hints
source: BaseIterable = open_iterable('data.csv')

# BaseIterable methods have type hints
row: Row = source.read()
rows: list[Row] = source.read_bulk(100)

# write() and write_bulk() accept Row types
source.write(row)
source.write_bulk(rows)
```

## Typed Helper Functions

### `as_dataclasses()`

Convert dict-based rows into dataclass instances for type-safe data processing.

```python
from dataclasses import dataclass
from iterable import open_iterable, as_dataclasses

@dataclass
class Person:
    name: str
    age: int
    email: str

with open_iterable('people.csv') as source:
    for person in as_dataclasses(source, Person):
        # person is typed as Person
        print(f"{person.name} is {person.age} years old")
        # IDE autocomplete works for person.name, person.age, etc.
```

**Parameters:**
- `iterable`: The iterable to read rows from (`BaseIterable`)
- `dataclass_type`: The dataclass type to convert rows to (`type[T]`)
- `skip_empty`: Whether to skip empty rows (default: `True`)

**Returns:**
- Iterator of dataclass instances (`Iterator[T]`)

**Behavior:**
- Only includes fields that exist in the dataclass (extra fields are ignored)
- Raises `ValueError` if required fields are missing
- Works with any dataclass that can be instantiated from keyword arguments

**Example with Extra Fields:**

```python
@dataclass
class Person:
    name: str
    age: int
    # email field not included

# CSV has: name,age,email,city
# Only name and age are used, email and city are ignored
with open_iterable('people.csv') as source:
    for person in as_dataclasses(source, Person):
        print(person.name)  # Works
        # person.email  # AttributeError - field not in dataclass
```

### `as_pydantic()`

Convert dict-based rows into Pydantic model instances with optional validation.

```python
from pydantic import BaseModel
from iterable import open_iterable, as_pydantic

class PersonModel(BaseModel):
    name: str
    age: int
    email: str

# With validation (default)
with open_iterable('people.csv') as source:
    for person in as_pydantic(source, PersonModel, validate=True):
        # Rows are validated against the model schema
        # Invalid rows raise ValueError with ValidationError details
        print(f"{person.name} ({person.email})")
```

**Parameters:**
- `iterable`: The iterable to read rows from (`BaseIterable`)
- `model_type`: The Pydantic model type to convert rows to (`type[T]`)
- `skip_empty`: Whether to skip empty rows (default: `True`)
- `validate`: Whether to validate rows against the model schema (default: `True`)

**Returns:**
- Iterator of Pydantic model instances (`Iterator[T]`)

**Raises:**
- `ImportError`: If pydantic is not installed (with helpful installation message)
- `TypeError`: If model_type is not a Pydantic BaseModel subclass
- `ValueError`: If validation fails and validate=True

**Installation:**

```bash
pip install iterabledata[pydantic]
# or
pip install pydantic>=2.0.0
```

**Example with Validation Disabled:**

```python
# Skip validation for faster processing (use with caution)
with open_iterable('people.csv') as source:
    for person in as_pydantic(source, PersonModel, validate=False):
        # No validation, faster but less safe
        print(person.name)
```

**Example with Type Conversion:**

Pydantic automatically converts types:

```python
class PersonModel(BaseModel):
    name: str
    age: int  # Automatically converts string "30" to int 30
    email: str

# CSV: name,age,email
# Alice,30,alice@example.com
# Bob,25,bob@example.com

with open_iterable('people.csv') as source:
    for person in as_pydantic(source, PersonModel):
        print(type(person.age))  # <class 'int'> (converted from string)
```

## Type Checking

The package includes a `py.typed` marker file, indicating to type checkers that the package supports type checking.

### Using mypy

```bash
pip install mypy
mypy your_code.py
```

### Using pyright

```bash
pip install pyright
pyright your_code.py
```

### Example Type-Checked Code

```python
from iterable import open_iterable, Row, as_dataclasses
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int

def process_people(filename: str) -> list[Person]:
    people: list[Person] = []
    with open_iterable(filename) as source:
        for person in as_dataclasses(source, Person):
            people.append(person)
    return people

# Type checker validates:
# - filename is str ✓
# - return type is list[Person] ✓
# - person is Person type ✓
```

## Benefits

- **IDE Support**: Better autocomplete, type checking, and documentation in modern IDEs
- **Error Prevention**: Catch type-related mistakes before runtime
- **Code Clarity**: Type hints serve as inline documentation
- **Refactoring Safety**: Type checkers help ensure refactoring doesn't break code
- **Team Collaboration**: Type hints make code easier to understand and maintain

## Backward Compatibility

All type hints are **additive** and don't affect runtime behavior:
- Existing code continues to work without modifications
- Type hints are optional and don't change function behavior
- No performance impact (type hints are ignored at runtime)

## See Also

- [Basic Usage](/getting-started/basic-usage#type-hints-and-type-safety) - Type hints examples
- [Migration Guide](/getting-started/migration-guide#type-hint-improvements) - Type hint improvements overview
