## ADDED Requirements

### Requirement: Schema Inference
The system SHALL provide a function to infer schema from an iterable dataset, detecting field names, types, and constraints.

#### Scenario: Infer schema from dataset
- **WHEN** `schema.infer()` is called with an iterable
- **THEN** the function returns a schema object containing:
  - Field names and types
  - Nullability information
  - Sample values for each field
  - Type confidence scores
- **AND** inference uses sampling for large datasets to maintain performance

#### Scenario: Infer schema with type detection
- **WHEN** `schema.infer()` is called with `detect_dates=True`
- **THEN** the function attempts to detect date and datetime fields
- **AND** date formats are recognized and documented in the schema
- **AND** type inference handles mixed types gracefully

#### Scenario: Infer schema with constraints
- **WHEN** `schema.infer()` is called with `detect_constraints=True`
- **THEN** the function detects constraints such as:
  - Minimum/maximum values (for numeric fields)
  - String length constraints
  - Enum-like value sets
- **AND** constraints are included in the schema object

### Requirement: JSON Schema Output
The system SHALL provide a function to convert inferred schema to JSON Schema format.

#### Scenario: Convert to JSON Schema
- **WHEN** `schema.to_jsonschema()` is called with an inferred schema
- **THEN** the function returns a valid JSON Schema document
- **AND** the schema includes field definitions, types, and constraints
- **AND** the schema is compatible with JSON Schema validators

#### Scenario: JSON Schema with nested structures
- **WHEN** `schema.to_jsonschema()` is called with a schema containing nested objects or arrays
- **THEN** the function generates appropriate JSON Schema structure definitions
- **AND** nested types are correctly represented

### Requirement: YAML Schema Output
The system SHALL provide a function to convert inferred schema to YAML format.

#### Scenario: Convert to YAML
- **WHEN** `schema.to_yaml()` is called with an inferred schema
- **THEN** the function returns a YAML string containing the schema
- **AND** the YAML is valid and human-readable
- **AND** the schema structure matches the inferred schema

### Requirement: Cerberus Schema Output
The system SHALL provide a function to convert inferred schema to Cerberus validation schema format.

#### Scenario: Convert to Cerberus schema
- **WHEN** `schema.to_cerberus()` is called with an inferred schema
- **THEN** the function returns a Cerberus-compatible schema dictionary
- **AND** the schema can be used directly with Cerberus validators
- **AND** field rules and constraints are properly converted

### Requirement: Avro Schema Output
The system SHALL provide a function to convert inferred schema to Avro schema format.

#### Scenario: Convert to Avro schema
- **WHEN** `schema.to_avro()` is called with an inferred schema
- **THEN** the function returns a valid Avro schema JSON
- **AND** the schema includes namespace and record definitions
- **AND** Avro types are correctly mapped from inferred types

#### Scenario: Avro schema with complex types
- **WHEN** `schema.to_avro()` is called with a schema containing arrays or unions
- **THEN** the function generates appropriate Avro type definitions
- **AND** complex types are correctly represented

### Requirement: Parquet Schema Output
The system SHALL provide a function to convert inferred schema to Parquet metadata format.

#### Scenario: Convert to Parquet metadata
- **WHEN** `schema.to_parquet_metadata()` is called with an inferred schema
- **THEN** the function returns Parquet-compatible schema metadata
- **AND** the metadata can be used when writing Parquet files
- **AND** Parquet types are correctly mapped from inferred types

#### Scenario: Parquet schema with nested types
- **WHEN** `schema.to_parquet_metadata()` is called with nested structures
- **THEN** the function generates appropriate Parquet nested type definitions
- **AND** nested schemas are correctly represented

### Requirement: Schema Validation
The system SHALL provide a function to validate data against an inferred or provided schema.

#### Scenario: Validate data against schema
- **WHEN** `schema.validate()` is called with an iterable and a schema
- **THEN** the function returns validation results indicating:
  - Valid rows
  - Invalid rows with error details
  - Overall validation statistics
- **AND** validation is performed efficiently

#### Scenario: Schema validation with strict mode
- **WHEN** `schema.validate()` is called with `strict=True`
- **THEN** the function enforces strict type checking
- **AND** additional fields not in schema are flagged as errors
- **AND** missing required fields are flagged as errors
