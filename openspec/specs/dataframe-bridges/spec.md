# dataframe-bridges Specification

## Purpose
TBD - created by archiving change add-dataframe-bridges. Update Purpose after archive.
## Requirements
### Requirement: Pandas DataFrame Conversion
The system SHALL provide a `to_pandas()` method on all iterable objects that converts the iterable data into a pandas DataFrame.

#### Scenario: Convert entire iterable to single DataFrame
- **WHEN** user calls `to_pandas()` without `chunksize` parameter on an iterable object
- **THEN** the method SHALL collect all rows from the iterable and return a single pandas DataFrame
- **AND** the DataFrame SHALL contain all data from the iterable
- **AND** nested data structures SHALL be preserved as dict/list columns or flattened appropriately

#### Scenario: Convert iterable to chunked DataFrames
- **WHEN** user calls `to_pandas(chunksize=100000)` with a `chunksize` parameter
- **THEN** the method SHALL return an iterator that yields pandas DataFrames
- **AND** each DataFrame SHALL contain at most `chunksize` rows (except possibly the last chunk)
- **AND** this SHALL enable memory-efficient processing of large datasets

#### Scenario: Pandas not installed
- **WHEN** user calls `to_pandas()` but pandas is not installed
- **THEN** the method SHALL raise an `ImportError` with a helpful message indicating pandas must be installed
- **AND** the message SHALL include installation instructions

#### Scenario: Empty iterable
- **WHEN** user calls `to_pandas()` on an empty iterable
- **THEN** the method SHALL return an empty pandas DataFrame with appropriate column structure

### Requirement: Polars DataFrame Conversion
The system SHALL provide a `to_polars()` method on all iterable objects that converts the iterable data into a Polars DataFrame.

#### Scenario: Convert entire iterable to single DataFrame
- **WHEN** user calls `to_polars()` without `chunksize` parameter on an iterable object
- **THEN** the method SHALL collect all rows from the iterable and return a single Polars DataFrame
- **AND** the DataFrame SHALL contain all data from the iterable
- **AND** nested data structures SHALL be preserved as struct/list columns or flattened appropriately

#### Scenario: Convert iterable to chunked DataFrames
- **WHEN** user calls `to_polars(chunksize=100000)` with a `chunksize` parameter
- **THEN** the method SHALL return an iterator that yields Polars DataFrames
- **AND** each DataFrame SHALL contain at most `chunksize` rows (except possibly the last chunk)
- **AND** this SHALL enable memory-efficient processing of large datasets

#### Scenario: Polars not installed
- **WHEN** user calls `to_polars()` but Polars is not installed
- **THEN** the method SHALL raise an `ImportError` with a helpful message indicating Polars must be installed
- **AND** the message SHALL include installation instructions

#### Scenario: Empty iterable
- **WHEN** user calls `to_polars()` on an empty iterable
- **THEN** the method SHALL return an empty Polars DataFrame with appropriate column structure

### Requirement: Dask DataFrame Conversion
The system SHALL provide a `to_dask()` method on iterable objects and a helper function for converting iterable data into Dask DataFrames.

#### Scenario: Convert single file iterable to Dask DataFrame
- **WHEN** user calls `to_dask()` on a single iterable object
- **THEN** the method SHALL return a Dask DataFrame representing the iterable data
- **AND** the Dask DataFrame SHALL be constructed with appropriate chunking strategy

#### Scenario: Convert multiple files to unified Dask DataFrame
- **WHEN** user calls `to_dask(['file1.csv', 'file2.jsonl', 'file3.parquet'])` with a list of file paths
- **THEN** the helper function SHALL use `open_iterable()` to detect the format of each file
- **AND** the function SHALL build a Dask computation graph that combines all files
- **THEN** the function SHALL return a unified Dask DataFrame containing data from all files

#### Scenario: Dask not installed
- **WHEN** user calls `to_dask()` but Dask is not installed
- **THEN** the method SHALL raise an `ImportError` with a helpful message indicating Dask must be installed
- **AND** the message SHALL include installation instructions

#### Scenario: Automatic format detection for multi-file Dask
- **WHEN** user provides multiple files with different formats to `to_dask()`
- **THEN** the system SHALL automatically detect each file's format using `open_iterable()`
- **AND** the system SHALL handle each file according to its detected format
- **AND** all files SHALL be combined into a single unified Dask DataFrame

