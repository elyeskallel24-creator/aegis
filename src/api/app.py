"""FastAPI application factory for AEGIS."""

from fastapi import FastAPI
from src.config.settings import Settings
from src.core.governor import ResourceGovernor
from src.api.middleware import correlation_id_middleware
from src.api.exception_handlers import aegis_error_handler, generic_exception_handler
from src.api.errors import AegisError


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

    # Instantiate and attach the resource governor
    governor = ResourceGovernor(
        max_ai_calls=settings.max_concurrent_ai_calls,
        max_tool_calls=settings.max_concurrent_tool_calls
    )
    app.state.governor = governor

    # Register correlation ID middleware
    app.middleware("http")(correlation_id_middleware)

    # Register exception handlers
    app.add_exception_handler(AegisError, aegis_error_handler)
    app.add_exception_handler(Exception, generic_exception_handler)

    # Register health endpoint
    @app.get("/health/live", tags=["health"])
    async def health_live() -> dict[str, str]:
        """Live health check endpoint.

        Returns:
            Dict with status indicating the application is alive.
        """
        return {"status": "alive"}

    return app
