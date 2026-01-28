# Validation Hooks Design

## Executive Summary

This document designs a validation hooks system for IterableData that allows users to automatically validate data during read and write operations. Validation hooks integrate seamlessly with existing operations while maintaining backward compatibility and performance.

## Current State

IterableData already has validation capabilities, but they require explicit calls:

1. **`iterable.validate` module** - Rule-based validation
   - `validate.iterable()` - Validates rows against rules
   - Built-in rules (email, URL, etc.)
   - Custom rule registration

2. **`iterable.ops.schema` module** - Schema-based validation
   - `schema.validate()` - Validates against inferred/provided schemas
   - Type checking, nullable fields, strict mode

3. **Pydantic integration** - `as_pydantic()` helper
   - Converts rows to Pydantic models
   - Optional validation flag

**Limitation**: All validation is post-processing - users must explicitly call validation functions after reading data.

## Use Cases for Validation Hooks

### 1. Automatic Validation During Read

**Scenario**: Validate data as it's read, fail fast on invalid data

```python
# Current (manual validation)
with open_iterable('data.csv') as source:
    for row in source:
        errors = validate_row(row, rules)
        if errors:
            raise ValueError(f"Invalid row: {errors}")

# With validation hooks (automatic)
def validate_row(row):
    errors = []
    if not row.get('email') or '@' not in row['email']:
        errors.append("Invalid email")
    if errors:
        raise ValueError(errors)
    return row

with open_iterable('data.csv', validation_hook=validate_row) as source:
    for row in source:  # Validation happens automatically
        process(row)
```

### 2. Validation During Write

**Scenario**: Ensure only valid data is written

```python
# With validation hooks
def validate_before_write(row):
    if 'id' not in row:
        raise ValueError("Row missing required 'id' field")
    return row

with open_iterable('output.jsonl', mode='w', validation_hook=validate_before_write) as dest:
    dest.write({'id': 1, 'name': 'test'})  # Validated before write
```

### 3. Schema Validation Integration

**Scenario**: Automatically validate against schema during read

```python
from iterable.ops import schema

# Infer schema
sch = schema.infer('data.csv')

# Use schema validation hook
def schema_validator(row):
    return schema.validate_row(row, sch)  # Returns validated row or raises

with open_iterable('data.csv', validation_hook=schema_validator) as source:
    for row in source:  # Automatically validated against schema
        process(row)
```

### 4. Pydantic Model Validation

**Scenario**: Automatically validate rows as Pydantic models

```python
from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age: int

def pydantic_validator(row):
    return Person.model_validate(row).model_dump()

with open_iterable('people.csv', validation_hook=pydantic_validator) as source:
    for row in source:  # Automatically validated as Person
        process(row)
```

### 5. Error Handling Modes

**Scenario**: Different behaviors for validation failures

```python
# Mode 1: Raise exception (fail fast)
with open_iterable('data.csv', validation_hook=validator, on_validation_error='raise') as source:
    for row in source:  # Raises on first invalid row
        process(row)

# Mode 2: Skip invalid rows
with open_iterable('data.csv', validation_hook=validator, on_validation_error='skip') as source:
    for row in source:  # Skips invalid rows, continues
        process(row)

# Mode 3: Log errors, continue
with open_iterable('data.csv', validation_hook=validator, on_validation_error='log') as source:
    for row in source:  # Logs errors, continues processing
        process(row)
```

## Design Patterns

### Pattern 1: Hook Function Signature

Validation hooks are callable objects that take a row and return a row (or raise):

```python
ValidationHook = Callable[[Row], Row]

def validation_hook(row: Row) -> Row:
    """Validate and return row, or raise exception"""
    # Validate
    if not is_valid(row):
        raise ValueError("Invalid row")
    # Optionally transform
    return row
```

**Return Behavior**:
- Return row: Validation passed, row may be transformed
- Raise exception: Validation failed

### Pattern 2: Integration Points

Validation hooks can be attached at multiple points:

1. **Read Hook** - Validates rows as they're read
   - Applied in `read()`, `read_bulk()`, `__iter__()`
   - Can transform rows before returning

2. **Write Hook** - Validates rows before writing
   - Applied in `write()`, `write_bulk()`
   - Can transform rows before writing

3. **Pipeline Hook** - Validates rows during pipeline processing
   - Applied in `pipeline()` function
   - Can be combined with `process_func`

### Pattern 3: Error Handling Policies

Similar to `on_error` parameter, support `on_validation_error`:

- `'raise'` - Raise exception on validation failure (default)
- `'skip'` - Skip invalid rows, continue processing
- `'log'` - Log errors, continue processing
- `'warn'` - Issue warning, continue processing

### Pattern 4: Hook Chaining

Support multiple validation hooks:

```python
def validate_schema(row):
    return schema.validate_row(row, sch)

def validate_business_rules(row):
    if row['status'] not in ['active', 'inactive']:
        raise ValueError("Invalid status")
    return row

# Chain multiple hooks
with open_iterable(
    'data.csv',
    validation_hook=[validate_schema, validate_business_rules]
) as source:
    for row in source:  # Both hooks applied in sequence
        process(row)
```

