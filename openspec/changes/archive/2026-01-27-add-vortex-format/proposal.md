# Change: Add Support for Vortex File Format

## Why
Users need to process Vortex files, a modern columnar data format designed for efficient querying and compression. Vortex provides fast random access compared to Parquet, supports selective row reading, and offers excellent compression ratios. Adding support for Vortex files expands the utility of `iterabledata` for high-performance data processing pipelines, particularly in scenarios requiring efficient columnar storage with fast access patterns.

## What Changes
-   **Dependencies**:
    -   Add `vortex-data>=0.56.0` for Vortex format support.
    -   Update `pyproject.toml` to include this as an optional dependency (extra).
    -   **Note**: `vortex-data` requires Python ≥3.11, but the library supports Python 3.10+. The implementation will gracefully handle this version constraint.
-   **New Iterable**:
    -   `iterable/datatypes/vortex.py`: Implement `VortexIterable` class.
    -   Support both read and write operations.
    -   Integrate with PyArrow for data conversion (Vortex arrays ↔ Python dicts).
-   **Detection**:
    -   Update `iterable/helpers/detect.py` to recognize extensions: `.vortex`, `.vtx`.
    -   Add magic number detection (`VTXF` at file start) for content-based format detection.
    -   Add `vortex` and `vtx` to `FLAT_TYPES` list.

## Impact
-   **New Capability**:
    -   `vortex-format` - Support for reading and writing Vortex columnar files
-   **Affected Files**:
    -   `pyproject.toml` - Add `vortex-data` dependency
    -   `iterable/helpers/detect.py` - Register format and add detection logic
    -   `iterable/datatypes/vortex.py` (new) - Vortex format implementation
    -   `tests/test_vortex.py` (new) - Test suite for Vortex format
    -   `docs/docs/formats/vortex.md` (new) - Format documentation
    -   `CHANGELOG.md` - Document new format support
-   **Python Version Consideration**:
    -   `vortex-data` requires Python ≥3.11, while the library supports 3.10+.
    -   The implementation will raise a clear `ImportError` when the dependency is missing or Python version is incompatible.
    -   This is acceptable as optional dependencies may have stricter version requirements.
