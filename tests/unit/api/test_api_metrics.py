"""Unit tests for the metrics API endpoint."""

import pytest
from fastapi.testclient import TestClient
from src.api.app import create_app


class TestMetricsEndpoint:
    """Tests for the /metrics endpoint."""

    @pytest.fixture
    def client(self):
        """Create a test client."""
        app = create_app()
        return TestClient(app)

    def test_metrics_endpoint_success(self, client):
        """Test successful metrics request."""
        response = client.get("/metrics")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        # The /metrics endpoint itself should be tracked after this request
        # but since we check immediately, it might not be in the response yet.
        # We just verify the structure is correct.

    def test_metrics_tracks_requests(self, client):
        """Test that making requests updates the metrics."""
        # Make a few requests to different endpoints
        client.get("/health/live")
        client.get("/health/live")
        client.post("/chat", json={"message": "test"})
        
        # Now check metrics
        response = client.get("/metrics")
        assert response.status_code == 200
        data = response.json()
        
        # Verify health endpoint was tracked
        assert "/health/live" in data
        assert data["/health/live"]["count"] >= 2
        
        # Verify chat endpoint was tracked
        assert "/chat" in data
        assert data["/chat"]["count"] >= 1
        
        # Verify latency is recorded
        assert data["/health/live"]["avg_latency_ms"] >= 0