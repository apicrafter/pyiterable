# Change: Add DataFrame Bridges (Pandas/Polars/Dask)

## Why
Many data practitioners work with DataFrames (Pandas, Polars, Dask) as their primary data structure. While IterableData excels at streaming row-by-row processing, users often need to convert iterable data into DataFrames for analysis, visualization, or integration with existing DataFrame-based workflows.

Currently, users must manually convert iterables to DataFrames:
- Collect all rows into a list and pass to `pd.DataFrame()` or `pl.DataFrame()`
- Handle chunking for large datasets manually
- Write custom code to build Dask DataFrames from multiple files

This creates friction and discourages adoption. Adding simple bridge methods (`to_pandas()`, `to_polars()`) and a Dask adapter will:
- Lower the barrier to entry for DataFrame users
- Enable seamless integration with existing DataFrame workflows
- Support memory-efficient chunked processing for large datasets
- Provide a one-liner conversion that encourages library adoption

## What Changes
- **Pandas Bridge**:
  - Add `to_pandas(chunksize=None)` method to `BaseIterable`
  - When `chunksize=None`: return a single pandas DataFrame with all data
  - When `chunksize` is specified: return an iterator of DataFrames for chunked processing
  - Handle nested data structures appropriately (flatten or preserve as needed)
- **Polars Bridge**:
  - Add `to_polars(chunksize=None)` method to `BaseIterable`
  - When `chunksize=None`: return a single Polars DataFrame with all data
  - When `chunksize` is specified: return an iterator of Polars DataFrames for chunked processing
  - Leverage Polars' efficient lazy evaluation when possible
- **Dask DataFrame Adapter**:
  - Add `to_dask()` method or helper function that builds a Dask DataFrame from iterable(s)
  - Support single file: `df = src.to_dask()`
  - Support multiple files: `df = to_dask(['file1.csv', 'file2.csv'])` - automatically detects formats
  - Build Dask computation graph from multiple files detected by `open_iterable()`
- **Optional Dependencies**:
  - Add `pandas` and `polars` to optional dependencies in `pyproject.toml`
  - Add `dask[dataframe]` to optional dependencies
  - Methods raise `ImportError` with helpful message if dependencies are missing

## Impact
- **Affected Specs**:
  - `dataframe-bridges` - NEW capability for DataFrame conversion methods
- **Affected Files**:
  - `iterable/base.py` - Add `to_pandas()`, `to_polars()`, `to_dask()` methods to `BaseIterable`
  - `iterable/helpers/bridges.py` (new) - Helper functions for Dask multi-file support
  - `pyproject.toml` - Add optional dependencies: `pandas`, `polars`, `dask[dataframe]`
  - `tests/test_dataframe_bridges.py` (new) - Comprehensive tests for all bridge methods
  - `CHANGELOG.md` - Document new DataFrame bridge features
  - `docs/docs/api/dataframe-bridges.md` (new) - Documentation for DataFrame bridges
- **Dependencies**:
  - New optional dependencies: `pandas`, `polars`, `dask[dataframe]`
  - All dependencies are optional - core library remains lightweight
- **Backward Compatibility**:
  - All changes are additive and backward compatible
  - Existing code continues to work without modifications
  - Methods are opt-in - no impact on existing iterable behavior
