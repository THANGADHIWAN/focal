"""
Audit and approval related constants
"""
from enum import Enum

class AuditAction(str, Enum):
    """Actions tracked in audit logs"""
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    VIEW = "VIEW"

class ValidationStatus(str, Enum):
    """Validation status values"""
    VALID = "VALID"
    INVALID = "INVALID"
    PENDING = "PENDING"
    EXPIRED = "EXPIRED"

class ApprovalStatus(str, Enum):
    """Approval status values"""
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    REVIEW = "REVIEW"
