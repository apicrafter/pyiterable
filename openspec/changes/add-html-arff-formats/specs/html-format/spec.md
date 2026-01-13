## ADDED Requirements

### Requirement: HTML Table Reading
The system SHALL support reading HTML files and extracting tabular data from HTML tables, yielding each table row as a dictionary record.

#### Scenario: Read HTML file with single table
- **WHEN** opening a valid `.html` file containing a single `<table>` element
- **THEN** it yields records where each row is converted to a dictionary with column headers as keys

#### Scenario: Read HTML file with multiple tables
- **WHEN** opening an HTML file containing multiple `<table>` elements
- **THEN** it yields records from all tables, with each record optionally including a table identifier

#### Scenario: Read HTML with automatic detection
- **WHEN** using `open_iterable` on a `.html` or `.htm` file
- **THEN** it automatically selects `HTMLIterable` for processing

#### Scenario: Handle HTML without tables
- **WHEN** opening an HTML file that contains no `<table>` elements
- **THEN** it yields no records (empty iterator) or raises an appropriate error

#### Scenario: Handle missing dependency
- **WHEN** `beautifulsoup4` is not installed
- **THEN** it raises an `ImportError` with a helpful message instructing to install `iterabledata[html]`

#### Scenario: Extract table headers
- **WHEN** reading an HTML table with `<th>` header cells
- **THEN** it uses those headers as dictionary keys for row data

#### Scenario: Handle tables without headers
- **WHEN** reading an HTML table without `<th>` elements
- **THEN** it generates column names (e.g., `column_0`, `column_1`) or uses the first row as headers
