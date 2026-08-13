"""Exception handlers for AEGIS API with structured logging."""

import logging
import traceback
from fastapi import Request, status
from fastapi.responses import JSONResponse

from src.utils.logger import correlation_id_ctx
from src.api.errors import AegisError, ErrorResponse, InternalError

logger = logging.getLogger(__name__)


async def aegis_error_handler(request: Request, exc: AegisError) -> JSONResponse:
    """Handle AegisError exceptions with structured JSON response."""
    corr_id = correlation_id_ctx.get() or "unknown"
    
    error_response = ErrorResponse(
        error_code=exc.error_code,
        message=exc.message,
        correlation_id=corr_id,
        details=getattr(exc, 'details', None)
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump()
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle generic exceptions - log full traceback, return safe 500 response."""
    corr_id = correlation_id_ctx.get() or "unknown"
    
    # Log full traceback with correlation ID
    logger.error(
        f"Unhandled exception: {str(exc)}",
        extra={
            "correlation_id": corr_id,
            "traceback": traceback.format_exc()
        }
    )
    
    # Return safe error response (no stack trace leaked)
    error_response = ErrorResponse(
        error_code="INTERNAL_ERROR",
        message="An unexpected error occurred",
        correlation_id=corr_id
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.model_dump()
    )
