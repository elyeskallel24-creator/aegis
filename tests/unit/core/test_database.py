"""Unit tests for the database connection pool."""

import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from src.core.database import init_db_pool, close_db_pool, get_pool
from src.config.settings import DatabaseSettings


class TestDatabasePool:
    """Tests for database pool lifecycle management."""

    @pytest.mark.asyncio
    async def test_init_db_pool(self):
        """Test that init_db_pool creates a pool with correct settings."""
        settings = DatabaseSettings()
        
        # Mock asyncpg.create_pool to return an awaitable
        mock_pool = AsyncMock()
        
        async def mock_create_pool(*args, **kwargs):
            return mock_pool
        
        with patch('src.core.database.asyncpg.create_pool', side_effect=mock_create_pool) as mock_create:
            pool = await init_db_pool(settings)
            
            # Verify create_pool was called with correct parameters
            mock_create.assert_called_once()
            call_args = mock_create.call_args
            assert call_args[1]['dsn'] == settings.database_url
            assert call_args[1]['min_size'] == 2
            assert call_args[1]['max_size'] == 10
            assert call_args[1]['command_timeout'] == 60
            
            # Verify pool is returned
            assert pool == mock_pool

    @pytest.mark.asyncio
    async def test_init_db_pool_reuses_existing(self):
        """Test that init_db_pool returns existing pool if already initialized."""
        settings = DatabaseSettings()
        mock_pool = AsyncMock()
        
        async def mock_create_pool(*args, **kwargs):
            return mock_pool
        
        with patch('src.core.database.asyncpg.create_pool', side_effect=mock_create_pool):
            # First call creates pool
            pool1 = await init_db_pool(settings)
            # Second call should reuse
            pool2 = await init_db_pool(settings)
            
            assert pool1 == pool2

    @pytest.mark.asyncio
    async def test_close_db_pool(self):
        """Test that close_db_pool closes the pool properly."""
        mock_pool = AsyncMock()
        
        # Set global _pool
        from src.core import database
        database._pool = mock_pool
        
        await close_db_pool(mock_pool)
        
        # Verify pool.close() was called
        mock_pool.close.assert_called_once()
        # Verify global _pool is reset
        assert database._pool is None

    @pytest.mark.asyncio
    async def test_close_db_pool_with_none(self):
        """Test that close_db_pool handles None gracefully."""
        # Should not raise any exception
        await close_db_pool(None)

    def test_get_pool_from_app_state(self):
        """Test that get_pool retrieves pool from app state."""
        # Create mock app state
        class MockAppState:
            pool = "test_pool"
        
        app_state = MockAppState()
        pool = get_pool(app_state)
        
        assert pool == "test_pool"

    def test_get_pool_no_pool(self):
        """Test that get_pool returns None when no pool exists."""
        class MockAppState:
            pass
        
        app_state = MockAppState()
        pool = get_pool(app_state)
        
        assert pool is None