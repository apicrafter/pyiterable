"""Tests for observability features: progress callbacks, metrics, and logging."""

import os
import time

import pytest

from iterable.convert.core import convert
from iterable.datatypes import CSVIterable, JSONLinesIterable
from iterable.pipeline import Pipeline, pipeline
from iterable.types import ConversionResult, PipelineResult


class TestConversionResult:
    """Test ConversionResult class."""

    def test_conversion_result_creation(self):
        """Test creating a ConversionResult object."""
        result = ConversionResult(
            rows_in=100, rows_out=100, elapsed_seconds=1.5, bytes_read=1024, bytes_written=2048, errors=[]
        )

        assert result.rows_in == 100
        assert result.rows_out == 100
        assert result.elapsed_seconds == 1.5
        assert result.bytes_read == 1024
        assert result.bytes_written == 2048
        assert result.errors == []

    def test_conversion_result_with_errors(self):
        """Test ConversionResult with errors."""
        error = ValueError("Test error")
        result = ConversionResult(rows_in=50, rows_out=45, elapsed_seconds=0.5, errors=[error])

        assert len(result.errors) == 1
        assert result.errors[0] == error


class TestPipelineResult:
    """Test PipelineResult class."""

    def test_pipeline_result_creation(self):
        """Test creating a PipelineResult object."""
        result = PipelineResult(
            rows_processed=100, elapsed_seconds=1.5, exceptions=2, nulls=5, time_start=0.0, time_end=1.5
        )

        assert result.rows_processed == 100
        assert result.elapsed_seconds == 1.5
        assert result.exceptions == 2
        assert result.nulls == 5
        assert result.rec_count == 100  # Should default to rows_processed

    def test_pipeline_result_throughput(self):
        """Test throughput calculation."""
        result = PipelineResult(rows_processed=100, elapsed_seconds=2.0, exceptions=0)

        assert result.throughput == 50.0  # 100 rows / 2 seconds

    def test_pipeline_result_throughput_zero_time(self):
        """Test throughput with zero elapsed time."""
        result = PipelineResult(rows_processed=100, elapsed_seconds=0.0, exceptions=0)

        assert result.throughput is None

    def test_pipeline_result_dict_access(self):
        """Test dictionary-style access for backward compatibility."""
        result = PipelineResult(
            rows_processed=100, elapsed_seconds=1.5, exceptions=2, nulls=5, time_start=0.0, time_end=1.5
        )

        # Test dictionary-style access
        assert result["rec_count"] == 100
        assert result["rows_processed"] == 100
        assert result["exceptions"] == 2
        assert result["nulls"] == 5
        assert result["duration"] == 1.5
        assert result["elapsed_seconds"] == 1.5

    def test_pipeline_result_contains(self):
        """Test 'in' operator support."""
        result = PipelineResult(rows_processed=100, elapsed_seconds=1.5, exceptions=0)

        assert "rec_count" in result
        assert "rows_processed" in result
        assert "exceptions" in result
        assert "invalid_key" not in result

    def test_pipeline_result_get(self):
        """Test dict.get() method support."""
        result = PipelineResult(rows_processed=100, elapsed_seconds=1.5, exceptions=0)

        assert result.get("rec_count") == 100
        assert result.get("invalid_key") is None
        assert result.get("invalid_key", "default") == "default"

    def test_pipeline_result_to_dict(self):
        """Test conversion to dictionary."""
        result = PipelineResult(
            rows_processed=100, elapsed_seconds=1.5, exceptions=2, nulls=5, time_start=0.0, time_end=1.5
        )

        d = result.to_dict()
        assert isinstance(d, dict)
        assert d["rec_count"] == 100
        assert d["rows_processed"] == 100
        assert d["throughput"] == pytest.approx(100 / 1.5)


