## ADDED Requirements

### Requirement: DXF File Reading
The system SHALL support reading DXF (Drawing Exchange Format) files and yielding CAD entities as dictionary records.

#### Scenario: Read DXF file with automatic detection
- **WHEN** using `open_iterable` on a `.dxf` file
- **THEN** it automatically selects `DXFIterable` for processing

#### Scenario: Read DXF entities
- **WHEN** reading a DXF file with CAD entities
- **THEN** it yields records containing entity data (lines, circles, arcs, text, etc.)

#### Scenario: Handle DXF entity types
- **WHEN** reading DXF entities of different types
- **THEN** it properly represents entity properties and geometry in the yielded records

#### Scenario: Handle DXF layers
- **WHEN** reading a DXF file with entities organized in layers
- **THEN** it preserves layer information in the yielded records

#### Scenario: Handle DXF blocks and references
- **WHEN** reading a DXF file with block definitions and insertions
- **THEN** it properly handles block references and expands them if needed

#### Scenario: Handle missing dependency
- **WHEN** `ezdxf` is not installed
- **THEN** it raises an `ImportError` with a helpful message instructing to install `iterabledata[dxf]`
