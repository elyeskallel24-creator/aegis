"""Mock LLM provider for testing and development."""

from src.core.llm import BaseLLMProvider, LLMResponse


class MockLLMProvider(BaseLLMProvider):
    """Deterministic mock provider that echoes the prompt."""

    @property
    def provider_name(self) -> str:
        return "mock"

    async def generate(self, prompt: str) -> LLMResponse:
        return LLMResponse(
            content=f"Mock response to: {prompt}",
            model="mock-model-v1",
            usage={"prompt_tokens": len(prompt.split()), "completion_tokens": 5}
        )