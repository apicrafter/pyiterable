## 1. Implementation
- [x] 1.1 Create `iterable/helpers/capabilities.py` module
- [x] 1.2 Implement `_detect_capabilities()` helper function to introspect format classes
- [x] 1.3 Implement `get_format_capabilities(format_id: str) -> dict` function
- [x] 1.4 Implement `list_all_capabilities() -> dict[str, dict]` function
- [x] 1.5 Implement `get_capability(format_id: str, capability: str) -> bool | None` function
- [x] 1.6 Add capability caching mechanism to avoid repeated introspection
- [x] 1.7 Integrate with `detect.py` to access format registry
- [x] 1.8 Handle optional dependencies gracefully (ImportError handling)
- [x] 1.9 Export capability functions in `iterable/helpers/__init__.py`

## 2. Testing
- [x] 2.1 Create `tests/test_capabilities.py` test file
- [x] 2.2 Test `get_format_capabilities()` for known formats (CSV, JSON, Parquet, XML)
- [x] 2.3 Test `list_all_capabilities()` returns all registered formats
- [x] 2.4 Test `get_capability()` for individual capability queries
- [x] 2.5 Test error handling (unknown format, missing dependencies)
- [x] 2.6 Test capability detection accuracy across different format types
- [x] 2.7 Test caching behavior (same format returns same results)
- [x] 2.8 Verify capabilities match actual format implementations

## 3. Documentation
- [ ] 3.1 Add capability reporting examples to main README
- [ ] 3.2 Update API documentation with capability functions
- [ ] 3.3 Add capability reporting section to getting started guide
- [ ] 3.4 Update capability matrix documentation to reference new API
- [ ] 3.5 Add examples showing how to use capabilities programmatically

## 4. Integration
- [x] 4.1 Verify capability functions work with all registered formats (138 formats tested)
- [x] 4.2 Test with formats that have optional dependencies (graceful handling implemented)
- [x] 4.3 Ensure backward compatibility (no breaking changes - new functionality only)
- [x] 4.4 Run full test suite to ensure no regressions (25 tests passing)
