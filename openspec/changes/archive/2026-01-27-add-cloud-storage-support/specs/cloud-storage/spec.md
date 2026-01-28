## ADDED Requirements

### Requirement: Cloud Storage URI Support
The system SHALL support reading from and writing to cloud object storage services (Amazon S3, Google Cloud Storage, Azure Blob Storage) via URI schemes, transparently integrating with existing format detection and codec logic.

#### Scenario: Read from S3
- **WHEN** a user calls `open_iterable('s3://bucket/path/file.csv')`
- **THEN** the system detects the S3 URI scheme, opens the file via fsspec, and returns an iterable that works identically to local files

#### Scenario: Read compressed file from GCS
- **WHEN** a user calls `open_iterable('gs://bucket/data.jsonl.gz')`
- **THEN** the system detects the GCS URI, opens the file via fsspec, detects the gzip compression codec, and returns an iterable that transparently decompresses and parses the JSONL format

#### Scenario: Write to Azure Blob Storage
- **WHEN** a user calls `open_iterable('az://container/file.parquet', mode='w')`
- **THEN** the system detects the Azure URI, creates a writable stream via fsspec, and writes data in Parquet format to the cloud storage location

#### Scenario: Format detection with cloud URIs
- **WHEN** a user calls `open_iterable('s3://bucket/data.parquet')` with a Parquet file
- **THEN** the system detects the Parquet format from the URI extension and returns an appropriate Parquet iterable, regardless of the storage backend

#### Scenario: Missing cloud storage dependency
- **WHEN** a user calls `open_iterable('s3://bucket/file.csv')` without `s3fs` installed
- **THEN** the system raises an ImportError with a helpful message indicating that `s3fs` must be installed for S3 support

#### Scenario: Authentication via environment variables
- **WHEN** a user calls `open_iterable('s3://bucket/file.csv')` with AWS credentials set via environment variables
- **THEN** the system uses fsspec's authentication mechanism to access S3 using the environment credentials

#### Scenario: Authentication via storage_options
- **WHEN** a user calls `open_iterable('s3://bucket/file.csv', iterableargs={'storage_options': {'key': '...', 'secret': '...'}})`
- **THEN** the system passes the storage_options to fsspec for authentication

#### Scenario: Streaming from cloud storage
- **WHEN** a user iterates over a large file from cloud storage (e.g., `s3://bucket/large.csv`)
- **THEN** the system streams data without loading the entire file into memory, maintaining memory efficiency

#### Scenario: Codec support with cloud storage
- **WHEN** a user calls `open_iterable('gs://bucket/data.jsonl.zst')` with a ZStandard-compressed file
- **THEN** the system detects the compression codec, opens the file via fsspec, and applies the codec transparently, just as with local files

#### Scenario: Backward compatibility with local files
- **WHEN** a user calls `open_iterable('/local/path/file.csv')` with a local file path
- **THEN** the system continues to work exactly as before, with no changes to existing behavior
