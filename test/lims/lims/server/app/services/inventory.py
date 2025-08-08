"""
Inventory management service layer
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException
from datetime import datetime
from typing import List, Optional
from app.db.models.material import (
    Material,
    MaterialLot,
    MaterialUsageLog,
    MaterialInventoryAdjustment
)
from app.api.schemas.inventory import (
    MaterialCreate,
    MaterialUpdate,
    MaterialLotCreate,
    MaterialLotUpdate,
    MaterialUsageLogCreate,
    MaterialInventoryAdjustmentCreate
)

class InventoryService:
    def __init__(self, db: Session):
        self.db = db

    def get_materials(
        self,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        material_type: Optional[str] = None
    ) -> List[Material]:
        query = self.db.query(Material)
        
        if search:
            query = query.filter(
                Material.name.ilike(f"%{search}%") |
                Material.cas_number.ilike(f"%{search}%") |
                Material.manufacturer.ilike(f"%{search}%")
            )
        
        if material_type:
            query = query.filter(Material.material_type == material_type)
        
        return query.offset(skip).limit(limit).all()

    def create_material(self, material: MaterialCreate) -> Material:
        db_material = Material(**material.model_dump())
        self.db.add(db_material)
        self.db.commit()
        self.db.refresh(db_material)
        return db_material

    def get_material(self, material_id: int) -> Material:
        material = self.db.query(Material).filter(Material.id == material_id).first()
        if not material:
            raise HTTPException(status_code=404, detail="Material not found")
        return material

    def update_material(self, material_id: int, material: MaterialUpdate) -> Material:
        db_material = self.get_material(material_id)
        for field, value in material.model_dump(exclude_unset=True).items():
            setattr(db_material, field, value)
        self.db.commit()
        self.db.refresh(db_material)
        return db_material

    def get_material_lots(
        self,
        skip: int = 0,
        limit: int = 100,
        material_id: Optional[int] = None,
        status: Optional[str] = None
    ) -> List[MaterialLot]:
        query = self.db.query(MaterialLot)
        
        if material_id:
            query = query.filter(MaterialLot.material_id == material_id)
        
        if status:
            query = query.filter(MaterialLot.status == status)
        
        return query.offset(skip).limit(limit).all()

    def create_material_lot(self, lot: MaterialLotCreate) -> MaterialLot:
        # Verify material exists
        self.get_material(lot.material_id)
        
        db_lot = MaterialLot(**lot.model_dump())
        self.db.add(db_lot)
        self.db.commit()
        self.db.refresh(db_lot)
        return db_lot

    def get_material_lot(self, lot_id: int) -> MaterialLot:
        lot = self.db.query(MaterialLot).filter(MaterialLot.id == lot_id).first()
        if not lot:
            raise HTTPException(status_code=404, detail="Material lot not found")
        return lot

    def update_material_lot(self, lot_id: int, lot: MaterialLotUpdate) -> MaterialLot:
        db_lot = self.get_material_lot(lot_id)
        for field, value in lot.model_dump(exclude_unset=True).items():
            setattr(db_lot, field, value)
        self.db.commit()
        self.db.refresh(db_lot)
        return db_lot

    def create_usage_log(self, usage: MaterialUsageLogCreate) -> MaterialUsageLog:
        # Verify lot exists and has sufficient quantity
        lot = self.get_material_lot(usage.material_lot_id)
        if lot.current_quantity < usage.used_quantity:
            raise HTTPException(
                status_code=400,
                detail="Insufficient quantity available"
            )
        
        # Create usage log
        db_usage = MaterialUsageLog(**usage.model_dump())
        self.db.add(db_usage)
        
        # Update lot quantity
        lot.current_quantity -= usage.used_quantity
        
        self.db.commit()
        self.db.refresh(db_usage)
        return db_usage

    def get_usage_logs(
        self,
        skip: int = 0,
        limit: int = 100,
        material_lot_id: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[MaterialUsageLog]:
        query = self.db.query(MaterialUsageLog)
        
        if material_lot_id:
            query = query.filter(MaterialUsageLog.material_lot_id == material_lot_id)
        
        if start_date and end_date:
            query = query.filter(
                and_(
                    MaterialUsageLog.used_on >= start_date,
                    MaterialUsageLog.used_on <= end_date
                )
            )
        
        return query.offset(skip).limit(limit).all()

    def create_inventory_adjustment(
        self,
        adjustment: MaterialInventoryAdjustmentCreate
    ) -> MaterialInventoryAdjustment:
        # Verify lot exists
        lot = self.get_material_lot(adjustment.material_lot_id)
        
        # Create adjustment record
        db_adjustment = MaterialInventoryAdjustment(**adjustment.model_dump())
        self.db.add(db_adjustment)
        
        # Update lot quantity based on adjustment type
        if adjustment.adjustment_type == "addition":
            lot.current_quantity += adjustment.quantity
        elif adjustment.adjustment_type == "subtraction":
            if lot.current_quantity < adjustment.quantity:
                raise HTTPException(
                    status_code=400,
                    detail="Insufficient quantity for adjustment"
                )
            lot.current_quantity -= adjustment.quantity
        
        self.db.commit()
        self.db.refresh(db_adjustment)
        return db_adjustment

    def get_inventory_adjustments(
        self,
        skip: int = 0,
        limit: int = 100,
        material_lot_id: Optional[int] = None,
        adjustment_type: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[MaterialInventoryAdjustment]:
        query = self.db.query(MaterialInventoryAdjustment)
        
        if material_lot_id:
            query = query.filter(MaterialInventoryAdjustment.material_lot_id == material_lot_id)
        
        if adjustment_type:
            query = query.filter(MaterialInventoryAdjustment.adjustment_type == adjustment_type)
        
        if start_date and end_date:
            query = query.filter(
                and_(
                    MaterialInventoryAdjustment.adjusted_on >= start_date,
                    MaterialInventoryAdjustment.adjusted_on <= end_date
                )
            )
        
        return query.offset(skip).limit(limit).all()
