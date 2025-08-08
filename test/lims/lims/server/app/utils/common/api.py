"""
Helper functions for API request/response handling
"""
from typing import List, Type, TypeVar, Optional, Any, Union
from enum import Enum

T = TypeVar('T', bound=Enum)

def ensure_enum_list(values: Optional[List[Union[str, T]]], enum_class: Type[T]) -> Optional[List[T]]:
    """
    Convert a list of string values to their corresponding enum values.
    This is useful for converting query parameters to enum values.
    
    Args:
        values: List of string values or enum values
        enum_class: The enum class to convert to
        
    Returns:
        List of enum values or None if values is None
    """
    if values is None:
        return None
        
    result = []
    for value in values:
        if isinstance(value, str):
            # Try to convert string to enum
            try:
                # First try by value
                result.append(enum_class(value))
            except ValueError:
                # Then try by name (uppercase)
                try:
                    result.append(enum_class[value.upper()])
                except KeyError:
                    # If neither works, just use the string value
                    # This is less strict but prevents API failures
                    result.append(value)
        else:
            # Value is already an enum instance
            result.append(value)
            
    return result
