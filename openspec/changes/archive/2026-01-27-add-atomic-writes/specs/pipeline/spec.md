## MODIFIED Requirements

### Requirement: Data Processing Pipeline
The system SHALL provide a data processing pipeline that reads data from a source, processes it through user-defined functions, and writes results to a destination.

The system SHALL support atomic writes for destination files when processing pipelines write to file outputs. When atomic writes are enabled, the system SHALL write to a temporary file and atomically rename it to the final destination only upon successful completion of all pipeline processing.

#### Scenario: Atomic write on successful pipeline execution
- **WHEN** `pipeline()` is called with `atomic=True` and a file destination, and pipeline execution completes successfully
- **THEN** all data is written to a temporary file (e.g., `output.tmp`)
- **AND** the temporary file is atomically renamed to the final destination using `os.replace()` after all writes complete
- **AND** the temporary file is removed after successful rename
- **AND** the final output file is only visible when fully written

#### Scenario: Atomic write preserves original file on pipeline failure
- **WHEN** `pipeline()` is called with `atomic=True` and pipeline execution fails or is interrupted
- **THEN** the temporary file is cleaned up
- **AND** the original destination file (if it existed) remains unchanged
- **AND** no partial or corrupted output file is left at the destination

#### Scenario: Non-atomic write (backward compatibility)
- **WHEN** `pipeline()` is called with `atomic=False` (default)
- **THEN** data is written directly to the destination file
- **AND** behavior matches existing implementation

#### Scenario: Atomic write with batch processing
- **WHEN** `pipeline()` processes data in batches with `atomic=True`
- **THEN** all batches are written to the temporary file
- **AND** atomic rename occurs only after all batches are successfully written
- **AND** if any batch write fails, the temporary file is cleaned up and original file preserved

## ADDED Requirements

### Requirement: Atomic Write Parameter for Pipeline
The `pipeline()` function and `Pipeline` class SHALL accept an optional `atomic` parameter (default: `False`) that enables atomic write operations for destination files.

#### Scenario: Atomic parameter defaults to False
- **WHEN** `pipeline()` is called without specifying `atomic` parameter
- **THEN** `atomic` defaults to `False`
- **AND** writes occur directly to destination file (backward compatible behavior)

#### Scenario: Atomic write only applies to file destinations
- **WHEN** `pipeline()` is called with `atomic=True` but destination is not a file (e.g., stream, in-memory)
- **THEN** atomic write logic is skipped
- **AND** normal write behavior is used

#### Scenario: Atomic write error handling
- **WHEN** atomic write operation fails during pipeline execution (e.g., cross-filesystem rename, permission error)
- **THEN** a clear error message is raised explaining the failure
- **AND** temporary files are cleaned up
- **AND** original destination file remains unchanged
