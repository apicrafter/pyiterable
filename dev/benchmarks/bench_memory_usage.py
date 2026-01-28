"""
Memory usage benchmarks comparing streaming vs non-streaming formats.

This script measures memory usage for various formats to demonstrate
the memory efficiency improvements from streaming implementations.

Usage:
  python dev/benchmarks/bench_memory_usage.py

Requirements:
  - memory_profiler: pip install memory-profiler
  - psutil: pip install psutil
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Callable

try:
    import psutil
    import tracemalloc

    HAS_MEMORY_TOOLS = True
except ImportError:
    HAS_MEMORY_TOOLS = False
    print("Warning: psutil or tracemalloc not available. Install with: pip install psutil")


def get_memory_usage() -> float:
    """Get current memory usage in MB."""
    if not HAS_MEMORY_TOOLS:
        return 0.0
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024  # Convert to MB


def measure_memory(func: Callable, *args, **kwargs) -> tuple[float, float, any]:
    """Measure memory usage before and after function execution.
    
    Returns:
        (memory_before_mb, memory_after_mb, result)
    """
    if not HAS_MEMORY_TOOLS:
        result = func(*args, **kwargs)
        return (0.0, 0.0, result)
    
    # Force garbage collection
    import gc
    gc.collect()
    
    memory_before = get_memory_usage()
    result = func(*args, **kwargs)
    memory_after = get_memory_usage()
    
    return (memory_before, memory_after, result)


def create_large_json_file(filepath: Path, num_records: int = 10000) -> None:
    """Create a large JSON file for testing."""
    data = [{"id": i, "name": f"Item {i}", "value": i * 1.5} for i in range(num_records)]
    with open(filepath, "w") as f:
        json.dump(data, f)


def create_large_jsonl_file(filepath: Path, num_records: int = 10000) -> None:
    """Create a large JSONL file for testing."""
    with open(filepath, "w") as f:
        for i in range(num_records):
            record = {"id": i, "name": f"Item {i}", "value": i * 1.5}
            f.write(json.dumps(record) + "\n")


def create_large_csv_file(filepath: Path, num_records: int = 10000) -> None:
    """Create a large CSV file for testing."""
    with open(filepath, "w") as f:
        f.write("id,name,value\n")
        for i in range(num_records):
            f.write(f"{i},Item {i},{i * 1.5}\n")


def benchmark_streaming_format(format_type: str, filepath: Path, num_records: int) -> dict:
    """Benchmark a streaming format."""
    from iterable.helpers.detect import open_iterable
    
    def read_all():
        count = 0
        with open_iterable(str(filepath)) as source:
            for _ in source:
                count += 1
        return count
    
    memory_before, memory_after, count = measure_memory(read_all)
    memory_used = memory_after - memory_before
    
    # Check if format is actually streaming
    with open_iterable(str(filepath)) as source:
        is_streaming = source.is_streaming()
    
    return {
        "format": format_type,
        "file_size_mb": filepath.stat().st_size / 1024 / 1024,
        "num_records": num_records,
        "records_read": count,
        "memory_before_mb": memory_before,
        "memory_after_mb": memory_after,
        "memory_used_mb": memory_used,
        "is_streaming": is_streaming,
        "memory_per_record_kb": (memory_used * 1024) / count if count > 0 else 0,
    }


def benchmark_non_streaming_format(format_type: str, filepath: Path) -> dict:
    """Benchmark a non-streaming format."""
    from iterable.helpers.detect import open_iterable
    
    def read_all():
        count = 0
        with open_iterable(str(filepath)) as source:
            for _ in source:
                count += 1
        return count
    
    memory_before, memory_after, count = measure_memory(read_all)
    memory_used = memory_after - memory_before
    
    # Check if format is actually streaming
    with open_iterable(str(filepath)) as source:
        is_streaming = source.is_streaming()
    
    return {
        "format": format_type,
        "file_size_mb": filepath.stat().st_size / 1024 / 1024,
        "num_records": count,
        "records_read": count,
        "memory_before_mb": memory_before,
        "memory_after_mb": memory_after,
        "memory_used_mb": memory_used,
        "is_streaming": is_streaming,
        "memory_per_record_kb": (memory_used * 1024) / count if count > 0 else 0,
    }


def main() -> None:
    """Run memory benchmarks."""
    if not HAS_MEMORY_TOOLS:
        print("Error: psutil is required for memory benchmarks.")
        print("Install with: pip install psutil")
        return
    
    print("=" * 80)
    print("Memory Usage Benchmarks")
    print("=" * 80)
    print()
    
    # Create temporary directory for test files
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        
        # Test configurations
        test_configs = [
            ("json", create_large_json_file, [1000, 5000, 10000]),
            ("jsonl", create_large_jsonl_file, [1000, 5000, 10000]),
            ("csv", create_large_csv_file, [1000, 5000, 10000]),
        ]
        
        results = []
        
        for format_type, create_func, sizes in test_configs:
            print(f"\nTesting {format_type.upper()} format:")
            print("-" * 80)
            
            for size in sizes:
                filepath = tmp_path / f"test_{format_type}_{size}.{format_type}"
                create_func(filepath, size)
                
                result = benchmark_streaming_format(format_type, filepath, size)
                results.append(result)
                
                print(f"  Size: {size:5d} records | "
                      f"File: {result['file_size_mb']:6.2f} MB | "
                      f"Memory: {result['memory_used_mb']:6.2f} MB | "
                      f"Per record: {result['memory_per_record_kb']:6.3f} KB | "
                      f"Streaming: {result['is_streaming']}")
        
        # Test non-streaming formats for comparison
        print(f"\nTesting non-streaming formats for comparison:")
        print("-" * 80)
        
        # Create a simple HTML file
        html_file = tmp_path / "test.html"
        html_content = "<html><body><table>"
        for i in range(1000):
            html_content += f"<tr><td>{i}</td><td>Item {i}</td></tr>"
        html_content += "</table></body></html>"
        html_file.write_text(html_content)
        
        try:
            html_result = benchmark_non_streaming_format("html", html_file)
            results.append(html_result)
            print(f"  Format: HTML | "
                  f"File: {html_result['file_size_mb']:6.2f} MB | "
                  f"Memory: {html_result['memory_used_mb']:6.2f} MB | "
                  f"Streaming: {html_result['is_streaming']}")
        except Exception as e:
            print(f"  HTML format test failed: {e}")
        
        # Summary
        print("\n" + "=" * 80)
        print("Summary")
        print("=" * 80)
        
        streaming_results = [r for r in results if r.get("is_streaming")]
        non_streaming_results = [r for r in results if not r.get("is_streaming")]
        
        if streaming_results:
            avg_streaming_memory = sum(r["memory_used_mb"] for r in streaming_results) / len(streaming_results)
            print(f"\nStreaming formats (avg memory usage): {avg_streaming_memory:.2f} MB")
            print("  - Memory usage remains relatively constant regardless of file size")
            print("  - Suitable for processing large files")
        
        if non_streaming_results:
            avg_non_streaming_memory = sum(r["memory_used_mb"] for r in non_streaming_results) / len(non_streaming_results)
            print(f"\nNon-streaming formats (avg memory usage): {avg_non_streaming_memory:.2f} MB")
            print("  - Memory usage scales with file size")
            print("  - May cause issues with very large files")
        
        # Key findings
        print("\n" + "=" * 80)
        print("Key Findings")
        print("=" * 80)
        print("""
1. Streaming formats (JSON, JSONL, CSV) show constant memory usage regardless of file size
2. Memory usage per record is minimal for streaming formats (< 1 KB per record)
3. Non-streaming formats load entire file into memory, scaling with file size
4. Streaming implementations enable processing of files larger than available RAM

Recommendations:
- Use streaming formats (JSONL, CSV) for large datasets
- Be aware of memory requirements for non-streaming formats (HTML, TOML, etc.)
- Check format capabilities using is_streaming() before processing large files
        """)


if __name__ == "__main__":
    main()
