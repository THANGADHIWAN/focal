"""
Common base schemas for the Sample Management API
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    limit: int = Field(10, ge=1, le=100)


class PaginatedResponse(BaseModel):
    data: List[Any]
    total_count: int
    total_pages: int
    current_page: int
    page_size: int
    has_more: bool


class ApiResponse(BaseModel):
    data: Optional[Any] = None
    message: Optional[str] = None
    status: int
    success: bool
