"""
Database management for the LIMS application.

This module provides centralized database connection management, session handling,
and database utilities with proper error handling and connection pooling.
"""

from contextlib import contextmanager
from typing import Generator, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import QueuePool

from .config import settings
from .exceptions import DatabaseError
from .logging import get_logger

logger = get_logger(__name__)


class DatabaseManager:
    """Database connection manager with connection pooling and error handling."""
    
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self._initialized = False
    
    def initialize(self) -> None:
        """Initialize database connection and session factory."""
        try:
            # Create engine with connection pooling
            self.engine = create_engine(
                settings.database_url,
                poolclass=QueuePool,
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True,
                pool_recycle=3600,  # Recycle connections every hour
                echo=settings.debug
            )
            
            # Create session factory
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            
            self._initialized = True
            logger.info("Database connection initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize database: {str(e)}")
            raise DatabaseError(f"Database initialization failed: {str(e)}")
    
    def get_session(self) -> Session:
        """Get a new database session."""
        if not self._initialized:
            self.initialize()
        
        return self.SessionLocal()
    
    @contextmanager
    def get_db_session(self) -> Generator[Session, None, None]:
        """Context manager for database sessions with automatic cleanup."""
        session = self.get_session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {str(e)}")
            raise
        finally:
            session.close()
    
    def test_connection(self) -> bool:
        """Test database connection."""
        try:
            with self.get_db_session() as session:
                session.execute(text("SELECT 1"))
                return True
        except Exception as e:
            logger.error(f"Database connection test failed: {str(e)}")
            return False
    
    def close(self) -> None:
        """Close all database connections."""
        if self.engine:
            self.engine.dispose()
            logger.info("Database connections closed")


# Global database manager instance
db_manager = DatabaseManager()


def get_db() -> Session:
    """
    Dependency function to get database session.
    
    Returns:
        Database session
    """
    return db_manager.get_session()


def get_db_session() -> Session:
    """Get a database session (use with context manager)."""
    return db_manager.get_session()


def test_database_connection() -> bool:
    """Test if database connection is working."""
    return db_manager.test_connection()


def initialize_database() -> None:
    """Initialize database connection."""
    db_manager.initialize()


def close_database() -> None:
    """Close database connections."""
    db_manager.close() 