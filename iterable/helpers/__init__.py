"""Helper modules for IterableData."""

from .capabilities import (
    get_capability,
    get_format_capabilities,
    list_all_capabilities,
    supports_write,
)

try:
    from .bridges import to_dask
except ImportError:
    # Dask not available
    to_dask = None

__all__ = [
    "get_capability",
    "get_format_capabilities",
    "list_all_capabilities",
    "supports_write",
]

if to_dask is not None:
    __all__.append("to_dask")