class TestConvertProgress:
    """Test progress callbacks and metrics in convert()."""

    def test_convert_returns_conversion_result(self):
        """Test that convert() returns ConversionResult."""
        os.makedirs("testdata", exist_ok=True)
        input_file = "fixtures/2cols6rows.csv"
        output_file = "testdata/test_convert_result.jsonl"

        result = convert(input_file, output_file)

        assert isinstance(result, ConversionResult)
        assert result.rows_in > 0
        assert result.rows_out > 0
        assert result.elapsed_seconds >= 0

        if os.path.exists(output_file):
            os.unlink(output_file)

    def test_convert_progress_callback(self):
        """Test progress callback during conversion."""
        os.makedirs("testdata", exist_ok=True)
        input_file = "fixtures/2cols6rows.csv"
        output_file = "testdata/test_convert_progress.jsonl"

        progress_calls = []

        def progress_callback(stats):
            progress_calls.append(stats.copy())

        result = convert(input_file, output_file, progress=progress_callback)

        # Progress callback should have been called at least once
        assert len(progress_calls) > 0

        # Check that callback received expected stats
        for call in progress_calls:
            assert "rows_read" in call
            assert "rows_written" in call
            assert "elapsed" in call
            assert call["rows_read"] >= 0
            assert call["rows_written"] >= 0

        # Final result should match last progress update
        assert result.rows_in == progress_calls[-1]["rows_read"]
        assert result.rows_out == progress_calls[-1]["rows_written"]

        if os.path.exists(output_file):
            os.unlink(output_file)

    def test_convert_progress_callback_estimated_total(self):
        """Test progress callback with estimated_total when use_totals=True."""
        os.makedirs("testdata", exist_ok=True)
        input_file = "fixtures/2cols6rows.csv"
        output_file = "testdata/test_convert_progress_totals.jsonl"

        progress_calls = []

        def progress_callback(stats):
            progress_calls.append(stats.copy())

        # Use a format that supports totals (like Parquet if available)
        # For now, test with CSV which may not support totals
        result = convert(input_file, output_file, progress=progress_callback, use_totals=True)

        assert len(progress_calls) > 0
        # estimated_total may be None if format doesn't support it
        for call in progress_calls:
            assert "estimated_total" in call

        if os.path.exists(output_file):
            os.unlink(output_file)

    def test_convert_show_progress(self):
        """Test show_progress parameter."""
        os.makedirs("testdata", exist_ok=True)
        input_file = "fixtures/2cols6rows.csv"
        output_file = "testdata/test_convert_show_progress.jsonl"

        # show_progress should not raise an error
        result = convert(input_file, output_file, show_progress=True, silent=False)

        assert isinstance(result, ConversionResult)
        assert result.rows_in > 0

        if os.path.exists(output_file):
            os.unlink(output_file)

    def test_convert_show_progress_respects_silent(self):
        """Test that show_progress is ignored when silent=True."""
        os.makedirs("testdata", exist_ok=True)
        input_file = "fixtures/2cols6rows.csv"
        output_file = "testdata/test_convert_silent.jsonl"

        # Even with show_progress=True, if silent=True, no progress bar should show
        result = convert(input_file, output_file, show_progress=True, silent=True)

        assert isinstance(result, ConversionResult)

        if os.path.exists(output_file):
            os.unlink(output_file)

    def test_convert_backward_compatibility(self):
        """Test that existing code without return value handling still works."""
        os.makedirs("testdata", exist_ok=True)
        input_file = "fixtures/2cols6rows.csv"
        output_file = "testdata/test_convert_backward.jsonl"

        # Old code that doesn't handle return value should still work
        convert(input_file, output_file)

        # File should have been created
        assert os.path.exists(output_file)

        if os.path.exists(output_file):
            os.unlink(output_file)


