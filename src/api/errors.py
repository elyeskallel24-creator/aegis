"""Error classes and response models for AEGIS API."""

from typing import Optional, Any, Dict
from pydantic import BaseModel


class AegisError(Exception):
    """Base exception for AEGIS errors."""
    
    def __init__(self, message: str, error_code: str = "UNKNOWN_ERROR", status_code: int = 500, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)


class ValidationError(AegisError):
    """Raised when validation fails."""
    
    def __init__(self, message: str = "Validation failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            status_code=400,
            details=details
        )


class NotFoundError(AegisError):
    """Raised when a resource is not found."""
    
    def __init__(self, message: str = "Resource not found"):
        super().__init__(
            message=message,
            error_code="NOT_FOUND",
            status_code=404
        )


class InternalError(AegisError):
    """Raised for internal server errors."""
    
    def __init__(self, message: str = "Internal server error"):
        super().__init__(
            message=message,
            error_code="INTERNAL_ERROR",
            status_code=500
        )


class ErrorResponse(BaseModel):
    """JSON error response model."""
    
    error_code: str
    message: str
    correlation_id: str
    details: Optional[Dict[str, Any]] = None
