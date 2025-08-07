export enum SampleStatus {
  LOGGED_IN = 'LOGGED_IN',
  IN_PROGRESS = 'IN_PROGRESS',
  COMPLETED = 'COMPLETED',
  ARCHIVED = 'ARCHIVED'
}

export enum TestStatus {
  PENDING = 'PENDING',
  IN_PROGRESS = 'IN_PROGRESS',
  COMPLETED = 'COMPLETED',
  CANCELLED = 'CANCELLED'
}

export enum SpecificationType {
  EXACT = 'EXACT',
  RANGE = 'RANGE',
  LESS_THAN = 'LESS_THAN',
  GREATER_THAN = 'GREATER_THAN'
}

export enum ParameterType {
  NUMERIC = 'NUMERIC',
  TEXT = 'TEXT',
  BOOLEAN = 'BOOLEAN',
  DATETIME = 'DATETIME'
}

export enum StepResult {
  PASS = 'PASS',
  FAIL = 'FAIL',
  NOT_APPLICABLE = 'NOT_APPLICABLE'
}

export enum ResultStatus {
  PASS = 'PASS',
  FAIL = 'FAIL',
  OOS = 'OUT_OF_SPECIFICATION',
  INVALID = 'INVALID'
}

export enum Priority {
  LOW = 'LOW',
  MEDIUM = 'MEDIUM',
  HIGH = 'HIGH',
  URGENT = 'URGENT'
}

export enum EquipmentStatus {
  AVAILABLE = 'AVAILABLE',
  IN_USE = 'IN_USE',
  UNDER_MAINTENANCE = 'UNDER_MAINTENANCE',
  OUT_OF_SERVICE = 'OUT_OF_SERVICE',
  QUARANTINED = 'QUARANTINED'
}
