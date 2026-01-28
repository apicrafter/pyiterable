# validate Specification

## Purpose
TBD - created by archiving change add-high-level-operations. Update Purpose after archive.
## Requirements
### Requirement: Validation Pipeline
The system SHALL provide a function to validate rows in an iterable dataset against a set of validation rules.

#### Scenario: Validate with rules dictionary
- **WHEN** `validate.iterable()` is called with an iterable and rules dictionary
- **THEN** the function validates each row against the specified rules
- **AND** returns an iterator of (record, errors) tuples
- **AND** errors is a list of validation error messages (empty if valid)

#### Scenario: Validation with stats mode
- **WHEN** `validate.iterable()` is called with `mode="stats"`
- **THEN** the function returns validation statistics:
  - Total rows processed
  - Valid rows count
  - Invalid rows count
  - Error counts by rule type
- **AND** individual row errors are not returned (only statistics)

#### Scenario: Validation with invalid mode
- **WHEN** `validate.iterable()` is called with `mode="invalid"`
- **THEN** the function returns only rows that failed validation
- **AND** each returned row includes its validation errors

#### Scenario: Validation with valid mode
- **WHEN** `validate.iterable()` is called with `mode="valid"`
- **THEN** the function returns only rows that passed all validation rules
- **AND** invalid rows are filtered out

### Requirement: Built-in Validation Rules
The system SHALL provide a set of built-in validation rules for common validation needs.

#### Scenario: Email validation rule
- **WHEN** `validate.iterable()` is called with rule `{"email": ["common.email"]}`
- **THEN** the email field is validated using the built-in email validation rule
- **AND** valid email addresses pass validation
- **AND** invalid email addresses fail with appropriate error messages

#### Scenario: URL validation rule
- **WHEN** `validate.iterable()` is called with rule `{"url": ["common.url"]}`
- **THEN** the url field is validated using the built-in URL validation rule
- **AND** valid URLs pass validation
- **AND** invalid URLs fail with appropriate error messages

#### Scenario: Russian INN validation rule
- **WHEN** `validate.iterable()` is called with rule `{"inn": ["ru.org.inn"]}`
- **THEN** the inn field is validated as a Russian INN (tax identification number)
- **AND** valid INN formats pass validation
- **AND** invalid INN formats fail with appropriate error messages

#### Scenario: Russian OGRN validation rule
- **WHEN** `validate.iterable()` is called with rule `{"ogrn": ["ru.org.ogrn"]}`
- **THEN** the ogrn field is validated as a Russian OGRN (state registration number)
- **AND** valid OGRN formats pass validation
- **AND** invalid OGRN formats fail with appropriate error messages

#### Scenario: Multiple rules per field
- **WHEN** `validate.iterable()` is called with rule `{"email": ["common.email", "required"]}`
- **THEN** the email field is validated against all specified rules
- **AND** the row fails if any rule fails
- **AND** error messages indicate which rules failed

### Requirement: Custom Validator Registration
The system SHALL provide a mechanism to register custom validation functions.

#### Scenario: Register custom validator
- **WHEN** a custom validator function is registered using `validate.register()`
- **THEN** the validator can be referenced by name in validation rules
- **AND** the validator function receives the field value and returns True/False or raises ValidationError
- **AND** custom validators work alongside built-in rules

#### Scenario: Custom validator with parameters
- **WHEN** a custom validator is registered with parameters
- **THEN** the validator can accept configuration parameters
- **AND** parameters are passed when the validator is invoked
- **AND** validator configuration is flexible

### Requirement: Validation Error Reporting
The system SHALL provide detailed error reporting for validation failures.

#### Scenario: Error messages with context
- **WHEN** validation fails for a field
- **THEN** error messages include:
  - Field name
  - Rule name that failed
  - Field value (if safe to include)
  - Reason for failure
- **AND** error messages are human-readable

#### Scenario: Multiple errors per row
- **WHEN** a row fails multiple validation rules
- **THEN** all errors are reported
- **AND** errors are organized by field
- **AND** error collection continues even after first failure

### Requirement: Validation Performance
The system SHALL validate data efficiently, supporting large datasets.

#### Scenario: Streaming validation
- **WHEN** `validate.iterable()` is called on a large dataset
- **THEN** validation is performed in a streaming fashion
- **AND** memory usage remains constant regardless of dataset size
- **AND** validation can be interrupted and resumed

#### Scenario: Validation with early termination
- **WHEN** `validate.iterable()` is called with `max_errors=100`
- **THEN** validation stops after 100 errors are encountered
- **AND** partial results are returned
- **AND** performance is improved for datasets with many errors

