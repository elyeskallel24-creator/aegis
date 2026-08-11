# AEGIS Documentation

## Overview

AEGIS (Advanced Extensible Guarded Intelligence System) is a modular AI framework following Qwen Max standards.

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Architecture](#architecture)
4. [API Reference](#api-reference)
5. [Contributing](#contributing)

## Installation

```bash
pip install -e .
```

For development:

```bash
pip install -e ".[dev]"
```

## Quick Start

```python
from aegis.core import Engine

# Initialize the engine
engine = Engine()
engine.initialize()

# Register a module
engine.register_module("my_module", my_module_instance)

# Retrieve a module
module = engine.get_module("my_module")
```

## Architecture

AEGIS follows a modular architecture with the following components:

- **Core**: Main engine and orchestration logic
- **Modules**: Pluggable feature modules
- **Utils**: Shared utilities and helpers
- **Config**: Configuration management

## API Reference

### Engine

The `Engine` class is the main entry point for AEGIS.

```python
class Engine:
    def __init__(self, config_path: Optional[str] = None)
    def initialize(self) -> None
    def is_initialized(self) -> bool
    def register_module(self, name: str, module: Any) -> None
    def get_module(self, name: str) -> Optional[Any]
```

### Settings

The `Settings` class manages configuration.

```python
class Settings:
    def __init__(self, config_path: Optional[Path] = None)
    def load(self) -> Settings
    def get(self, key: str, default: Any = None) -> Any
    def set(self, key: str, value: Any) -> None
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `pytest`
5. Submit a pull request

## License

MIT License
