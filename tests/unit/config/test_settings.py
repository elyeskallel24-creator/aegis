"""Unit tests for Settings class."""

import os
from src.config.settings import Settings, DatabaseSettings


class TestDatabaseSettingsDefaults:
    """Test that DatabaseSettings uses safe defaults."""

    def test_database_url_default(self):
        """Test default database URL."""
        db_settings = DatabaseSettings()
        assert db_settings.database_url == "postgresql://postgres:postgres@localhost:5432/aegis"


class TestDatabaseSettingsEnvironmentOverride:
    """Test that environment variables override DatabaseSettings defaults."""

    def test_database_url_override(self, monkeypatch):
        """Test AEGIS_DB_DATABASE_URL overrides default."""
        monkeypatch.setenv("AEGIS_DB_DATABASE_URL", "postgresql://user:pass@host:5432/mydb")
        db_settings = DatabaseSettings()
        assert db_settings.database_url == "postgresql://user:pass@host:5432/mydb"


class TestSettingsDefaults:
    """Test that Settings uses safe defaults when no env vars are set."""

    def test_env_default(self):
        """Test default environment is 'development'."""
        settings = Settings()
        assert settings.env == "development"

    def test_debug_default(self):
        """Test debug defaults to False."""
        settings = Settings()
        assert settings.debug is False

    def test_log_level_default(self):
        """Test log level defaults to 'INFO'."""
        settings = Settings()
        assert settings.log_level == "INFO"

    def test_api_host_default(self):
        """Test API host defaults to '127.0.0.1'."""
        settings = Settings()
        assert settings.api_host == "127.0.0.1"

    def test_api_port_default(self):
        """Test API port defaults to 8000."""
        settings = Settings()
        assert settings.api_port == 8000

    def test_max_concurrent_ai_calls_default(self):
        """Test max concurrent AI calls defaults to 2."""
        settings = Settings()
        assert settings.max_concurrent_ai_calls == 2

    def test_max_concurrent_tool_calls_default(self):
        """Test max concurrent tool calls defaults to 5."""
        settings = Settings()
        assert settings.max_concurrent_tool_calls == 5

    def test_database_settings_default(self):
        """Test that database settings are initialized."""
        settings = Settings()
        assert settings.database is not None
        assert settings.database.database_url == "postgresql://postgres:postgres@localhost:5432/aegis"


class TestSettingsEnvironmentOverride:
    """Test that environment variables correctly override defaults."""

    def test_env_override(self, monkeypatch):
        """Test AEGIS_ENV overrides default."""
        monkeypatch.setenv("AEGIS_ENV", "production")
        settings = Settings()
        assert settings.env == "production"

    def test_debug_override(self, monkeypatch):
        """Test AEGIS_DEBUG overrides default."""
        monkeypatch.setenv("AEGIS_DEBUG", "true")
        settings = Settings()
        assert settings.debug is True

    def test_log_level_override(self, monkeypatch):
        """Test AEGIS_LOG_LEVEL overrides default."""
        monkeypatch.setenv("AEGIS_LOG_LEVEL", "DEBUG")
        settings = Settings()
        assert settings.log_level == "DEBUG"

    def test_api_host_override(self, monkeypatch):
        """Test AEGIS_API_HOST overrides default."""
        monkeypatch.setenv("AEGIS_API_HOST", "0.0.0.0")
        settings = Settings()
        assert settings.api_host == "0.0.0.0"

    def test_api_port_override(self, monkeypatch):
        """Test AEGIS_API_PORT overrides default."""
        monkeypatch.setenv("AEGIS_API_PORT", "9999")
        settings = Settings()
        assert settings.api_port == 9999

    def test_max_concurrent_ai_calls_override(self, monkeypatch):
        """Test AEGIS_MAX_CONCURRENT_AI_CALLS overrides default."""
        monkeypatch.setenv("AEGIS_MAX_CONCURRENT_AI_CALLS", "10")
        settings = Settings()
        assert settings.max_concurrent_ai_calls == 10

    def test_max_concurrent_tool_calls_override(self, monkeypatch):
        """Test AEGIS_MAX_CONCURRENT_TOOL_CALLS overrides default."""
        monkeypatch.setenv("AEGIS_MAX_CONCURRENT_TOOL_CALLS", "20")
        settings = Settings()
        assert settings.max_concurrent_tool_calls == 20