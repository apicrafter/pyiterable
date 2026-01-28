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

## ADDED Requirements

### Requirement: Exception Class Hierarchy
The system SHALL define a comprehensive exception hierarchy in `iterable/exceptions.py`.

#### Scenario: Base exception class
- **WHEN** any iterable data error occurs
- **THEN** exception inherits from `IterableDataError`
- **AND** users can catch all iterable errors with base class
- **AND** base class provides common error handling interface

#### Scenario: Format error hierarchy
- **WHEN** format-related error occurs
- **THEN** exception inherits from `FormatError`
- **AND** specific format errors inherit from `FormatError`:
  - `FormatNotSupportedError` - Format not available
  - `FormatDetectionError` - Cannot detect format
  - `FormatParseError` - Format parsing failed

#### Scenario: Codec error hierarchy
- **WHEN** compression codec error occurs
- **THEN** exception inherits from `CodecError`
- **AND** specific codec errors inherit from `CodecError`:
  - `CodecNotSupportedError` - Codec not available
  - `CodecDecompressionError` - Decompression failed
  - `CodecCompressionError` - Compression failed

#### Scenario: Read/Write error hierarchy
- **WHEN** I/O operation error occurs
- **THEN** exception inherits from `ReadError` or `WriteError`
- **AND** specific I/O errors inherit appropriately:
  - `StreamingNotSupportedError` - Format doesn't support streaming
  - `FileNotFoundError` - File does not exist (may wrap standard exception)
  - `PermissionError` - Insufficient permissions (may wrap standard exception)

#### Scenario: Resource error hierarchy
- **WHEN** resource management error occurs
- **THEN** exception inherits from `ResourceError`
- **AND** specific resource errors inherit from `ResourceError`:
  - `StreamNotSeekableError` - Cannot reset non-seekable stream
  - `ResourceLeakError` - Resource not properly closed

### Requirement: Error Codes
The system SHALL provide error codes for programmatic error handling.

#### Scenario: Error code format
- **WHEN** exception is raised
- **THEN** exception includes `error_code` attribute
- **AND** error code is string identifier (e.g., "FORMAT_NOT_SUPPORTED")
- **AND** error codes are documented for user reference

#### Scenario: Error code usage
- **WHEN** user catches exception
- **THEN** user can check `error_code` attribute
- **AND** user can handle errors programmatically based on code
- **AND** error codes are stable across versions

### Requirement: Actionable Error Messages
The system SHALL provide error messages that help users resolve issues.

#### Scenario: Descriptive error messages
- **WHEN** exception is raised
- **THEN** error message explains what went wrong
- **AND** error message suggests how to fix the issue
- **AND** error message includes relevant context (filename, format, etc.)

#### Scenario: Error message format
- **WHEN** exception message is displayed
- **THEN** message follows consistent format
- **AND** message includes: problem description, suggested solution, relevant context
- **AND** message is user-friendly (not technical jargon)

### Requirement: Exception Migration
The system SHALL provide migration path for existing code using generic exceptions.

#### Scenario: Deprecated exception aliases
- **WHEN** old exception pattern is used internally
- **THEN** system may provide deprecated aliases for backward compatibility
- **AND** deprecation warnings guide users to new exceptions
- **AND** migration guide explains changes

#### Scenario: Exception migration guide
- **WHEN** user has code catching generic exceptions
- **THEN** migration guide explains how to update code
- **AND** guide provides examples of new exception handling
- **AND** guide lists all exception classes and when to use them
