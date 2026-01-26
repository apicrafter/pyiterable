# Change: Add Cloud Storage Support (S3/GCS/Azure)

## Why
Many real-world datasets are stored in cloud object storage services like Amazon S3, Google Cloud Storage (GCS), and Azure Blob Storage. Currently, IterableData only supports local filesystem paths, which limits its practical utility for modern data workflows that operate on cloud-hosted data.

Users must currently download files locally before processing, which:
- Adds unnecessary steps and complexity to data pipelines
- Requires local disk space for potentially large datasets
- Prevents direct streaming from cloud storage
- Creates friction for cloud-native workflows

Adding transparent cloud storage support via `fsspec` will:
- Enable direct access to cloud-hosted datasets without local downloads
- Maintain the existing format detection and codec logic unchanged
- Provide a unified interface for local and cloud files
- Support streaming processing from cloud storage (memory-efficient)
- Add significant practical value with minimal architectural changes

## What Changes
- **Cloud Storage URI Detection**:
  - Modify `open_iterable()` to detect cloud storage URIs (e.g., `s3://`, `gs://`, `az://`, `abfs://`)
  - Support common URI schemes: `s3://`, `s3a://`, `gs://`, `gcs://`, `az://`, `abfs://`, `abfss://`
- **fsspec Integration**:
  - Use `fsspec` as the abstraction layer for cloud storage backends
  - Create file-like objects from cloud storage URIs via `fsspec.open()`
  - Pass these file-like objects to existing codec and iterable logic
  - Handle both read and write modes for cloud storage
- **Stream Handling**:
  - Ensure cloud storage streams work with existing codec implementations
  - Support compression codecs (gzip, zstd, etc.) on cloud storage files
  - Maintain streaming behavior for memory efficiency
- **Authentication**:
  - Support standard cloud storage authentication methods (environment variables, credentials files, IAM roles)
  - Rely on fsspec's built-in authentication mechanisms
  - Document authentication requirements in documentation
- **Optional Dependency**:
  - Add `fsspec` and cloud-specific backends (`s3fs`, `gcsfs`, `adlfs`) as optional dependencies
  - Methods raise `ImportError` with helpful message if dependencies are missing
  - Core library remains lightweight without cloud storage dependencies

## Impact
- **Affected Specs**:
  - `cloud-storage` - NEW capability for cloud storage URI support
- **Affected Files**:
  - `iterable/helpers/detect.py` - Modify `open_iterable()` to detect and handle cloud URIs
  - `iterable/base.py` - Ensure `BaseFileIterable` can handle fsspec file-like objects
  - `pyproject.toml` - Add optional dependencies: `fsspec`, `s3fs`, `gcsfs`, `adlfs`
  - `tests/test_cloud_storage.py` (new) - Comprehensive tests for cloud storage support
  - `CHANGELOG.md` - Document new cloud storage feature
  - `docs/docs/api/cloud-storage.md` (new) - Documentation for cloud storage usage
- **Dependencies**:
  - New optional dependencies: `fsspec`, `s3fs`, `gcsfs`, `adlfs`
  - All dependencies are optional - core library remains lightweight
  - Users only install cloud backends they need
- **Backward Compatibility**:
  - All changes are additive and backward compatible
  - Existing local file paths continue to work unchanged
  - Cloud storage support is transparent - no API changes required
  - Format detection and codec logic remain unchanged
