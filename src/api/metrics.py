"""Metrics API endpoints."""

from fastapi import APIRouter, Request


router = APIRouter(tags=["metrics"])


@router.get("/metrics")
async def metrics_endpoint(request: Request):
    """Expose collected application metrics."""
    collector = request.app.state.metrics
    return collector.get_metrics()