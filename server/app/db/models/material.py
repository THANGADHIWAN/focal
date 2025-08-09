"""
Material management models for the Sample Management API
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Numeric, Text
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime


class Material(Base):
    __tablename__ = "material"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    material_type = Column(String(20))
    cas_number = Column(String(100))
    manufacturer = Column(String(100))
    grade = Column(String(100))
    unit_of_measure = Column(String(50))
    shelf_life_days = Column(Integer)
    is_controlled = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    material_lots = relationship("MaterialLot", back_populates="material", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Material {self.id}: {self.name}>"


class MaterialLot(Base):
    __tablename__ = "material_lot"

    id = Column(Integer, primary_key=True, autoincrement=True)
    material_id = Column(Integer, ForeignKey("material.id"), nullable=False)
    lot_number = Column(String(100), nullable=False)
    received_date = Column(DateTime)
    expiry_date = Column(DateTime)
    received_quantity = Column(Numeric(10, 2))
    current_quantity = Column(Numeric(10, 2))
    storage_location_id = Column(Integer, ForeignKey("storage_location.id"))
    status = Column(String(20), nullable=False, default="Available")
    remarks = Column(Text)

    material = relationship("Material", back_populates="material_lots")
    storage_location = relationship("StorageLocation", backref="material_lots")
    usage_logs = relationship("MaterialUsageLog", back_populates="material_lot", cascade="all, delete-orphan")
    inventory_adjustments = relationship("MaterialInventoryAdjustment", back_populates="material_lot", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<MaterialLot {self.id}: {self.lot_number}>"


class MaterialUsageLog(Base):
    __tablename__ = "material_usage_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    material_lot_id = Column(Integer, ForeignKey("material_lot.id"), nullable=False)
    used_by = Column(String(100))
    used_on = Column(DateTime, default=datetime.utcnow)
    used_quantity = Column(Numeric(10, 2))
    purpose = Column(String(255))
    associated_sample_id = Column(Integer, ForeignKey("sample.id"))
    remarks = Column(Text)

    material_lot = relationship("MaterialLot", back_populates="usage_logs")
    sample = relationship("Sample", backref="material_usage_logs")

    def __repr__(self):
        return f"<MaterialUsageLog {self.id}: {self.used_quantity}>"


class MaterialInventoryAdjustment(Base):
    __tablename__ = "material_inventory_adjustment"

    id = Column(Integer, primary_key=True, autoincrement=True)
    material_lot_id = Column(Integer, ForeignKey("material_lot.id"), nullable=False)
    adjusted_by = Column(String(100))
    adjusted_on = Column(DateTime, default=datetime.utcnow)
    adjustment_type = Column(String(20))
    quantity = Column(Numeric(10, 2))
    reason = Column(Text)
    remarks = Column(Text)

    material_lot = relationship("MaterialLot", back_populates="inventory_adjustments")

    def __repr__(self):
        return f"<MaterialInventoryAdjustment {self.id}: {self.adjustment_type}>" 