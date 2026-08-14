"""Base interface for executable tools."""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseTool(ABC):
    """Abstract base class for all executable tools."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique tool name (used by LLM to call the tool)."""

    @property
    @abstractmethod
    def description(self) -> str:
        """Human-readable description of what the tool does."""

    @property
    @abstractmethod
    def parameters(self) -> Dict[str, Any]:
        """JSON schema describing the tool's input parameters."""

    @abstractmethod
    async def execute(self, **kwargs: Any) -> Any:
        """Execute the tool with the given parameters and return the result."""