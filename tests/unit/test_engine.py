"""
Unit tests for core module.
"""

import unittest
from src.core.engine import Engine


class TestEngine(unittest.TestCase):
    """Test cases for the Engine class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.engine = Engine()

    def test_initialization(self) -> None:
        """Test engine initialization."""
        self.assertFalse(self.engine.is_initialized())
        self.engine.initialize()
        self.assertTrue(self.engine.is_initialized())

    def test_double_initialization(self) -> None:
        """Test that double initialization is safe."""
        self.engine.initialize()
        self.engine.initialize()  # Should not raise
        self.assertTrue(self.engine.is_initialized())

    def test_module_registration(self) -> None:
        """Test module registration and retrieval."""
        mock_module = {"name": "test_module"}
        self.engine.register_module("test", mock_module)
        
        retrieved = self.engine.get_module("test")
        self.assertEqual(retrieved, mock_module)

    def test_module_not_found(self) -> None:
        """Test retrieving non-existent module."""
        result = self.engine.get_module("nonexistent")
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
