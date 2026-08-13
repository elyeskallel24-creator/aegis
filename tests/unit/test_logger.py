"""Unit tests for the structured logger and correlation ID injection."""

import json
import logging
import pytest
from contextvars import copy_context

from src.utils.logger import get_logger, StructuredFormatter, correlation_id_ctx


class TestStructuredFormatter:
    """Tests for the StructuredFormatter class."""

    def test_format_produces_valid_json(self):
        """Test that formatter produces valid JSON output."""
        formatter = StructuredFormatter()
        record = logging.LogRecord(
            name="test_logger",
            level=logging.INFO,
            pathname="test.py",
            lineno=1,
            msg="Test message",
            args=(),
            exc_info=None,
        )
        output = formatter.format(record)
        # Should be valid JSON
        data = json.loads(output)
        assert data["level"] == "INFO"
        assert data["message"] == "Test message"
        assert "logger" in data
        assert "timestamp" in data

    def test_format_includes_correlation_id_when_set(self):
        """Test that correlation_id is included when set in context."""
        formatter = StructuredFormatter()
        
        # Set correlation ID in context
        token = correlation_id_ctx.set("test-corr-id-123")
        try:
            record = logging.LogRecord(
                name="test_logger",
                level=logging.INFO,
                pathname="test.py",
                lineno=1,
                msg="Test message",
                args=(),
                exc_info=None,
            )
            output = formatter.format(record)
            data = json.loads(output)
            assert data["correlation_id"] == "test-corr-id-123"
        finally:
            correlation_id_ctx.reset(token)

    def test_format_excludes_correlation_id_when_not_set(self):
        """Test that correlation_id is omitted when not set in context."""
        formatter = StructuredFormatter()
        
        # Ensure no correlation ID in context
        token = correlation_id_ctx.set(None)
        try:
            record = logging.LogRecord(
                name="test_logger",
                level=logging.INFO,
                pathname="test.py",
                lineno=1,
                msg="Test message",
                args=(),
                exc_info=None,
            )
            output = formatter.format(record)
            data = json.loads(output)
            assert "correlation_id" not in data or data.get("correlation_id") is None
        finally:
            correlation_id_ctx.reset(token)


class TestCorrelationIdContext:
    """Tests for correlation ID context variable."""

    def test_context_isolation(self):
        """Test that correlation ID is isolated per context."""
        # Set correlation ID in main context
        token1 = correlation_id_ctx.set("context-1-id")
        
        # Create a new context with different correlation ID
        ctx = copy_context()
        result = ctx.run(lambda: (
            correlation_id_ctx.set("context-2-id"),
            correlation_id_ctx.get()
        ))
        
        # Main context should still have original value
        assert correlation_id_ctx.get() == "context-1-id"
        
        # Clean up
        correlation_id_ctx.reset(token1)

    def test_context_var_default_is_none(self):
        """Test that default correlation ID is None."""
        assert correlation_id_ctx.get() is None
