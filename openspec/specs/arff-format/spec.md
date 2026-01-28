# arff-format Specification

## Purpose
TBD - created by archiving change add-html-arff-formats. Update Purpose after archive.
## Requirements
### Requirement: ARFF File Reading
The system SHALL support reading ARFF (Attribute-Relation File Format) files and yielding data instances as dictionary records with proper type conversion based on attribute definitions.

#### Scenario: Read standard ARFF file
- **WHEN** opening a valid `.arff` file with attribute definitions and data section
- **THEN** it yields records containing attribute values with proper types (numeric, nominal, string, date)

#### Scenario: Read ARFF with automatic detection
- **WHEN** using `open_iterable` on a `.arff` file
- **THEN** it automatically selects `ARFFIterable` for processing

#### Scenario: Parse ARFF attributes
- **WHEN** reading an ARFF file with attribute definitions
- **THEN** it extracts attribute names and types from the `@attribute` declarations

#### Scenario: Handle ARFF sparse format
- **WHEN** reading an ARFF file with sparse data format (using `{index value}` notation)
- **THEN** it correctly expands sparse instances to full dictionaries with missing values

#### Scenario: Convert ARFF data types
- **WHEN** reading ARFF data instances
- **THEN** it converts values according to attribute types (numeric to float/int, nominal to string, date to datetime)

#### Scenario: Handle missing values
- **WHEN** reading ARFF data with missing values (represented as `?`)
- **THEN** it represents missing values as `None` in the dictionary records

#### Scenario: Handle ARFF relation name
- **WHEN** reading an ARFF file with a `@relation` declaration
- **THEN** it preserves or exposes the relation name (e.g., via metadata or as a special field)

#### Scenario: Handle missing dependency
- **WHEN** `liac-arff` is not installed
- **THEN** it raises an `ImportError` with a helpful message instructing to install `iterabledata[arff]`

