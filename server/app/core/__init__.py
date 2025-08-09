"""
Core module for the LIMS application.

This module contains shared utilities, base classes, and common functionality
used throughout the application.
"""

from .config import Settings
from .exceptions import LIMSException, ValidationError, NotFoundError, DatabaseError
from .logging import setup_logging
from .database import get_db, DatabaseManager
from .base_service import BaseService
from .base_router import BaseRouter

__all__ = [
    "Settings",
    "LIMSException",
    "ValidationError", 
    "NotFoundError",
    "DatabaseError",
    "setup_logging",
    "get_db",
    "DatabaseManager",
    "BaseService",
    "BaseRouter"
] 