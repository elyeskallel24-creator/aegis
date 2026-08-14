"""Unit tests for deep health checks."""
import pytest
from fastapi.testclient import TestClient
from src.api.app import create_app

class TestHealthEndpoints:
    @pytest.fixture
    def client(self):
        return TestClient(create_app())

    def test_liveness_returns_200(self, client):
        response = client.get("/health/live")
        assert response.status_code == 200
        assert response.json()["status"] == "alive"

    def test_readiness_returns_200_when_ready(self, client):
        response = client.get("/health/ready")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"
        assert "checks" in data
