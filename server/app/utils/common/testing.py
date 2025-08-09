"""
Testing and results related constants
"""
from enum import Enum

class TestStatus(str, Enum):
    """Status values for tests"""
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

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

class StepResult(str, Enum):
    """Results for test steps"""
    PASS = "PASS"
    FAIL = "FAIL"
    NA = "NOT_APPLICABLE"

class ResultStatus(str, Enum):
    """Status values for test results"""
    PASS = "PASS"
    FAIL = "FAIL"
    OOS = "OUT_OF_SPECIFICATION"
    INVALID = "INVALID"
