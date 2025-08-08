"""
Equipment/Instrument schemas for request/response validation
"""
from datetime import datetime
from typing import Optional, List, TypeVar, Generic
from pydantic import BaseModel, Field
from app.core.constants.equipment import (
    EquipmentType, EquipmentStatus, MaintenanceType,
    MaintenanceStatus, CalibrationStatus, QualificationStatus
)

T = TypeVar('T')

class PaginationMetadata(BaseModel):
    currentPage: int
    totalPages: int
    totalItems: int
    itemsPerPage: int
    hasMore: bool

class PaginatedResponse(BaseModel, Generic[T]):
    data: List[T]
    status: int = 200
    success: bool = True
    pagination: PaginationMetadata

class CalibrationBase(BaseModel):
    calibrated_by: str
    due_date: datetime
    calibration_status: CalibrationStatus
    certificate_link: Optional[str] = None
    remarks: Optional[str] = None

class CalibrationCreate(CalibrationBase):
    pass

class Calibration(CalibrationBase):
    id: int
    instrument_id: int
    calibration_date: datetime

    class Config:
        from_attributes = True

class MaintenanceBase(BaseModel):
    performed_by: str
    maintenance_type: MaintenanceType
    description: str
    next_due_date: datetime
    remarks: Optional[str] = None

class MaintenanceCreate(MaintenanceBase):
    pass

class Maintenance(MaintenanceBase):
    id: int
    instrument_id: int
    maintenance_date: datetime
    status: MaintenanceStatus = MaintenanceStatus.COMPLETED

    class Config:
        from_attributes = True

class NoteBase(BaseModel):
    content: str
    user: str

class NoteCreate(NoteBase):
    pass

class Note(NoteBase):
    id: int
    instrument_id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class AttachmentBase(BaseModel):
    name: str
    type: str
    url: str

class AttachmentCreate(AttachmentBase):
    pass

class Attachment(AttachmentBase):
    id: int
    instrument_id: int
    uploaded_at: datetime

    class Config:
        from_attributes = True

class InstrumentBase(BaseModel):
    name: str
    description: Optional[str] = None
    instrument_type: EquipmentType
    serial_number: str
    manufacturer: str
    model_number: str
    location_id: int
    status: EquipmentStatus = EquipmentStatus.AVAILABLE
    assigned_to: Optional[str] = None
    team: Optional[str] = None
    qualification_status: Optional[QualificationStatus] = None
    maintenance_type: Optional[MaintenanceType] = None
    remarks: Optional[str] = None

class InstrumentCreate(InstrumentBase):
    purchase_date: Optional[datetime] = None

class InstrumentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    instrument_type: Optional[EquipmentType] = None
    serial_number: Optional[str] = None
    manufacturer: Optional[str] = None
    model_number: Optional[str] = None
    location_id: Optional[int] = None
    status: Optional[EquipmentStatus] = None
    assigned_to: Optional[str] = None
    team: Optional[str] = None
    qualification_status: Optional[QualificationStatus] = None
    maintenance_type: Optional[MaintenanceType] = None
    remarks: Optional[str] = None

class Instrument(InstrumentBase):
    id: int
    purchase_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    calibrations: List[Calibration] = []
    maintenance_logs: List[Maintenance] = []
    notes: List[Note] = []
    attachments: List[Attachment] = []

    class Config:
        from_attributes = True

class InstrumentList(BaseModel):
    items: List[Instrument]
    total: int
    page: int
    size: int
    pages: int

    class Config:
        from_attributes = True

# Response schemas
class CalibrationResponse(BaseModel):
    data: Calibration
    status: int = 200
    success: bool = True

class MaintenanceResponse(BaseModel):
    data: Maintenance
    status: int = 200
    success: bool = True

class NoteResponse(BaseModel):
    data: Note
    status: int = 200
    success: bool = True

class AttachmentResponse(BaseModel):
    data: Attachment
    status: int = 200
    success: bool = True

class InstrumentResponse(BaseModel):
    data: Instrument
    status: int = 200
    success: bool = True

class InstrumentListResponse(BaseModel):
    data: InstrumentList
    status: int = 200
    success: bool = True

class EnumValue(BaseModel):
    id: int
    value: str
    description: str

class EnumListResponse(BaseModel):
    data: List[EnumValue]
    status: int = 200
    success: bool = True

class ApiResponse(BaseModel, Generic[T]):
    data: T
    status: int = 200
    success: bool = True
