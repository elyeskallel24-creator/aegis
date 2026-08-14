"""Unit tests for the chat API endpoint."""

import pytest
from fastapi.testclient import TestClient
from src.api.app import create_app


class TestChatEndpoint:
    """Tests for the /chat endpoint."""

    @pytest.fixture
    def client(self):
        """Create a test client."""
        app = create_app()
        return TestClient(app)

    def test_chat_endpoint_success(self, client):
        """Test successful chat request."""
        response = client.post("/chat", json={"message": "Hello agent"})
        
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "history_length" in data
        assert data["history_length"] == 2  # user + assistant
        assert "Agent processed" in data["response"]

    def test_chat_endpoint_invalid_payload(self, client):
        """Test chat request with missing message field."""
        response = client.post("/chat", json={})
        assert response.status_code == 422  # Validation error

    def test_chat_history_grows(self, client):
        """Test that chat history grows with multiple requests."""
        response1 = client.post("/chat", json={"message": "First"})
        assert response1.status_code == 200
        len1 = response1.json()["history_length"]
        
        response2 = client.post("/chat", json={"message": "Second"})
        assert response2.status_code == 200
        len2 = response2.json()["history_length"]
        
        assert len2 == len1 + 2