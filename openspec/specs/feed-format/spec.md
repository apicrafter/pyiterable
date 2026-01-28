# feed-format Specification

## Purpose
TBD - created by archiving change add-additional-formats. Update Purpose after archive.
## Requirements
### Requirement: Feed File Reading
The system SHALL support reading Atom and RSS feed files and yielding feed entries as dictionary records.

#### Scenario: Read Atom feed with automatic detection
- **WHEN** using `open_iterable` on an `.atom` file or XML file containing Atom feed
- **THEN** it automatically selects `FeedIterable` for processing

#### Scenario: Read RSS feed with automatic detection
- **WHEN** using `open_iterable` on an `.rss` file or XML file containing RSS feed
- **THEN** it automatically selects `FeedIterable` for processing

#### Scenario: Read feed entries
- **WHEN** reading an Atom or RSS feed file
- **THEN** it yields records containing feed entry data (title, link, description, published date, etc.)

#### Scenario: Handle feed metadata
- **WHEN** reading a feed file
- **THEN** it preserves feed-level metadata (title, description, link) in addition to entries

#### Scenario: Handle feed entry fields
- **WHEN** reading feed entries
- **THEN** it includes standard fields: title, link, description, published date, author, and other feed-specific fields

#### Scenario: Handle missing dependency
- **WHEN** `feedparser` is not installed
- **THEN** it raises an `ImportError` with a helpful message instructing to install `iterabledata[feed]`

