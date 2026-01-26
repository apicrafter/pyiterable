# Error Handling

## MODIFIED Requirements

### Requirement: Exception Hierarchy
The system SHALL use a comprehensive exception hierarchy that allows users to catch and handle specific error types programmatically.

#### Scenario: Format-specific errors
- **WHEN** format operation fails due to format-specific issue
- **THEN** system raises `FormatError` or appropriate subclass
- **AND** exception provides actionable error message
- **AND** exception includes error code for programmatic handling

#### Scenario: Format not supported
- **WHEN** user attempts to use unsupported format
- **THEN** system raises `FormatNotSupportedError`
- **AND** exception message indicates which format was requested
- **AND** exception may suggest alternative formats

#### Scenario: Format detection failure
- **WHEN** system cannot detect file format
- **THEN** system raises `FormatDetectionError`
- **AND** exception message explains why detection failed
- **AND** exception may suggest explicit format specification

#### Scenario: Codec errors
- **WHEN** compression codec operation fails
- **THEN** system raises `CodecError` or appropriate subclass
- **AND** exception message indicates which codec failed
- **AND** exception includes underlying error information

#### Scenario: Read errors
- **WHEN** reading operation fails
- **THEN** system raises `ReadError` or appropriate subclass
- **AND** exception message indicates file and position
- **AND** exception includes underlying error information
- **AND** exception includes contextual information: filename, row number (if available), byte offset (if available), original line content (for text formats)

#### Scenario: Write errors
- **WHEN** writing operation fails
- **THEN** system raises `WriteError` or appropriate subclass
- **AND** exception message indicates file and operation
- **AND** exception includes underlying error information

#### Scenario: Streaming not supported
- **WHEN** user attempts streaming operation on non-streaming format
- **THEN** system raises `StreamingNotSupportedError`
- **AND** exception message explains limitation
- **AND** exception may suggest alternative approach

#### Scenario: Resource errors
- **WHEN** resource management operation fails (e.g., cannot reset non-seekable stream)
- **THEN** system raises `ResourceError`
- **AND** exception message explains resource constraint
- **AND** exception provides guidance on resolution

### Requirement: Format Parse Errors
The system SHALL provide detailed contextual information when format parsing fails.

#### Scenario: Parse error with context
- **WHEN** format parsing fails during iteration
- **THEN** system raises `FormatParseError`
- **AND** exception includes filename (if available)
- **AND** exception includes row number or approximate row offset (when determinable)
- **AND** exception includes byte offset in file (when available)
- **AND** exception includes original line content for text formats (when available)
- **AND** exception message includes all contextual information

#### Scenario: Context for text formats
- **WHEN** parsing fails in text-based format (CSV, JSONL, etc.)
- **THEN** exception includes the original line that failed to parse
- **AND** exception includes line number or row number
- **AND** exception includes byte offset where line starts

#### Scenario: Context for binary formats
- **WHEN** parsing fails in binary format (Parquet, Avro, etc.)
- **THEN** exception includes byte offset where error occurred
- **AND** exception includes record index if determinable
- **AND** exception may include partial record data if available

## ADDED Requirements

### Requirement: Configurable Error Policy
The system SHALL support configurable error handling policies that allow users to control how parse errors are handled during iteration.

#### Scenario: Error policy via iterableargs
- **WHEN** user specifies `on_error` in `iterableargs` parameter
- **THEN** system applies specified error policy during iteration
- **AND** valid values are: `'raise'` (default), `'skip'`, `'warn'`
- **AND** error policy applies to all parse errors during iteration

#### Scenario: Raise policy (default)
- **WHEN** `on_error='raise'` is specified or omitted (default)
- **THEN** system raises exception immediately when parse error occurs
- **AND** iteration stops
- **AND** behavior matches current implementation

#### Scenario: Skip policy
- **WHEN** `on_error='skip'` is specified
- **THEN** system silently skips malformed records
- **AND** iteration continues with next record
- **AND** skipped errors are logged if `error_log` is specified
- **AND** no exception is raised for parse errors

#### Scenario: Warn policy
- **WHEN** `on_error='warn'` is specified
- **THEN** system logs warning using Python's `warnings` module
- **AND** iteration continues with next record
- **AND** warning includes contextual information (filename, row, error message)
- **AND** skipped errors are logged if `error_log` is specified
- **AND** no exception is raised for parse errors

