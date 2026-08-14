"""Unit tests for the agent orchestration system."""

import pytest
from unittest.mock import AsyncMock, MagicMock
from src.core.agent import Agent
from src.core.llm import LLMResponse
from src.core.tool import BaseTool


class MockTool(BaseTool):
    """Mock tool for testing."""

    @property
    def name(self) -> str:
        return "mock_tool"

    @property
    def description(self) -> str:
        return "A mock tool"

    @property
    def parameters(self) -> dict:
        return {"type": "object", "properties": {}}

    async def execute(self, **kwargs):
        return f"Tool executed with {kwargs}"


class TestAgent:
    """Tests for agent orchestration."""

    @pytest.mark.asyncio
    async def test_agent_initialization(self):
        """Test that agent initializes with required components."""
        mock_llm = MagicMock()
        mock_registry = MagicMock()
        mock_governor = MagicMock()
        
        agent = Agent(mock_llm, mock_registry, mock_governor)
        
        assert agent.llm is mock_llm
        assert agent.tools is mock_registry
        assert agent.governor is mock_governor

    @pytest.mark.asyncio
    async def test_agent_run_without_tool(self):
        """Test agent run when LLM doesn't request tool use."""
        # Setup mocks
        mock_llm = MagicMock()
        mock_llm.generate = AsyncMock(return_value=LLMResponse(
            content="Just answer the question",
            model="mock",
            usage={}
        ))
        
        mock_registry = MagicMock()
        mock_registry.list_tools.return_value = []
        
        # Mock governor context managers
        mock_governor = MagicMock()
        mock_governor.ai_call.return_value.__aenter__ = AsyncMock()
        mock_governor.ai_call.return_value.__aexit__ = AsyncMock()
        
        agent = Agent(mock_llm, mock_registry, mock_governor)
        result = await agent.run("What is the weather?")
        
        assert "llm_response" in result
        assert "tool_result" in result
        assert result["tool_result"] is None
        assert result["llm_response"] == "Just answer the question"

    @pytest.mark.asyncio
    async def test_agent_run_with_tool(self):
        """Test agent run when LLM requests tool use."""
        # Setup mocks
        mock_llm = MagicMock()
        mock_llm.generate = AsyncMock(return_value=LLMResponse(
            content="I should use tool to get the answer",
            model="mock",
            usage={}
        ))
        
        mock_tool = MockTool()
        mock_registry = MagicMock()
        mock_registry.list_tools.return_value = [mock_tool]
        
        # Mock governor context managers
        mock_governor = MagicMock()
        mock_governor.ai_call.return_value.__aenter__ = AsyncMock()
        mock_governor.ai_call.return_value.__aexit__ = AsyncMock()
        mock_governor.tool_call.return_value.__aenter__ = AsyncMock()
        mock_governor.tool_call.return_value.__aexit__ = AsyncMock()
        
        agent = Agent(mock_llm, mock_registry, mock_governor)
        result = await agent.run("Get data for me")
        
        assert "llm_response" in result
        assert "tool_result" in result
        assert result["tool_result"] is not None
        assert "Tool executed" in result["tool_result"]
        assert "final_answer" in result

    @pytest.mark.asyncio
    async def test_agent_respects_governor_limits(self):
        """Test that agent uses governor for concurrency control."""
        mock_llm = MagicMock()
        mock_llm.generate = AsyncMock(return_value=LLMResponse(
            content="Simple answer",
            model="mock",
            usage={}
        ))
        
        mock_registry = MagicMock()
        mock_registry.list_tools.return_value = []
        
        # Track governor usage
        ai_call_count = 0
        tool_call_count = 0
        
        class MockGovernor:
            def ai_call(self):
                class ContextManager:
                    async def __aenter__(self):
                        nonlocal ai_call_count
                        ai_call_count += 1
                    async def __aexit__(self, *args):
                        pass
                return ContextManager()
            
            def tool_call(self):
                class ContextManager:
                    async def __aenter__(self):
                        nonlocal tool_call_count
                        tool_call_count += 1
                    async def __aexit__(self, *args):
                        pass
                return ContextManager()
        
        agent = Agent(mock_llm, mock_registry, MockGovernor())
        await agent.run("Test prompt")
        
        assert ai_call_count == 1  # Should use governor for LLM call
        assert tool_call_count == 0  # No tool was called