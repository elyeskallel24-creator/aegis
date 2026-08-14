"""Request middleware for AEGIS."""

import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from src.utils.logger import correlation_id_ctx


class CorrelationIDMiddleware(BaseHTTPMiddleware):
    """Middleware to inject and propagate correlation IDs."""

    async def dispatch(self, request: Request, call_next):
        correlation_id = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())
        correlation_id_ctx.set(correlation_id)

        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time

        if hasattr(request.app.state, 'metrics'):
            request.app.state.metrics.record_request(request.url.path, duration)

        response.headers["X-Correlation-ID"] = correlation_id
        return response


async def correlation_id_middleware(request: Request, call_next):
    """Functional middleware alternative."""
    correlation_id = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())
    correlation_id_ctx.set(correlation_id)

    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    if hasattr(request.app.state, 'metrics'):
        request.app.state.metrics.record_request(request.url.path, duration)

    response.headers["X-Correlation-ID"] = correlation_id
    return response
