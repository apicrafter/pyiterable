## 1. Exception Enhancements
- [ ] 1.1 Enhance `FormatParseError` to include contextual attributes (filename, row_number, byte_offset, original_line)
- [ ] 1.2 Enhance `ReadError` to include contextual attributes
- [ ] 1.3 Update exception constructors to accept and store contextual information
- [ ] 1.4 Ensure backward compatibility with existing exception usage

## 2. Error Policy Implementation
- [ ] 2.1 Add error policy configuration parsing in `BaseIterable.__init__()`
- [ ] 2.2 Implement error policy logic in `BaseIterable.read()` method
- [ ] 2.3 Implement error policy logic in iteration protocol (`__iter__`, `__next__`)
- [ ] 2.4 Add error policy support to `read_bulk()` method
- [ ] 2.5 Pass error policy configuration through `open_iterable()` function

## 3. Error Logging
- [ ] 3.1 Implement error logging functionality in `BaseIterable`
- [ ] 3.2 Create structured error log format (timestamp, filename, row, offset, message, line)
- [ ] 3.3 Support both file path strings and file-like objects for `error_log`
- [ ] 3.4 Ensure thread-safe error logging if needed
- [ ] 3.5 Handle error log file creation and permissions gracefully

## 4. Context Capture
- [ ] 4.1 Update CSV format to capture row number and original line
- [ ] 4.2 Update JSONL format to capture line number and original line
- [ ] 4.3 Update other text formats to capture contextual information where possible
- [ ] 4.4 Add byte offset tracking for binary formats
- [ ] 4.5 Ensure context capture doesn't significantly impact performance

## 5. Format-Specific Updates
- [ ] 5.1 Update `CSVIterable` to use error policy and capture context
- [ ] 5.2 Update `JSONLIterable` to use error policy and capture context
- [ ] 5.3 Update `XMLIterable` to use error policy and capture context
- [ ] 5.4 Update other major format implementations
- [ ] 5.5 Ensure error handling works with compression codecs

## 6. Testing
- [ ] 6.1 Create `tests/test_error_handling.py` with comprehensive test suite
- [ ] 6.2 Test `on_error='raise'` (default behavior)
- [ ] 6.3 Test `on_error='skip'` with various error types
- [ ] 6.4 Test `on_error='warn'` with warning capture
- [ ] 6.5 Test error logging functionality
- [ ] 6.6 Test contextual information in exceptions
- [ ] 6.7 Test error handling with different formats (CSV, JSONL, XML, etc.)
- [ ] 6.8 Test error handling with compressed files
- [ ] 6.9 Test backward compatibility (existing code should work unchanged)

## 7. Documentation
- [ ] 7.1 Update `CHANGELOG.md` with new error handling features
- [ ] 7.2 Update API documentation for `open_iterable()` with new parameters
- [ ] 7.3 Add examples of error handling usage to documentation
- [ ] 7.4 Document error log format
- [ ] 7.5 Update exception documentation with new contextual attributes