## API Design

### Option 1: Parameter-Based (Recommended)

Add validation hook parameters to `open_iterable()` and methods:

```python
def open_iterable(
    filename: str | None = None,
    ...,
    validation_hook: ValidationHook | list[ValidationHook] | None = None,
    on_validation_error: str = 'raise',  # 'raise', 'skip', 'log', 'warn'
) -> BaseIterable:
    ...
```

**Usage**:
```python
# Single hook
with open_iterable('data.csv', validation_hook=validator) as source:
    for row in source:
        process(row)

# Multiple hooks
with open_iterable('data.csv', validation_hook=[hook1, hook2]) as source:
    for row in source:
        process(row)

# Error handling
with open_iterable(
    'data.csv',
    validation_hook=validator,
    on_validation_error='skip'
) as source:
    for row in source:  # Invalid rows skipped
        process(row)
```

### Option 2: Method-Based

Add validation hook methods to `BaseIterable`:

```python
class BaseIterable:
    def set_validation_hook(
        self,
        hook: ValidationHook | list[ValidationHook],
        on_error: str = 'raise'
    ) -> None:
        """Set validation hook for this iterable"""
        ...
```

**Usage**:
```python
with open_iterable('data.csv') as source:
    source.set_validation_hook(validator, on_error='skip')
    for row in source:
        process(row)
```

**Pros**: More flexible, can change hooks dynamically  
**Cons**: More verbose, requires method call

### Option 3: Context Manager Wrapper

Create wrapper that adds validation:

```python
from iterable.helpers.validation import with_validation

with open_iterable('data.csv') as source:
    with with_validation(source, hook=validator) as validated:
        for row in validated:
            process(row)
```

**Pros**: No changes to core API  
**Cons**: More verbose, less discoverable

## Implementation Approach

### Phase 1: Core Infrastructure

1. **Define ValidationHook Protocol**
   ```python
   from typing import Protocol
   
   class ValidationHook(Protocol):
       def __call__(self, row: Row) -> Row:
           """Validate and return row, or raise exception"""
           ...
   ```

2. **Add Validation Hook Storage**
   ```python
   class BaseIterable:
       def __init__(self):
           self._validation_hooks: list[ValidationHook] = []
           self._on_validation_error: str = 'raise'
   ```

3. **Implement Hook Application**
   ```python
   def _apply_validation_hooks(self, row: Row) -> Row:
       """Apply all validation hooks to a row"""
       for hook in self._validation_hooks:
           try:
               row = hook(row)
           except Exception as e:
               if self._on_validation_error == 'raise':
                   raise
               elif self._on_validation_error == 'skip':
                   return None  # Signal to skip
               elif self._on_validation_error == 'log':
                   logger.warning(f"Validation failed: {e}")
               elif self._on_validation_error == 'warn':
                   warnings.warn(f"Validation failed: {e}")
       return row
   ```

### Phase 2: Integration Points

1. **Read Operations**
   ```python
   def read(self, skip_empty: bool = True) -> Row:
       row = self._read_impl(skip_empty)
       if row is None:
           return None
       validated = self._apply_validation_hooks(row)
       if validated is None:  # Skipped
           return self.read(skip_empty)  # Try next row
       return validated
   ```

2. **Write Operations**
   ```python
   def write(self, record: Row) -> None:
       validated = self._apply_validation_hooks(record)
       if validated is None:  # Skipped
           return  # Don't write invalid row
       self._write_impl(validated)
   ```

3. **Bulk Operations**
   ```python
   def read_bulk(self, num: int = DEFAULT_BULK_NUMBER) -> list[Row]:
       rows = self._read_bulk_impl(num)
       validated_rows = []
       for row in rows:
           validated = self._apply_validation_hooks(row)
           if validated is not None:
               validated_rows.append(validated)
       return validated_rows
   ```

### Phase 3: Error Handling

1. **Error Logging**
   - Track validation errors similar to `error_log` parameter
   - Support file or file-like object for validation error log

2. **Statistics**
   - Track validation statistics (valid/invalid counts)
   - Expose via method or property

3. **Exception Types**
   - Create `ValidationError` exception type
   - Include row context in exception

## Integration with Existing Validation

### Leverage Existing Validation Modules

```python
# Schema validation hook factory
def create_schema_validator(schema: dict[str, Any], strict: bool = False):
    def validator(row: Row) -> Row:
        errors = schema.validate_row(row, schema, strict)
        if errors:
            raise ValidationError(f"Schema validation failed: {errors}")
        return row
    return validator

# Rule validation hook factory
def create_rule_validator(rules: dict[str, list[str]]):
    def validator(row: Row) -> Row:
        errors = []
        for field, rule_names in rules.items():
            for rule_name in rule_names:
                is_valid, error_msg = validate_value(row.get(field), rule_name)
                if not is_valid:
                    errors.append(f"{field}: {error_msg}")
        if errors:
            raise ValidationError(f"Rule validation failed: {errors}")
        return row
    return validator

# Usage
schema_validator = create_schema_validator(sch)
with open_iterable('data.csv', validation_hook=schema_validator) as source:
    for row in source:
        process(row)
```

