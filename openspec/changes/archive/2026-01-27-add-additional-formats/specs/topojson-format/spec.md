## ADDED Requirements

### Requirement: TopoJSON File Reading
The system SHALL support reading TopoJSON files and yielding geographic features as dictionary records.

#### Scenario: Read TopoJSON file with automatic detection
- **WHEN** using `open_iterable` on a `.topojson` file
- **THEN** it automatically selects `TopoJSONIterable` for processing

#### Scenario: Read TopoJSON features
- **WHEN** reading a TopoJSON file with geographic features
- **THEN** it yields records containing feature geometries and properties

#### Scenario: Handle TopoJSON topology
- **WHEN** reading a TopoJSON file with shared topology (arcs)
- **THEN** it properly decodes topology and reconstructs feature geometries

#### Scenario: Handle TopoJSON geometry types
- **WHEN** reading TopoJSON features with different geometry types
- **THEN** it properly represents geometries in the yielded records

#### Scenario: Handle missing dependency
- **WHEN** `topojson` is not installed
- **THEN** it raises an `ImportError` with a helpful message instructing to install `iterabledata[topojson]` or `iterabledata[geospatial]`
