"""
Core validation engine.

Provides the main validation pipeline for iterables.
"""

from __future__ import annotations

import collections.abc
from typing import Any, Iterator

from ..helpers.detect import open_iterable
from ..types import Row
from .rules import validate_value

ValidationResult = tuple[Row, list[str]]
ValidationStats = dict[str, Any]


def iterable(
    iterable: collections.abc.Iterable[Row],
    rules: dict[str, list[str]],
    mode: str = "default",
    max_errors: int | None = None,
) -> Iterator[ValidationResult] | ValidationStats:
    """
    Validate rows in an iterable dataset against validation rules.

    Args:
        iterable: An iterable of row dictionaries, or a file path/stream
        rules: Dictionary mapping field names to lists of rule names
               (e.g., {"email": ["common.email", "required"]})
        mode: Validation mode - "default", "stats", "invalid", or "valid"
        max_errors: Maximum number of errors to collect before stopping (None for no limit)

    Returns:
        - If mode="stats": Dictionary with validation statistics
        - Otherwise: Iterator of (record, errors) tuples where errors is a list of error messages

    Example:
        >>> from iterable import validate
        >>> rules = {"email": ["common.email"], "url": ["common.url"]}
        >>> for record, errors in validate.iterable("data.csv", rules):
        ...     if errors:
        ...         print(f"Errors: {errors}")
    """
    if isinstance(iterable, str):
        iterable = open_iterable(iterable)

    # Statistics tracking
    stats: ValidationStats = {
        "total_rows": 0,
        "valid_rows": 0,
        "invalid_rows": 0,
        "error_counts": {},
        "errors_by_field": {},
    }

    error_count = 0

    for row in iterable:
        stats["total_rows"] += 1
        errors: list[str] = []

        # Validate each field according to rules
        for field_name, rule_names in rules.items():
            value = row.get(field_name)

            for rule_name in rule_names:
                is_valid, error_msg = validate_value(value, rule_name)

                if not is_valid:
                    error_msg_full = f"{field_name}: {error_msg}"
                    errors.append(error_msg_full)

                    # Update statistics
                    rule_key = f"{field_name}.{rule_name}"
                    stats["error_counts"][rule_key] = stats["error_counts"].get(rule_key, 0) + 1

                    if field_name not in stats["errors_by_field"]:
                        stats["errors_by_field"][field_name] = []
                    stats["errors_by_field"][field_name].append(error_msg)

                    error_count += 1
                    if max_errors is not None and error_count >= max_errors:
                        break

            if max_errors is not None and error_count >= max_errors:
                break

        # Update row statistics
        if not errors:
            stats["valid_rows"] += 1
        else:
            stats["invalid_rows"] += 1

        # Yield based on mode
        if mode == "stats":
            # Don't yield individual results, just collect stats
            continue
        elif mode == "invalid":
            # Only yield invalid rows
            if errors:
                yield (row, errors)
        elif mode == "valid":
            # Only yield valid rows
            if not errors:
                yield (row, [])
        else:  # mode == "default"
            # Yield all rows with their errors
            yield (row, errors)

    # Return stats if in stats mode
    if mode == "stats":
        return stats
