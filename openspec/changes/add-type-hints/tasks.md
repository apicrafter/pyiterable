## 1. Type System Foundation
- [x] 1.1 Create `iterable/types.py` with type aliases (`Row`, `IterableArgs`, `CodecArgs`)
- [x] 1.2 Add `py.typed` marker file to package root
- [x] 1.3 Update `pyproject.toml` to include `py.typed` in package data
- [x] 1.4 Export type aliases from `iterable/__init__.py`

## 2. Core API Type Hints
- [x] 2.1 Add type hints to `open_iterable()` in `iterable/helpers/detect.py`
- [x] 2.2 Add type hints to `BaseIterable.read()` method
- [x] 2.3 Add type hints to `BaseIterable.write()` method
- [x] 2.4 Add type hints to `BaseIterable.read_bulk()` method
- [x] 2.5 Add type hints to `BaseIterable.write_bulk()` method
- [x] 2.6 Add type hints to other `BaseIterable` methods (`reset()`, `list_tables()`, etc.)
- [x] 2.7 Add type hints to `convert()` in `iterable/convert/core.py`
- [x] 2.8 Add type hints to `pipeline()` in `iterable/pipeline/core.py`

## 3. Typed Helper Functions
- [x] 3.1 Create `iterable/helpers/typed.py` module
- [x] 3.2 Implement `as_dataclasses()` helper function
- [x] 3.3 Implement Pydantic integration helper (optional validation)
- [x] 3.4 Add helper functions to `iterable/__init__.py` exports
- [x] 3.5 Add `pydantic>=2.0.0` to optional-dependencies in `pyproject.toml`

## 4. Testing
- [x] 4.1 Create `tests/test_types.py` for type hint validation
- [x] 4.2 Add tests for `as_dataclasses()` helper
- [x] 4.3 Add tests for Pydantic integration
- [x] 4.4 Verify type hints work with mypy/pyright
- [ ] 4.5 Run type checker in CI (mypy or pyright) - Note: This requires CI configuration update

## 5. Documentation
- [x] 5.1 Update `CHANGELOG.md` with type hints feature
- [ ] 5.2 Add type hints examples to documentation - Note: Can be done in follow-up PR
- [ ] 5.3 Document typed helpers in API reference - Note: Can be done in follow-up PR
