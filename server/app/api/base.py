"""
Base router class for the LIMS application.

This module provides a base router class with common CRUD endpoints
to eliminate duplicate code across different route modules.
"""

from typing import TypeVar, Generic, Type, List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session
from pydantic import BaseModel

from .database import get_db
from .exceptions import LIMSException, NotFoundError
from .logging import LoggerMixin

# Type variables for generic router
T = TypeVar('T')  # SQLAlchemy model
CreateSchema = TypeVar('CreateSchema', bound=BaseModel)  # Create schema
UpdateSchema = TypeVar('UpdateSchema', bound=BaseModel)  # Update schema
ResponseSchema = TypeVar('ResponseSchema', bound=BaseModel)  # Response schema


class BaseRouter(Generic[T, CreateSchema, UpdateSchema, ResponseSchema], LoggerMixin):
    """
    Base router class with common CRUD endpoints.
    
    This class provides standard CRUD endpoints that can be inherited
    by specific router classes to eliminate duplicate code.
    """
    
    def __init__(
        self,
        prefix: str,
        tags: List[str],
        service_class: Type,
        create_schema: Type[CreateSchema],
        update_schema: Type[UpdateSchema],
        response_schema: Type[ResponseSchema],
        model_name: str = "item"
    ):
        """
        Initialize base router.
        
        Args:
            prefix: API route prefix
            tags: OpenAPI tags
            service_class: Service class to use
            create_schema: Create schema class
            update_schema: Update schema class
            response_schema: Response schema class
            model_name: Human-readable model name for error messages
        """
        self.prefix = prefix
        self.tags = tags
        self.service_class = service_class
        self.create_schema = create_schema
        self.update_schema = update_schema
        self.response_schema = response_schema
        self.model_name = model_name
        
        # Create router
        self.router = APIRouter(
            prefix=prefix,
            tags=tags,
            responses={404: {"description": "Not found"}}
        )
        
        # Register routes
        self._register_routes()
    
    def _register_routes(self) -> None:
        """Register all CRUD routes."""
        
        @self.router.get("", response_model=Dict[str, Any])
        def get_all_items(
            page: int = Query(1, ge=1, description="Page number"),
            limit: int = Query(10, ge=1, le=100, description="Number of items per page"),
            order_by: Optional[str] = Query(None, description="Field to order by"),
            order_direction: str = Query("asc", description="Order direction (asc/desc)"),
            db: Session = Depends(get_db)
        ):
            """Get all items with pagination and filtering."""
            try:
                service = self.service_class()
                items, total_count, total_pages = service.get_all(
                    db=db,
                    page=page,
                    limit=limit,
                    order_by=order_by,
                    order_direction=order_direction
                )
                
                return {
                    "data": {
                        "items": items,
                        "total_count": total_count,
                        "total_pages": total_pages,
                        "current_page": page,
                        "page_size": limit,
                        "has_more": page < total_pages
                    },
                    "status": 200,
                    "success": True
                }
            except LIMSException as e:
                raise HTTPException(status_code=e.status_code, detail=e.message)
            except Exception as e:
                self.logger.error(f"Error in get_all_items: {str(e)}")
                raise HTTPException(status_code=500, detail="Internal server error")
        
        @self.router.get("/{item_id}", response_model=Dict[str, Any])
        def get_item_by_id(
            item_id: int,
            db: Session = Depends(get_db)
        ):
            """Get item by ID."""
            try:
                service = self.service_class()
                item = service.get_by_id(db=db, record_id=item_id)
                
                if not item:
                    raise NotFoundError(self.model_name, item_id)
                
                return {
                    "data": item,
                    "status": 200,
                    "success": True
                }
            except NotFoundError as e:
                raise HTTPException(status_code=404, detail=e.message)
            except LIMSException as e:
                raise HTTPException(status_code=e.status_code, detail=e.message)
            except Exception as e:
                self.logger.error(f"Error in get_item_by_id: {str(e)}")
                raise HTTPException(status_code=500, detail="Internal server error")
        
        @self.router.post("", response_model=Dict[str, Any])
        def create_item(
            item_data: self.create_schema,
            db: Session = Depends(get_db)
        ):
            """Create a new item."""
            try:
                service = self.service_class()
                item = service.create(db=db, data=item_data)
                
                return {
                    "data": item,
                    "status": 201,
                    "success": True
                }
            except LIMSException as e:
                raise HTTPException(status_code=e.status_code, detail=e.message)
            except Exception as e:
                self.logger.error(f"Error in create_item: {str(e)}")
                raise HTTPException(status_code=500, detail="Internal server error")
        
        @self.router.patch("/{item_id}", response_model=Dict[str, Any])
        def update_item(
            item_id: int,
            item_data: self.update_schema,
            db: Session = Depends(get_db)
        ):
            """Update an item."""
            try:
                service = self.service_class()
                item = service.update(db=db, record_id=item_id, data=item_data)
                
                if not item:
                    raise NotFoundError(self.model_name, item_id)
                
                return {
                    "data": item,
                    "status": 200,
                    "success": True
                }
            except NotFoundError as e:
                raise HTTPException(status_code=404, detail=e.message)
            except LIMSException as e:
                raise HTTPException(status_code=e.status_code, detail=e.message)
            except Exception as e:
                self.logger.error(f"Error in update_item: {str(e)}")
                raise HTTPException(status_code=500, detail="Internal server error")
        
        @self.router.delete("/{item_id}", response_model=Dict[str, Any])
        def delete_item(
            item_id: int,
            db: Session = Depends(get_db)
        ):
            """Delete an item."""
            try:
                service = self.service_class()
                deleted = service.delete(db=db, record_id=item_id)
                
                if not deleted:
                    raise NotFoundError(self.model_name, item_id)
                
                return {
                    "data": {"message": f"{self.model_name} deleted successfully"},
                    "status": 200,
                    "success": True
                }
            except NotFoundError as e:
                raise HTTPException(status_code=404, detail=e.message)
            except LIMSException as e:
                raise HTTPException(status_code=e.status_code, detail=e.message)
            except Exception as e:
                self.logger.error(f"Error in delete_item: {str(e)}")
                raise HTTPException(status_code=500, detail="Internal server error")
    
    def get_router(self) -> APIRouter:
        """Get the configured router."""
        return self.router 