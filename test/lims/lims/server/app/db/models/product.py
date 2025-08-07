"""
Product management models for the LIMS Sample Management API
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.utils.constants import ProductStatus
from datetime import datetime


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(100), nullable=False)
    description = Column(Text)
    status = Column(Enum(ProductStatus), nullable=False, default=ProductStatus.NOT_STARTED)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    samples = relationship("Sample", back_populates="product", cascade="all, delete-orphan")
    tests = relationship("Test", back_populates="product")

    def __repr__(self):
        return f"<Product {self.id}: {self.product_code} - {self.name}>"