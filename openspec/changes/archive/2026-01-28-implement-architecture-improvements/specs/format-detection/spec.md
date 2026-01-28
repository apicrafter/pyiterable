# Format Detection

## MODIFIED Requirements

### Requirement: File Type Detection
The system SHALL detect file types using both filename extensions and content-based detection (magic numbers and heuristics) to support files without extensions, streams, and files with incorrect extensions.

#### Scenario: Filename-based detection (existing behavior)
- **WHEN** file has a recognized extension (e.g., `.csv`, `.json`, `.parquet`)
- **THEN** system detects format from extension
- **AND** detection is fast and reliable

#### Scenario: Content-based detection for binary formats
- **WHEN** file has no extension or unknown extension
- **AND** file is a binary format (Parquet, ORC, ZIP-based formats)
- **THEN** system reads first bytes (magic numbers) to detect format
- **AND** system identifies format from magic number signatures:
  - `PAR1` → Parquet
  - `ORC` → ORC
  - `PK\x03\x04` → ZIP-based formats (XLSX, DOCX, etc.)
- **AND** file pointer is reset to beginning after detection

#### Scenario: Content-based detection for text formats
- **WHEN** file has no extension or unknown extension
- **AND** file is a text format (JSON, CSV, JSONL)
- **THEN** system reads first bytes to analyze content
- **AND** system uses heuristics to detect format:
  - Starts with `{` or `[` → JSON
  - Contains commas or tabs in first 100 bytes → CSV
  - Each line is valid JSON → JSONL
- **AND** detection includes confidence score

#### Scenario: Combined detection strategy
- **WHEN** both filename and content detection are available
- **THEN** system uses filename as primary method
- **AND** content detection is used as fallback or validation
- **AND** system reports confidence score for detection result

#### Scenario: Stream detection
- **WHEN** file object is a stream without filename
- **THEN** system uses content-based detection exclusively
- **AND** system reads minimum bytes needed for detection
- **AND** stream position is preserved or reset when possible

#### Scenario: Detection confidence
- **WHEN** format is detected
- **THEN** system provides confidence score (high/medium/low)
- **AND** high confidence: filename matches content
- **AND** medium confidence: content matches but no filename
- **AND** low confidence: ambiguous content, user confirmation may be needed

## ADDED Requirements

### Requirement: Magic Number Detection
The system SHALL detect binary file formats by reading and analyzing magic number signatures from file headers.

#### Scenario: Detect Parquet format
- **WHEN** file starts with `PAR1` magic number
- **THEN** system identifies format as Parquet
- **AND** returns format ID "parquet"

#### Scenario: Detect ORC format
- **WHEN** file starts with `ORC` magic number
- **THEN** system identifies format as ORC
- **AND** returns format ID "orc"

#### Scenario: Detect ZIP-based formats
- **WHEN** file starts with `PK\x03\x04` (ZIP signature)
- **THEN** system reads ZIP structure to identify specific format
- **AND** checks for format-specific markers (e.g., `xl/` for XLSX)
- **AND** returns appropriate format ID (xlsx, docx, etc.)

#### Scenario: Handle non-seekable streams
- **WHEN** file object is not seekable
- **THEN** system reads magic numbers into buffer
- **AND** provides buffer to format parser if needed
- **AND** does not attempt to seek back

### Requirement: Content Heuristic Detection
The system SHALL use content heuristics to detect text-based formats when filename is unavailable or unreliable.

#### Scenario: Detect JSON from content
- **WHEN** file content starts with `{` or `[` after whitespace
- **AND** content appears to be valid JSON structure
- **THEN** system identifies format as JSON
- **AND** returns format ID "json"

#### Scenario: Detect CSV from content
- **WHEN** file content contains commas or tabs in first 100 bytes
- **AND** content has consistent delimiter pattern
- **THEN** system identifies format as CSV
- **AND** returns format ID "csv"

#### Scenario: Detect JSONL from content
- **WHEN** each line of file appears to be valid JSON
- **AND** file has multiple lines
- **THEN** system identifies format as JSONL
- **AND** returns format ID "jsonl"

#### Scenario: Ambiguous content handling
- **WHEN** content matches multiple format patterns
- **THEN** system returns format with highest confidence
- **AND** may require explicit format specification from user
