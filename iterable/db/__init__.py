"""
Database driver registry and utilities.

This module provides a registry for database drivers that enable reading
from SQL and NoSQL databases as iterable data sources.
"""

from .base import DBDriver

# Registry mapping engine names to driver classes
_DRIVER_REGISTRY: dict[str, type[DBDriver]] = {}


def register_driver(engine_name: str, driver_class: type[DBDriver]) -> None:
    """Register a database driver for a given engine name.

    Args:
        engine_name: Name of the database engine (e.g., 'postgres', 'mongo')
        driver_class: Driver class that inherits from DBDriver

    Raises:
        ValueError: If engine_name is invalid or driver_class is not a subclass of DBDriver
    """
    if not engine_name or not isinstance(engine_name, str):
        raise ValueError(f"engine_name must be a non-empty string, got {engine_name!r}")
    if not issubclass(driver_class, DBDriver):
        raise ValueError(f"driver_class must be a subclass of DBDriver, got {driver_class}")
    if engine_name in _DRIVER_REGISTRY:
        raise ValueError(f"Driver for engine '{engine_name}' is already registered")

    _DRIVER_REGISTRY[engine_name] = driver_class


def get_driver(engine_name: str) -> type[DBDriver] | None:
    """Get a registered driver class for an engine name.

    Args:
        engine_name: Name of the database engine

    Returns:
        Driver class if registered, None otherwise
    """
    return _DRIVER_REGISTRY.get(engine_name)


def list_drivers() -> list[str]:
    """List all registered database engine names.

    Returns:
        List of registered engine names
    """
    return list(_DRIVER_REGISTRY.keys())


def is_database_engine(engine_name: str) -> bool:
    """Check if an engine name is a registered database engine.

    Args:
        engine_name: Name of the engine to check

    Returns:
        True if the engine is a registered database engine, False otherwise
    """
    return engine_name in _DRIVER_REGISTRY


def _register_builtin_drivers() -> None:
    """Register built-in database drivers."""
    # PostgreSQL driver
    try:
        from .postgres import PostgresDriver

        register_driver("postgres", PostgresDriver)
        register_driver("postgresql", PostgresDriver)  # Alias
    except ImportError:
        # psycopg2 not available - skip registration
        pass


# Register built-in drivers on import
_register_builtin_drivers()

__all__ = ["DBDriver", "register_driver", "get_driver", "list_drivers", "is_database_engine"]
