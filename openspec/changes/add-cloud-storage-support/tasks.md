## 1. Implementation

### 1.1 Cloud Storage URI Detection
- [ ] 1.1.1 Create helper function to detect cloud storage URIs in `iterable/helpers/detect.py`
  - [ ] Support schemes: `s3://`, `s3a://`, `gs://`, `gcs://`, `az://`, `abfs://`, `abfss://`
  - [ ] Return boolean indicating if URI is cloud storage
  - [ ] Handle edge cases (empty strings, malformed URIs)
- [ ] 1.1.2 Modify `open_iterable()` to check for cloud storage URIs
  - [ ] Call detection helper before local file existence check
  - [ ] Route cloud URIs to fsspec-based handling
  - [ ] Keep existing local file logic unchanged

### 1.2 fsspec Integration
- [ ] 1.2.1 Add fsspec file opening logic in `iterable/helpers/detect.py`
  - [ ] Use `fsspec.open()` to create file-like objects from cloud URIs
  - [ ] Handle both text and binary modes appropriately
  - [ ] Support read and write modes
  - [ ] Pass file-like object to existing iterable initialization
- [ ] 1.2.2 Ensure compatibility with existing codec system
  - [ ] Verify codecs work with fsspec file-like objects
  - [ ] Test compression codecs (gzip, zstd, etc.) with cloud storage
  - [ ] Handle streaming behavior correctly
- [ ] 1.2.3 Update `BaseFileIterable` if needed
  - [ ] Ensure it can handle fsspec file-like objects
  - [ ] Verify stream handling works correctly
  - [ ] Test reset() behavior with cloud storage (if supported)

### 1.3 Authentication and Configuration
- [ ] 1.3.1 Document authentication requirements
  - [ ] Document S3 authentication (AWS credentials, IAM roles)
  - [ ] Document GCS authentication (service account, application default credentials)
  - [ ] Document Azure authentication (connection strings, service principals)
  - [ ] Include examples in documentation
- [ ] 1.3.2 Support fsspec storage options
  - [ ] Allow passing storage_options to `open_iterable()` via `iterableargs`
  - [ ] Forward storage_options to fsspec.open()
  - [ ] Document usage in API docs

### 1.4 Dependencies
- [ ] 1.4.1 Add optional dependencies to `pyproject.toml`:
  - [ ] Add `fsspec` to optional dependencies
  - [ ] Add `s3fs` to optional dependencies (for S3 support)
  - [ ] Add `gcsfs` to optional dependencies (for GCS support)
  - [ ] Add `adlfs` to optional dependencies (for Azure support)
  - [ ] Create `cloud` convenience group: `fsspec`, `s3fs`, `gcsfs`, `adlfs`
  - [ ] Update `all` convenience group to include cloud dependencies
- [ ] 1.4.2 Add ImportError handling
  - [ ] Check for fsspec availability when cloud URI detected
  - [ ] Raise helpful ImportError with installation instructions
  - [ ] Check for specific backend (s3fs/gcsfs/adlfs) when needed
  - [ ] Provide clear error messages

## 2. Testing

- [ ] 2.1 Create `tests/test_cloud_storage.py`
- [ ] 2.2 Test S3 URI handling:
  - [ ] Test `s3://` URI detection
  - [ ] Test reading from S3 (mock or test bucket)
  - [ ] Test writing to S3 (mock or test bucket)
  - [ ] Test with compression (e.g., `s3://bucket/file.jsonl.gz`)
  - [ ] Test ImportError when s3fs not installed (mock)
  - [ ] Test authentication handling
- [ ] 2.3 Test GCS URI handling:
  - [ ] Test `gs://` and `gcs://` URI detection
  - [ ] Test reading from GCS (mock or test bucket)
  - [ ] Test writing to GCS (mock or test bucket)
  - [ ] Test with compression
  - [ ] Test ImportError when gcsfs not installed (mock)
- [ ] 2.4 Test Azure URI handling:
  - [ ] Test `az://`, `abfs://`, `abfss://` URI detection
  - [ ] Test reading from Azure (mock or test container)
  - [ ] Test writing to Azure (mock or test container)
  - [ ] Test with compression
  - [ ] Test ImportError when adlfs not installed (mock)
- [ ] 2.5 Test format detection with cloud URIs:
  - [ ] Test CSV detection from cloud storage
  - [ ] Test JSONL detection from cloud storage
  - [ ] Test Parquet detection from cloud storage
  - [ ] Test codec detection (gzip, zstd, etc.) from cloud URIs
- [ ] 2.6 Test edge cases:
  - [ ] Test empty files in cloud storage
  - [ ] Test non-existent files (error handling)
  - [ ] Test malformed URIs
  - [ ] Test streaming behavior with large files
  - [ ] Test reset() behavior (if supported by backend)
- [ ] 2.7 Test backward compatibility:
  - [ ] Verify local file paths still work
  - [ ] Verify no regression in existing functionality
- [ ] 2.8 Run all tests: `pytest tests/test_cloud_storage.py -v`

## 3. Documentation

- [ ] 3.1 Create `docs/docs/api/cloud-storage.md`:
  - [ ] Document supported URI schemes
  - [ ] Document authentication methods for each cloud provider
  - [ ] Include examples for S3, GCS, and Azure
  - [ ] Document compression support
  - [ ] Include installation instructions for optional dependencies
  - [ ] Document storage_options parameter
  - [ ] Include troubleshooting section
- [ ] 3.2 Update `docs/docs/api/open-iterable.md`:
  - [ ] Add cloud storage URI examples
  - [ ] Document cloud storage support in filename parameter
  - [ ] Link to cloud-storage.md for detailed information
- [ ] 3.3 Update `CHANGELOG.md`:
  - [ ] Add entry for cloud storage support feature
  - [ ] Document new optional dependencies
  - [ ] Include examples
- [ ] 3.4 Update main README if needed:
  - [ ] Add cloud storage to features list
  - [ ] Add quick example in usage section
  - [ ] Update installation instructions for cloud support

## 4. Validation

- [ ] 4.1 Run linter: `ruff check iterable tests`
- [ ] 4.2 Run formatter: `ruff format iterable tests`
- [ ] 4.3 Run type checker: `mypy iterable` (with --ignore-missing-imports for optional deps)
- [ ] 4.4 Run all tests: `pytest --verbose` (with and without cloud dependencies)
- [ ] 4.5 Validate OpenSpec: `openspec validate add-cloud-storage-support --strict`
