## ADDED Requirements

### Requirement: Progress Callbacks for Conversions
The `convert()` function SHALL accept an optional `progress` parameter that accepts a callback function. The callback SHALL be invoked periodically during conversion with a statistics dictionary containing progress information.

#### Scenario: Progress callback during conversion
- **WHEN** `convert()` is called with a `progress` callback function
- **THEN** the callback is invoked periodically with a stats dictionary containing:
  - `rows_read`: number of rows read from source
  - `rows_written`: number of rows written to destination
  - `elapsed`: elapsed time in seconds
  - `estimated_total`: estimated total rows (if available, otherwise None)

#### Scenario: Progress callback with custom reporting
- **WHEN** a user provides a progress callback that logs to a monitoring system
- **THEN** the callback receives stats updates at regular intervals
- **AND** the callback can access all progress metrics for custom reporting

### Requirement: Progress Callbacks for Pipelines
The `pipeline()` function SHALL accept an optional `progress` parameter that accepts a callback function. The callback SHALL be invoked periodically during pipeline execution with a statistics dictionary containing progress information.

#### Scenario: Progress callback during pipeline execution
- **WHEN** `pipeline()` is called with a `progress` callback function
- **THEN** the callback is invoked periodically with a stats dictionary containing:
  - `rows_processed`: number of rows processed
  - `elapsed`: elapsed time in seconds
  - `throughput`: rows per second (if calculable)
  - Other existing pipeline stats (rec_count, exceptions, etc.)

### Requirement: Built-in Progress Bars
The `convert()` function SHALL support a `show_progress` parameter that displays a progress bar using `tqdm` when available, with graceful fallback when `tqdm` is not installed.

#### Scenario: Show progress bar during conversion
- **WHEN** `convert()` is called with `show_progress=True`
- **THEN** a progress bar is displayed using `tqdm` (if installed)
- **AND** the progress bar shows rows processed and estimated time remaining
- **AND** if `tqdm` is not available, the function continues without a progress bar (no error)

#### Scenario: Progress bar respects silent parameter
- **WHEN** `convert()` is called with `silent=True`
- **THEN** no progress bar is displayed regardless of `show_progress` value
- **AND** progress callbacks (if provided) are still invoked

### Requirement: Conversion Metrics Object
The `convert()` function SHALL return a `ConversionResult` object containing structured metrics about the conversion operation.

#### Scenario: Access conversion metrics
- **WHEN** `convert()` completes successfully
- **THEN** it returns a `ConversionResult` object with attributes:
  - `rows_in`: total rows read from source
  - `rows_out`: total rows written to destination
  - `elapsed_seconds`: total elapsed time in seconds
  - `bytes_read`: bytes read from source (if available)
  - `bytes_written`: bytes written to destination (if available)
  - `errors`: list of errors encountered (empty if none)

#### Scenario: Programmatic metrics access
- **WHEN** a user calls `result = convert('input.csv', 'output.parquet')`
- **THEN** `result` is a `ConversionResult` instance
- **AND** metrics can be accessed via attributes: `result.rows_in`, `result.rows_out`, `result.elapsed_seconds`
- **AND** metrics can be used in programmatic workflows (CI/CD, monitoring, etc.)

#### Scenario: Backward compatibility for convert return value
- **WHEN** existing code calls `convert()` without handling the return value
- **THEN** the code continues to work without modification
- **AND** the return value is simply ignored

### Requirement: Pipeline Metrics Object
The `pipeline()` function SHALL return a `PipelineResult` object (or enhanced stats dictionary) containing structured metrics about the pipeline execution.

#### Scenario: Access pipeline metrics
- **WHEN** `pipeline()` completes execution
- **THEN** it returns a `PipelineResult` object (or dict-like object) with attributes:
  - `rows_processed`: total rows processed
  - `elapsed_seconds`: total elapsed time in seconds
  - `throughput`: rows per second
  - `exceptions`: number of exceptions encountered
  - Other existing pipeline stats (rec_count, nulls, etc.)

#### Scenario: Backward compatibility for pipeline return value
- **WHEN** existing code accesses pipeline stats as a dictionary
- **THEN** the code continues to work without modification
- **AND** stats can be accessed via dictionary keys or object attributes

### Requirement: Metrics Collection During Execution
Progress callbacks SHALL receive metrics that are collected and updated during execution, allowing real-time progress tracking.

#### Scenario: Real-time metrics in progress callback
- **WHEN** a progress callback is invoked during conversion or pipeline execution
- **THEN** the stats dictionary contains current values (not final values)
- **AND** metrics are updated as processing continues
- **AND** callbacks can track progress in real-time
