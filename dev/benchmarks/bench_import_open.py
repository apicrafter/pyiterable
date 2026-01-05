"""
Ad-hoc micro-benchmarks (not part of pytest runs).

Usage:
  python dev/benchmarks/bench_import_open.py
"""

from __future__ import annotations

import time
from pathlib import Path


def _timeit(fn, n: int = 5) -> float:
    best = float("inf")
    for _ in range(n):
        t0 = time.perf_counter()
        fn()
        best = min(best, time.perf_counter() - t0)
    return best


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    fixtures = root / "tests" / "fixtures"
    sample_csv = fixtures / "2cols6rows.csv"

    def do_import():
        import importlib

        importlib.invalidate_caches()
        import iterable  # noqa: F401

    def do_open_read():
        from iterable.helpers.detect import open_iterable

        with open_iterable(str(sample_csv)) as it:
            for _ in it:
                pass

    print("Best-of timing (seconds):")
    print(f"- import iterable:  {_timeit(do_import):.6f}")
    print(f"- open+iterate csv: {_timeit(do_open_read):.6f}")


if __name__ == "__main__":
    main()


