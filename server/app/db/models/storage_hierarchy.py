"""
Storage hierarchy models for the Sample Management API
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Numeric, Text
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime


class StorageLocation(Base):
    __tablename__ = "storage_location"

    id = Column(Integer, primary_key=True, autoincrement=True)
    location_name = Column(String(100), nullable=False)
    location_code = Column(String(50), unique=True)
    temperature_celsius = Column(Numeric(5, 2))
    humidity_percent = Column(Numeric(5, 2))
    description = Column(Text)

    storage_rooms = relationship("StorageRoom", back_populates="storage_location")

    def __repr__(self):
        return f"<StorageLocation {self.id}: {self.location_name}>"


class StorageRoom(Base):
    __tablename__ = "storage_room"

    id = Column(Integer, primary_key=True, autoincrement=True)
    room_name = Column(String(100), nullable=False, unique=True)
    floor = Column(Integer)
    building = Column(String(100))
    access_control = Column(Boolean, nullable=False, default=False)
    temperature_range = Column(String(50))
    humidity_range = Column(String(50))
    notes = Column(Text)
    storage_location_id = Column(Integer, ForeignKey("storage_location.id"))

    storage_location = relationship("StorageLocation", back_populates="storage_rooms")
    freezers = relationship("Freezer", back_populates="storage_room")

    def __repr__(self):
        return f"<StorageRoom {self.id}: {self.room_name}>"


class Freezer(Base):
    __tablename__ = "freezer"

    id = Column(Integer, primary_key=True, autoincrement=True)
    freezer_name = Column(String(100), nullable=False)
    freezer_type = Column(String(100))
    storage_room_id = Column(Integer, ForeignKey("storage_room.id"))
    temperature_range = Column(String(50))
    notes = Column(Text)

    storage_room = relationship("StorageRoom", back_populates="freezers")
    boxes = relationship("Box", back_populates="freezer")

    def __repr__(self):
        return f"<Freezer {self.id}: {self.freezer_name}>"


class Box(Base):
    __tablename__ = "box"

    id = Column(Integer, primary_key=True, autoincrement=True)
    box_code = Column(String(50), nullable=False, unique=True)
    box_type = Column(String(100))
    rack = Column(String(50))
    shelf = Column(String(50))
    drawer = Column(String(50))
    capacity = Column(Integer)
    freezer_id = Column(Integer, ForeignKey("freezer.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    freezer = relationship("Freezer", back_populates="boxes")
    inventory_slots = relationship("InventorySlot", back_populates="box")
    samples = relationship("Sample", back_populates="box")

    def __repr__(self):
        return f"<Box {self.id}: {self.box_code}>"


class InventorySlot(Base):
    __tablename__ = "inventory_slot"

    id = Column(Integer, primary_key=True, autoincrement=True)
    slot_code = Column(String(50), nullable=False)
    is_occupied = Column(Boolean, nullable=False, default=False)
    aliquot_id = Column(Integer, ForeignKey("aliquot.id"), nullable=True)
    box_id = Column(Integer, ForeignKey("box.id"))

    box = relationship("Box", back_populates="inventory_slots")
    aliquot = relationship("Aliquot", back_populates="inventory_slot")

    def __repr__(self):
        return f"<InventorySlot {self.id}: {self.slot_code}>" 