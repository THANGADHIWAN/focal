"""
Product schemas for request/response serialization
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from app.utils.constants import ProductStatus


class ProductBase(BaseModel):
    """Base product schema with common fields"""
    product_name: str = Field(..., description="Product name", max_length=100)
    description: Optional[str] = Field(None, description="Product description")
    status: ProductStatus = Field(default=ProductStatus.NOT_STARTED, description="Product status")


class ProductCreate(ProductBase):
    """Schema for creating a new product"""
    pass


class ProductUpdate(BaseModel):
    """Schema for updating an existing product"""
    product_name: Optional[str] = Field(None, description="Product name", max_length=100)
    description: Optional[str] = Field(None, description="Product description")
    status: Optional[ProductStatus] = Field(None, description="Product status")


class ProductResponse(ProductBase):
    """Schema for product response with additional computed fields"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="Product ID")
    created_at: datetime = Field(..., description="Product creation timestamp")
    updated_at: datetime = Field(..., description="Product last update timestamp")
    
    # Related counts (computed fields)
    sample_count: Optional[int] = Field(None, description="Number of samples associated with this product")
    test_count: Optional[int] = Field(None, description="Number of tests associated with this product")


class ProductListResponse(BaseModel):
    """Schema for paginated product list response"""
    items: List[ProductResponse] = Field(..., description="List of products")
    total: int = Field(..., description="Total number of products")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Page size")
    pages: int = Field(..., description="Total number of pages")


class ProductSummary(BaseModel):
    """Schema for product summary with minimal information"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="Product ID")
    product_code: str = Field(..., description="Unique product code")
    name: str = Field(..., description="Product name")
    status: ProductStatus = Field(..., description="Product status")