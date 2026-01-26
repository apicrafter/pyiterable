"""
Database ingestion framework.

Provides functions for ingesting data from iterables into various database systems.
"""

from .core import to_db

__all__ = ["to_db"]
