#!/usr/bin/env python3
"""
Setup script for AEGIS development environment.
"""

import subprocess
import sys
from pathlib import Path


def run_command(command: list[str], description: str) -> bool:
    """Run a command and return success status."""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        if e.stderr:
            print(e.stderr)
        return False


def main() -> int:
    """Main setup function."""
    print("AEGIS Development Environment Setup")
    print("=" * 60)
    
    # Check Python version
    print(f"\nPython version: {sys.version}")
    if sys.version_info < (3, 9):
        print("ERROR: Python 3.9+ is required")
        return 1
    
    # Install development dependencies
    if not run_command(
        [sys.executable, "-m", "pip", "install", "-e", ".[dev]"],
        "Installing AEGIS with development dependencies"
    ):
        print("WARNING: Failed to install dependencies")
    
    # Verify installation
    print("\nVerifying installation...")
    try:
        from src.core import Engine
        print("✓ Core module imported successfully")
        
        engine = Engine()
        print("✓ Engine class instantiated successfully")
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return 1
    
    print("\n" + "=" * 60)
    print("Setup complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("  - Run tests: pytest")
    print("  - Format code: black src/ tests/")
    print("  - Lint code: ruff check src/ tests/")
    print("  - Type check: mypy src/")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
