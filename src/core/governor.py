"""Resource governor for enforcing concurrency limits."""

import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator


class ResourceGovernor:
    """Enforces concurrency limits for AI and tool calls using semaphores."""

    def __init__(self, max_ai_calls: int, max_tool_calls: int):
        """
        Initialize the governor with concurrency limits.

        Args:
            max_ai_calls: Maximum concurrent AI calls allowed.
            max_tool_calls: Maximum concurrent tool calls allowed.
        """
        self._ai_semaphore = asyncio.Semaphore(max_ai_calls)
        self._tool_semaphore = asyncio.Semaphore(max_tool_calls)
        self._max_ai_calls = max_ai_calls
        self._max_tool_calls = max_tool_calls

    @asynccontextmanager
    async def ai_call(self) -> AsyncIterator[None]:
        """Context manager for AI calls that enforces the limit."""
        async with self._ai_semaphore:
            yield

    @asynccontextmanager
    async def tool_call(self) -> AsyncIterator[None]:
        """Context manager for tool calls that enforces the limit."""
        async with self._tool_semaphore:
            yield

    @property
    def max_ai_calls(self) -> int:
        """Return the maximum AI calls limit."""
        return self._max_ai_calls

    @property
    def max_tool_calls(self) -> int:
        """Return the maximum tool calls limit."""
        return self._max_tool_calls
