"""Format capability reporting module.

This module provides functions to query format capabilities programmatically,
allowing users to discover what operations and features are supported by each data format.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .detect import DATATYPE_REGISTRY, _load_symbol

if TYPE_CHECKING:
    from ..base import BaseIterable

# Capability cache: format_id -> capabilities dict
_CAPABILITY_CACHE: dict[str, dict[str, bool | None]] = {}


def _detect_capabilities(format_class: type[BaseIterable]) -> dict[str, bool | None]:
    """Detect capabilities for a format class by introspection.

    Args:
        format_class: The format class to introspect

    Returns:
        Dictionary with capability flags (True/False/None)
    """
    caps: dict[str, bool | None] = {
        "readable": None,
        "writable": None,
        "bulk_read": None,
        "bulk_write": None,
        "totals": None,
        "streaming": None,
        "flat_only": None,
        "tables": None,
        "compression": None,
        "nested": None,
    }

    # Check for read/write methods
    caps["readable"] = hasattr(format_class, "read") and callable(getattr(format_class, "read", None))
    caps["writable"] = hasattr(format_class, "write") and callable(getattr(format_class, "write", None))
    caps["bulk_read"] = hasattr(format_class, "read_bulk") and callable(getattr(format_class, "read_bulk", None))
    caps["bulk_write"] = hasattr(format_class, "write_bulk") and callable(getattr(format_class, "write_bulk", None))

    # Check static methods for format characteristics
    try:
        if hasattr(format_class, "has_totals") and callable(getattr(format_class, "has_totals", None)):
            caps["totals"] = format_class.has_totals()
        else:
            caps["totals"] = False
    except (ImportError, AttributeError, TypeError):
        caps["totals"] = None

    try:
        if hasattr(format_class, "has_tables") and callable(getattr(format_class, "has_tables", None)):
            caps["tables"] = format_class.has_tables()
        else:
            caps["tables"] = False
    except (ImportError, AttributeError, TypeError):
        caps["tables"] = None

    try:
        if hasattr(format_class, "is_flatonly") and callable(getattr(format_class, "is_flatonly", None)):
            caps["flat_only"] = format_class.is_flatonly()
            caps["nested"] = not caps["flat_only"]
        else:
            # Default: assume nested data is supported unless proven otherwise
            caps["flat_only"] = False
            caps["nested"] = True
    except (ImportError, AttributeError, TypeError):
        caps["flat_only"] = None
        caps["nested"] = None

    # Check for streaming support
    try:
        # is_streaming() is an instance method, so we can't call it directly on the class
        # Most formats in IterableData are designed for streaming (row-by-row processing)
        # Formats that don't stream (like JSON loading entire file) are exceptions
        # For simplicity, we infer: if format is readable, it likely streams
        # This is a reasonable default as the library emphasizes streaming processing
        caps["streaming"] = caps["readable"]
    except (ImportError, AttributeError, TypeError):
        caps["streaming"] = None

    # Compression support: most text formats support compression
    # Binary formats may or may not. We'll be conservative and set to None
    # unless we can determine otherwise. In practice, most formats work with codecs.
    try:
        # Check if format is in TEXT_DATA_TYPES from detect.py (indirect check)
        # For now, assume compression is supported if format is readable
        # This is a reasonable default as most formats work with codecs
        caps["compression"] = caps["readable"]
    except (ImportError, AttributeError, TypeError):
        caps["compression"] = None

    return caps


def _get_format_class(format_id: str) -> type[BaseIterable]:
    """Get format class for a format ID.

    Args:
        format_id: Format identifier (file extension or format name)

    Returns:
        Format class

    Raises:
        ValueError: If format_id is not in registry
        ImportError: If format class cannot be loaded (optional dependency missing)
    """
    format_id_lower = format_id.lower()
    if format_id_lower not in DATATYPE_REGISTRY:
        raise ValueError(f"Unknown format: '{format_id}'. Available formats: {sorted(set(DATATYPE_REGISTRY.keys()))}")

    module_path, symbol = DATATYPE_REGISTRY[format_id_lower]
    try:
        return _load_symbol(module_path, symbol)
    except ImportError as e:
        # Re-raise with more context
        raise ImportError(
            f"Failed to load format class for '{format_id}'. "
            f"This format likely requires an optional dependency. "
            f"Original error: {e}"
        ) from e


def get_format_capabilities(format_id: str) -> dict[str, bool | None]:
    """Get all capabilities for a specific format.

    Args:
        format_id: Format identifier (file extension or format name, e.g., "csv", "json", "parquet")

    Returns:
        Dictionary with capability flags:
        - readable: Format supports reading data
        - writable: Format supports writing data
        - bulk_read: Format supports bulk reading
        - bulk_write: Format supports bulk writing
        - totals: Format supports row count totals
        - streaming: Format supports streaming (doesn't load entire file)
        - flat_only: Format only supports flat (non-nested) data
        - tables: Format supports multiple tables/sheets/datasets
        - compression: Format supports compression codecs
        - nested: Format can preserve nested data structures

        Values are True/False/None (None indicates unknown/unsupported)

    Raises:
        ValueError: If format_id is not recognized
        ImportError: If format class cannot be loaded (optional dependency missing)

    Example:
        >>> caps = get_format_capabilities("csv")
        >>> print(caps["readable"])
        True
        >>> print(caps["writable"])
        True
    """
    format_id_lower = format_id.lower()

    # Check cache first
    if format_id_lower in _CAPABILITY_CACHE:
        return _CAPABILITY_CACHE[format_id_lower].copy()

    # Get format class and detect capabilities
    try:
        format_class = _get_format_class(format_id_lower)
        capabilities = _detect_capabilities(format_class)

        # Cache the result
        _CAPABILITY_CACHE[format_id_lower] = capabilities.copy()

        return capabilities
    except ImportError:
        # If import fails, return dict with None values
        # This allows graceful handling of missing optional dependencies
        capabilities = {
            "readable": None,
            "writable": None,
            "bulk_read": None,
            "bulk_write": None,
            "totals": None,
            "streaming": None,
            "flat_only": None,
            "tables": None,
            "compression": None,
            "nested": None,
        }
        _CAPABILITY_CACHE[format_id_lower] = capabilities.copy()
        return capabilities


def list_all_capabilities() -> dict[str, dict[str, bool | None]]:
    """List capabilities for all registered formats.

    Returns:
        Dictionary mapping format IDs to their capability dictionaries.
        Each capability dictionary has the same structure as returned by
        `get_format_capabilities()`.

    Example:
        >>> all_caps = list_all_capabilities()
        >>> print(all_caps["csv"]["readable"])
        True
        >>> print(all_caps["json"]["nested"])
        True
    """
    # Get unique format classes (multiple extensions may map to same class)
    format_classes_seen: set[tuple[str, str]] = set()
    result: dict[str, dict[str, bool | None]] = {}

    for format_id in sorted(DATATYPE_REGISTRY.keys()):
        module_path, symbol = DATATYPE_REGISTRY[format_id]
        class_key = (module_path, symbol)

        # Only process each unique class once, but include all format IDs
        if class_key not in format_classes_seen:
            format_classes_seen.add(class_key)
            try:
                result[format_id] = get_format_capabilities(format_id)
            except (ValueError, ImportError):
                # Skip formats that can't be loaded
                # Return empty capabilities dict
                result[format_id] = {
                    "readable": None,
                    "writable": None,
                    "bulk_read": None,
                    "bulk_write": None,
                    "totals": None,
                    "streaming": None,
                    "flat_only": None,
                    "tables": None,
                    "compression": None,
                    "nested": None,
                }
        else:
            # Reuse capabilities from the first format ID that uses this class
            # Find the first format_id that uses this class
            for first_id in sorted(DATATYPE_REGISTRY.keys()):
                first_module, first_symbol = DATATYPE_REGISTRY[first_id]
                if (first_module, first_symbol) == class_key:
                    result[format_id] = result[first_id].copy()
                    break

    return result


def get_capability(format_id: str, capability: str) -> bool | None:
    """Get a specific capability for a format.

    Args:
        format_id: Format identifier (file extension or format name)
        capability: Capability name (one of: readable, writable, bulk_read, bulk_write,
                   totals, streaming, flat_only, tables, compression, nested)

    Returns:
        Capability value (True/False/None), or None if capability name is invalid

    Raises:
        ValueError: If format_id is not recognized

    Example:
        >>> is_writable = get_capability("csv", "writable")
        >>> print(is_writable)
        True
        >>> has_totals = get_capability("json", "totals")
        >>> print(has_totals)
        True
    """
    capabilities = get_format_capabilities(format_id)
    return capabilities.get(capability)
