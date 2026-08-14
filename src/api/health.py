"""Health check API endpoints."""
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from src.core.health import HealthChecker

router = APIRouter(tags=["health"])

@router.get("/health/live")
async def liveness():
    return {"status": "alive"}

@router.get("/health/ready")
async def readiness(request: Request):
    db_pool = getattr(request.app.state, "db_pool", None)
    llm = getattr(request.app.state, "llm_provider", None)
    agent = getattr(request.app.state, "agent", None)
    
    checker = HealthChecker(db_pool=db_pool, llm_provider=llm, agent=agent)
    result, is_ready = await checker.check_readiness()
    
    status_code = 200 if is_ready else 503
    return JSONResponse(content=result, status_code=status_code)
