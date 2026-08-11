"""Unit tests for the FastAPI application factory and health endpoint."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.api.app import create_app, AppSettings


class TestAppFactory:
    """Tests for the FastAPI application factory."""

    def test_create_app_returns_fastapi_instance(self):
        """Test that create_app returns a FastAPI instance."""
        app = create_app()
        assert isinstance(app, FastAPI)

    def test_create_app_with_custom_settings(self):
        """Test that create_app uses custom settings when provided."""
        custom_settings = AppSettings(
            app_name="CustomAEGIS",
            app_version="2.0.0",
            debug=True,
        )
        app = create_app(settings=custom_settings)
        assert isinstance(app, FastAPI)
        assert app.title == "CustomAEGIS"
        assert app.version == "2.0.0"
        assert app.debug is True

    def test_create_app_default_settings(self):
        """Test that create_app uses default settings when none provided."""
        app = create_app()
        assert app.title == "AEGIS"
        assert app.version == "0.1.0"
        assert app.debug is False


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
