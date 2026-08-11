"""
Logging utilities for AEGIS.
"""

import logging
from typing import Optional


def get_logger(
    name: str,
    level: Optional[str] = None,
    format_string: Optional[str] = None,
) -> logging.Logger:
    """
    Get a configured logger instance.
    
    Args:
        name: Logger name (typically __name__).
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        format_string: Custom log format string.
        
    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger(name)
    
    if logger.handlers:
        return logger
    
    level = level or "INFO"
    format_string = format_string or (
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(format_string))
    
    logger.setLevel(getattr(logging, level.upper()))
    logger.addHandler(handler)
    
    return logger
