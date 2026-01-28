## MODIFIED Requirements

### Requirement: File Format Conversion
The system SHALL convert data between different file formats with automatic format detection, schema extraction, and efficient batch processing.

The system SHALL support converting data from database sources (SQL and NoSQL databases) to file formats, treating database query results as iterable sources identical to file-based sources.

The system SHALL support atomic writes for safer production file operations. When atomic writes are enabled, the system SHALL write to a temporary file and atomically rename it to the final destination only upon successful completion, ensuring that output files are never left in a partially written state.

#### Scenario: Convert from PostgreSQL to Parquet file
- **WHEN** `convert()` is called with `fromfile="postgresql://user:pass@host:5432/dbname"` and `tofile="output.parquet"` with `iterableargs={"engine": "postgres", "query": "SELECT * FROM orders"}`
- **THEN** the system connects to PostgreSQL, executes the query, streams results, and writes to Parquet format
- **AND** database connection is properly closed after conversion completes
- **AND** conversion metrics include rows read from database

#### Scenario: Convert from MongoDB to JSONL file
- **WHEN** `convert()` is called with `fromfile="mongodb://user:pass@host:27017"` and `tofile="output.jsonl"` with `iterableargs={"engine": "mongo", "database": "analytics", "collection": "events"}`
- **THEN** the system connects to MongoDB, queries the collection, streams documents, and writes to JSONL format
- **AND** database connection is properly closed after conversion completes

#### Scenario: Convert from database with batch processing
- **WHEN** `convert()` is called with a database source and `batch_size=10000`
- **THEN** the system processes database results in batches of 10000 rows/documents
- **AND** maintains memory efficiency for large database result sets
- **AND** conversion metrics accurately reflect batch processing

#### Scenario: Convert from database with error handling
- **WHEN** `convert()` is called with a database source and database connection fails or query errors occur
- **THEN** the system raises an appropriate exception with clear error message
- **AND** database connection is properly closed even on error
- **AND** no partial output file is created

#### Scenario: Atomic write on successful conversion from database
- **WHEN** `convert()` is called with `atomic=True` and a database source, and conversion completes successfully
- **THEN** data is written to a temporary file (e.g., `output.tmp`)
- **AND** the temporary file is atomically renamed to the final destination using `os.replace()`
- **AND** the temporary file is removed after successful rename
- **AND** the final output file is only visible when fully written

#### Scenario: Atomic write preserves original file on database conversion failure
- **WHEN** `convert()` is called with `atomic=True` and a database source, and conversion fails or is interrupted
- **THEN** the temporary file is cleaned up
- **AND** the original destination file (if it existed) remains unchanged
- **AND** no partial or corrupted output file is left at the destination
- **AND** database connection is properly closed

#### Scenario: Non-atomic write (backward compatibility)
- **WHEN** `convert()` is called with `atomic=False` (default)
- **THEN** data is written directly to the destination file
- **AND** behavior matches existing implementation

#### Scenario: Atomic write with bulk conversion from databases
- **WHEN** `bulk_convert()` processes multiple database sources with `atomic=True`
- **THEN** each database conversion uses atomic writes independently
- **AND** temporary files are cleaned up for each conversion regardless of overall batch success or failure
- **AND** database connections are properly managed for each source

#### Scenario: Convert from database with progress tracking
- **WHEN** `convert()` is called with a database source and `progress` callback or `show_progress=True`
- **THEN** the system invokes progress callbacks with database-specific metrics (rows read, elapsed time)
- **AND** progress tracking works consistently with file-based sources

#### Scenario: Convert from database with format-specific options
- **WHEN** `convert()` is called with a database source and `toiterableargs` specifying output format options (e.g., Parquet compression, CSV delimiter)
- **THEN** the system applies format-specific options to the output file
- **AND** database source options are handled via `iterableargs` separately

#### Scenario: Backward compatibility with file sources
- **WHEN** `convert()` is called with file paths (not database connection strings)
- **THEN** the system continues to work exactly as before, with no changes to existing behavior
