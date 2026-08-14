"""Unit tests for BaseModule and ComponentRegistry."""

import pytest
from src.core.module import BaseModule
from src.core.registry import ComponentRegistry


class DummyModule(BaseModule):
    """Concrete module for testing lifecycle behavior."""

    def __init__(self, name: str, version: str = "1.0.0"):
        self._name = name
        self._version = version
        self.calls = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def version(self) -> str:
        return self._version

    async def initialize(self) -> None:
        self.calls.append("initialize")

    async def start(self) -> None:
        self.calls.append("start")

    async def stop(self) -> None:
        self.calls.append("stop")

    async def health_check(self) -> bool:
        return True


class TestBaseModule:
    """Tests for the abstract module interface."""

    def test_cannot_instantiate_abstract(self):
        """BaseModule cannot be instantiated directly."""
        with pytest.raises(TypeError):
            BaseModule()

    def test_concrete_module_implements_interface(self):
        """A concrete subclass satisfies the interface."""
        module = DummyModule("dummy")
        assert module.name == "dummy"
        assert module.version == "1.0.0"


class TestComponentRegistry:
    """Tests for the component registry."""

    def test_register_and_get(self):
        registry = ComponentRegistry()
        module = DummyModule("alpha")
        registry.register(module)
        assert registry.get("alpha") is module

    def test_get_missing_returns_none(self):
        registry = ComponentRegistry()
        assert registry.get("missing") is None

    def test_duplicate_registration_raises(self):
        registry = ComponentRegistry()
        registry.register(DummyModule("alpha"))
        with pytest.raises(ValueError):
            registry.register(DummyModule("alpha"))

    def test_list_modules_registration_order(self):
        registry = ComponentRegistry()
        registry.register(DummyModule("alpha"))
        registry.register(DummyModule("beta"))
        assert registry.list_modules() == ["alpha", "beta"]

    @pytest.mark.asyncio
    async def test_initialize_and_start_all(self):
        registry = ComponentRegistry()
        first = DummyModule("first")
        second = DummyModule("second")
        registry.register(first)
        registry.register(second)

        await registry.initialize_all()
        await registry.start_all()

        assert first.calls == ["initialize", "start"]
        assert second.calls == ["initialize", "start"]

    @pytest.mark.asyncio
    async def test_stop_all_reverse_order(self):
        registry = ComponentRegistry()
        order = []

        class OrderModule(BaseModule):
            def __init__(self, name):
                self._name = name

            @property
            def name(self):
                return self._name

            @property
            def version(self):
                return "1.0.0"

            async def initialize(self):
                pass

            async def start(self):
                pass

            async def stop(self):
                order.append(self._name)

            async def health_check(self):
                return True

        registry.register(OrderModule("first"))
        registry.register(OrderModule("second"))

        await registry.stop_all()

        assert order == ["second", "first"]