## Performance Considerations

### Overhead

- **Hook invocation**: Minimal overhead per row
- **Error handling**: Conditional logic adds small overhead
- **Hook chaining**: Linear overhead with number of hooks

### Optimization Strategies

1. **Lazy Hook Application**
   - Only apply hooks if they're set
   - Check `if self._validation_hooks:` before applying

2. **Bulk Optimization**
   - For `read_bulk()`, apply hooks in batch
   - Can parallelize validation for bulk operations

3. **Early Exit**
   - If hook raises exception and `on_validation_error='raise'`, fail fast
   - No need to continue processing

4. **Caching**
   - Cache validation results if hooks are pure functions
   - Not recommended (rows are usually unique)

## Examples

### Example 1: Basic Validation Hook

```python
def validate_email(row):
    if 'email' in row and '@' not in row['email']:
        raise ValueError("Invalid email format")
    return row

with open_iterable('users.csv', validation_hook=validate_email) as source:
    for row in source:
        print(row)
```

### Example 2: Schema Validation Hook

```python
from iterable.ops import schema

# Infer schema
sch = schema.infer('data.csv')

# Create validator
def schema_validator(row):
    errors = []
    for field_name, field_info in sch['fields'].items():
        value = row.get(field_name)
        expected_type = field_info.get('type', 'string')
        if value is not None:
            type_mapping = {'string': str, 'integer': int, 'float': float}
            if not isinstance(value, type_mapping.get(expected_type, str)):
                errors.append(f"{field_name}: expected {expected_type}")
    if errors:
        raise ValueError(f"Schema validation failed: {errors}")
    return row

with open_iterable('data.csv', validation_hook=schema_validator) as source:
    for row in source:
        process(row)
```

### Example 3: Pydantic Validation Hook

```python
from pydantic import BaseModel, ValidationError

class Person(BaseModel):
    name: str
    age: int

def pydantic_validator(row):
    try:
        return Person.model_validate(row).model_dump()
    except ValidationError as e:
        raise ValueError(f"Pydantic validation failed: {e}")

with open_iterable('people.csv', validation_hook=pydantic_validator) as source:
    for row in source:
        process(row)
```

### Example 4: Error Handling Modes

```python
# Fail fast (default)
with open_iterable('data.csv', validation_hook=validator) as source:
    for row in source:  # Raises on first invalid row
        process(row)

# Skip invalid rows
with open_iterable(
    'data.csv',
    validation_hook=validator,
    on_validation_error='skip'
) as source:
    for row in source:  # Invalid rows skipped
        process(row)

# Log errors, continue
with open_iterable(
    'data.csv',
    validation_hook=validator,
    on_validation_error='log',
    validation_error_log='validation_errors.log'
) as source:
    for row in source:  # Errors logged, processing continues
        process(row)
```

### Example 5: Multiple Hooks

```python
def validate_schema(row):
    # Schema validation
    return row

def validate_business_rules(row):
    # Business logic validation
    return row

def sanitize_data(row):
    # Data sanitization
    row['name'] = row['name'].strip()
    return row

with open_iterable(
    'data.csv',
    validation_hook=[validate_schema, validate_business_rules, sanitize_data]
) as source:
    for row in source:  # All hooks applied in sequence
        process(row)
```

## Testing Considerations

1. **Test hook invocation** - Verify hooks are called for each row
2. **Test hook chaining** - Verify multiple hooks work correctly
3. **Test error handling modes** - Verify all modes work (raise, skip, log, warn)
4. **Test performance** - Ensure hooks don't significantly slow down operations
5. **Test with empty files** - Ensure hooks work with empty data
6. **Test hook exceptions** - Verify exception handling works correctly
7. **Test hook transformation** - Verify hooks can transform rows
8. **Test integration** - Verify hooks work with all formats and operations

## Documentation Updates

1. **API Documentation**
   - Document `validation_hook` parameter
   - Document `on_validation_error` parameter
   - Document `ValidationHook` protocol

2. **User Guide**
   - Add validation hooks section
   - Examples for common use cases
   - Integration with existing validation modules

3. **Best Practices**
   - When to use validation hooks
   - Performance considerations
   - Error handling strategies

## Migration Path

### Backward Compatibility

- All parameters optional (default: no validation)
- Existing code continues to work unchanged
- Validation hooks are opt-in feature

### Gradual Adoption

1. **Phase 1**: Add validation hooks to `open_iterable()`
2. **Phase 2**: Add validation hooks to `read()`, `write()`, `read_bulk()`, `write_bulk()`
3. **Phase 3**: Add validation hooks to `pipeline()`, `convert()`

## Conclusion

Validation hooks provide a powerful way to automatically validate data during read/write operations. The design:

- **Integrates seamlessly** with existing operations
- **Maintains backward compatibility** (all optional)
- **Supports multiple hooks** for complex validation
- **Provides flexible error handling** (raise, skip, log, warn)
- **Leverages existing validation modules** (schema, rules, Pydantic)
- **Minimal performance overhead** (only when hooks are set)

**Recommended Implementation**: Option 1 (Parameter-Based) with integration at read/write level.
