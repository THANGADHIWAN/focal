"""
Inventory management API routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.core.database import get_db
from app.api.schemas.inventory import (
    MaterialCreate, MaterialUpdate, MaterialResponse,
    MaterialLotCreate, MaterialLotUpdate, MaterialLotResponse,
    MaterialUsageLogCreate, MaterialUsageLogResponse,
    MaterialInventoryAdjustmentCreate, MaterialInventoryAdjustmentResponse
)
from app.services.inventory import InventoryService

router = APIRouter(prefix="/api/inventory", tags=["inventory"])

@router.get("/materials", response_model=List[MaterialResponse])
async def get_materials(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    material_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of materials with optional filtering"""
    service = InventoryService(db)
    return service.get_materials(skip=skip, limit=limit, search=search, material_type=material_type)

@router.post("/materials", response_model=MaterialResponse)
async def create_material(material: MaterialCreate, db: Session = Depends(get_db)):
    """Create a new material"""
    service = InventoryService(db)
    return service.create_material(material)

@router.get("/materials/{material_id}", response_model=MaterialResponse)
async def get_material(material_id: int, db: Session = Depends(get_db)):
    """Get material by ID"""
    service = InventoryService(db)
    return service.get_material(material_id)

@router.put("/materials/{material_id}", response_model=MaterialResponse)
async def update_material(
    material_id: int,
    material: MaterialUpdate,
    db: Session = Depends(get_db)
):
    """Update material details"""
    service = InventoryService(db)
    return service.update_material(material_id, material)

@router.get("/material-lots", response_model=List[MaterialLotResponse])
async def get_material_lots(
    skip: int = 0,
    limit: int = 100,
    material_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of material lots with optional filtering"""
    service = InventoryService(db)
    return service.get_material_lots(skip=skip, limit=limit, material_id=material_id, status=status)

@router.post("/material-lots", response_model=MaterialLotResponse)
async def create_material_lot(lot: MaterialLotCreate, db: Session = Depends(get_db)):
    """Create a new material lot"""
    service = InventoryService(db)
    return service.create_material_lot(lot)

@router.get("/material-lots/{lot_id}", response_model=MaterialLotResponse)
async def get_material_lot(lot_id: int, db: Session = Depends(get_db)):
    """Get material lot by ID"""
    service = InventoryService(db)
    return service.get_material_lot(lot_id)

@router.put("/material-lots/{lot_id}", response_model=MaterialLotResponse)
async def update_material_lot(
    lot_id: int,
    lot: MaterialLotUpdate,
    db: Session = Depends(get_db)
):
    """Update material lot details"""
    service = InventoryService(db)
    return service.update_material_lot(lot_id, lot)

@router.post("/usage-logs", response_model=MaterialUsageLogResponse)
async def log_material_usage(usage: MaterialUsageLogCreate, db: Session = Depends(get_db)):
    """Record material usage"""
    service = InventoryService(db)
    return service.create_usage_log(usage)

@router.get("/usage-logs", response_model=List[MaterialUsageLogResponse])
async def get_usage_logs(
    skip: int = 0,
    limit: int = 100,
    material_lot_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """Get material usage logs with optional filtering"""
    service = InventoryService(db)
    return service.get_usage_logs(
        skip=skip,
        limit=limit,
        material_lot_id=material_lot_id,
        start_date=start_date,
        end_date=end_date
    )

@router.post("/inventory-adjustments", response_model=MaterialInventoryAdjustmentResponse)
async def create_inventory_adjustment(
    adjustment: MaterialInventoryAdjustmentCreate,
    db: Session = Depends(get_db)
):
    """Create inventory adjustment record"""
    service = InventoryService(db)
    return service.create_inventory_adjustment(adjustment)

@router.get("/inventory-adjustments", response_model=List[MaterialInventoryAdjustmentResponse])
async def get_inventory_adjustments(
    skip: int = 0,
    limit: int = 100,
    material_lot_id: Optional[int] = None,
    adjustment_type: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """Get inventory adjustments with optional filtering"""
    service = InventoryService(db)
    return service.get_inventory_adjustments(
        skip=skip,
        limit=limit,
        material_lot_id=material_lot_id,
        adjustment_type=adjustment_type,
        start_date=start_date,
        end_date=end_date
    )
