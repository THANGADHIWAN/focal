"""
Equipment and maintenance related constants
"""
from enum import Enum

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

class MaintenanceType(str, Enum):
    """Types of maintenance activities"""
    PREVENTIVE = "Preventive"
    CORRECTIVE = "Corrective"
    CALIBRATION = "Calibration"
    CLEANING = "Cleaning"
    INSPECTION = "Inspection"

class MaintenanceStatus(str, Enum):
    """Status values for maintenance activities"""
    SCHEDULED = "Scheduled"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    OVERDUE = "Overdue"

class CalibrationStatus(str, Enum):
    """Status values for calibration"""
    VALID = "Valid"
    EXPIRED = "Expired"
    DUE_SOON = "Due Soon"
    OVERDUE = "Overdue"
    NOT_REQUIRED = "Not Required"

class QualificationStatus(str, Enum):
    """Status values for equipment qualification"""
    QUALIFIED = "Qualified"
    PENDING = "Pending"
    FAILED = "Failed"
    NOT_REQUIRED = "Not Required"
