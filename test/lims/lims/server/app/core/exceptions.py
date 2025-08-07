"""
Custom exceptions for the LIMS application.

This module provides centralized exception handling with custom exceptions
for different types of errors that can occur in the application.
"""

from typing import Any, Dict, Optional
from fastapi import HTTPException


class LIMSException(Exception):
    """Base exception for LIMS application."""
    
    def __init__(
        self, 
        message: str, 
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(LIMSException):
    """Exception raised when data validation fails."""
    
    def __init__(self, message: str, field: Optional[str] = None, value: Any = None):
        details = {}
        if field:
            details["field"] = field
        if value is not None:
            details["value"] = value
        
        super().__init__(
            message=message,
            status_code=422,
            details=details
        )


class NotFoundError(LIMSException):
    """Exception raised when a requested resource is not found."""
    
    def __init__(self, resource_type: str, resource_id: Any):
        super().__init__(
            message=f"{resource_type} with id {resource_id} not found",
            status_code=404,
            details={"resource_type": resource_type, "resource_id": resource_id}
        )


class DatabaseError(LIMSException):
    """Exception raised when database operations fail."""
    
    def __init__(self, message: str, operation: Optional[str] = None):
        details = {}
        if operation:
            details["operation"] = operation
        
        super().__init__(
            message=message,
            status_code=500,
            details=details
        )


class AuthenticationError(LIMSException):
    """Exception raised when authentication fails."""
    
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            message=message,
            status_code=401
        )


class AuthorizationError(LIMSException):
    """Exception raised when authorization fails."""
    
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(
            message=message,
            status_code=403
        )


class ConflictError(LIMSException):
    """Exception raised when there's a conflict with existing data."""
    
    def __init__(self, message: str, resource_type: Optional[str] = None):
        details = {}
        if resource_type:
            details["resource_type"] = resource_type
        
        super().__init__(
            message=message,
            status_code=409,
            details=details
        )


def lims_exception_handler(exc: LIMSException) -> HTTPException:
    """Convert LIMSException to FastAPI HTTPException."""
    return HTTPException(
        status_code=exc.status_code,
        detail={
            "message": exc.message,
            "details": exc.details
        }
    ) 