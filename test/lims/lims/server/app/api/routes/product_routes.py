"""
Product routes for the Sample Management API
Clean route definitions that delegate to API service layer
"""
from fastapi import APIRouter, Depends, Query, Path, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.database import get_db
from app.api.schemas import ApiResponse
from app.api.schemas.product import ProductCreate, ProductUpdate
from app.services.product_service import ProductService
from app.services.sample_service import SampleService
from app.services.test_service import TestService

# Create router
router = APIRouter(
    prefix="/products",
    tags=["products"]
)


@router.get("", response_model=ApiResponse)
def get_all_products(
    page: int = Query(..., ge=1, description="Page number", example=1 ),
    limit: int = Query(..., ge=1, le=100, description="Number of items per page", example=10),
    status: Optional[List[str]] = Query(None, description="Filter by product statuses"),
    search: Optional[str] = Query(None, description="Search term for product name, description, or product code"),
    db: Session = Depends(get_db)
):
    """Get all products with pagination and filtering options"""
    filters = {}
    if status:
        filters["status"] = status
    if search:
        filters["search"] = search
        
    return ProductService.get_all_products(
        db=db,
        page=page,
        limit=limit,
        filters=filters
    )


@router.get("/{product_id}", response_model=ApiResponse)
def get_product_by_id(
    product_id: int = Path(..., description="The ID of the product"),
    db: Session = Depends(get_db)
):
    """Get a specific product by ID"""
    result = ProductService.get_product_by_id(db=db, product_id=product_id)
    return {
        "data": result,
        "status": 200,
        "success": True,
        "error": None
    }


@router.post("", response_model=ApiResponse)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db)
):
    """Create a new product"""
    result = ProductService.create_product(db=db, product_data=product_data)
    return {
        "data": result,
        "status": 201,
        "success": True,
        "error": None
    }


@router.put("/{product_id}", response_model=ApiResponse)
def update_product(
    product_id: int = Path(..., description="The ID of the product"),
    product_data: ProductUpdate = ...,
    db: Session = Depends(get_db)
):
    """Update an existing product"""
    result = ProductService.update_product(db=db, product_id=product_id, product_data=product_data)
    return {
        "data": result,
        "status": 201,
        "success": True,
        "error": None
    }


@router.delete("/{product_id}", response_model=ApiResponse)
def delete_product(
    product_id: int = Path(..., description="The ID of the product"),
    db: Session = Depends(get_db)
):
    """Delete a product by ID"""
    result = ProductService.delete_product(db=db, product_id=product_id)
    return {
        "data": {"message": f"Product {product_id} deleted successfully"},
        "status": 200,
        "success": True,
        "error": None
    }


@router.get("/{product_id}/samples", response_model=ApiResponse)
def get_product_samples(
    product_id: int = Path(..., description="The ID of the product"),
    db: Session = Depends(get_db)
):
    """Get all samples associated with a product"""
    # First check if product exists
    product = ProductService.get_product_by_id(db=db, product_id=product_id)
    
    # Get samples filtered by product
    samples = SampleService.get_samples_by_product_id(db=db, product_id=product_id)
    
    return {
        "data": {
            "samples": samples,
            "product": product
        },
        "status": 200,
        "success": True,
        "error": None
    }


@router.get("/{product_id}/tests", response_model=ApiResponse)
def get_product_tests(
    product_id: int = Path(..., description="The ID of the product"),
    db: Session = Depends(get_db)
):
    """Get all tests associated with a product"""
    # First check if product exists
    product = ProductService.get_product_by_id(db=db, product_id=product_id)
    
    # Get tests filtered by product
    tests = TestService.get_tests_by_product_id(db=db, product_id=product_id)
    
    return {
        "data": {
            "tests": tests,
            "product": product
        },
        "status": 204,
        "success": True,
        "error": None
    }