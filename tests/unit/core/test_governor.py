"""Unit tests for the ResourceGovernor class."""

import asyncio
import pytest
from src.core.governor import ResourceGovernor


class TestResourceGovernorInit:
    """Tests for ResourceGovernor initialization."""

    def test_init_with_default_limits(self):
        """Test governor initializes with correct limits."""
        governor = ResourceGovernor(max_ai_calls=2, max_tool_calls=5)
        assert governor.max_ai_calls == 2
        assert governor.max_tool_calls == 5

    def test_init_with_custom_limits(self):
        """Test governor initializes with custom limits."""
        governor = ResourceGovernor(max_ai_calls=10, max_tool_calls=20)
        assert governor.max_ai_calls == 10
        assert governor.max_tool_calls == 20


class TestResourceGovernorAiCall:
    """Tests for ai_call context manager."""

    @pytest.mark.asyncio
    async def test_ai_call_acquires_releases_semaphore(self):
        """Test that ai_call properly acquires and releases semaphore."""
        governor = ResourceGovernor(max_ai_calls=1, max_tool_calls=1)
        
        async with governor.ai_call():
            # Inside context, semaphore should be acquired
            pass
        # Outside context, semaphore should be released

    @pytest.mark.asyncio
    async def test_ai_call_enforces_limit(self):
        """Test that ai_call enforces the concurrency limit."""
        governor = ResourceGovernor(max_ai_calls=1, max_tool_calls=5)
        acquired = False
        
        async def hold_ai_call():
            nonlocal acquired
            async with governor.ai_call():
                acquired = True
                await asyncio.sleep(0.1)
        
        async def try_ai_call():
            async with governor.ai_call():
                return True
        
        # Start first call
        task1 = asyncio.create_task(hold_ai_call())
        await asyncio.sleep(0.01)  # Let first task acquire semaphore
        assert acquired is True
        
        # Try second call - should block
        task2 = asyncio.create_task(try_ai_call())
        done, pending = await asyncio.wait([task2], timeout=0.05)
        
        # task2 should still be pending (blocked by semaphore)
        assert len(pending) == 1
        
        # Cancel and cleanup
        task2.cancel()
        await task1
        try:
            await task2
        except asyncio.CancelledError:
            pass


class TestResourceGovernorToolCall:
    """Tests for tool_call context manager."""

    @pytest.mark.asyncio
    async def test_tool_call_acquires_releases_semaphore(self):
        """Test that tool_call properly acquires and releases semaphore."""
        governor = ResourceGovernor(max_ai_calls=1, max_tool_calls=1)
        
        async with governor.tool_call():
            # Inside context, semaphore should be acquired
            pass
        # Outside context, semaphore should be released

    @pytest.mark.asyncio
    async def test_tool_call_enforces_limit(self):
        """Test that tool_call enforces the concurrency limit."""
        governor = ResourceGovernor(max_ai_calls=5, max_tool_calls=1)
        acquired = False
        
        async def hold_tool_call():
            nonlocal acquired
            async with governor.tool_call():
                acquired = True
                await asyncio.sleep(0.1)
        
        async def try_tool_call():
            async with governor.tool_call():
                return True
        
        # Start first call
        task1 = asyncio.create_task(hold_tool_call())
        await asyncio.sleep(0.01)
        assert acquired is True
        
        # Try second call - should block
        task2 = asyncio.create_task(try_tool_call())
        done, pending = await asyncio.wait([task2], timeout=0.05)
        
        # task2 should still be pending (blocked by semaphore)
        assert len(pending) == 1
        
        # Cancel and cleanup
        task2.cancel()
        await task1
        try:
            await task2
        except asyncio.CancelledError:
            pass