class TestPipelineProgress:
    """Test progress callbacks and metrics in pipeline()."""

    def test_pipeline_returns_pipeline_result(self):
        """Test that pipeline() returns PipelineResult."""
        source = CSVIterable("fixtures/2cols6rows.csv")
        output_file = "testdata/test_pipeline_result.jsonl"
        os.makedirs("testdata", exist_ok=True)
        destination = JSONLinesIterable(output_file, mode="w")

        def process_func(record, state):
            return record

        result = pipeline(source=source, destination=destination, process_func=process_func)

        assert isinstance(result, PipelineResult)
        assert result.rows_processed > 0
        assert result.elapsed_seconds >= 0

        source.close()
        destination.close()
        if os.path.exists(output_file):
            os.unlink(output_file)

    def test_pipeline_progress_callback(self):
        """Test progress callback during pipeline execution."""
        source = CSVIterable("fixtures/2cols6rows.csv")
        output_file = "testdata/test_pipeline_progress.jsonl"
        os.makedirs("testdata", exist_ok=True)
        destination = JSONLinesIterable(output_file, mode="w")

        progress_calls = []

        def process_func(record, state):
            return record

        def progress_callback(stats):
            progress_calls.append(stats.copy())

        result = pipeline(
            source=source, destination=destination, process_func=process_func, progress=progress_callback
        )

        # Progress callback should have been called at least once
        assert len(progress_calls) > 0

        # Check that callback received expected stats
        for call in progress_calls:
            assert "rows_processed" in call
            assert "elapsed" in call
            assert call["rows_processed"] >= 0

        # Final result should match last progress update
        assert result.rows_processed == progress_calls[-1]["rows_processed"]

        source.close()
        destination.close()
        if os.path.exists(output_file):
            os.unlink(output_file)

    def test_pipeline_progress_callback_throughput(self):
        """Test that progress callback includes throughput."""
        source = CSVIterable("fixtures/2cols6rows.csv")
        output_file = "testdata/test_pipeline_throughput.jsonl"
        os.makedirs("testdata", exist_ok=True)
        destination = JSONLinesIterable(output_file, mode="w")

        progress_calls = []

        def process_func(record, state):
            return record

        def progress_callback(stats):
            progress_calls.append(stats.copy())

        result = pipeline(
            source=source, destination=destination, process_func=process_func, progress=progress_callback
        )

        # Check that later calls include throughput
        for call in progress_calls:
            if call["elapsed"] > 0:
                assert "throughput" in call
                assert call["throughput"] is not None or call["elapsed"] == 0

        source.close()
        destination.close()
        if os.path.exists(output_file):
            os.unlink(output_file)

    def test_pipeline_backward_compatibility_dict_access(self):
        """Test that existing code using dict access still works."""
        source = CSVIterable("fixtures/2cols6rows.csv")
        output_file = "testdata/test_pipeline_dict.jsonl"
        os.makedirs("testdata", exist_ok=True)
        destination = JSONLinesIterable(output_file, mode="w")

        def process_func(record, state):
            return record

        stats = pipeline(source=source, destination=destination, process_func=process_func)

        # Old code using dict access should still work
        assert stats["rec_count"] > 0
        assert stats["exceptions"] >= 0
        assert "duration" in stats
        assert "time_start" in stats
        assert "time_end" in stats

        source.close()
        destination.close()
        if os.path.exists(output_file):
            os.unlink(output_file)

    def test_pipeline_result_throughput_property(self):
        """Test PipelineResult throughput property."""
        source = CSVIterable("fixtures/2cols6rows.csv")
        output_file = "testdata/test_pipeline_throughput_prop.jsonl"
        os.makedirs("testdata", exist_ok=True)
        destination = JSONLinesIterable(output_file, mode="w")

        def process_func(record, state):
            return record

        result = pipeline(source=source, destination=destination, process_func=process_func)

        # Test throughput property
        if result.elapsed_seconds > 0:
            assert result.throughput is not None
            assert result.throughput > 0
            # Throughput should be approximately rows_processed / elapsed_seconds
            assert result.throughput == pytest.approx(result.rows_processed / result.elapsed_seconds, rel=0.1)

        source.close()
        destination.close()
        if os.path.exists(output_file):
            os.unlink(output_file)


class TestProgressCallbackErrors:
    """Test error handling in progress callbacks."""

    def test_convert_progress_callback_error_doesnt_stop_conversion(self):
        """Test that errors in progress callback don't stop conversion."""
        os.makedirs("testdata", exist_ok=True)
        input_file = "fixtures/2cols6rows.csv"
        output_file = "testdata/test_convert_progress_error.jsonl"

        def progress_callback(stats):
            if stats["rows_read"] > 0:
                raise ValueError("Test error in callback")

        # Conversion should complete despite callback error
        result = convert(input_file, output_file, progress=progress_callback)

        assert isinstance(result, ConversionResult)
        assert result.rows_in > 0

        if os.path.exists(output_file):
            os.unlink(output_file)

    def test_pipeline_progress_callback_error_doesnt_stop_pipeline(self):
        """Test that errors in progress callback don't stop pipeline."""
        source = CSVIterable("fixtures/2cols6rows.csv")
        output_file = "testdata/test_pipeline_progress_error.jsonl"
        os.makedirs("testdata", exist_ok=True)
        destination = JSONLinesIterable(output_file, mode="w")

        def process_func(record, state):
            return record

        def progress_callback(stats):
            if stats["rows_processed"] > 0:
                raise ValueError("Test error in callback")

        # Pipeline should complete despite callback error
        result = pipeline(source=source, destination=destination, process_func=process_func, progress=progress_callback)

        assert isinstance(result, PipelineResult)
        assert result.rows_processed > 0

        source.close()
        destination.close()
        if os.path.exists(output_file):
            os.unlink(output_file)
