"""
Metadata schemas for the Sample Management API
"""
from pydantic import BaseModel
from typing import Optional


class SampleTypeResponse(BaseModel):
    id: int
    value: str  # Changed from name to value for consistency
    description: Optional[str] = None
    
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "value": "Blood",
                "description": "Blood sample type"
            }
        }
    }


class SampleStatusResponse(BaseModel):
    id: int
    value: str  # Changed from name to value for consistency
    description: Optional[str] = None
    
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "value": "Submitted",
                "description": "Sample has been submitted"
            }
        }
    }


class LabLocationResponse(BaseModel):
    id: int
    value: str  # Changed from name to value for consistency
    description: Optional[str] = None
    
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "value": "Lab 1",
                "description": "Main laboratory"
            }
        }
    }


class UserResponse(BaseModel):
    id: int
    value: str  # Changed from name to value for consistency
    email: str
    role: str
    
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "value": "Dr. Smith",
                "email": "smith@example.com",
                "role": "scientist"
            }
        }
    }


class StorageLocationResponse(BaseModel):
    id: int
    value: str  # Changed from name to value for consistency
    drawer: Optional[str] = None
    rack: Optional[str] = None
    shelf: Optional[str] = None
    freezer: Optional[str] = None
    lab: Optional[str] = None
    capacity: int
    available_spaces: int
    
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "value": "Storage Box 1",
                "drawer": "D1",
                "rack": "R1",
                "shelf": "S1",
                "freezer": "Freezer 1",
                "lab": "Lab 1",
                "capacity": 100,
                "available_spaces": 50
            }
        }
    }
