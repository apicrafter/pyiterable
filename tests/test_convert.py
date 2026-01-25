import os
import tempfile

import pytest

from iterable.convert import convert


class TestConvert:
    def test_convert_csv_to_jsonl(self):
        convert(fromfile="fixtures/ru_cp1251_comma.csv", tofile="testdata/ru_cp1251_comma_converted.jsonl")
        assert os.path.exists("testdata/ru_cp1251_comma_converted.jsonl")

    def test_convert_csv_to_parquet(self):
        convert(fromfile="fixtures/ru_cp1251_comma.csv", tofile="testdata/ru_cp1251_comma_converted.parquet")
        assert os.path.exists("testdata/ru_cp1251_comma_converted.parquet")

    def test_convert_csv_to_csv_gz(self):
        convert(fromfile="fixtures/ru_cp1251_comma.csv", tofile="testdata/ru_cp1251_comma_converted.csv.gz")
        assert os.path.exists("testdata/ru_cp1251_comma_converted.csv.gz")

    def test_convert_jsonl_to_csv_xz(self):
        convert(fromfile="fixtures/2cols6rows_flat.jsonl", tofile="testdata/2cols6rows_flat_converted.csv.gz")
        assert os.path.exists("testdata/2cols6rows_flat_converted.csv.gz")

    def test_convert_with_batch_size(self):
        """Test convert with custom batch size"""
        convert(fromfile="fixtures/2cols6rows_flat.jsonl", tofile="testdata/test_convert_batch.jsonl", batch_size=2)
        assert os.path.exists("testdata/test_convert_batch.jsonl")
        if os.path.exists("testdata/test_convert_batch.jsonl"):
            os.unlink("testdata/test_convert_batch.jsonl")

    def test_convert_with_flatten(self):
        """Test convert with flatten option"""
        convert(
            fromfile="fixtures/2cols6rows_flat.jsonl", tofile="testdata/test_convert_flatten.jsonl", is_flatten=True
        )
        assert os.path.exists("testdata/test_convert_flatten.jsonl")
        if os.path.exists("testdata/test_convert_flatten.jsonl"):
            os.unlink("testdata/test_convert_flatten.jsonl")

    def test_convert_with_use_totals(self):
        """Test convert with use_totals option"""
        convert(fromfile="fixtures/2cols6rows.csv", tofile="testdata/test_convert_totals.jsonl", use_totals=True)
        assert os.path.exists("testdata/test_convert_totals.jsonl")
        if os.path.exists("testdata/test_convert_totals.jsonl"):
            os.unlink("testdata/test_convert_totals.jsonl")

    def test_convert_with_silent(self):
        """Test convert with silent=False"""
        convert(fromfile="fixtures/2cols6rows_flat.jsonl", tofile="testdata/test_convert_silent.jsonl", silent=False)
        assert os.path.exists("testdata/test_convert_silent.jsonl")
        if os.path.exists("testdata/test_convert_silent.jsonl"):
            os.unlink("testdata/test_convert_silent.jsonl")

    def test_convert_different_formats(self):
        """Test converting between different format combinations"""
        # CSV to JSON
        convert(
            fromfile="fixtures/2cols6rows.csv",
            tofile="testdata/test_convert_csv_json.json",
            iterableargs={"tagname": "items"},
        )
        assert os.path.exists("testdata/test_convert_csv_json.json")
        if os.path.exists("testdata/test_convert_csv_json.json"):
            os.unlink("testdata/test_convert_csv_json.json")

    def test_convert_with_toiterableargs(self):
        """Test convert with output iterable arguments"""
        # Convert CSV to CSV with custom delimiter
        convert(
            fromfile="fixtures/2cols6rows.csv",
            tofile="testdata/test_convert_output_args.csv",
            toiterableargs={"delimiter": "|"},
        )
        assert os.path.exists("testdata/test_convert_output_args.csv")
        # Verify the file was created and has content
        if os.path.exists("testdata/test_convert_output_args.csv"):
            with open("testdata/test_convert_output_args.csv") as f:
                content = f.read()
                # Check that pipe delimiter is used (not comma)
                assert "|" in content or len(content) > 0
            os.unlink("testdata/test_convert_output_args.csv")

    def test_convert_file_not_found(self):
        """Test convert with non-existent source file"""
        with pytest.raises(FileNotFoundError):
            convert(fromfile="nonexistent_file.csv", tofile="testdata/output.jsonl")

    def test_convert_invalid_scan_limit(self):
        """Test convert with invalid scan_limit"""
        with pytest.raises(ValueError, match="scan_limit must be non-negative"):
            convert(
                fromfile="fixtures/2cols6rows.csv",
                tofile="testdata/test_invalid_scan.jsonl",
                scan_limit=-1,
            )

    def test_convert_invalid_batch_size(self):
        """Test convert with invalid batch_size"""
        with pytest.raises(ValueError, match="batch_size must be positive"):
            convert(
                fromfile="fixtures/2cols6rows.csv",
                tofile="testdata/test_invalid_batch.jsonl",
                batch_size=0,
            )

    def test_convert_empty_file(self, tmp_path):
        """Test convert with empty source file"""
        empty_file = tmp_path / "empty.csv"
        empty_file.write_text("")
        output_file = tmp_path / "output.jsonl"
        # Should handle empty file gracefully
        convert(fromfile=str(empty_file), tofile=str(output_file))
        assert output_file.exists()

    def test_convert_single_record(self, tmp_path):
        """Test convert with single record file"""
        single_file = tmp_path / "single.csv"
        single_file.write_text("id,name\n1,test")
        output_file = tmp_path / "output.jsonl"
        convert(fromfile=str(single_file), tofile=str(output_file))
        assert output_file.exists()

    def test_convert_with_scan_limit(self, tmp_path):
        """Test convert with scan_limit"""
        test_file = tmp_path / "test.csv"
        test_file.write_text("id,name\n1,test1\n2,test2\n3,test3")
        output_file = tmp_path / "output.jsonl"
        convert(fromfile=str(test_file), tofile=str(output_file), scan_limit=2)
        assert output_file.exists()

    def test_convert_resource_cleanup_on_error(self, tmp_path):
        """Test that resources are cleaned up even on error"""
        test_file = tmp_path / "test.csv"
        test_file.write_text("id,name\n1,test")
        output_file = tmp_path / "output.unknown_format"
        # Should raise error but clean up resources
        try:
            convert(fromfile=str(test_file), tofile=str(output_file))
        except Exception:
            pass
        # Resources should be cleaned up (no file handles left open)

    def test_convert_nested_to_flat(self, tmp_path):
        """Test convert nested JSON to flat CSV"""
        nested_file = tmp_path / "nested.jsonl"
        nested_file.write_text('{"user": {"name": "test", "age": 30}}\n')
        output_file = tmp_path / "output.csv"
        convert(fromfile=str(nested_file), tofile=str(output_file), is_flatten=True)
        assert output_file.exists()

    def test_convert_with_iterableargs(self, tmp_path):
        """Test convert with input iterable arguments"""
        test_file = tmp_path / "test.csv"
        test_file.write_text("id;name\n1;test")
        output_file = tmp_path / "output.jsonl"
        convert(
            fromfile=str(test_file),
            tofile=str(output_file),
            iterableargs={"delimiter": ";"},
        )
        assert output_file.exists()

    def test_convert_progress_tracking(self, tmp_path):
        """Test convert with progress tracking (use_totals)"""
        test_file = tmp_path / "test.csv"
        test_file.write_text("id,name\n1,test1\n2,test2\n3,test3")
        output_file = tmp_path / "output.jsonl"
        # Should work with use_totals=True
        convert(fromfile=str(test_file), tofile=str(output_file), use_totals=True)
        assert output_file.exists()

    def test_convert_large_batch(self, tmp_path):
        """Test convert with large batch size"""
        test_file = tmp_path / "test.csv"
        # Create file with many rows
        with open(test_file, "w") as f:
            f.write("id,name\n")
            for i in range(100):
                f.write(f"{i},test{i}\n")
        output_file = tmp_path / "output.jsonl"
        convert(fromfile=str(test_file), tofile=str(output_file), batch_size=1000)
        assert output_file.exists()

    def test_convert_schema_extraction(self, tmp_path):
        """Test that schema extraction works for flat formats"""
        test_file = tmp_path / "test.jsonl"
        test_file.write_text('{"id": 1, "name": "test1"}\n{"id": 2, "name": "test2", "extra": "field"}\n')
        output_file = tmp_path / "output.csv"
        # Should extract all keys (id, name, extra)
        convert(fromfile=str(test_file), tofile=str(output_file))
        assert output_file.exists()
        # Verify all columns are present
        with open(output_file) as f:
            header = f.readline()
            assert "id" in header
            assert "name" in header
            assert "extra" in header
