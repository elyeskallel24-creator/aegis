"""Unit tests for the tool execution system."""

import pytest
from typing import Any, Dict
from src.core.tool import BaseTool
from src.core.tool_registry import ToolRegistry


class DummyTool(BaseTool):
    """Concrete tool for testing."""

    def __init__(self, name: str = "dummy_tool"):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return "A dummy tool for testing."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "input_value": {"type": "string", "description": "Test input"}
            },
            "required": ["input_value"]
        }

    async def execute(self, **kwargs: Any) -> Any:
        return f"Executed with: {kwargs.get('input_value')}"


class TestBaseTool:
    """Tests for the abstract tool interface."""

    def test_cannot_instantiate_abstract(self):
        """BaseTool cannot be instantiated directly."""
        with pytest.raises(TypeError):
            BaseTool()

    def test_concrete_tool_implements_interface(self):
        """A concrete subclass satisfies the interface."""
        tool = DummyTool()
        assert tool.name == "dummy_tool"
        assert tool.description == "A dummy tool for testing."
        assert "properties" in tool.parameters


class TestToolRegistry:
    """Tests for the tool registry."""

    def test_register_and_get(self):
        registry = ToolRegistry()
        tool = DummyTool("test_tool")
        registry.register(tool)
        assert registry.get("test_tool") is tool

    def test_get_missing_returns_none(self):
        registry = ToolRegistry()
        assert registry.get("missing") is None

    def test_duplicate_registration_raises(self):
        registry = ToolRegistry()
        registry.register(DummyTool("test_tool"))
        with pytest.raises(ValueError):
            registry.register(DummyTool("test_tool"))

    def test_list_tools(self):
        registry = ToolRegistry()
        tool1 = DummyTool("tool1")
        tool2 = DummyTool("tool2")
        registry.register(tool1)
        registry.register(tool2)
        assert len(registry.list_tools()) == 2

    def test_get_schemas(self):
        registry = ToolRegistry()
        tool = DummyTool("schema_tool")
        registry.register(tool)
        
        schemas = registry.get_schemas()
        assert len(schemas) == 1
        assert schemas[0]["name"] == "schema_tool"
        assert schemas[0]["description"] == "A dummy tool for testing."
        assert "properties" in schemas[0]["parameters"]

    @pytest.mark.asyncio
    async def test_execute_tool(self):
        """Test that a registered tool can be executed."""
        registry = ToolRegistry()
        tool = DummyTool()
        registry.register(tool)
        
        retrieved_tool = registry.get("dummy_tool")
        result = await retrieved_tool.execute(input_value="hello")
        assert result == "Executed with: hello"