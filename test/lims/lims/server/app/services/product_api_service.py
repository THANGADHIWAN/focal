"""
Product API Service - Handles API-specific logic, validation, and response formatting
Separates API concerns from business logic
"""
from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import logging

from app.schemas import ApiResponse
from app.schemas.product import (
    ProductCreate, ProductUpdate, ProductResponse, 
    ProductListResponse, ProductSummary
)
from app.services.product_service import ProductService

# Set up logging
logger = logging.getLogger(__name__)


class ProductAPIService:
    """
    API Service layer for Product operations
    Handles request validation, error formatting, and response structure
    """

    @staticmethod
    def get_all_products(
        db: Session,
        page: int,
        limit: int,
        status: Optional[List[str]] = None,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Handle GET /products endpoint with validation and error handling
        """
        try:
            ProductAPIService._validate_pagination(page, limit)
            filters = ProductAPIService._build_filters(status, search)
            result = ProductService.get_all_products(db, page, limit, filters)
            return {
                "data": result,
                "status": 200,
                "success": True
            }
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error in get_all_products: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred while retrieving products"
            )

    @staticmethod
    def get_product_by_id(db: Session, product_id: int) -> Dict[str, Any]:
        """
        Handle GET /products/{product_id} endpoint
        """
        try:
            ProductAPIService._validate_product_id(product_id)
            product = ProductService.get_product_by_id(db, product_id)
            
            if not product:
                raise HTTPException(
                    status_code=404,
                    detail=f"Product with ID {product_id} not found"
                )
            
            return {
                "data": product,
                "status": 200,
                "success": True
            }
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error in get_product_by_id: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred while retrieving the product"
            )

    @staticmethod
    def create_product(db: Session, product_data: ProductCreate) -> Dict[str, Any]:
        """
        Handle POST /products endpoint
        """
        try:
            # API-level validation
            ProductAPIService._validate_product_create(product_data)
            product = ProductService.create_product(db, product_data)
            
            return {
                "data": product,
                "status": 201,
                "success": True
            }
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error in create_product: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred while creating the product"
            )

    @staticmethod
    def update_product(db: Session, product_id: int, product_data: ProductUpdate) -> Dict[str, Any]:
        """
        Handle PUT /products/{product_id} endpoint
        """
        try:
            ProductAPIService._validate_product_id(product_id)
            ProductAPIService._validate_product_update(product_data)
                
            product = ProductService.update_product(db, product_id, product_data)
            
            if not product:
                raise HTTPException(
                    status_code=404,
                    detail=f"Product with ID {product_id} not found"
                )
            
            return {
                "data": product,
                "status": 200,
                "success": True
            }
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error in update_product: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred while updating the product"
            )

    @staticmethod
    def delete_product(db: Session, product_id: int) -> Dict[str, Any]:
        """
        Handle DELETE /products/{product_id} endpoint
        """
        try:
            ProductAPIService._validate_product_id(product_id)
                
            success = ProductService.delete_product(db, product_id)
            
            if not success:
                raise HTTPException(
                    status_code=404,
                    detail=f"Product with ID {product_id} not found"
                )
            
            return {
                "data": {"message": f"Product {product_id} deleted successfully"},
                "status": 200,
                "success": True
            }
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error in delete_product: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred while deleting the product"
            )

    @staticmethod
    def get_product_samples(db: Session, product_id: int) -> Dict[str, Any]:
        """
        Handle GET /products/{product_id}/samples endpoint
        """
        try:
            # First check if product exists
            product = ProductService.get_product_by_id(db, product_id)
            if not product:
                raise HTTPException(
                    status_code=404,
                    detail=f"Product with ID {product_id} not found"
                )
            
            # Import here to avoid circular imports
            from app.services.sample_service import SampleService
            
            # Get samples filtered by product
            filters = {"product_id": product_id}
            samples, total, total_pages = SampleService.get_all_samples(db, 1, 100, filters)
            
            return {
                "data": {
                    "samples": samples,
                    "total": total,
                    "product": product
                },
                "status": 200,
                "success": True
            }
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in get_product_samples: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}"
            )

    @staticmethod
    def get_product_tests(db: Session, product_id: int) -> Dict[str, Any]:
        """
        Handle GET /products/{product_id}/tests endpoint
        """
        try:
            # First check if product exists
            product = ProductService.get_product_by_id(db, product_id)
            if not product:
                raise HTTPException(
                    status_code=404,
                    detail=f"Product with ID {product_id} not found"
                )
            
            # Import here to avoid circular imports
            from app.db.models.test import Test
            
            # Get tests filtered by product directly from database
            tests = db.query(Test).filter(Test.product_id == product_id).all()
            
            return {
                "data": {
                    "tests": tests,
                    "total": len(tests),
                    "product": product
                },
                "status": 200,
                "success": True
            }
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in get_product_tests: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}"
            )

    # Private validation methods
    @staticmethod
    def _validate_pagination(page: int, limit: int) -> None:
        """Validate pagination parameters"""
        if page < 1:
            raise HTTPException(status_code=400, detail="Page number must be greater than 0")
        if limit < 1 or limit > 100:
            raise HTTPException(status_code=400, detail="Limit must be between 1 and 100")

    @staticmethod
    def _validate_product_id(product_id: int) -> None:
        """Validate product ID"""
        if product_id <= 0:
            raise HTTPException(
                status_code=400,
                detail="Product ID must be a positive integer"
            )

    @staticmethod
    def _validate_product_create(product_data: ProductCreate) -> None:
        """Validate product creation data"""
        if not product_data.name or not product_data.name.strip():
            raise HTTPException(
                status_code=400,
                detail="Product name is required"
            )

    @staticmethod
    def _validate_product_update(product_data: ProductUpdate) -> None:
        """Validate product update data"""
        update_data = product_data.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=400,
                detail="No data provided for update"
            )

    @staticmethod
    def _build_filters(
        status: Optional[List[str]],
        search: Optional[str]
    ) -> Dict[str, Any]:
        """Build and validate filters"""
        filters = {}
        
        if status:
            # Validate status values
            valid_statuses = ["NOT_STARTED", "IN_PROGRESS", "COMPLETED"]
            for status_val in status:
                if status_val not in valid_statuses:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Invalid status '{status_val}'. Valid values are: {', '.join(valid_statuses)}"
                    )
            filters["status"] = status
            
        if search:
            if len(search.strip()) > 255:
                raise HTTPException(status_code=400, detail="Search term cannot exceed 255 characters")
            filters["search"] = search.strip()
            
        return filters