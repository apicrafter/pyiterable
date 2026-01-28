## 1. Implementation

### 1.1 Cloud Storage URI Detection
- [x] 1.1.1 Create helper function to detect cloud storage URIs in `iterable/helpers/detect.py`
  - [x] Support schemes: `s3://`, `s3a://`, `gs://`, `gcs://`, `az://`, `abfs://`, `abfss://`
  - [x] Return boolean indicating if URI is cloud storage
  - [x] Handle edge cases (empty strings, malformed URIs)
- [x] 1.1.2 Modify `open_iterable()` to check for cloud storage URIs
  - [x] Call detection helper before local file existence check
  - [x] Route cloud URIs to fsspec-based handling
  - [x] Keep existing local file logic unchanged

### 1.2 fsspec Integration
- [x] 1.2.1 Add fsspec file opening logic in `iterable/helpers/detect.py`
  - [x] Use `fsspec.open()` to create file-like objects from cloud URIs
  - [x] Handle both text and binary modes appropriately
  - [x] Support read and write modes
  - [x] Pass file-like object to existing iterable initialization
- [x] 1.2.2 Ensure compatibility with existing codec system
  - [x] Verify codecs work with fsspec file-like objects
  - [x] Test compression codecs (gzip, zstd, etc.) with cloud storage
  - [x] Handle streaming behavior correctly
- [x] 1.2.3 Update `BaseFileIterable` if needed
  - [x] Ensure it can handle fsspec file-like objects
  - [x] Verify stream handling works correctly
  - [x] Test reset() behavior with cloud storage (if supported)

### 1.3 Authentication and Configuration
- [x] 1.3.1 Document authentication requirements
  - [x] Document S3 authentication (AWS credentials, IAM roles)
  - [x] Document GCS authentication (service account, application default credentials)
  - [x] Document Azure authentication (connection strings, service principals)
  - [x] Include examples in documentation
- [x] 1.3.2 Support fsspec storage options
  - [x] Allow passing storage_options to `open_iterable()` via `iterableargs`
  - [x] Forward storage_options to fsspec.open()
  - [x] Document usage in API docs

### 1.4 Dependencies
- [x] 1.4.1 Add optional dependencies to `pyproject.toml`:
  - [x] Add `fsspec` to optional dependencies
  - [x] Add `s3fs` to optional dependencies (for S3 support)
  - [x] Add `gcsfs` to optional dependencies (for GCS support)
  - [x] Add `adlfs` to optional dependencies (for Azure support)
  - [x] Create `cloud` convenience group: `fsspec`, `s3fs`, `gcsfs`, `adlfs`
  - [x] Update `all` convenience group to include cloud dependencies
- [x] 1.4.2 Add ImportError handling
  - [x] Check for fsspec availability when cloud URI detected
  - [x] Raise helpful ImportError with installation instructions
  - [x] Check for specific backend (s3fs/gcsfs/adlfs) when needed
  - [x] Provide clear error messages

## 2. Testing

- [x] 2.1 Create `tests/test_cloud_storage.py`
- [x] 2.2 Test S3 URI handling:
  - [x] Test `s3://` URI detection
  - [x] Test reading from S3 (mock or test bucket)
  - [x] Test writing to S3 (mock or test bucket)
  - [x] Test with compression (e.g., `s3://bucket/file.jsonl.gz`)
  - [x] Test ImportError when s3fs not installed (mock)
  - [x] Test authentication handling
- [x] 2.3 Test GCS URI handling:
  - [x] Test `gs://` and `gcs://` URI detection
  - [x] Test reading from GCS (mock or test bucket)
  - [x] Test writing to GCS (mock or test bucket)
  - [x] Test with compression
  - [x] Test ImportError when gcsfs not installed (mock)
- [x] 2.4 Test Azure URI handling:
  - [x] Test `az://`, `abfs://`, `abfss://` URI detection
  - [x] Test reading from Azure (mock or test container)
  - [x] Test writing to Azure (mock or test container)
  - [x] Test with compression
  - [x] Test ImportError when adlfs not installed (mock)
- [x] 2.5 Test format detection with cloud URIs:
  - [x] Test CSV detection from cloud storage
  - [x] Test JSONL detection from cloud storage
  - [x] Test Parquet detection from cloud storage
  - [x] Test codec detection (gzip, zstd, etc.) from cloud URIs
- [x] 2.6 Test edge cases:
  - [x] Test empty files in cloud storage
  - [x] Test non-existent files (error handling)
  - [x] Test malformed URIs
  - [x] Test streaming behavior with large files
  - [x] Test reset() behavior (if supported by backend)
- [x] 2.7 Test backward compatibility:
  - [x] Verify local file paths still work
  - [x] Verify no regression in existing functionality
- [x] 2.8 Run all tests: `pytest tests/test_cloud_storage.py -v`

## 3. Documentation

- [x] 3.1 Create `docs/docs/api/cloud-storage.md`:
  - [x] Document supported URI schemes
  - [x] Document authentication methods for each cloud provider
  - [x] Include examples for S3, GCS, and Azure
  - [x] Document compression support
  - [x] Include installation instructions for optional dependencies
  - [x] Document storage_options parameter
  - [x] Include troubleshooting section
- [x] 3.2 Update `docs/docs/api/open-iterable.md`:
  - [x] Add cloud storage URI examples
  - [x] Document cloud storage support in filename parameter
  - [x] Link to cloud-storage.md for detailed information
- [x] 3.3 Update `CHANGELOG.md`:
  - [x] Add entry for cloud storage support feature
  - [x] Document new optional dependencies
  - [x] Include examples
- [x] 3.4 Update main README if needed:
  - [x] Add cloud storage to features list
  - [x] Add quick example in usage section
  - [x] Update installation instructions for cloud support

## 4. Validation

- [x] 4.1 Run linter: `ruff check iterable tests`
- [x] 4.2 Run formatter: `ruff format iterable tests`
- [x] 4.3 Run type checker: `mypy iterable` (with --ignore-missing-imports for optional deps)
- [x] 4.4 Run all tests: `pytest --verbose` (with and without cloud dependencies)
- [x] 4.5 Validate OpenSpec: `openspec validate add-cloud-storage-support --strict`
