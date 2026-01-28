## MODIFIED Requirements

### Requirement: File Format Conversion
The system SHALL convert data between different file formats with automatic format detection, schema extraction, and efficient batch processing.

The system SHALL support atomic writes for safer production file operations. When atomic writes are enabled, the system SHALL write to a temporary file and atomically rename it to the final destination only upon successful completion, ensuring that output files are never left in a partially written state.

#### Scenario: Atomic write on successful conversion
- **WHEN** `convert()` is called with `atomic=True` and conversion completes successfully
- **THEN** data is written to a temporary file (e.g., `output.tmp`)
- **AND** the temporary file is atomically renamed to the final destination using `os.replace()`
- **AND** the temporary file is removed after successful rename
- **AND** the final output file is only visible when fully written

#### Scenario: Atomic write preserves original file on failure
- **WHEN** `convert()` is called with `atomic=True` and conversion fails or is interrupted
- **THEN** the temporary file is cleaned up
- **AND** the original destination file (if it existed) remains unchanged
- **AND** no partial or corrupted output file is left at the destination

#### Scenario: Non-atomic write (backward compatibility)
- **WHEN** `convert()` is called with `atomic=False` (default)
- **THEN** data is written directly to the destination file
- **AND** behavior matches existing implementation

#### Scenario: Atomic write with bulk conversion
- **WHEN** `bulk_convert()` processes multiple files with `atomic=True`
- **THEN** each file conversion uses atomic writes independently
- **AND** temporary files are cleaned up for each file regardless of overall batch success or failure

## ADDED Requirements

### Requirement: Atomic Write Parameter
The `convert()` function SHALL accept an optional `atomic` parameter (default: `False`) that enables atomic write operations for safer file handling in production environments.

#### Scenario: Atomic parameter defaults to False
- **WHEN** `convert()` is called without specifying `atomic` parameter
- **THEN** `atomic` defaults to `False`
- **AND** writes occur directly to destination file (backward compatible behavior)

#### Scenario: Atomic write error handling
- **WHEN** atomic write operation fails (e.g., cross-filesystem rename, permission error)
- **THEN** a clear error message is raised explaining the failure
- **AND** temporary files are cleaned up
- **AND** original destination file remains unchanged
