"""
Base service class for the LIMS application.

This module provides a base service class with common CRUD operations
to eliminate duplicate code across different services.
"""

from typing import TypeVar, Generic, Type, List, Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel

from .exceptions import NotFoundError, DatabaseError, ValidationError
from .logging import LoggerMixin

# Type variables for generic service
T = TypeVar('T')  # SQLAlchemy model
CreateSchema = TypeVar('CreateSchema', bound=BaseModel)  # Create schema
UpdateSchema = TypeVar('UpdateSchema', bound=BaseModel)  # Update schema
ResponseSchema = TypeVar('ResponseSchema', bound=BaseModel)  # Response schema


class BaseService(Generic[T, CreateSchema, UpdateSchema, ResponseSchema], LoggerMixin):
    """
    Base service class with common CRUD operations.
    
    This class provides standard CRUD operations that can be inherited
    by specific service classes to eliminate duplicate code.
    """
    
    def __init__(self, model: Type[T]):
        """
        Initialize base service.
        
        Args:
            model: SQLAlchemy model class
        """
        self.model = model
    
    def get_all(
        self,
        db: Session,
        page: int = 1,
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
        order_direction: str = "asc"
    ) -> Tuple[List[ResponseSchema], int, int]:
        """
        Get all records with pagination and filtering.
        
        Args:
            db: Database session
            page: Page number (1-based)
            limit: Number of items per page
            filters: Optional filters to apply
            order_by: Field to order by
            order_direction: Order direction (asc/desc)
            
        Returns:
            Tuple of (items, total_count, total_pages)
        """
        try:
            query = db.query(self.model)
            
            # Apply filters
            if filters:
                query = self._apply_filters(query, filters)
            
            # Apply ordering
            if order_by:
                query = self._apply_ordering(query, order_by, order_direction)
            
            # Count total results
            total_count = query.count()
            total_pages = (total_count + limit - 1) // limit if total_count > 0 else 0
            
            # Apply pagination
            offset = (page - 1) * limit
            items = query.offset(offset).limit(limit).all()
            
            # Convert to response schemas
            response_items = [self._to_response_schema(item) for item in items]
            
            return response_items, total_count, total_pages
            
        except Exception as e:
            self.logger.error(f"Error in get_all: {str(e)}")
            raise DatabaseError(f"Failed to retrieve {self.model.__name__} records: {str(e)}")
    
    def get_by_id(
        self,
        db: Session,
        record_id: Any
    ) -> Optional[ResponseSchema]:
        """
        Get a record by ID.
        
        Args:
            db: Database session
            record_id: Record ID
            
        Returns:
            Record if found, None otherwise
        """
        try:
            item = db.query(self.model).filter(self.model.id == record_id).first()
            
            if not item:
                return None
            
            return self._to_response_schema(item)
            
        except Exception as e:
            self.logger.error(f"Error in get_by_id: {str(e)}")
            raise DatabaseError(f"Failed to retrieve {self.model.__name__}: {str(e)}")
    
    def create(
        self,
        db: Session,
        data: CreateSchema
    ) -> ResponseSchema:
        """
        Create a new record.
        
        Args:
            db: Database session
            data: Create data
            
        Returns:
            Created record
        """
        try:
            # Convert Pydantic model to dict
            item_data = data.dict(exclude_unset=True)
            
            # Create model instance
            item = self.model(**item_data)
            
            # Add to database
            db.add(item)
            db.commit()
            db.refresh(item)
            
            self.logger.info(f"Created {self.model.__name__} with ID: {item.id}")
            return self._to_response_schema(item)
            
        except Exception as e:
            db.rollback()
            self.logger.error(f"Error in create: {str(e)}")
            raise DatabaseError(f"Failed to create {self.model.__name__}: {str(e)}")
    
    def update(
        self,
        db: Session,
        record_id: Any,
        data: UpdateSchema
    ) -> Optional[ResponseSchema]:
        """
        Update a record.
        
        Args:
            db: Database session
            record_id: Record ID
            data: Update data
            
        Returns:
            Updated record if found, None otherwise
        """
        try:
            # Get existing record
            item = db.query(self.model).filter(self.model.id == record_id).first()
            
            if not item:
                return None
            
            # Convert Pydantic model to dict
            update_data = data.dict(exclude_unset=True)
            
            # Update fields
            for field, value in update_data.items():
                if hasattr(item, field):
                    setattr(item, field, value)
            
            db.commit()
            db.refresh(item)
            
            self.logger.info(f"Updated {self.model.__name__} with ID: {item.id}")
            return self._to_response_schema(item)
            
        except Exception as e:
            db.rollback()
            self.logger.error(f"Error in update: {str(e)}")
            raise DatabaseError(f"Failed to update {self.model.__name__}: {str(e)}")
    
    def delete(
        self,
        db: Session,
        record_id: Any
    ) -> bool:
        """
        Delete a record.
        
        Args:
            db: Database session
            record_id: Record ID
            
        Returns:
            True if deleted, False if not found
        """
        try:
            item = db.query(self.model).filter(self.model.id == record_id).first()
            
            if not item:
                return False
            
            db.delete(item)
            db.commit()
            
            self.logger.info(f"Deleted {self.model.__name__} with ID: {record_id}")
            return True
            
        except Exception as e:
            db.rollback()
            self.logger.error(f"Error in delete: {str(e)}")
            raise DatabaseError(f"Failed to delete {self.model.__name__}: {str(e)}")
    
    def exists(
        self,
        db: Session,
        record_id: Any
    ) -> bool:
        """
        Check if a record exists.
        
        Args:
            db: Database session
            record_id: Record ID
            
        Returns:
            True if exists, False otherwise
        """
        try:
            return db.query(self.model).filter(self.model.id == record_id).first() is not None
        except Exception as e:
            self.logger.error(f"Error in exists: {str(e)}")
            return False
    
    def count(
        self,
        db: Session,
        filters: Optional[Dict[str, Any]] = None
    ) -> int:
        """
        Count records with optional filters.
        
        Args:
            db: Database session
            filters: Optional filters to apply
            
        Returns:
            Number of records
        """
        try:
            query = db.query(self.model)
            
            if filters:
                query = self._apply_filters(query, filters)
            
            return query.count()
            
        except Exception as e:
            self.logger.error(f"Error in count: {str(e)}")
            raise DatabaseError(f"Failed to count {self.model.__name__} records: {str(e)}")
    
    def _apply_filters(self, query, filters: Dict[str, Any]):
        """Apply filters to query (to be overridden by subclasses)."""
        return query
    
    def _apply_ordering(self, query, order_by: str, order_direction: str):
        """Apply ordering to query (to be overridden by subclasses)."""
        if hasattr(self.model, order_by):
            field = getattr(self.model, order_by)
            if order_direction.lower() == "desc":
                return query.order_by(field.desc())
            else:
                return query.order_by(field.asc())
        return query
    
    def _to_response_schema(self, item: T) -> ResponseSchema:
        """Convert model to response schema (to be overridden by subclasses)."""
        raise NotImplementedError("Subclasses must implement _to_response_schema") 