"""FastAPI application factory for AEGIS."""

from fastapi import FastAPI
from src.config.settings import Settings


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create and configure the FastAPI application.

    Args:
        settings: Optional Settings instance. If not provided, default settings are used.

    Returns:
        Configured FastAPI application instance.
    """
    if settings is None:
        settings = Settings()

    app = FastAPI(
        title="AEGIS",
        version="0.1.0",
        debug=settings.debug,
    )

    # Register health endpoint
    @app.get("/health/live", tags=["health"])
    async def health_live() -> dict[str, str]:
        """Live health check endpoint.

        Returns:
            Dict with status indicating the application is alive.
        """
        return {"status": "alive"}

    return app
