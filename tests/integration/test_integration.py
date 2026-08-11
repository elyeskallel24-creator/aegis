"""
Integration tests for AEGIS.
"""

import unittest
from src.core.engine import Engine
from src.config.settings import Settings


class TestEngineWithSettings(unittest.TestCase):
    """Integration tests for Engine with Settings."""

    def test_engine_with_custom_settings(self) -> None:
        """Test engine initialization with custom settings."""
        settings = Settings()
        settings.set("debug", True)
        settings.set("log_level", "DEBUG")
        
        engine = Engine()
        engine.initialize()
        
        self.assertTrue(engine.is_initialized())

    def test_full_initialization_flow(self) -> None:
        """Test complete initialization workflow."""
        engine = Engine()
        
        # Pre-initialization checks
        self.assertFalse(engine.is_initialized())
        
        # Initialize
        engine.initialize()
        
        # Post-initialization checks
        self.assertTrue(engine.is_initialized())
        
        # Register a module
        engine.register_module("settings", Settings())
        
        # Verify module registration
        settings_module = engine.get_module("settings")
        self.assertIsInstance(settings_module, Settings)


if __name__ == "__main__":
    unittest.main()
