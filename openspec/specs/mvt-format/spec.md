# mvt-format Specification

## Purpose
TBD - created by archiving change add-additional-formats. Update Purpose after archive.
## Requirements
### Requirement: MVT File Reading
The system SHALL support reading MVT (Mapbox Vector Tiles) files and yielding vector tile features as dictionary records.

#### Scenario: Read MVT file with automatic detection
- **WHEN** using `open_iterable` on a `.mvt` or `.pbf` file containing vector tiles
- **THEN** it automatically selects `MVTIterable` for processing

#### Scenario: Read MVT tile features
- **WHEN** reading an MVT file with vector tile data
- **THEN** it yields records containing feature geometries and properties

#### Scenario: Handle MVT geometry types
- **WHEN** reading MVT features with different geometry types (Point, LineString, Polygon)
- **THEN** it properly decodes and represents geometries in the yielded records

#### Scenario: Handle MVT layers
- **WHEN** reading an MVT file with multiple layers
- **THEN** it yields features from all layers or allows layer selection

#### Scenario: Handle missing dependency
- **WHEN** `mapbox-vector-tile` is not installed
- **THEN** it raises an `ImportError` with a helpful message instructing to install `iterabledata[mvt]` or `iterabledata[geospatial]`

