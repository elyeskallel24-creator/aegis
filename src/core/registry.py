"""Component registry for managing AEGIS modules."""

from typing import Dict, List, Optional
from src.core.module import BaseModule


class ComponentRegistry:
    """Tracks registered modules and drives their lifecycle in order."""

    def __init__(self) -> None:
        self._modules: Dict[str, BaseModule] = {}

    def register(self, module: BaseModule) -> None:
        """Register a module. Raises ValueError on duplicate name."""
        if module.name in self._modules:
            raise ValueError(f"Module already registered: {module.name}")
        self._modules[module.name] = module

    def get(self, name: str) -> Optional[BaseModule]:
        """Return the registered module or None."""
        return self._modules.get(name)

    def list_modules(self) -> List[str]:
        """Return registered module names in registration order."""
        return list(self._modules.keys())

    async def initialize_all(self) -> None:
        """Initialize all modules in registration order."""
        for module in self._modules.values():
            await module.initialize()

    async def start_all(self) -> None:
        """Start all modules in registration order."""
        for module in self._modules.values():
            await module.start()

    async def stop_all(self) -> None:
        """Stop all modules in reverse registration order."""
        for module in reversed(list(self._modules.values())):
            await module.stop()