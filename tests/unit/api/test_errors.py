"""Unit tests for structured error handling."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.api.errors import AegisError, ValidationError, NotFoundError, InternalError
from src.api.exception_handlers import aegis_error_handler, generic_exception_handler
from src.api.middleware import CorrelationIDMiddleware


def create_test_app_with_errors():
    """Create app with exception handlers and middleware for testing."""
    app = FastAPI(title="TestApp")
    
    # Add middleware using the class-based approach
    app.add_middleware(CorrelationIDMiddleware)
    
    # Register exception handlers
    app.add_exception_handler(AegisError, aegis_error_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
    
    @app.get("/test/validation-error")
    async def raise_validation_error():
        raise ValidationError(message="Invalid input", details={"field": "email"})
    
    @app.get("/test/not-found")
    async def raise_not_found_error():
        raise NotFoundError(message="User not found")
    
    @app.get("/test/internal-error")
    async def raise_internal_error():
        raise InternalError(message="Database connection failed")
    
    @app.get("/test/generic-exception")
    async def raise_generic_exception():
        raise RuntimeError("Something went wrong!")
    
    return app


class TestAegisErrorHandling:
    """Tests for AegisError subclass handling."""
    
    def test_validation_error_returns_400(self):
        """Test that ValidationError returns 400 status code."""
        app = create_test_app_with_errors()
        client = TestClient(app)
        response = client.get("/test/validation-error")
        assert response.status_code == 400
    
    def test_validation_error_structure(self):
        """Test that ValidationError returns correct JSON structure."""
        app = create_test_app_with_errors()
        client = TestClient(app)
        response = client.get("/test/validation-error")
        data = response.json()
        assert data["error_code"] == "VALIDATION_ERROR"
        assert data["message"] == "Invalid input"
        assert "correlation_id" in data
        assert data["details"] == {"field": "email"}
    
    def test_not_found_error_returns_404(self):
        """Test that NotFoundError returns 404 status code."""
        app = create_test_app_with_errors()
        client = TestClient(app)
        response = client.get("/test/not-found")
        assert response.status_code == 404
    
    def test_not_found_error_structure(self):
        """Test that NotFoundError returns correct JSON structure."""
        app = create_test_app_with_errors()
        client = TestClient(app)
        response = client.get("/test/not-found")
        data = response.json()
        assert data["error_code"] == "NOT_FOUND"
        assert data["message"] == "User not found"
        assert "correlation_id" in data
    
    def test_internal_error_returns_500(self):
        """Test that InternalError returns 500 status code."""
        app = create_test_app_with_errors()
        client = TestClient(app)
        response = client.get("/test/internal-error")
        assert response.status_code == 500
    
    def test_correlation_id_in_error_response(self):
        """Test that correlation_id is included in all error responses."""
        app = create_test_app_with_errors()
        client = TestClient(app)
        
        # Test with custom correlation ID
        custom_corr_id = "test-correlation-123"
        headers = {"X-Correlation-ID": custom_corr_id}
        
        response = client.get("/test/validation-error", headers=headers)
        data = response.json()
        assert data["correlation_id"] == custom_corr_id
        
        # Verify it's echoed back in response header too
        assert response.headers.get("X-Correlation-ID") == custom_corr_id


class TestGenericExceptionHandling:
    """Tests for generic exception handling."""
    
    def test_generic_exception_returns_500(self):
        """Test that generic exceptions return 500 status code."""
        app = create_test_app_with_errors()
        client = TestClient(app, raise_server_exceptions=False)
        response = client.get("/test/generic-exception")
        assert response.status_code == 500
    
    def test_generic_exception_hides_traceback(self):
        """Test that generic exceptions don't leak stack traces."""
        app = create_test_app_with_errors()
        client = TestClient(app, raise_server_exceptions=False)
        response = client.get("/test/generic-exception")
        data = response.json()
        
        # Should have safe message, not the actual exception message
        assert data["message"] == "An unexpected error occurred"
        assert data["error_code"] == "INTERNAL_ERROR"
        assert "correlation_id" in data
        
        # Should NOT contain the original exception message
        assert "RuntimeError" not in str(data)
        assert "Something went wrong!" not in str(data)
    
    def test_generic_exception_correlation_id(self):
        """Test that correlation_id is included in generic error responses."""
        app = create_test_app_with_errors()
        client = TestClient(app, raise_server_exceptions=False)
        response = client.get("/test/generic-exception")
        data = response.json()
        assert "correlation_id" in data
        assert len(data["correlation_id"]) > 0  # Should be a valid UUID string
