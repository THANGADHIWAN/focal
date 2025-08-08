"""
Aliquot schemas for the Sample Management API
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime
from uuid import UUID

# Import TestResponse - using forward reference to avoid circular imports
from typing import ForwardRef
TestResponse = ForwardRef("TestResponse")


class AliquotBase(BaseModel):
    aliquot_code: str = Field(..., description="Unique aliquot code")
    sample_id: int = Field(..., description="ID of the parent sample")
    volume_ml: Optional[float] = Field(None, description="Volume of the aliquot in mL", gt=0)
    status: str = Field(default="Logged_In", description="Status of the aliquot")
    created_by: str = Field(..., description="Creator of the aliquot")
    

class AliquotCreate(AliquotBase):
    assigned_to: Optional[UUID] = Field(None, description="UUID of assigned user")
    purpose: Optional[str] = Field(None, description="Purpose of the aliquot")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "aliquot_code": "ALQ-001",
                "sample_id": 1,
                "volume_ml": 5.0,
                "status": "Logged_In",
                "created_by": "John Doe",
                "assigned_to": "user-uuid-here",
                "purpose": "Testing aliquot"
            }
        }
    }


class AliquotUpdate(BaseModel):
    aliquot_code: Optional[str] = Field(None, description="Unique aliquot code")
    volume_ml: Optional[float] = Field(None, description="Volume of the aliquot in mL")
    status: Optional[str] = Field(None, description="Status of the aliquot")
    assigned_to: Optional[UUID] = Field(None, description="UUID of assigned user")
    purpose: Optional[str] = Field(None, description="Purpose of the aliquot")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "In_Progress",
                "volume_ml": 4.5,
                "purpose": "Updated testing purpose"
            }
        }
    }


class AliquotResponse(BaseModel):
    id: int
    sample_id: int
    aliquot_code: str
    volume_ml: Optional[float] = None
    creation_date: Optional[datetime] = None
    status: str
    assigned_to: Optional[UUID] = None
    created_by: str
    created_at: datetime
    purpose: Optional[str] = None
    sample: Optional[Any] = None
    tests: List["TestResponse"] = Field(default_factory=list)
    
    model_config = {
        "from_attributes": True,  # Replaces orm_mode=True
        "json_schema_extra": {
            "example": {
                "id": 1,
                "sample_id": 1,
                "aliquot_code": "ALQ-001",
                "volume_ml": 5.0,
                "creation_date": "2024-12-01T10:30:00",
                "status": "Logged_In",
                "assigned_to": "user-uuid-here",
                "created_by": "John Doe",
                "created_at": "2024-12-01T10:30:00",
                "purpose": "Testing aliquot",
                "sample": {
                    "id": 1,
                    "sample_code": "SAM-20241201-0001",
                    "sample_name": "Blood Sample 001"
                },
                "tests": []
            }
        }
    }


# Resolve forward references
from .test import TestResponse
AliquotResponse.update_forward_refs()
