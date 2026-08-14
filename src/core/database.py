"""Database connection pool management using asyncpg."""

import asyncpg
from typing import Optional
from src.config.settings import DatabaseSettings

_pool: Optional[asyncpg.Pool] = None


async def init_db_pool(settings: DatabaseSettings) -> asyncpg.Pool:
    """
    Initialize the database connection pool.
    
    Args:
        settings: DatabaseSettings instance with connection URL.
        
    Returns:
        asyncpg.Pool instance.
    """
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(
            dsn=settings.database_url,
            min_size=2,
            max_size=10,
            command_timeout=60
        )
    return _pool


async def close_db_pool(pool: asyncpg.Pool) -> None:
    """
    Close the database connection pool.
    
    Args:
        pool: The asyncpg.Pool instance to close.
    """
    global _pool
    if pool:
        await pool.close()
        _pool = None


def get_pool(app_state) -> asyncpg.Pool:
    """
    Retrieve the pool from app state.
    
    Args:
        app_state: FastAPI app.state object.
        
    Returns:
        asyncpg.Pool instance or None if not initialized.
    """
    return getattr(app_state, 'pool', None)