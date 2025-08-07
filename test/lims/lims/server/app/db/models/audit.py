"""
Audit models for the Sample Management API
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, JSON, UUID
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime
import uuid


class AuditTrail(Base):
    __tablename__ = "audit_trail"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_type = Column(String(100), nullable=False)
    entity_id = Column(PostgresUUID(as_uuid=True), nullable=False)
    action = Column(String(20), nullable=False)
    user_id = Column(PostgresUUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    old_value = Column(JSON)
    new_value = Column(JSON)
    justification = Column(Text)
    signature = Column(String(255))
    performed_at = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String(50))

    user = relationship("Users", backref="audit_trails")

    def __repr__(self):
        return f"<AuditTrail {self.id}: {self.action} on {self.entity_type}>"


class ElectronicSignature(Base):
    __tablename__ = "electronic_signature"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_type = Column(String(100), nullable=False)
    entity_id = Column(PostgresUUID(as_uuid=True), nullable=False)
    signed_by = Column(PostgresUUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    signature_type = Column(String(20), nullable=False)
    comments = Column(Text)
    signed_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("Users", backref="electronic_signatures")

    def __repr__(self):
        return f"<ElectronicSignature {self.id}: {self.signature_type} by {self.signed_by}>" 