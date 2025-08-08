"""
Core exceptions module for standardized error handling across the application
"""
from typing import Any, Dict, Optional
from fastapi import HTTPException
import logging

# Set up logging
logger = logging.getLogger(__name__)

class LIMSException(HTTPException):
    """
    Base exception class for LIMS application
    All custom exceptions should inherit from this
    """
    def __init__(
        self,
        status_code: int,
        error_message: str,
        error_details: Optional[Dict[str, Any]] = None,
        log_message: Optional[str] = None
    ):
        self.status_code = status_code
        self.error_message = error_message
        self.error_details = error_details

        # Log the error
        if log_message:
            logger.error(log_message)
        else:
            logger.error(f"Error {status_code}: {error_message}")

        # Format the error response
        detail = {
            "data": None,
            "status": status_code,
            "success": False,
            "error": error_message
        }
        if error_details:
            detail["details"] = error_details

        super().__init__(status_code=status_code, detail=detail)

# Common validation exceptions
class ValidationError(LIMSException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            status_code=400,
            error_message=message,
            error_details=details,
            log_message=f"Validation error: {message}"
        )

class NotFoundError(LIMSException):
    def __init__(self, resource: str, resource_id: Any):
        super().__init__(
            status_code=404,
            error_message=f"{resource} with ID {resource_id} not found",
            log_message=f"{resource} not found: {resource_id}"
        )

class DatabaseError(LIMSException):
    def __init__(self, operation: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            status_code=500,
            error_message=f"Database error during {operation}",
            error_details=details,
            log_message=f"Database error during {operation}: {details if details else ''}"
        )

class DuplicateError(LIMSException):
    def __init__(self, resource: str, field: str, value: Any):
        super().__init__(
            status_code=409,
            error_message=f"{resource} with {field} '{value}' already exists",
            log_message=f"Duplicate {resource} {field}: {value}"
        )

class RelatedResourceError(LIMSException):
    def __init__(self, resource: str, related_resources: Dict[str, int]):
        message = f"Cannot delete {resource}. It has "
        details = []
        for name, count in related_resources.items():
            if count > 0:
                details.append(f"{count} {name}")
        message += " and ".join(details) + " associated with it."
        
        super().__init__(
            status_code=400,
            error_message=message,
            error_details=related_resources,
            log_message=f"Cannot delete {resource} due to related resources: {related_resources}"
        )

class AuthorizationError(LIMSException):
    def __init__(self, message: str):
        super().__init__(
            status_code=403,
            error_message=message,
            log_message=f"Authorization error: {message}"
        )

class UnexpectedError(LIMSException):
    def __init__(self, operation: str, error: Exception):
        super().__init__(
            status_code=500,
            error_message=f"An unexpected error occurred during {operation}",
            error_details={"original_error": str(error)},
            log_message=f"Unexpected error in {operation}: {str(error)}"
        )

# Input validation exceptions
class InvalidPageError(ValidationError):
    def __init__(self, page: int):
        super().__init__(f"Page number must be greater than 0, got {page}")

class InvalidLimitError(ValidationError):
    def __init__(self, limit: int):
        super().__init__(f"Limit must be between 1 and 100, got {limit}")

class InvalidFilterError(ValidationError):
    def __init__(self, filter_name: str, value: Any, valid_values: Optional[list] = None):
        message = f"Invalid value for filter '{filter_name}': {value}"
        if valid_values:
            message += f". Valid values are: {', '.join(map(str, valid_values))}"
        super().__init__(message)

class RequiredFieldError(ValidationError):
    def __init__(self, field_name: str):
        super().__init__(f"{field_name} is required")

class InvalidFormatError(ValidationError):
    def __init__(self, field_name: str, value: Any, expected_format: str):
        super().__init__(
            f"Invalid format for {field_name}: {value}. Expected format: {expected_format}"
        )

# Business logic exceptions
class InvalidStatusTransitionError(ValidationError):
    def __init__(self, resource: str, current_status: str, requested_status: str):
        super().__init__(
            f"Cannot transition {resource} from '{current_status}' to '{requested_status}'"
        )

class ResourceInUseError(ValidationError):
    def __init__(self, resource: str, usage_details: Dict[str, Any]):
        super().__init__(
            f"{resource} is currently in use",
            details=usage_details
        )

class InvalidOperationError(ValidationError):
    def __init__(self, operation: str, reason: str):
        super().__init__(
            f"Cannot perform operation '{operation}': {reason}"
        )
