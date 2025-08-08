"""
Pydantic schemas for inventory management
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

class MaterialBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    material_type: Optional[str] = Field(None, max_length=20)
    cas_number: Optional[str] = Field(None, max_length=100)
    manufacturer: Optional[str] = Field(None, max_length=100)
    grade: Optional[str] = Field(None, max_length=100)
    unit_of_measure: Optional[str] = Field(None, max_length=50)
    shelf_life_days: Optional[int] = None
    is_controlled: bool = False

class MaterialCreate(MaterialBase):
    pass

class MaterialUpdate(MaterialBase):
    pass

class MaterialResponse(MaterialBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class MaterialLotBase(BaseModel):
    material_id: int
    lot_number: str = Field(..., max_length=100)
    received_date: Optional[datetime]
    expiry_date: Optional[datetime]
    received_quantity: Decimal = Field(..., ge=0, decimal_places=2)
    current_quantity: Decimal = Field(..., ge=0, decimal_places=2)
    storage_location_id: Optional[int]
    status: str = Field(..., max_length=20)
    remarks: Optional[str]

class MaterialLotCreate(MaterialLotBase):
    pass

class MaterialLotUpdate(BaseModel):
    lot_number: Optional[str] = Field(None, max_length=100)
    received_date: Optional[datetime]
    expiry_date: Optional[datetime]
    current_quantity: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    storage_location_id: Optional[int]
    status: Optional[str] = Field(None, max_length=20)
    remarks: Optional[str]

class MaterialLotResponse(MaterialLotBase):
    id: int
    material: MaterialResponse

    class Config:
        from_attributes = True

class MaterialUsageLogBase(BaseModel):
    material_lot_id: int
    used_by: str = Field(..., max_length=100)
    used_quantity: Decimal = Field(..., gt=0, decimal_places=2)
    purpose: Optional[str] = Field(None, max_length=255)
    associated_sample_id: Optional[int]
    remarks: Optional[str]

class MaterialUsageLogCreate(MaterialUsageLogBase):
    pass

class MaterialUsageLogResponse(MaterialUsageLogBase):
    id: int
    used_on: datetime
    material_lot: MaterialLotResponse

    class Config:
        from_attributes = True

class MaterialInventoryAdjustmentBase(BaseModel):
    material_lot_id: int
    adjusted_by: str = Field(..., max_length=100)
    adjustment_type: str = Field(..., max_length=20)
    quantity: Decimal = Field(..., decimal_places=2)
    reason: str
    remarks: Optional[str]

class MaterialInventoryAdjustmentCreate(MaterialInventoryAdjustmentBase):
    pass

class MaterialInventoryAdjustmentResponse(MaterialInventoryAdjustmentBase):
    id: int
    adjusted_on: datetime
    material_lot: MaterialLotResponse

    class Config:
        from_attributes = True
