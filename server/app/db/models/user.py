"""
User models for the Sample Management API
"""
from sqlalchemy import Column, String, Boolean, DateTime, UUID
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from app.db.database import Base
from datetime import datetime
import uuid


class Users(Base):
    __tablename__ = "users"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    role = Column(String(20))
    department = Column(String(100))
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Users {self.id}: {self.full_name} ({self.email})>"
