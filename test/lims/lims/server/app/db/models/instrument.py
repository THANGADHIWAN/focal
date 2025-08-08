"""
Instrument models for the Sample Management API
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime


class Instrument(Base):
    __tablename__ = "instrument"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    instrument_type = Column(String(100), nullable=False)
    serial_number = Column(String(100), unique=True)
    manufacturer = Column(String(100))
    model_number = Column(String(100))
    purchase_date = Column(DateTime)
    location_id = Column(Integer, ForeignKey("storage_location.id"))
    status = Column(String(20), nullable=False, default="Available")
    assigned_to = Column(String(100))
    team = Column(String(100))
    qualification_status = Column(String(20))
    maintenance_type = Column(String(20))
    remarks = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    storage_location = relationship("StorageLocation", backref="instruments")
    calibrations = relationship("InstrumentCalibration", back_populates="instrument", cascade="all, delete-orphan")
    maintenance_logs = relationship("InstrumentMaintenanceLog", back_populates="instrument", cascade="all, delete-orphan")
    notes = relationship("Note", back_populates="instrument", cascade="all, delete-orphan")
    tests = relationship("Test", back_populates="instrument")

    def __repr__(self):
        return f"<Instrument {self.id}: {self.name}>"


class InstrumentCalibration(Base):
    __tablename__ = "instrument_calibration"

    id = Column(Integer, primary_key=True, autoincrement=True)
    instrument_id = Column(Integer, ForeignKey("instrument.id"), nullable=False)
    calibration_date = Column(DateTime)
    calibrated_by = Column(String(100))
    due_date = Column(DateTime)
    calibration_status = Column(String(20))
    certificate_link = Column(String(255))
    remarks = Column(Text)

    instrument = relationship("Instrument", back_populates="calibrations")

    def __repr__(self):
        return f"<InstrumentCalibration {self.id}: {self.calibration_date}>"


class InstrumentMaintenanceLog(Base):
    __tablename__ = "instrument_maintenance_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    instrument_id = Column(Integer, ForeignKey("instrument.id"), nullable=False)
    maintenance_date = Column(DateTime)
    performed_by = Column(String(100))
    maintenance_type = Column(String(20))
    description = Column(Text)
    next_due_date = Column(DateTime)
    remarks = Column(Text)

    instrument = relationship("Instrument", back_populates="maintenance_logs")

    def __repr__(self):
        return f"<InstrumentMaintenanceLog {self.id}: {self.maintenance_type}>"


class Note(Base):
    __tablename__ = "instrument_notes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    instrument_id = Column(Integer, ForeignKey("instrument.id"), nullable=False)
    content = Column(Text, nullable=False)
    user = Column(String(100), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    instrument = relationship("Instrument", back_populates="notes")

    def __repr__(self):
        return f"<Note {self.id}: {self.timestamp}>" 