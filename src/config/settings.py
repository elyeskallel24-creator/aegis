"""Settings and configuration management using pydantic-settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class DatabaseSettings(BaseSettings):
    """Database configuration settings."""
    
    database_url: str = "postgresql://postgres:postgres@localhost:5432/aegis"
    
    model_config = SettingsConfigDict(
        env_prefix="AEGIS_DB_",
        extra='ignore',
    )

class Settings(BaseSettings):
    """
    Centralized configuration management for AEGIS.
    
    Uses pydantic-settings for environment variable loading with AEGIS_ prefix.
    """

    # Environment settings
    env: str = "development"
    debug: bool = False
    log_level: str = "INFO"

    # API server settings
    api_host: str = "127.0.0.1"
    api_port: int = 8000

    # Concurrency limits
    max_concurrent_ai_calls: int = 2
    max_concurrent_tool_calls: int = 5
    # Database settings
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)

    model_config = SettingsConfigDict(
        env_prefix="AEGIS_",
        env_file=".env",
        env_file_encoding="utf-8",
    )
