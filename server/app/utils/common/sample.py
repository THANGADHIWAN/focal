"""
Sample management related constants
"""
from enum import Enum

class SampleStatus(str, Enum):
    """Status values for samples"""
    LOGGED_IN = "LOGGED_IN"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    ARCHIVED = "ARCHIVED"

class SampleCategory(str, Enum):
    """Categories of samples"""
    RAW_MATERIAL = "RAW_MATERIAL"
    IN_PROCESS = "IN_PROCESS"
    FINISHED_PRODUCT = "FINISHED_PRODUCT"
    STABILITY = "STABILITY"
    ENVIRONMENTAL = "ENVIRONMENTAL"

class SampleType(str, Enum):
    """Types of samples"""
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

class StorageCondition(str, Enum):
    """Storage conditions for samples"""
    ROOM_TEMP = "ROOM_TEMPERATURE"
    REFRIGERATED = "REFRIGERATED"
    FROZEN = "FROZEN"
    INCUBATED = "INCUBATED"
    CONTROLLED = "CONTROLLED"
