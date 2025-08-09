"""
Test schemas for the Sample Management API
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime
from uuid import UUID

class TestBase(BaseModel):
    sample_id: int = Field(..., description="ID of the parent sample")
    aliquot_id: Optional[int] = Field(None, description="ID of the parent aliquot")
    test_master_id: int = Field(..., description="ID of the test master")
    analyst_id: Optional[UUID] = Field(None, description="UUID of the analyst assigned")
    instrument_id: Optional[int] = Field(None, description="ID of the instrument used")
    status: str = Field(default="Pending", description="Status of the test")
    

class TestCreate(TestBase):
    scheduled_date: Optional[datetime] = Field(None, description="Scheduled date for the test")
    remarks: Optional[str] = Field(None, description="Additional remarks about the test")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "sample_id": 1,
                "aliquot_id": 1,
                "test_master_id": 1,
                "analyst_id": "user-uuid-here",
                "instrument_id": 1,
                "status": "Pending",
                "scheduled_date": "2024-12-02T09:00:00",
                "remarks": "Standard blood test"
            }
        }
    }


class TestUpdate(BaseModel):
    sample_id: Optional[int] = Field(None, description="ID of the parent sample")
    aliquot_id: Optional[int] = Field(None, description="ID of the parent aliquot")
    test_master_id: Optional[int] = Field(None, description="ID of the test master")
    analyst_id: Optional[UUID] = Field(None, description="UUID of the analyst assigned")
    instrument_id: Optional[int] = Field(None, description="ID of the instrument used")
    scheduled_date: Optional[datetime] = Field(None, description="Scheduled date for the test")
    start_date: Optional[datetime] = Field(None, description="Start date of the test")
    end_date: Optional[datetime] = Field(None, description="End date of the test")
    status: Optional[str] = Field(None, description="Status of the test")
    remarks: Optional[str] = Field(None, description="Additional remarks about the test")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "Completed",
                "start_date": "2024-12-02T09:00:00",
                "end_date": "2024-12-02T11:00:00",
                "remarks": "Test completed successfully"
            }
        }
    }


class TestMethodResponse(BaseModel):
    id: int
    name: str
    version: Optional[str] = None
    description: Optional[str] = None
    validated: bool = False
    
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Blood Analysis",
                "version": "1.0",
                "description": "Standard blood analysis method",
                "validated": True
            }
        }
    }


class TestResponse(BaseModel):
    id: int
    sample_id: int
    aliquot_id: Optional[int] = None
    test_master_id: int
    analyst_id: Optional[UUID] = None
    instrument_id: Optional[int] = None
    scheduled_date: Optional[datetime] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: str
    remarks: Optional[str] = None
    sample: Optional[Any] = None
    aliquot: Optional[Any] = None
    test_results: List[Any] = Field(default_factory=list)
    
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "sample_id": 1,
                "aliquot_id": 1,
                "test_master_id": 1,
                "analyst_id": "user-uuid-here",
                "instrument_id": 1,
                "scheduled_date": "2024-12-02T09:00:00",
                "start_date": "2024-12-02T09:00:00",
                "end_date": "2024-12-02T11:00:00",
                "status": "Completed",
                "remarks": "Standard blood test",
                "sample": {
                    "id": 1,
                    "sample_code": "SAM-20241201-0001",
                    "sample_name": "Blood Sample 001"
                },
                "aliquot": {
                    "id": 1,
                    "aliquot_code": "ALQ-001"
                },
                "test_results": []
            }
        }
    }
