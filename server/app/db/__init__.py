"""
Database package for the LIMS application.

This package provides database models, initialization, and seeding functionality.
It exports the essential components needed for database operations throughout the application.
"""

from app.core.database import db_manager, get_db, get_db_session, initialize_database as init_core_db
# from app.db.init_db import init_database, verify_initialization, DatabaseInitializer
# from app.db.seed import seed_database, DatabaseSeeder

# Import all models to ensure they are registered with SQLAlchemy
from app.db.models.base import Base
from app.db.models.user import Users
from app.db.models.sample import Sample, SampleType, Aliquot, ChainOfCustody, SampleStatusLog, StorageTransactionLog
from app.db.models.test import (
    Test, TestMethod, TestParameter, TestSpecification, 
    TestProcedure, TestStep, TestStepExecution, TestMaster, TestResult
)
from app.db.models.storage_hierarchy import Freezer, StorageRoom, StorageLocation, Box, InventorySlot
from app.db.models.material import Material, MaterialLot, MaterialUsageLog, MaterialInventoryAdjustment
from app.db.models.instrument import Instrument, InstrumentCalibration, InstrumentMaintenanceLog
from app.db.models.quality_events import OOS, OOSInvestigation, Deviation, CAPA, CAPAAction
from app.db.models.audit import AuditTrail, ElectronicSignature
from app.db.models.product import Product

# Database utilities
__all__ = [
    # Core database components
    "db_manager",
    "get_db", 
    "get_db_session",
    "Base",
    
    # Database initialization
    "init_database",
    "init_core_db", 
    "verify_initialization",
    "DatabaseInitializer",
    
    # Database seeding
    "seed_database",
    "DatabaseSeeder",
    
    # Models - User & Authentication
    "Users",
    
    # Models - Sample Management
    "Sample",
    "SampleType", 
    "Aliquot",
    
    # Models - Test Management
    "Test",
    "TestMethod",
    "TestParameter", 
    "TestSpecification",
    "TestProcedure",
    "TestStep",
    "TestStepExecution",
    "TestMaster",
    "TestResult",
    
    # Models - Storage Management
    "StorageLocation",
    "StorageRoom",
    "Freezer", 
    "Box",
    "InventorySlot",
    "ChainOfCustody",
    "SampleStatusLog",
    "StorageTransactionLog",
    
    # Models - Material Management
    "Material",
    "MaterialLot",
    "MaterialUsageLog", 
    "MaterialInventoryAdjustment",
    
    # Models - Instrument Management
    "Instrument",
    "InstrumentCalibration",
    "InstrumentMaintenanceLog",
    
    # Models - Quality Events
    "OOS",
    "OOSInvestigation",
    "Deviation",
    "CAPA",
    "CAPAAction",
    
    # Models - Audit Trail
    "AuditTrail",
    "ElectronicSignature",
    
    # Models - Product Management
    "Product"
]
