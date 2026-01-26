"""
High-level operations for data processing.

This module provides reusable functions for common data operations:
- Inspection: count, head, tail, headers, sniff, analyze
- Statistics: compute, frequency, uniq
- Transformations: head, tail, sample, dedup, select, slice, and more
- Filtering: expression-based filtering, regex search, query support
- Schema: schema inference and generation
"""

from . import filter, inspect, schema, stats, transform

__all__ = ["filter", "inspect", "schema", "stats", "transform"]
