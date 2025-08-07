"""
Schemas for storage management.
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class BoxBase(BaseModel):
    box_code: str
    box_type: Optional[str] = None
    freezer_id: int
    rack: Optional[str] = None
    shelf: Optional[str] = None
    drawer: Optional[str] = None
    capacity: Optional[int] = 100

class BoxCreate(BoxBase):
    created_by: str

class BoxUpdate(BoxBase):
    box_code: Optional[str] = None
    box_type: Optional[str] = None
    freezer_id: Optional[int] = None
    rack: Optional[str] = None
    shelf: Optional[str] = None
    drawer: Optional[str] = None

class BoxResponse(BoxBase):
    id: int
    created_by: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    freezer_name: Optional[str] = None
    freezer_location: Optional[str] = None

    class Config:
        from_attributes = True

class FreezerBase(BaseModel):
    name: str
    code: str
    location: str
    temperature_range: Optional[str] = None
    maintenance_status: Optional[str] = None
    notes: Optional[str] = None

class FreezerCreate(FreezerBase):
    created_by: str

class FreezerUpdate(FreezerBase):
    name: Optional[str] = None
    code: Optional[str] = None
    location: Optional[str] = None

class FreezerResponse(FreezerBase):
    id: int
    created_by: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    boxes: List[BoxResponse] = []

    class Config:
        from_attributes = True
