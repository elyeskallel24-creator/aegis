"""FastAPI application factory."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.config.settings import Settings
from src.core.governor import ResourceGovernor
from src.core.events import EventBus
from src.core.tool_registry import ToolRegistry
from src.core.mock_llm import MockLLMProvider
from src.core.agent import Agent
from src.core.chat import ChatHistory
from src.core.metrics import MetricsCollector
from src.api.middleware import correlation_id_middleware
from src.api.errors import AegisError
from src.api.exception_handlers import aegis_error_handler, generic_exception_handler
from src.api.chat import router as chat_router
from src.api.metrics import router as metrics_router
from src.api.health import router as health_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    yield
    # Shutdown


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create and configure the FastAPI application.

    Args:
        settings: Optional Settings instance. If not provided, default settings are used.

    Returns:
        Configured FastAPI application instance.
    """
    if settings is None:
        settings = Settings()

    app = FastAPI(
        title="AEGIS",
        version="0.1.0",
        debug=settings.debug,
        lifespan=lifespan,
    )

    # Instantiate and attach the resource governor
    governor = ResourceGovernor(
        max_ai_calls=settings.max_concurrent_ai_calls,
        max_tool_calls=settings.max_concurrent_tool_calls
    )
    app.state.governor = governor

    # Instantiate and attach the event bus
    event_bus = EventBus()
    app.state.event_bus = event_bus

    # Initialize agent components
    tool_registry = ToolRegistry()
    llm_provider = MockLLMProvider()
    agent = Agent(llm_provider, tool_registry, governor)
    app.state.agent = agent
    app.state.chat_history = ChatHistory()
    app.state.llm_provider = llm_provider

    # Initialize metrics collector
    metrics_collector = MetricsCollector()
    app.state.metrics = metrics_collector

    # Register routers
    app.include_router(metrics_router)
    app.include_router(chat_router)
    app.include_router(health_router)

    # Register correlation ID middleware
    app.middleware("http")(correlation_id_middleware)

    # Register exception handlers
    app.add_exception_handler(AegisError, aegis_error_handler)
    app.add_exception_handler(Exception, generic_exception_handler)

    return app
