"""Structured logging utility with correlation ID support."""

import logging
import json
import contextvars
from typing import Any, Dict

# Context variable for correlation ID
correlation_id_ctx: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "correlation_id", default=None
)


class StructuredFormatter(logging.Formatter):
    """JSON formatter that injects correlation_id from context."""

    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {
            "level": record.levelname,
            "message": record.getMessage(),
            "timestamp": self.formatTime(record),
            "logger": record.name,
        }

        # Inject correlation_id if present in context
        corr_id = correlation_id_ctx.get()
        if corr_id:
            log_data["correlation_id"] = corr_id

        # Add extra fields if present
        if hasattr(record, "extra_fields"):
            log_data.update(record.extra_fields)

        return json.dumps(log_data)


def get_logger(
    name: str,
    level: str | None = None,
    format_string: str | None = None,
) -> logging.Logger:
    """Get a logger with structured JSON formatting."""
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    level = level or "INFO"
    
    handler = logging.StreamHandler()
    if format_string is None:
        handler.setFormatter(StructuredFormatter())
    else:
        handler.setFormatter(logging.Formatter(format_string))

    logger.setLevel(getattr(logging, level.upper()))
    logger.addHandler(handler)

    return logger
