"""
SQLAlchemy models for the Sample Management API

This module imports and re-exports all models for easy access.
"""
# Import base models first to avoid circular dependencies
from .user import Users
from .audit import AuditTrail, ElectronicSignature

# Import storage hierarchy models
from .storage_hierarchy import StorageLocation, StorageRoom, Freezer, Box, InventorySlot

# Import product models (depends on Users)
from .product import Product

# Import sample models (depends on Users, Product and storage hierarchy)
from .sample import Sample, SampleType, Aliquot, ChainOfCustody, SampleStatusLog, StorageTransactionLog

# Import material models (depends on storage hierarchy)
from .material import Material, MaterialLot, MaterialUsageLog, MaterialInventoryAdjustment

# Import instrument models (depends on storage hierarchy)
from .instrument import Instrument, InstrumentCalibration, InstrumentMaintenanceLog

# Import test models (depends on Users, Sample, Aliquot, Product, Instrument)
from .test import TestMethod, TestParameter, TestSpecification, TestProcedure, TestStep, TestStepExecution, TestMaster, Test, TestResult

# Import quality events models (depends on Users, Sample, Test, Instrument, TestMethod)
from .quality_events import OOS, OOSInvestigation, Deviation, CAPA, CAPAAction

# Import enums from utils/constants.py
from app.utils.constants import (
    SampleStatus, TestStatus, SamplePriority, SampleStatus,
    SpecificationType, ParameterType, StepResultEnum, TestStatus,
    ResultStatusEnum, InvestigationPhase, DeviationSeverity, DeviationStatus,
    CapaActionType, CapaStatus, CapaTaskStatus, ProductStatus
)

# Export all models for easy access
__all__ = [
    # Core models
    'Users',
    'AuditTrail', 'ElectronicSignature',
    
    # Storage hierarchy
    'StorageLocation', 'StorageRoom', 'Freezer', 'Box', 'InventorySlot',
    
    # Product management
    'Product',
    
    # Sample management
    'Sample', 'SampleType', 'Aliquot', 'ChainOfCustody', 'SampleStatusLog', 'StorageTransactionLog',
    
    # Material management
    'Material', 'MaterialLot', 'MaterialUsageLog', 'MaterialInventoryAdjustment',
    
    # Instrument management
    'Instrument', 'InstrumentCalibration', 'InstrumentMaintenanceLog',
    
    # Test management
    'TestMethod', 'TestParameter', 'TestSpecification', 'TestProcedure', 'TestStep', 
    'TestStepExecution', 'TestMaster', 'Test', 'TestResult',
    
    # Quality events
    'OOS', 'OOSInvestigation', 'Deviation', 'CAPA', 'CAPAAction',
    
    # Enums
    'SampleStatus', 'TestStatus', 'SamplePriority', 'SampleStatus',
    'SpecificationType', 'ParameterType', 'StepResultEnum', 'TestStatus',
    'ResultStatusEnum', 'InvestigationPhase', 'DeviationSeverity', 'DeviationStatus',
    'CapaActionType', 'CapaStatus', 'CapaTaskStatus'
]
