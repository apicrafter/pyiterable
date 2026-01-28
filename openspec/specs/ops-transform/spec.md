# ops-transform Specification

## Purpose
TBD - created by archiving change add-high-level-operations. Update Purpose after archive.
## Requirements
### Requirement: Row Slicing Operations
The system SHALL provide functions to slice rows from an iterable dataset (head, tail, slice).

#### Scenario: Get first N rows
- **WHEN** `transform.head()` is called with an iterable and `n=100`
- **THEN** the function returns an iterator yielding the first 100 rows
- **AND** the original iterable is not fully consumed

#### Scenario: Get last N rows
- **WHEN** `transform.tail()` is called with an iterable and `n=50`
- **THEN** the function returns a list containing the last 50 rows
- **AND** the function handles datasets smaller than N rows gracefully

#### Scenario: Slice rows by range
- **WHEN** `transform.slice_rows()` is called with `start=100, end=200`
- **THEN** the function returns an iterator yielding rows 100-199 (inclusive start, exclusive end)
- **AND** the function handles edge cases (start > dataset size, etc.)

### Requirement: Random Sampling
The system SHALL provide a function to randomly sample rows from an iterable dataset.

#### Scenario: Sample N rows
- **WHEN** `transform.sample_rows()` is called with an iterable and `n=1000`
- **THEN** the function returns an iterator yielding approximately 1000 randomly selected rows
- **AND** sampling is performed efficiently without materializing the entire dataset when possible

#### Scenario: Sample with seed
- **WHEN** `transform.sample_rows()` is called with `seed=42`
- **THEN** the sampling is reproducible
- **AND** the same seed produces the same sample

### Requirement: Deduplication
The system SHALL provide a function to remove duplicate rows based on specified key fields.

#### Scenario: Deduplicate by key fields
- **WHEN** `transform.deduplicate()` is called with `keys=["email"]`
- **THEN** the function returns an iterator with duplicate rows removed
- **AND** only the first occurrence of each unique key combination is kept by default

#### Scenario: Deduplicate with keep strategy
- **WHEN** `transform.deduplicate()` is called with `keys=["id"]` and `keep="last"`
- **THEN** the function keeps the last occurrence of each duplicate
- **AND** earlier occurrences are removed

#### Scenario: Deduplicate with custom comparison
- **WHEN** `transform.deduplicate()` is called with a custom key function
- **THEN** the function uses the custom function to determine uniqueness
- **AND** deduplication works correctly with the custom logic

### Requirement: Column Selection
The system SHALL provide a function to select specific columns from rows.

#### Scenario: Select specific fields
- **WHEN** `transform.select()` is called with `fields=["id", "name", "email"]`
- **THEN** the function returns an iterator where each row contains only the specified fields
- **AND** missing fields are handled gracefully (included as None or omitted)

#### Scenario: Select with field renaming
- **WHEN** `transform.select()` is called with field mapping `{"old_name": "new_name"}`
- **THEN** the function returns rows with renamed fields
- **AND** original fields are removed if not in the mapping

### Requirement: Field Enumeration
The system SHALL provide a function to add sequence numbers or enumeration to rows.

#### Scenario: Add sequence field
- **WHEN** `transform.enum_field()` is called with `field="seq_id"` and `type="int"`
- **THEN** each row receives a new field `seq_id` with an incrementing integer value
- **AND** enumeration starts from 0 or 1 (configurable)

#### Scenario: Enum with UUID
- **WHEN** `transform.enum_field()` is called with `field="id"` and `type="uuid"`
- **THEN** each row receives a new field `id` with a unique UUID value
- **AND** UUIDs are generated for each row

### Requirement: Missing Value Filling
The system SHALL provide a function to fill missing/null values in fields.

#### Scenario: Fill with forward strategy
- **WHEN** `transform.fill_missing()` is called with `field="status"` and `strategy="forward"`
- **THEN** missing values are filled using the last valid value (forward fill)
- **AND** the function handles consecutive missing values correctly

#### Scenario: Fill with constant value
- **WHEN** `transform.fill_missing()` is called with `field="category"` and `value="unknown"`
- **THEN** all missing values in the field are replaced with "unknown"
- **AND** the function works for all data types

### Requirement: Field Renaming
The system SHALL provide a function to rename fields in rows.

#### Scenario: Rename single field
- **WHEN** `transform.rename_fields()` is called with `{"old_name": "new_name"}`
- **THEN** all rows have the field `old_name` renamed to `new_name`
- **AND** other fields remain unchanged

