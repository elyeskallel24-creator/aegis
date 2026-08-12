"""FastAPI middleware for correlation ID handling."""

import uuid
from fastapi import Request, Response

from src.utils.logger import correlation_id_ctx


async def correlation_id_middleware(request: Request, call_next):
    """Extract or generate correlation ID, store in context, add to response.
    
    Args:
        request: Incoming FastAPI request.
        call_next: Next middleware/handler in chain.
        
    Returns:
        Response with X-Correlation-ID header.
    """
    # Get or generate correlation ID
    corr_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
    
    # Store in context for duration of request
    token = correlation_id_ctx.set(corr_id)
    
    try:
        response = await call_next(request)
    finally:
        # Restore previous context
        correlation_id_ctx.reset(token)
    
    # Add to response headers
    response.headers["X-Correlation-ID"] = corr_id
    
    return response
