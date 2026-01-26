# Type System Specification

## ADDED Requirements

### Requirement: Type Hints for Public API
The library SHALL provide complete type annotations for all public API functions and methods, enabling static type checking with tools like mypy, pyright, and pyre.

#### Scenario: Type checking open_iterable
- **WHEN** a user calls `open_iterable()` with type checking enabled
- **THEN** the function signature shows correct parameter types (`str`, `Literal["r", "w"]`, etc.) and return type (`BaseIterable`)
- **AND** type checkers can validate argument types and return value usage

#### Scenario: Type checking iterable methods
- **WHEN** a user calls methods on a `BaseIterable` instance (e.g., `read()`, `write()`, `read_bulk()`)
- **THEN** method signatures show correct parameter and return types
- **AND** type checkers can validate that `read()` returns `dict[str, Any]` and `write()` accepts `dict[str, Any]`

#### Scenario: Type checking convert function
- **WHEN** a user calls `convert()` with type checking enabled
- **THEN** the function signature shows correct parameter types for `fromfile`, `tofile`, `iterableargs`, etc.
- **AND** type checkers can validate argument types

### Requirement: Type Aliases
The library SHALL provide type aliases for common types used throughout the API, improving code readability and maintainability.

#### Scenario: Using Row type alias
- **WHEN** a user imports `Row` from `iterable`
- **THEN** `Row` is defined as `dict[str, Any]`
- **AND** it can be used in type annotations for functions that work with data rows

#### Scenario: Using IterableArgs type alias
- **WHEN** a user imports `IterableArgs` from `iterable`
- **THEN** `IterableArgs` is defined as `dict[str, Any]`
- **AND** it can be used in type annotations for functions that accept iterable configuration arguments

### Requirement: Type Marker File
The library SHALL include a `py.typed` marker file to indicate to type checkers that the package supports type checking.

#### Scenario: Type checker detection
- **WHEN** a type checker (mypy, pyright) processes the `iterabledata` package
- **THEN** it detects the `py.typed` marker file
- **AND** it uses the type hints provided in the package for type checking

### Requirement: Typed Helper for Dataclasses
The library SHALL provide a helper function `as_dataclasses()` that converts dict-based rows into dataclass instances, enabling type-safe data processing.

#### Scenario: Converting rows to dataclasses
- **WHEN** a user calls `as_dataclasses(iterable, MyDataclass)` where `MyDataclass` is a dataclass
- **THEN** the function yields instances of `MyDataclass` instead of plain dicts
- **AND** each row from the iterable is converted to a dataclass instance with proper type validation
- **AND** type checkers recognize the yielded type as `MyDataclass`

#### Scenario: Type safety with dataclasses
- **WHEN** a user processes rows using `as_dataclasses(iterable, MyDataclass)`
- **THEN** IDE autocomplete and type checkers provide correct type information for dataclass fields
- **AND** type errors are caught at development time if fields are accessed incorrectly

### Requirement: Optional Pydantic Integration
The library SHALL provide optional Pydantic integration for row validation, allowing users to catch schema issues early.

#### Scenario: Pydantic validation enabled
- **WHEN** a user opens an iterable with `validate_row=True` and provides a Pydantic model
- **THEN** each row is validated against the Pydantic model schema
- **AND** validation errors are raised immediately if a row doesn't match the schema
- **AND** validated rows are returned as Pydantic model instances

#### Scenario: Pydantic validation disabled
- **WHEN** Pydantic is not installed or validation is not enabled
- **THEN** the library functions normally without validation
- **AND** no errors are raised due to missing Pydantic dependency
