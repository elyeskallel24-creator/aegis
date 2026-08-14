"""Unit tests for LLM provider interface and mock."""

import pytest
from src.core.llm import BaseLLMProvider, LLMResponse
from src.core.mock_llm import MockLLMProvider


class TestBaseLLMProvider:
    """Tests for the abstract LLM interface."""

    def test_cannot_instantiate_abstract(self):
        """BaseLLMProvider cannot be instantiated directly."""
        with pytest.raises(TypeError):
            BaseLLMProvider()


class TestMockLLMProvider:
    """Tests for the mock LLM implementation."""

    def test_provider_name(self):
        """Mock provider reports correct name."""
        provider = MockLLMProvider()
        assert provider.provider_name == "mock"

    @pytest.mark.asyncio
    async def test_generate_returns_response(self):
        """Mock provider returns correctly formatted LLMResponse."""
        provider = MockLLMProvider()
        response = await provider.generate("Hello world")
        
        assert isinstance(response, LLMResponse)
        assert response.content == "Mock response to: Hello world"
        assert response.model == "mock-model-v1"
        assert response.usage["prompt_tokens"] == 2
        assert response.usage["completion_tokens"] == 5