# Change: Add Full Type Hints and Typed Helpers

## Why
Modern Python projects increasingly rely on type checkers (mypy, pyright, pyre) to catch errors at development time and improve IDE support. Currently, `iterabledata` has minimal type hints, making it difficult for users to:
- See correct function signatures in IDEs
- Catch type-related mistakes before runtime
- Understand API capabilities without reading extensive documentation
- Integrate with type-checked codebases

Adding comprehensive type hints and typed helpers will make `iterabledata` more pleasant to use in modern, type-checked Python projects, improving developer experience and code quality.

## What Changes
- **Type Hints Across Public API**:
  - Add complete type annotations to `open_iterable()` function (parameters and return type)
  - Add type hints to `BaseIterable` methods (`read()`, `write()`, `read_bulk()`, `write_bulk()`, etc.)
  - Add type hints to `convert()` function
  - Add type hints to `pipeline()` function
  - Use type aliases like `Row = dict[str, Any]` and `IterableArgs = dict[str, Any]` for clarity
- **Type Marker File**:
  - Add `py.typed` marker file to indicate the package supports type checking
  - Update `pyproject.toml` to include `py.typed` in package data
- **Typed Helper Functions**:
  - Add `as_dataclasses()` helper that yields dataclass instances instead of plain dicts
  - Add optional Pydantic integration (`validate_row=True`) to catch schema issues early
  - These helpers provide type-safe alternatives to the dict-based API
- **Type Aliases Module**:
  - Create `iterable.types` module with common type aliases (`Row`, `IterableArgs`, `CodecArgs`, etc.)
  - Export type aliases from main `__init__.py` for convenience

## Impact
- **Affected Specs**:
  - `type-system` - New capability for type hints and typed helpers
- **Affected Files**:
  - `iterable/__init__.py` - Export type aliases and new helpers
  - `iterable/types.py` (new) - Type aliases and protocol definitions
  - `iterable/helpers/detect.py` - Add type hints to `open_iterable()`
  - `iterable/base.py` - Add type hints to `BaseIterable` methods
  - `iterable/convert/core.py` - Add type hints to `convert()`
  - `iterable/pipeline/core.py` - Add type hints to `pipeline()`
  - `iterable/helpers/typed.py` (new) - Typed helper functions (`as_dataclasses`, pydantic integration)
  - `py.typed` (new) - Type marker file
  - `pyproject.toml` - Include `py.typed` in package data
  - `tests/test_types.py` (new) - Tests for type hints and typed helpers
  - `CHANGELOG.md` - Document new type support
- **Dependencies**:
  - No new required dependencies (uses `typing` from standard library)
  - Optional: `pydantic>=2.0.0` for Pydantic integration (added to optional-dependencies)
- **Backward Compatibility**:
  - All changes are additive and backward compatible
  - Existing code continues to work without modifications
  - Type hints are optional and don't affect runtime behavior
