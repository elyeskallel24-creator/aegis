"""Health check aggregation."""

class HealthChecker:
    def __init__(self, db_pool=None, llm_provider=None, agent=None):
        self.db_pool = db_pool
        self.llm_provider = llm_provider
        self.agent = agent

    async def check_readiness(self) -> tuple:
        status = {"status": "ready", "checks": {}}
        is_ready = True

        if self.db_pool:
            status["checks"]["database"] = "up"
        else:
            status["checks"]["database"] = "skipped"

        if self.llm_provider:
            status["checks"]["llm"] = "up"
        else:
            status["checks"]["llm"] = "skipped"

        status["status"] = "ready" if is_ready else "not_ready"
        return status, is_ready
