"""
Sample models for the Sample Management API
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Enum, Boolean, Numeric
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base
from app.db.models.storage_hierarchy import Box, StorageLocation, Freezer, StorageRoom
from app.db.models.instrument import Instrument
from app.utils.constants import SampleStatus, SamplePriority


class SampleType(Base):
    __tablename__ = "sample_type"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    matrix_type = Column(String(100))
    
    samples = relationship("Sample", back_populates="sample_type")
    
    def __repr__(self):
        return f"<SampleType {self.id}: {self.name}>"


class Sample(Base):
    __tablename__ = "sample"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sample_code = Column(String(50), nullable=False, unique=True)
    sample_name = Column(String(50))
    sample_type_id = Column(Integer, ForeignKey("sample_type.id"))
    product_id = Column(Integer, ForeignKey("product.id"))
    status = Column(String(100), nullable=False, default="Completed")
    box_id = Column(Integer, ForeignKey("box.id"))
    volume_ml = Column(Integer)
    received_date = Column(DateTime)
    due_date = Column(DateTime)
    priority = Column(Enum(SamplePriority), nullable=False, default=SamplePriority.MEDIUM)
    quantity = Column(Numeric(10, 2))
    is_aliquot = Column(Boolean, nullable=False, default=False)
    number_of_aliquots = Column(Integer, nullable=False, default=0)
    created_by = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    purpose = Column(String(255))

    sample_type = relationship("SampleType", back_populates="samples")
    product = relationship("Product", back_populates="samples")
    box = relationship("Box", back_populates="samples")
    aliquots = relationship("Aliquot", back_populates="sample", cascade="all, delete-orphan")
    tests = relationship("Test", back_populates="sample")
    sample_status_logs = relationship("SampleStatusLog", back_populates="sample", cascade="all, delete-orphan")
    storage_transaction_logs = relationship("StorageTransactionLog", back_populates="sample", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Sample {self.id}: {self.sample_code} ({self.sample_name})>"


class Aliquot(Base):
    __tablename__ = "aliquot"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sample_id = Column(Integer, ForeignKey("sample.id"), nullable=False)
    aliquot_code = Column(String(50), nullable=False, unique=True)
    volume_ml = Column(Numeric(10, 2))
    creation_date = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(SampleStatus), nullable=False, default=SampleStatus.LOGGED_IN)
    assigned_to = Column(PostgresUUID(as_uuid=True), ForeignKey("users.id"))
    created_by = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    purpose = Column(String(255))

    sample = relationship("Sample", back_populates="aliquots")
    user = relationship("Users", backref="assigned_aliquots")
    tests = relationship("Test", back_populates="aliquot")
    inventory_slot = relationship("InventorySlot", back_populates="aliquot", uselist=False)
    chain_of_custody = relationship("ChainOfCustody", back_populates="aliquot")

    def __repr__(self):
        return f"<Aliquot {self.id}: {self.aliquot_code}>"


class ChainOfCustody(Base):
    __tablename__ = "chain_of_custody"

    id = Column(Integer, primary_key=True, autoincrement=True)
    aliquot_id = Column(Integer, ForeignKey("aliquot.id"), nullable=False)
    transferred_from = Column(String(100), nullable=False)
    transferred_to = Column(String(100), nullable=False)
    transfer_date = Column(DateTime, default=datetime.utcnow)
    condition_on_transfer = Column(Text)
    remarks = Column(Text)

    aliquot = relationship("Aliquot", back_populates="chain_of_custody")

    def __repr__(self):
        return f"<ChainOfCustody {self.id}: {self.transferred_from} -> {self.transferred_to}>"


class SampleStatusLog(Base):
    __tablename__ = "sample_status_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sample_id = Column(Integer, ForeignKey("sample.id"), nullable=False)
    status = Column(String(20), nullable=False)
    changed_by = Column(String(100))
    changed_at = Column(DateTime, default=datetime.utcnow)
    remarks = Column(Text)

    sample = relationship("Sample", back_populates="sample_status_logs")

    def __repr__(self):
        return f"<SampleStatusLog {self.id}: {self.status}>"


class StorageTransactionLog(Base):
    __tablename__ = "storage_transaction_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sample_id = Column(Integer, ForeignKey("sample.id"), nullable=False)
    from_location_id = Column(Integer, ForeignKey("storage_location.id"))
    to_location_id = Column(Integer, ForeignKey("storage_location.id"))
    moved_by = Column(String(100))
    moved_at = Column(DateTime, default=datetime.utcnow)
    reason = Column(String(255))
    remarks = Column(Text)

    sample = relationship("Sample", back_populates="storage_transaction_logs")
    from_location = relationship("StorageLocation", foreign_keys=[from_location_id])
    to_location = relationship("StorageLocation", foreign_keys=[to_location_id])

    def __repr__(self):
        return f"<StorageTransactionLog {self.id}: {self.sample_id}>"
