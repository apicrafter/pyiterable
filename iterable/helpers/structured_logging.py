"""Structured logging framework for IterableData.

This module provides structured logging capabilities with JSON output format,
enabling better log analysis, filtering, and integration with log aggregation systems.
"""

import json
import logging
import os
import uuid
from contextvars import ContextVar
from datetime import datetime, timezone
from typing import Any, Literal

# Context variables for operation tracking
operation_id: ContextVar[str | None] = ContextVar("operation_id", default=None)
correlation_id: ContextVar[str | None] = ContextVar("correlation_id", default=None)


class LogEventType:
    """Standard log event types for structured logging."""

    FORMAT_DETECTION = "format_detection"
    FILE_IO = "file_io"
    PARSING = "parsing"
    CONVERSION = "conversion"
    PIPELINE = "pipeline"
    ERROR = "error"
    PERFORMANCE = "performance"
    VALIDATION = "validation"


class StructuredJSONFormatter(logging.Formatter):
    """JSON formatter for structured logging.

    Formats log records as JSON with consistent structure, enabling easy parsing
    and integration with log aggregation systems.
    """

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Add operation context if available
        op_id = operation_id.get()
        if op_id:
            log_data["operation_id"] = op_id

        corr_id = correlation_id.get()
        if corr_id:
            log_data["correlation_id"] = corr_id

        # Add extra context from record (structured fields)
        for key, value in record.__dict__.items():
            if key not in [
                "name",
                "msg",
                "args",
                "created",
                "filename",
                "funcName",
                "levelname",
                "levelno",
                "lineno",
                "module",
                "msecs",
                "message",
                "pathname",
                "process",
                "processName",
                "relativeCreated",
                "thread",
                "threadName",
                "exc_info",
                "exc_text",
                "stack_info",
            ]:
                # Only include JSON-serializable values
                try:
                    json.dumps(value)
                    log_data[key] = value
                except (TypeError, ValueError):
                    # Skip non-serializable values
                    pass

        return json.dumps(log_data, default=str)


class HumanReadableFormatter(logging.Formatter):
    """Human-readable formatter for structured logging.

    Formats log records in a human-readable format suitable for development
    and debugging, while still including structured context.
    """

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as human-readable text."""
        parts = [
            f"[{record.levelname}]",
            f"{record.name}",
            f"{record.funcName}:{record.lineno}",
        ]

        # Add operation context if available
        op_id = operation_id.get()
        if op_id:
            parts.append(f"op_id={op_id[:8]}")

        corr_id = correlation_id.get()
        if corr_id:
            parts.append(f"corr_id={corr_id[:8]}")

        parts.append(f"- {record.getMessage()}")

        # Add structured context fields
        context_parts = []
        for key, value in record.__dict__.items():
            if key not in [
                "name",
                "msg",
                "args",
                "created",
                "filename",
                "funcName",
                "levelname",
                "levelno",
                "lineno",
                "module",
                "msecs",
                "message",
                "pathname",
                "process",
                "processName",
                "relativeCreated",
                "thread",
                "threadName",
                "exc_info",
                "exc_text",
                "stack_info",
            ]:
                context_parts.append(f"{key}={value}")

        if context_parts:
            parts.append(f"({', '.join(context_parts)})")

        # Add exception info if present
        if record.exc_info:
            parts.append(f"\n{self.formatException(record.exc_info)}")

        return " ".join(parts)


class OperationContext:
    """Context manager for operation tracking with structured logging.

    Provides operation ID generation and context propagation for structured logs.
    """

    def __init__(self, operation_type: str, **context: Any):
        """Initialize operation context.

        Args:
            operation_type: Type of operation (e.g., "pipeline", "conversion")
            **context: Additional context to include in logs
        """
        self.operation_type = operation_type
        self.context = context
        self.operation_id = self._generate_operation_id()
        self._token: Any = None

    def __enter__(self) -> "OperationContext":
        """Enter operation context."""
        self._token = operation_id.set(self.operation_id)
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit operation context."""
        if self._token:
            operation_id.reset(self._token)

    def _generate_operation_id(self) -> str:
        """Generate unique operation ID."""
        return str(uuid.uuid4())


def configure_structured_logging(
    format: Literal["json", "human"] = "json",
    level: int = logging.INFO,
    handler: logging.Handler | None = None,
    output: str | None = None,
) -> None:
    """Configure structured logging for IterableData.

    Args:
        format: Output format - "json" for JSON, "human" for human-readable
        level: Logging level (default: logging.INFO)
        handler: Optional logging handler (default: StreamHandler to stderr)
        output: Output file path (None for stderr)

    Example:
        >>> from iterable.helpers.structured_logging import configure_structured_logging
        >>> import logging
        >>> configure_structured_logging(format="json", level=logging.INFO)
        >>> # Now all IterableData operations will use structured logging
    """
    # Create handler if not provided
    if handler is None:
        if output:
            handler = logging.FileHandler(output)
        else:
            handler = logging.StreamHandler()

    # Set formatter based on format
    if format == "json":
        formatter = StructuredJSONFormatter()
    else:
        formatter = HumanReadableFormatter()

    handler.setFormatter(formatter)

    # Configure root iterable logger
    logger = logging.getLogger("iterable")
    logger.setLevel(level)
    if not logger.handlers:
        logger.addHandler(handler)
    logger.propagate = False

    # Configure sub-loggers
    for sub_logger_name in [
        "iterable.detect",
        "iterable.io",
        "iterable.parse",
        "iterable.perf",
    ]:
        sub_logger = logging.getLogger(sub_logger_name)
        sub_logger.setLevel(level)
        if not sub_logger.handlers:
            sub_logger.addHandler(handler)
        sub_logger.propagate = False


def is_structured_logging_enabled() -> bool:
    """Check if structured logging is enabled.

    Checks the ITERABLEDATA_STRUCTURED_LOGGING environment variable.

    Returns:
        True if structured logging is enabled, False otherwise
    """
    return os.getenv("ITERABLEDATA_STRUCTURED_LOGGING", "").lower() in ("1", "true", "yes")


def configure_structured_logging_from_env() -> None:
    """Configure structured logging from environment variable.

    If ITERABLEDATA_STRUCTURED_LOGGING environment variable is set, enables structured logging.
    Format can be specified via ITERABLEDATA_LOG_FORMAT (json or human).
    """
    if is_structured_logging_enabled():
        log_format = os.getenv("ITERABLEDATA_LOG_FORMAT", "json").lower()
        if log_format not in ("json", "human"):
            log_format = "json"
        configure_structured_logging(format=log_format)


# Auto-configure from environment on import
configure_structured_logging_from_env()