#### Scenario: Rename multiple fields
- **WHEN** `transform.rename_fields()` is called with multiple field mappings
- **THEN** all specified fields are renamed according to the mapping
- **AND** renaming is applied atomically to all rows

### Requirement: Field Explosion
The system SHALL provide a function to explode array or delimited string fields into multiple rows.

#### Scenario: Explode array field
- **WHEN** `transform.explode()` is called with `field="tags"` where tags is an array
- **THEN** each row with multiple tags is split into multiple rows (one per tag)
- **AND** other fields are duplicated for each exploded row

#### Scenario: Explode delimited string
- **WHEN** `transform.explode()` is called with `field="categories"` and `separator=","`
- **THEN** comma-separated values are split into separate rows
- **AND** whitespace is trimmed appropriately

### Requirement: Value Replacement
The system SHALL provide a function to replace values in fields based on patterns or exact matches.

#### Scenario: Replace with pattern
- **WHEN** `transform.replace_values()` is called with `pattern="foo"` and `replacement="bar"`
- **THEN** all occurrences of "foo" in the specified field are replaced with "bar"
- **AND** replacement works for string fields

#### Scenario: Replace with regex
- **WHEN** `transform.replace_values()` is called with `pattern=r"\d+"` and `replacement="NUMBER"`
- **THEN** all numeric sequences are replaced with "NUMBER"
- **AND** regex replacement works correctly

### Requirement: Row Sorting
The system SHALL provide a function to sort rows by specified fields.

#### Scenario: Sort by single field
- **WHEN** `transform.sort_rows()` is called with `by=["date"]`
- **THEN** rows are sorted by the date field in ascending order
- **AND** sorting handles different data types correctly

#### Scenario: Sort by multiple fields
- **WHEN** `transform.sort_rows()` is called with `by=["status", "id"]` and `desc=[True, False]`
- **THEN** rows are sorted first by status (descending), then by id (ascending)
- **AND** multi-field sorting works correctly

#### Scenario: Sort with materialization
- **WHEN** `transform.sort_rows()` is called on a large dataset
- **THEN** the function may materialize data as needed for sorting
- **AND** memory usage is documented and optimized where possible

### Requirement: Row/Column Transposition
The system SHALL provide a function to transpose rows and columns.

#### Scenario: Transpose dataset
- **WHEN** `transform.transpose()` is called with an iterable
- **THEN** rows become columns and columns become rows
- **AND** the function handles variable-length rows appropriately

### Requirement: Field Splitting
The system SHALL provide a function to split fields into multiple fields.

#### Scenario: Split field by delimiter
- **WHEN** `transform.split()` is called with `field="full_name"` and `separator=" "` into `["first", "last"]`
- **THEN** the field is split into two new fields
- **AND** original field is removed or preserved (configurable)

### Requirement: Field Length Fixing
The system SHALL provide a function to fix field lengths (padding or truncation).

#### Scenario: Fix field lengths
- **WHEN** `transform.fixlengths()` is called with length constraints
- **THEN** fields are padded or truncated to specified lengths
- **AND** padding uses specified character (default: space)

### Requirement: Iterable Concatenation
The system SHALL provide a function to concatenate multiple iterables.

#### Scenario: Concatenate iterables
- **WHEN** `transform.cat()` is called with multiple iterables
- **THEN** the function returns an iterator that yields all rows from all iterables in sequence
- **AND** field schemas are handled appropriately (union of all fields)

### Requirement: Relational Join Operations
The system SHALL provide functions to join two iterables based on key fields.

#### Scenario: Inner join
- **WHEN** `transform.join()` is called with two iterables and `join_type="inner"`
- **THEN** the function returns rows where keys match in both iterables
- **AND** joined rows contain fields from both iterables

#### Scenario: Left join
- **WHEN** `transform.join()` is called with `join_type="left"`
- **THEN** all rows from the left iterable are included
- **AND** missing matches from the right iterable have null values

#### Scenario: Join with DuckDB optimization
- **WHEN** `transform.join()` is called with DuckDB engine available
- **THEN** the join is performed efficiently using DuckDB when possible
- **AND** falls back to Python implementation when needed

### Requirement: Set Difference Operations
The system SHALL provide functions to compute set differences between iterables.

#### Scenario: Diff operation
- **WHEN** `transform.diff()` is called with two iterables and key fields
- **THEN** the function returns rows present in the first iterable but not in the second
- **AND** comparison is based on specified key fields

#### Scenario: Exclude operation
- **WHEN** `transform.exclude()` is called with an iterable and exclusion criteria
- **THEN** rows matching the exclusion criteria are removed
- **AND** the function works with both key-based and expression-based exclusion

