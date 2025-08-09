"""
Constants and enumerations used throughout the application.
"""
from enum import Enum
from typing import List

class EquipmentType(str, Enum):
    """Types of equipment available in the system"""
    HPLC = "HPLC"
    CENTRIFUGE = "Centrifuge"
    MICROSCOPE = "Microscope"
    PCR = "PCR"
    SPECTROPHOTOMETER = "Spectrophotometer"
    BALANCE = "Balance"
    PH_METER = "pH Meter"

class EquipmentStatus(str, Enum):
    """Status values for equipment in the system"""
    AVAILABLE = "AVAILABLE"
    IN_USE = "IN_USE"
    UNDER_MAINTENANCE = "UNDER_MAINTENANCE"
    OUT_OF_SERVICE = "OUT_OF_SERVICE"
    QUARANTINED = "QUARANTINED"

class InventoryCategory(str, Enum):
    """Categories for inventory items"""
    REAGENT = "REAGENT"
    SOLVENT = "SOLVENT"
    STANDARD = "STANDARD"
    BUFFER = "BUFFER"
    CONSUMABLE = "CONSUMABLE"

class InventoryStatus(str, Enum):
    """Status values for inventory items"""
    IN_STOCK = "IN_STOCK"
    LOW_STOCK = "LOW_STOCK"
    OUT_OF_STOCK = "OUT_OF_STOCK"
    EXPIRED = "EXPIRED"
    ORDERED = "ORDERED"
    QUARANTINED = "QUARANTINED"

class Location(str, Enum):
    """Lab locations in the system"""
    LAB_1 = "LAB_1"
    LAB_2 = "LAB_2"
    LAB_3 = "LAB_3"
    STORAGE_ROOM = "STORAGE_ROOM"
    FREEZER = "FREEZER"
    REFRIGERATOR = "REFRIGERATOR"

class SampleType(str, Enum):
    """Types of samples in the system"""
    BLOOD = "BLOOD"
    TISSUE = "TISSUE"
    URINE = "URINE"
    SALIVA = "SALIVA"
    CULTURE = "CULTURE"
    ENVIRONMENTAL = "ENVIRONMENTAL"
    OTHER = "OTHER"

class SamplePriority(str, Enum):
    """Priority levels for samples"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"

class SampleStatus(str, Enum):
    """Status values for samples"""
    LOGGED_IN = "LOGGED_IN"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    ARCHIVED = "ARCHIVED"

class SpecificationType(str, Enum):
    """Types of specifications"""
    EXACT = "EXACT"
    RANGE = "RANGE"
    LESS_THAN = "LESS_THAN"
    GREATER_THAN = "GREATER_THAN"

class ParameterType(str, Enum):
    """Types of parameters"""
    NUMERIC = "NUMERIC"
    TEXT = "TEXT"
    BOOLEAN = "BOOLEAN"
    DATETIME = "DATETIME"

class StepResultEnum(str, Enum):
    """Results for test steps"""
    PASS = "Pass"
    FAIL = "Fail"
    NA = "NA"

class TestStatus(str, Enum):
    """Status values for tests"""
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class ResultStatusEnum(str, Enum):
    """Status values for test results"""
    PASS = "Pass"
    FAIL = "Fail"
    OOS = "OOS"
    INVALID = "Invalid"

class InvestigationPhase(str, Enum):
    """Phases of investigation"""
    PHASE1_LAB = "phase1_lab"
    PHASE2_QC = "phase2_qc"
    PHASE3_QA = "phase3_qa"

class DeviationSeverity(str, Enum):
    """Severity levels for deviations"""
    MINOR = "MINOR"
    MAJOR = "MAJOR"
    CRITICAL = "CRITICAL"

class DeviationStatus(str, Enum):
    """Status values for deviations"""
    OPEN = "OPEN"
    UNDER_INVESTIGATION = "UNDER_INVESTIGATION"
    CLOSED = "CLOSED"

class CapaActionType(str, Enum):
    """Types of CAPA actions"""
    CORRECTIVE = "CORRECTIVE"
    PREVENTIVE = "PREVENTIVE"
    BOTH = "BOTH"

class CapaStatus(str, Enum):
    """Status values for CAPA"""
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    CLOSED = "CLOSED"
    VERIFIED = "VERIFIED"
    CANCELLED = "CANCELLED"

class CapaTaskStatus(str, Enum):
    """Status values for CAPA tasks"""
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

class ProductStatus(str, Enum):
    """Status values for products"""
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
