# netcdf-format Specification

## Purpose
TBD - created by archiving change add-additional-formats. Update Purpose after archive.
## Requirements
### Requirement: NetCDF File Reading
The system SHALL support reading NetCDF (Network Common Data Form) files and yielding data variables as dictionary records.

#### Scenario: Read NetCDF file with automatic detection
- **WHEN** using `open_iterable` on a `.nc` file
- **THEN** it automatically selects `NetCDFIterable` for processing

#### Scenario: Read NetCDF variables
- **WHEN** reading a NetCDF file with multiple variables
- **THEN** it yields records containing variable data with proper dimensions and attributes

#### Scenario: Handle NetCDF dimensions
- **WHEN** reading a NetCDF file with multi-dimensional variables
- **THEN** it properly handles dimension ordering and yields data in a structured format

#### Scenario: Access NetCDF attributes
- **WHEN** reading a NetCDF file with global or variable attributes
- **THEN** it preserves attribute information in the yielded records or metadata

#### Scenario: Handle missing dependency
- **WHEN** `netCDF4` is not installed
- **THEN** it raises an `ImportError` with a helpful message instructing to install `iterabledata[netcdf]`

