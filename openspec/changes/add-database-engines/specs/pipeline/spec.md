## MODIFIED Requirements

### Requirement: Data Processing Pipeline
The system SHALL provide a data processing pipeline that reads data from a source, processes it through user-defined functions, and writes results to a destination.

The system SHALL support database sources (SQL and NoSQL databases) as pipeline sources, treating database query results as iterable sources identical to file-based sources.

The system SHALL support atomic writes for destination files when processing pipelines write to file outputs. When atomic writes are enabled, the system SHALL write to a temporary file and atomically rename it to the final destination only upon successful completion of all pipeline processing.

#### Scenario: Pipeline with PostgreSQL source
- **WHEN** `pipeline()` is called with a source from `open_iterable("postgresql://...", engine="postgres", query="SELECT * FROM orders")` and a file destination
- **THEN** the system processes rows from PostgreSQL through the pipeline function and writes to the destination
- **AND** database connection is properly closed after pipeline execution completes
- **AND** pipeline metrics include rows processed from database

#### Scenario: Pipeline with MongoDB source
- **WHEN** `pipeline()` is called with a source from `open_iterable("mongodb://...", engine="mongo", database="analytics", collection="events")` and a file destination
- **THEN** the system processes documents from MongoDB through the pipeline function and writes to the destination
- **AND** database connection is properly closed after pipeline execution completes

#### Scenario: Pipeline with database source and streaming
- **WHEN** `pipeline()` is called with a database source and `batch_size=5000`
- **THEN** the system processes database results in batches, maintaining memory efficiency
- **AND** database results are streamed without loading entire result set into memory

#### Scenario: Pipeline with database source and error handling
- **WHEN** `pipeline()` is called with a database source and database connection fails or query errors occur during processing
- **THEN** the system raises an appropriate exception with clear error message
- **AND** database connection is properly closed even on error
- **AND** no partial output file is created

#### Scenario: Pipeline with database source and process function
- **WHEN** `pipeline()` is called with a database source and a `process_func` that transforms rows
- **THEN** each database row is passed to `process_func` for transformation
- **AND** transformed rows are written to destination
- **AND** database row format (dict) is consistent with file-based sources

#### Scenario: Pipeline with database source and progress tracking
- **WHEN** `pipeline()` is called with a database source and `progress` callback or `trigger_func`
- **THEN** the system invokes progress callbacks with database-specific metrics
- **AND** progress tracking works consistently with file-based sources

#### Scenario: Pipeline with database source and state management
- **WHEN** `pipeline()` is called with a database source and `start_state` dictionary
- **THEN** the state is passed to `process_func` and can be updated during processing
- **AND** state management works consistently with file-based sources

#### Scenario: Atomic write on successful pipeline execution with database source
- **WHEN** `pipeline()` is called with `atomic=True`, a database source, and a file destination, and pipeline execution completes successfully
- **THEN** all data is written to a temporary file (e.g., `output.tmp`)
- **AND** the temporary file is atomically renamed to the final destination using `os.replace()` after all writes complete
- **AND** the temporary file is removed after successful rename
- **AND** the final output file is only visible when fully written
- **AND** database connection is properly closed

#### Scenario: Atomic write preserves original file on pipeline failure with database source
- **WHEN** `pipeline()` is called with `atomic=True`, a database source, and pipeline execution fails or is interrupted
- **THEN** the temporary file is cleaned up
- **AND** the original destination file (if it existed) remains unchanged
- **AND** no partial or corrupted output file is left at the destination
- **AND** database connection is properly closed

#### Scenario: Non-atomic write (backward compatibility)
- **WHEN** `pipeline()` is called with `atomic=False` (default)
- **THEN** data is written directly to the destination file
- **AND** behavior matches existing implementation

#### Scenario: Atomic write with batch processing and database source
- **WHEN** `pipeline()` processes data from a database source in batches with `atomic=True`
- **THEN** all batches are written to the temporary file
- **AND** atomic rename occurs only after all batches are successfully written
- **AND** if any batch write fails, the temporary file is cleaned up and original file preserved
- **AND** database connection is properly closed

#### Scenario: Pipeline with database source and no destination
- **WHEN** `pipeline()` is called with a database source and `destination=None`
- **THEN** the system processes database rows through `process_func` without writing output
- **AND** database connection is properly closed after processing
- **AND** pipeline metrics are still tracked

#### Scenario: Pipeline reset with database source
- **WHEN** `pipeline()` is called with `reset_iterables=True` and a database source that supports reset
- **THEN** the database query is re-executed and pipeline processes from the beginning
- **AND** for databases that don't support reset, behavior is consistent with file-based sources

#### Scenario: Backward compatibility with file sources
- **WHEN** `pipeline()` is called with file-based sources (not database sources)
- **THEN** the system continues to work exactly as before, with no changes to existing behavior
