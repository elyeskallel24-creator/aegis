"""Base module interface for AEGIS components."""

from abc import ABC, abstractmethod


class BaseModule(ABC):
    """Abstract base class defining the lifecycle contract for AEGIS modules."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique module name."""

    @property
    @abstractmethod
    def version(self) -> str:
        """Module version string."""

    @abstractmethod
    async def initialize(self) -> None:
        """Allocate resources and validate configuration."""

    @abstractmethod
    async def start(self) -> None:
        """Begin module operation."""

    @abstractmethod
    async def stop(self) -> None:
        """Release resources and shut down cleanly."""

    @abstractmethod
    async def health_check(self) -> bool:
        """Return True if the module is healthy."""