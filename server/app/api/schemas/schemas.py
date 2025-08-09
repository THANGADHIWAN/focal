"""
DEPRECATED: This file is deprecated. Please use the new modular schema files instead.

The schemas have been moved to:
- base.py for common schemas
- sample.py for sample schemas
- aliquot.py for aliquot schemas
- test.py for test schemas
- metadata.py for metadata schemas

Import from app.schemas instead of app.schemas.schemas
"""

# Re-export everything from the new modular files
from .base import *
from .sample import *
from .aliquot import *
from .test import *
from .metadata import *

# Re-exports only - no schema definitions here
# All schemas moved to their respective files

class AliquotUpdate(BaseModel):
    location: str

class TestBase(BaseModel):
    name: str
    method: str
    
class TestCreate(TestBase):
    assigned_to: Optional[str] = None
    notes: Optional[str] = None

class TestUpdate(BaseModel):
    status: Optional[TestStatusEnum] = None
    results: Optional[str] = None
    notes: Optional[str] = None
    completion_date: Optional[datetime] = None

# Response models
class TestResponse(BaseModel):
    id: str
    name: str
    status: str
    assigned_to: Optional[str] = None
    start_date: datetime
    completion_date: Optional[datetime] = None
    method: str
    results: Optional[str] = None
    notes: Optional[str] = None
    
    class Config:
        orm_mode = True

class AliquotResponse(BaseModel):
    id: str
    volume: float
    created_at: datetime
    location: Optional[str] = None
    tests: List[TestResponse] = []
    
    class Config:
        orm_mode = True

class SampleResponse(BaseModel):
    id: str
    name: str
    type: str
    submission_date: datetime
    status: str
    owner: str
    box_id: Optional[str] = None
    location: Optional[str] = None
    last_movement: datetime
    volume_left: float
    total_volume: float
    aliquots_created: int
    aliquots: List[AliquotResponse] = []
    notes: Optional[str] = None
    
    class Config:
        orm_mode = True

class SampleTypeResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    
    class Config:
        orm_mode = True

class SampleStatusResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    
    class Config:
        orm_mode = True

class LabLocationResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    
    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str
    
    class Config:
        orm_mode = True

class StorageLocationResponse(BaseModel):
    id: str
    name: str
    drawer: Optional[str] = None
    rack: Optional[str] = None
    shelf: Optional[str] = None
    freezer: Optional[str] = None
    lab: Optional[str] = None
    capacity: int
    available_spaces: int
    
    class Config:
        orm_mode = True

class TestMethodResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    
    class Config:
        orm_mode = True

# Pagination and filtering
class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    limit: int = Field(10, ge=1, le=100)

class SampleFilter(BaseModel):
    type: Optional[List[str]] = None
    status: Optional[List[str]] = None
    location: Optional[List[str]] = None
    owner: Optional[List[str]] = None
    search: Optional[str] = None
    
    class Config:
        use_enum_values = True

class PaginatedResponse(BaseModel):
    data: List[Any]
    total_count: int
    total_pages: int
    current_page: int
    page_size: int
    has_more: bool

# Generic API response
class ApiResponse(BaseModel):
    data: Optional[Any] = None
    message: Optional[str] = None
    status: int
    success: bool
