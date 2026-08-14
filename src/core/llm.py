"""Base interface for LLM providers."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class LLMResponse:
    """Standardized response from an LLM provider."""
    content: str
    model: str
    usage: dict


class BaseLLMProvider(ABC):
    """Abstract base class for all LLM integrations."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the name of the provider."""

    @abstractmethod
    async def generate(self, prompt: str) -> LLMResponse:
        """Generate a completion for the given prompt."""