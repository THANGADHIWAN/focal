"""
Response formatting utilities to ensure consistent API responses
"""
from typing import Any, Dict, Optional
from fastapi.responses import JSONResponse


def format_success_response(
    data: Any = None,
    message: Optional[str] = None,
    status_code: int = 200
) -> Dict[str, Any]:
    """
    Format a successful API response
    
    Args:
        data: The response data
        message: Optional success message
        status_code: HTTP status code (default: 200)
    
    Returns:
        Dict with standardized response format
    """
    response = {
        "data": data,
        "status": status_code,
        "success": True,
        "error": None
    }
    if message:
        response["message"] = message
    return response


def format_paginated_response(
    items: list,
    total: int,
    page: int,
    page_size: int,
    total_pages: int,
    status_code: int = 200
) -> Dict[str, Any]:
    """
    Format a paginated API response
    
    Args:
        items: List of items for current page
        total: Total number of items
        page: Current page number
        page_size: Number of items per page
        total_pages: Total number of pages
        status_code: HTTP status code (default: 200)
    
    Returns:
        Dict with standardized paginated response format
    """
    return format_success_response(
        data={
            "items": items,
            "total": total,
            "page": page,
            "size": page_size,
            "pages": total_pages
        },
        status_code=status_code
    )


def format_error_response(error: Exception) -> JSONResponse:
    """
    Format an error response based on the exception type
    
    Args:
        error: The exception that occurred
    
    Returns:
        JSONResponse with standardized error format
    """
    # Handle our custom exceptions
    if hasattr(error, 'detail') and isinstance(error.detail, dict):
        return JSONResponse(
            status_code=getattr(error, 'status_code', 500),
            content=error.detail
        )
    
    # Handle other exceptions
    return JSONResponse(
        status_code=500,
        content={
            "data": None,
            "status": 500,
            "success": False,
            "error": "An unexpected error occurred",
            "details": str(error)
        }
    )
