"""FastAPI application factory for AEGIS."""

from pathlib import Path
from fastapi import FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Application settings using pydantic-settings."""

    app_name: str = "AEGIS"
    app_version: str = "0.1.0"
    debug: bool = False

    model_config = SettingsConfigDict(
        env_prefix="AEGIS_",
        env_file=".env",
    )


def create_app(settings: AppSettings | None = None) -> FastAPI:
    """Create and configure the FastAPI application.

    Args:
        settings: Optional AppSettings instance. If not provided, default settings are used.

    Returns:
        Configured FastAPI application instance.
    """
    if settings is None:
        settings = AppSettings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
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
