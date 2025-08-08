"""
API routes for equipment management
"""
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.equipment_service import EquipmentService
from app.api.schemas.equipment import (
    InstrumentResponse, InstrumentCreate, InstrumentUpdate,
    CalibrationCreate, MaintenanceCreate, NoteCreate,
    PaginatedResponse, ApiResponse
)

router = APIRouter(prefix="/api/metadata/equipment", tags=["Equipment"])

@router.get("", response_model=PaginatedResponse[InstrumentResponse])
async def get_all_equipment(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    type: Optional[str] = None,
    status: Optional[str] = None,
    location: Optional[str] = None,
    manufacturer: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = Query(None, regex="^(asc|desc)$"),
    db: Session = Depends(get_db)
) -> PaginatedResponse[InstrumentResponse]:
    """Get all equipment with pagination and filtering"""
    filters = {
        "type": type,
        "status": status,
        "location": location,
        "manufacturer": manufacturer
    }
    filters = {k: v for k, v in filters.items() if v is not None}
    
    skip = (page - 1) * limit
    result = EquipmentService.get_all_equipment(
        db, skip=skip, limit=limit,
        filters=filters, search=search
    )
    
    return PaginatedResponse(
        data=result["items"],
        status=200,
        success=True,
        pagination={
            "currentPage": result["page"],
            "totalPages": result["pages"],
            "totalItems": result["total"],
            "itemsPerPage": result["size"],
            "hasMore": result["page"] < result["pages"]
        }
    )

@router.get("/types", response_model=ApiResponse[List[Dict[str, Any]]])
async def get_equipment_types() -> ApiResponse[List[Dict[str, Any]]]:
    """Get all equipment types"""
    types = EquipmentService.get_equipment_types()
    return ApiResponse(data=types, status=200, success=True)

@router.get("/statuses", response_model=ApiResponse[List[Dict[str, Any]]])
async def get_equipment_statuses() -> ApiResponse[List[Dict[str, Any]]]:
    """Get all equipment statuses"""
    statuses = EquipmentService.get_equipment_statuses()
    return ApiResponse(data=statuses, status=200, success=True)

@router.get("/{equipment_id}", response_model=ApiResponse[InstrumentResponse])
async def get_equipment(
    equipment_id: int,
    db: Session = Depends(get_db)
) -> ApiResponse[InstrumentResponse]:
    """Get equipment by ID"""
    equipment = EquipmentService.get_equipment_by_id(db, equipment_id)
    return ApiResponse(data=equipment, status=200, success=True)

@router.post("", response_model=ApiResponse[InstrumentResponse])
async def create_equipment(
    equipment: InstrumentCreate,
    db: Session = Depends(get_db)
) -> ApiResponse[InstrumentResponse]:
    """Create new equipment"""
    created = EquipmentService.create_equipment(db, equipment)
    return ApiResponse(data=created, status=201, success=True)

@router.put("/{equipment_id}", response_model=ApiResponse[InstrumentResponse])
async def update_equipment(
    equipment_id: int,
    updates: InstrumentUpdate,
    db: Session = Depends(get_db)
) -> ApiResponse[InstrumentResponse]:
    """Update equipment"""
    updated = EquipmentService.update_equipment(db, equipment_id, updates)
    return ApiResponse(data=updated, status=200, success=True)

@router.delete("/{equipment_id}", response_model=ApiResponse[Dict[str, bool]])
async def delete_equipment(
    equipment_id: int,
    db: Session = Depends(get_db)
) -> ApiResponse[Dict[str, bool]]:
    """Delete equipment"""
    EquipmentService.delete_equipment(db, equipment_id)
    return ApiResponse(
        data={"deleted": True},
        status=200,
        success=True
    )

@router.post("/{equipment_id}/maintenance", response_model=ApiResponse[InstrumentResponse])
async def add_maintenance(
    equipment_id: int,
    maintenance: MaintenanceCreate,
    db: Session = Depends(get_db)
) -> ApiResponse[InstrumentResponse]:
    """Add maintenance record"""
    result = EquipmentService.add_maintenance(db, equipment_id, maintenance)
    equipment = EquipmentService.get_equipment_by_id(db, equipment_id)
    return ApiResponse(data=equipment, status=200, success=True)

@router.post("/{equipment_id}/calibration", response_model=ApiResponse[InstrumentResponse])
async def add_calibration(
    equipment_id: int,
    calibration: CalibrationCreate,
    db: Session = Depends(get_db)
) -> ApiResponse[InstrumentResponse]:
    """Add calibration record"""
    result = EquipmentService.add_calibration(db, equipment_id, calibration)
    equipment = EquipmentService.get_equipment_by_id(db, equipment_id)
    return ApiResponse(data=equipment, status=200, success=True)

@router.post("/{equipment_id}/notes", response_model=ApiResponse[InstrumentResponse])
async def add_note(
    equipment_id: int,
    note: NoteCreate,
    db: Session = Depends(get_db)
) -> ApiResponse[InstrumentResponse]:
    """Add note"""
    result = EquipmentService.add_note(db, equipment_id, note)
    equipment = EquipmentService.get_equipment_by_id(db, equipment_id)
    return ApiResponse(data=equipment, status=200, success=True)

@router.post("/{equipment_id}/attachments", response_model=ApiResponse[Dict[str, Any]])
async def add_attachment(
    equipment_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
) -> ApiResponse[Dict[str, Any]]:
    """Add attachment"""
    result = await EquipmentService.add_attachment(db, equipment_id, file)
    return ApiResponse(data=result, status=200, success=True)
