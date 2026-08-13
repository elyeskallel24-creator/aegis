"""Unit tests for the FastAPI application factory and health endpoint."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.api.app import create_app
from src.config.settings import Settings
from src.core.governor import ResourceGovernor


class TestAppFactory:
    """Tests for the FastAPI application factory."""

    def test_create_app_returns_fastapi_instance(self):
        """Test that create_app returns a FastAPI instance."""
        app = create_app()
        assert isinstance(app, FastAPI)

    def test_create_app_with_custom_settings(self):
        """Test that create_app uses custom settings when provided."""
        custom_settings = Settings(
            debug=True,
        )
        app = create_app(settings=custom_settings)
        assert isinstance(app, FastAPI)
        assert app.title == "AEGIS"
        assert app.version == "0.1.0"
        assert app.debug is True

    def test_create_app_default_settings(self):
        """Test that create_app uses default settings when none provided."""
        app = create_app()
        assert app.title == "AEGIS"
        assert app.version == "0.1.0"
        assert app.debug is False

    def test_create_app_attaches_governor(self):
        """Test that create_app attaches ResourceGovernor to app.state."""
        app = create_app()
        assert hasattr(app.state, 'governor')
        assert isinstance(app.state.governor, ResourceGovernor)

    def test_create_app_governor_has_correct_limits(self):
        """Test that governor is configured with limits from settings."""
        app = create_app()
        assert app.state.governor.max_ai_calls == 2
        assert app.state.governor.max_tool_calls == 5

    def test_create_app_governor_with_custom_limits(self):
        """Test that governor uses custom limits from settings."""
        custom_settings = Settings(
            max_concurrent_ai_calls=10,
            max_concurrent_tool_calls=20
        )
        app = create_app(settings=custom_settings)
        assert app.state.governor.max_ai_calls == 10
        assert app.state.governor.max_tool_calls == 20


class TestHealthEndpoint:
    """Tests for the /health/live endpoint."""

    @pytest.fixture
    def client(self) -> TestClient:
        """Create a test client for the application."""
        app = create_app()
        return TestClient(app)

    def test_health_live_returns_200(self, client: TestClient):
        """Test that GET /health/live returns 200 OK status."""
        response = client.get("/health/live")
        assert response.status_code == 200

    def test_health_live_returns_alive_status(self, client: TestClient):
        """Test that GET /health/live returns correct status body."""
        response = client.get("/health/live")
        data = response.json()
        assert data == {"status": "alive"}

    def test_health_live_content_type(self, client: TestClient):
        """Test that GET /health/live returns JSON content type."""
        response = client.get("/health/live")
        assert "application/json" in response.headers["content-type"]
