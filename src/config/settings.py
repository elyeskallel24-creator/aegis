"""
Settings and configuration management.
"""

from typing import Dict, Any, Optional
from pathlib import Path


class Settings:
    """
    Centralized configuration management for AEGIS.
    
    Supports loading from files, environment variables, and defaults.
    """

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize settings with optional config file path.
        
        Args:
            config_path: Path to configuration file (YAML/JSON).
        """
        self.config_path = config_path
        self._config: Dict[str, Any] = {}
        self._load_defaults()

    def _load_defaults(self) -> None:
        """Load default configuration values."""
        self._config = {
            "debug": False,
            "log_level": "INFO",
            "max_workers": 4,
            "timeout": 30,
            "modules": {},
        }

    def load(self) -> "Settings":
        """
        Load configuration from file if specified.
        
        Returns:
            Self for method chaining.
        """
        if self.config_path and self.config_path.exists():
            self._load_from_file()
        return self

    def _load_from_file(self) -> None:
        """Load configuration from the specified file."""
        # TODO: Implement YAML/JSON parsing
        pass

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value by key.
        
        Args:
            key: Configuration key.
            default: Default value if key not found.
            
        Returns:
            Configuration value or default.
        """
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.
        
        Args:
            key: Configuration key.
            value: Value to set.
        """
        self._config[key] = value

    def update(self, config_dict: Dict[str, Any]) -> None:
        """
        Update multiple configuration values.
        
        Args:
            config_dict: Dictionary of configuration updates.
        """
        self._config.update(config_dict)

    @property
    def debug(self) -> bool:
        """Get debug mode setting."""
        return self._config.get("debug", False)

    @property
    def log_level(self) -> str:
        """Get logging level setting."""
        return self._config.get("log_level", "INFO")
