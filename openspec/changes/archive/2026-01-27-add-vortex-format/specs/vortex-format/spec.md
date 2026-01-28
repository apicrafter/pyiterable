## ADDED Requirements

### Requirement: Vortex File Format Support
The system SHALL support reading and writing Vortex columnar data files, providing a unified iterator-based interface consistent with other formats in the library.

#### Scenario: Read Vortex file
- **WHEN** opening a valid `.vortex` or `.vtx` file with `open_iterable()`
- **THEN** it yields dictionary records representing rows from the Vortex file

#### Scenario: Write Vortex file
- **WHEN** writing dictionary records to a `.vortex` or `.vtx` file
- **THEN** it creates a valid Vortex file containing the data

#### Scenario: Automatic format detection by extension
- **WHEN** using `open_iterable()` on a file with `.vortex` or `.vtx` extension
- **THEN** it automatically selects `VortexIterable` without explicit format specification

#### Scenario: Automatic format detection by magic number
- **WHEN** using `open_iterable()` on a file starting with `VTXF` magic bytes
- **THEN** it automatically detects and selects `VortexIterable` even without extension

#### Scenario: Read-write roundtrip
- **WHEN** writing data to a Vortex file and then reading it back
- **THEN** the read data matches the original written data

#### Scenario: Bulk operations
- **WHEN** using `read_bulk()` or `write_bulk()` methods
- **THEN** it efficiently processes multiple records in batches

#### Scenario: Iterator interface
- **WHEN** iterating over a Vortex file using `for row in iterable:`
- **THEN** it yields dictionary records one at a time

#### Scenario: Reset functionality
- **WHEN** calling `reset()` on a Vortex iterable
- **THEN** subsequent reads start from the beginning of the file

#### Scenario: Totals support
- **WHEN** calling `totals()` on a Vortex file
- **THEN** it returns the total number of rows in the file

#### Scenario: Handle missing dependency
- **WHEN** `vortex-data` package is not installed
- **THEN** it raises an `ImportError` with a helpful message instructing to install `iterabledata[vortex]`

#### Scenario: Flat format indicator
- **WHEN** checking if Vortex format is flat-only
- **THEN** `is_flatonly()` returns `True` indicating tabular structure

#### Scenario: Context manager support
- **WHEN** using `with open_iterable('file.vortex') as source:`
- **THEN** the file is properly closed after the context exits
