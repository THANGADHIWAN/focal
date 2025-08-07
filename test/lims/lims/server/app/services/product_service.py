"""
Product service for the Sample Management API
"""
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import func, or_, and_, desc
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime
from fastapi import HTTPException
import logging
import uuid

from app.db.models.product import Product
from app.db.models.sample import Sample
from app.db.models.test import Test
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse, ProductListResponse, ProductSummary
from app.utils.constants import ProductStatus

# Set up logging
logger = logging.getLogger(__name__)


class ProductService:
    @staticmethod
    def _validate_pagination(page: int, limit: int) -> None:
        """Validate pagination parameters"""
        if page < 1:
            raise ValueError("Page number must be greater than 0")
        if limit < 1 or limit > 100:
            raise ValueError("Limit must be between 1 and 100")

    @staticmethod
    def _validate_filters(filters: Optional[Dict[str, Any]]) -> None:
        """Validate filter parameters"""
        if not filters:
            return
            
        if filters.get("status"):
            valid_statuses = ["NOT_STARTED", "IN_PROGRESS", "COMPLETED"]
            status_list = filters["status"] if isinstance(filters["status"], list) else [filters["status"]]
            for status_val in status_list:
                if status_val not in valid_statuses:
                    raise ValueError(f"Invalid status '{status_val}'. Valid values are: {', '.join(valid_statuses)}")
                    
        if filters.get("search"):
            if len(filters["search"].strip()) > 255:
                raise ValueError("Search term cannot exceed 255 characters")

    @staticmethod
    def get_all_products(
        db: Session,
        page: int,
        limit: int,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Get all products with pagination and filtering options
        Returns API response format with data and status
        """
        try:
            # Validate pagination and filters
            ProductService._validate_pagination(page, limit)
            ProductService._validate_filters(filters)
            print("qwerty")
            
            # Base query
            query = db.query(Product)
            
            # Apply filters if provided
            if filters:
                # Status filter
                if filters.get("status"):
                    if isinstance(filters["status"], list):
                        status_values = [ProductStatus(status) for status in filters["status"] if status]
                        if status_values:
                            query = query.filter(Product.status.in_(status_values))
                    else:
                        query = query.filter(Product.status == ProductStatus(filters["status"]))
                
                # Search filter (name, description, product_code)
                if filters.get("search"):
                    search_term = f"%{filters['search']}%"
                    query = query.filter(
                        or_(
                            Product.product_name.ilike(search_term),
                            Product.description.ilike(search_term)
                        )
                    )
                
                # Date range filters
                if filters.get("created_from"):
                    query = query.filter(Product.created_at >= filters["created_from"])
                
                if filters.get("created_to"):
                    query = query.filter(Product.created_at <= filters["created_to"])
            
            # Order by created date (newest first)
            query = query.order_by(desc(Product.created_at))
            
            # Get total count before pagination
            total = query.count()
            
            # Apply pagination
            offset = (page - 1) * limit
            products = query.offset(offset).limit(limit).all()
            
            # Calculate total pages
            total_pages = (total + limit - 1) // limit
            
            # Get counts for all products in a single query using subqueries
            sample_counts = db.query(
                Sample.product_id,
                func.count(Sample.id).label('sample_count')
            ).group_by(Sample.product_id).subquery()
            
            test_counts = db.query(
                Test.product_id,
                func.count(Test.id).label('test_count')
            ).group_by(Test.product_id).subquery()
            
            # Convert to response objects with related counts
            product_responses = []
            for product in products:
                # Get counts from the subquery results
                sample_count = db.query(sample_counts.c.sample_count)\
                    .filter(sample_counts.c.product_id == product.id).scalar() or 0
                test_count = db.query(test_counts.c.test_count)\
                    .filter(test_counts.c.product_id == product.id).scalar() or 0
                
                product_data = ProductResponse.model_validate(product)
                product_data.sample_count = sample_count
                product_data.test_count = test_count
                product_responses.append(product_data)
            
            response_data = ProductListResponse(
                items=product_responses,
                total=total,
                page=page,
                size=limit,
                pages=total_pages
            )
            
            return {
                "data": response_data,
                "status": 200,
                "success": True,
                "error": None
            }
            
        except ValueError as e:
            logger.error(f"Validation error in get_all_products: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail={
                    "data": None,
                    "status": 400,
                    "success": False,
                    "error": f"Invalid request parameters: {str(e)}"
                }
            )
        except Exception as e:
            logger.error(f"Unexpected error in get_all_products: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail={
                    "data": None,
                    "status": 500,
                    "success": False,
                    "error": "An unexpected error occurred while retrieving products"
                }
            )
    
    @staticmethod
    def get_product_by_id(db: Session, product_id: int) -> Optional[ProductResponse]:
        """
        Get a specific product by ID, including sample and test counts
        """
        try:
            # Fetch the product
            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                raise HTTPException(
                    status_code=404,
                    detail={
                        "data": None,
                        "status": 404,
                        "success": False,
                        "error": f"Product with ID {product_id} not found"
                    }
                )

            # Get sample and test counts via subqueries to avoid alias conflict
            sample_count = db.query(func.count(Sample.id)).filter(Sample.product_id == product_id).scalar()
            test_count = db.query(func.count(Test.id)).filter(Test.product_id == product_id).scalar()

            # Validate and augment the product response
            product_data = ProductResponse.model_validate(product)
            product_data.sample_count = sample_count or 0
            product_data.test_count = test_count or 0

            return product_data

        except ValueError as e:
            logger.error(f"Validation error in get_product_by_id: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail={
                    "data": None,
                    "status": 400,
                    "success": False,
                    "error": f"Invalid product ID: {str(e)}"
                }
            )
        except Exception as e:
            logger.error(f"Unexpected error in get_product_by_id: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail={
                    "data": None,
                    "status": 500,
                    "success": False,
                    "error": "An unexpected error occurred while retrieving the product"
                }
            )

    
    @staticmethod
    def create_product(db: Session, product_data: ProductCreate) -> ProductResponse:
        """
        Create a new product
        """
        try:
            # Validate input data
            if not product_data.product_name or not product_data.product_name.strip():
                raise HTTPException(
                    status_code=400,
                    detail={
                        "data": None,
                        "status": 400,
                        "success": False,
                        "error": "Product name is required"
                    }
                )
            
            if len(product_data.product_name.strip()) > 100:
                raise HTTPException(
                    status_code=400,
                    detail={
                        "data": None,
                        "status": 400,
                        "success": False,
                        "error": "Product name cannot exceed 100 characters"
                    }
                )
    
            
            # Create product instance
            product = Product(
                product_name=product_data.product_name.strip(),
                description=product_data.description.strip() if product_data.description else None,
                status=product_data.status
            )
            
            db.add(product)
            db.commit()
            db.refresh(product)
            
            # Return response with initial counts
            product_response = ProductResponse.model_validate(product)
            product_response.sample_count = 0
            product_response.test_count = 0
            
            logger.info(f"Created product {product.product_name}")
            return product_response
            
        except ValueError as e:
            db.rollback()
            logger.error(f"Validation error in create_product: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail={
                    "data": None,
                    "status": 400,
                    "success": False,
                    "error": f"Invalid product data: {str(e)}"
                }
            )
        except Exception as e:
            db.rollback()
            logger.error(f"Unexpected error in create_product: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail={
                    "data": None,
                    "status": 500,
                    "success": False,
                    "error": "An unexpected error occurred while creating the product"
                }
            )

    @staticmethod
    def update_product(
        db: Session, 
        product_id: int, 
        product_data: ProductUpdate
    ) -> Optional[ProductResponse]:
        """
        Update an existing product
        """
        try:
            if product_id <= 0:
                raise HTTPException(
                    status_code=400,
                    detail={
                        "data": None,
                        "status": 400,
                        "success": False,
                        "error": "Product ID must be a positive integer"
                    }
                )

            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                raise HTTPException(
                    status_code=404,
                    detail={
                        "data": None,
                        "status": 404,
                        "success": False,
                        "error": f"Product with ID {product_id} not found"
                    }
                )

            update_data = product_data.model_dump(exclude_unset=True)

            if 'product_name' in update_data:
                name = update_data['product_name'].strip()
                if not name:
                    raise ValueError("Product name cannot be empty")
                if len(name) > 100:
                    raise ValueError("Product name cannot exceed 100 characters")
                product.product_name = name

            if 'description' in update_data:
                desc = update_data['description']
                if desc:
                    product.description = desc.strip()
                else:
                    product.description = None

            # Apply all remaining fields safely
            for field, value in update_data.items():
                if field not in ['product_name', 'description']:
                    setattr(product, field, value)

            product.updated_at = datetime.utcnow()

            db.commit()
            db.refresh(product)

            sample_count = db.query(func.count(Sample.id)).filter(Sample.product_id == product.id).scalar()
            test_count = db.query(func.count(Test.id)).filter(Test.product_id == product.id).scalar()

            product_response = ProductResponse.model_validate(product)
            product_response.sample_count = sample_count or 0
            product_response.test_count = test_count or 0

            logger.info(f"Updated product {product.product_name}")
            return product_response

        except ValueError as e:
            db.rollback()
            logger.error(f"Validation error in update_product: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail={
                    "status": 400,
                    "success": False,
                    "message": f"Invalid product data: {str(e)}"
                }
            )
        except Exception as e:
            db.rollback()
            logger.error(f"Unexpected error in update_product: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail={
                    "status": 500,
                    "success": False,
                    "message": "An unexpected error occurred while updating product"
                }
            )

    @staticmethod
    def delete_product(db: Session, product_id: int) -> bool:
        """
        Delete a product by ID
        """
        try:

            product = db.query(Product).filter(Product.id == product_id).first()
            
            if not product:
                raise HTTPException(
                    status_code=404,
                    detail={
                        "data": None,
                        "status": 404,
                        "success": False,
                        "error": f"Product with ID {product_id} not found"
                    }
                )
            
            # Check if product has associated samples or tests
            sample_count = db.query(func.count(Sample.id)).filter(Sample.product_id == product.id).scalar()
            test_count = db.query(func.count(Test.id)).filter(Test.product_id == product.id).scalar()
            
            if sample_count > 0 or test_count > 0:
                raise HTTPException(
                    status_code=400,
                    detail={
                        "data": None,
                        "status": 400,
                        "success": False,
                        "error": f"Cannot delete product {product.product_name}. It has {sample_count} samples and {test_count} tests associated with it."
                    }
                )
            
            db.delete(product)
            db.commit()
            
            logger.info(f"Deleted product {product.product_name}")
            return True
            
        except HTTPException:
            raise
        except ValueError as e:
            db.rollback()
            logger.error(f"Validation error in delete_product: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail={
                    "data": None,
                    "status": 400,
                    "success": False,
                    "error": f"Invalid product ID: {str(e)}"
                }
            )
        except Exception as e:
            db.rollback()
            logger.error(f"Unexpected error in delete_product: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail={
                    "data": None,
                    "status": 500,
                    "success": False,
                    "error": "An unexpected error occurred while deleting the product"
                }
            )
    
    @staticmethod
    def get_product_summaries(db: Session) -> List[ProductSummary]:
        """
        Get all products as summaries (for dropdowns, etc.)
        """
        try:
            products = db.query(Product).order_by(Product.name).all()
            return [ProductSummary.model_validate(product) for product in products]
            
        except Exception as e:
            logger.error(f"Unexpected error in get_product_summaries: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail={
                    "data": None,
                    "status": 500,
                    "success": False,
                    "error": "An unexpected error occurred while retrieving product summaries"
                }
            )
    
    @staticmethod
    def _generate_product_code(db: Session) -> str:
        """
        Generate a unique product code
        """
        # Get the count of existing products to determine the next number
        count = db.query(func.count(Product.id)).scalar()
        next_number = count + 1
        
        # Generate code in format PRD-XXX
        product_code = f"PRD-{str(next_number).zfill(3)}"
        
        # Check if code already exists (edge case)
        while db.query(Product).filter(Product.product_code == product_code).first():
            next_number += 1
            product_code = f"PRD-{str(next_number).zfill(3)}"
        
        return product_code