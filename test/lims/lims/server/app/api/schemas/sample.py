"""
Sample schemas for the Sample Management API
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Union, Any
from datetime import datetime


class SampleBase(BaseModel):
    sample_code: str = Field(..., description="Unique sample code")
    sample_name: str = Field(..., description="Name of the sample")
    sample_type_id: int = Field(..., description="Sample type ID")
    status: str = Field(default="Logged_In", description="Status of the sample")
    created_by: str = Field(..., description="Creator of the sample")
    

class SampleCreate(SampleBase):
    box_id: Optional[int] = Field(None, description="Box ID where the sample will be stored")
    volume_ml: Optional[int] = Field(None, description="Sample volume in mL", gt=0)
    received_date: Optional[datetime] = Field(None, description="Date when sample was received")
    due_date: Optional[datetime] = Field(None, description="Due date for sample processing")
    priority: Optional[str] = Field(default="Medium", description="Sample priority")
    quantity: Optional[float] = Field(None, description="Sample quantity")
    is_aliquot: Optional[bool] = Field(default=False, description="Whether this is an aliquot")
    number_of_aliquots: Optional[int] = Field(default=0, description="Number of aliquots created")
    purpose: Optional[str] = Field(None, description="Purpose of the sample")
    
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "sample_code": "SAM-20241201-0001",
                "sample_name": "Blood Sample 001",
                "sample_type_id": 1,
                "status": "Logged_In",
                "created_by": "John Doe",
                "box_id": 1,
                "volume_ml": 10,
                "received_date": "2024-12-01T10:00:00",
                "due_date": "2024-12-08T10:00:00",
                "priority": "Medium",
                "quantity": 10.5,
                "is_aliquot": False,
                "number_of_aliquots": 0,
                "purpose": "Clinical testing"
            }]
        }
    }


class SampleUpdate(BaseModel):
    sample_code: Optional[str] = Field(None, description="Unique sample code")
    sample_name: Optional[str] = Field(None, description="Name of the sample")
    sample_type_id: Optional[int] = Field(None, description="Sample type ID")
    status: Optional[str] = Field(None, description="Status of the sample")
    box_id: Optional[int] = Field(None, description="Box ID where the sample is stored")
    volume_ml: Optional[int] = Field(None, description="Sample volume in mL")
    received_date: Optional[datetime] = Field(None, description="Date when sample was received")
    due_date: Optional[datetime] = Field(None, description="Due date for sample processing")
    priority: Optional[str] = Field(None, description="Sample priority")
    quantity: Optional[float] = Field(None, description="Sample quantity")
    is_aliquot: Optional[bool] = Field(None, description="Whether this is an aliquot")
    number_of_aliquots: Optional[int] = Field(None, description="Number of aliquots created")
    created_by: Optional[str] = Field(None, description="Creator of the sample")
    purpose: Optional[str] = Field(None, description="Purpose of the sample")
    
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "sample_name": "Updated Blood Sample 001",
                "status": "In_Progress",
                "priority": "High",
                "purpose": "Updated clinical testing"
            }]
        }
    }


class AliquotSummary(BaseModel):
    id: int
    aliquot_code: str
    volume_ml: Optional[float] = None
    status: str
    created_at: datetime
    
    model_config = {
        "from_attributes": True
    }


class SampleResponse(BaseModel):
    id: int
    sample_code: str
    sample_name: str
    sample_type_id: int
    type_name: str
    status: str
    box_id: Optional[int] = None
    volume_ml: Optional[int] = None
    received_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    priority: Optional[str] = None
    quantity: Optional[float] = None
    is_aliquot: Optional[bool] = None
    number_of_aliquots: Optional[int] = None
    created_by: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    purpose: Optional[str] = None
    aliquots: List[AliquotSummary] = Field(default_factory=list)
    
    model_config = {
        "from_attributes": True,  # Replaces orm_mode=True
        "json_schema_extra": {
            "example": {
                "id": 1,
                "sample_code": "SAM-20241201-0001",
                "sample_name": "Blood Sample 001",
                "sample_type_id": 1,
                "status": "Logged_In",
                "box_id": 1,
                "volume_ml": 10,
                "received_date": "2024-12-01T10:00:00",
                "due_date": "2024-12-08T10:00:00",
                "priority": "Medium",
                "quantity": 10.5,
                "is_aliquot": False,
                "number_of_aliquots": 3,
                "created_by": "John Doe",
                "created_at": "2024-12-01T10:00:00",
                "updated_at": None,
                "purpose": "Clinical testing",
                "aliquots": []
            }
        }
    }


class SampleFilter(BaseModel):
    type: Optional[List[int]] = Field(
        None, 
        description="Filter by sample type IDs",
        examples=[1, 2]  # Using type IDs
    )
    status: Optional[List[str]] = Field(
        None, 
        description="Filter by sample statuses",
        examples=["Logged_In", "In_Progress", "Completed"]
    )
    location: Optional[List[int]] = Field(
        None, 
        description="Filter by box IDs",
        examples=[1, 2]  # Using box IDs
    )
    owner: Optional[List[str]] = Field(
        None, 
        description="Filter by created_by field",
        examples=["John Doe", "Jane Smith"]
    )
    search: Optional[str] = Field(
        None, 
        description="Search term for sample name or code",
        examples=["sample123"]
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "type": [1, 2],
                "status": ["Logged_In", "In_Progress"],
                "location": [1, 2],
                "owner": ["John Doe"],
                "search": "blood"
            }
        }
    }