#### Scenario: Error policy validation
- **WHEN** invalid `on_error` value is provided
- **THEN** system raises `ValueError` with valid options
- **AND** error occurs during initialization, not during iteration

### Requirement: Error Logging
The system SHALL support logging errors to a file or file-like object for later analysis.

#### Scenario: Error log file path
- **WHEN** user specifies `error_log` as file path string in `iterableargs`
- **THEN** system creates or appends to specified file
- **AND** all errors (regardless of policy) are logged to file
- **AND** log file is created if it doesn't exist
- **AND** log file is opened in append mode

#### Scenario: Error log file object
- **WHEN** user specifies `error_log` as file-like object in `iterableargs`
- **THEN** system writes errors to provided file object
- **AND** user is responsible for closing file object
- **AND** system does not close user-provided file objects

#### Scenario: Error log format
- **WHEN** error is logged
- **THEN** log entry includes: ISO timestamp, filename, row number (if available), byte offset (if available), error message, original line (if available)
- **AND** log format is structured and parseable (e.g., JSON or tab-separated)
- **AND** log entries are written one per line

#### Scenario: Error logging with skip policy
- **WHEN** `on_error='skip'` and `error_log` are both specified
- **THEN** skipped errors are logged to error log file
- **AND** iteration continues without raising exceptions
- **AND** user can review skipped records later

#### Scenario: Error logging with warn policy
- **WHEN** `on_error='warn'` and `error_log` are both specified
- **THEN** errors trigger both warning and log entry
- **AND** iteration continues without raising exceptions
- **AND** user receives immediate feedback (warning) and persistent record (log)

### Requirement: Contextual Error Information
The system SHALL capture and provide detailed contextual information about where errors occur.

#### Scenario: Filename in errors
- **WHEN** parse error occurs during iteration
- **THEN** exception includes `filename` attribute
- **AND** filename is set from `open_iterable()` filename parameter
- **AND** filename is `None` if not available (e.g., stream-based iteration)

#### Scenario: Row number tracking
- **WHEN** parse error occurs in text-based format
- **THEN** exception includes `row_number` attribute
- **AND** row number is 1-indexed (first data row is 1, header row excluded)
- **AND** row number is `None` if not determinable

#### Scenario: Byte offset tracking
- **WHEN** parse error occurs
- **THEN** exception includes `byte_offset` attribute
- **AND** byte offset indicates position in file where error occurred
- **AND** byte offset is `None` if not determinable (e.g., non-seekable streams)

#### Scenario: Original line content
- **WHEN** parse error occurs in text-based format
- **THEN** exception includes `original_line` attribute
- **AND** original line contains the raw line content that failed to parse
- **AND** original line is `None` for binary formats or when not available
- **AND** original line may be truncated if extremely long (with indication)

#### Scenario: Context in error messages
- **WHEN** exception message is formatted
- **THEN** message includes all available contextual information
- **AND** message format: "Failed to parse {format} at {filename}:{row} (byte {offset}): {message}"
- **AND** message omits unavailable context gracefully

### Requirement: Error Policy Integration
The system SHALL integrate error policy handling into all iteration methods.

#### Scenario: Error policy in read()
- **WHEN** `read()` method encounters parse error
- **THEN** method applies configured error policy
- **AND** if policy is 'skip' or 'warn', method continues to next record
- **AND** if policy is 'raise', method raises exception immediately

#### Scenario: Error policy in iteration
- **WHEN** iteration via `for row in iterable:` encounters parse error
- **THEN** iteration applies configured error policy
- **AND** if policy is 'skip' or 'warn', iteration continues to next record
- **AND** if policy is 'raise', iteration stops and raises exception

#### Scenario: Error policy in read_bulk()
- **WHEN** `read_bulk()` method encounters parse errors
- **THEN** method applies configured error policy
- **AND** if policy is 'skip' or 'warn', method skips bad records and continues
- **AND** returned list contains only successfully parsed records
- **AND** if policy is 'raise', method raises exception immediately

#### Scenario: Error policy inheritance
- **WHEN** error policy is specified in `open_iterable()`
- **THEN** policy is passed to all format-specific iterable implementations
- **AND** policy applies consistently across all iteration methods
- **AND** policy is accessible via iterable instance attributes
