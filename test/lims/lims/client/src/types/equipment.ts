export interface Equipment {
    id: string;
    name: string;
    description?: string;
    type: EquipmentType;
    model: string;
    manufacturer: string;
    serialNumber: string;
    location: string;
    status: EquipmentStatus;
    assignedTo?: string;
    team?: string;
    calibration?: {
        lastDate: string;
        nextDate: string;
        calibratedBy: string;
    };
    maintenanceHistory: MaintenanceRecord[];
    notes: Note[];
    attachments: Attachment[];
}

export interface MaintenanceRecord {
    id: string;
    date: string;
    performedBy: string;
    task: string;
    status: string;
    notes: string;
}

export interface Note {
    id: string;
    content: string;
    timestamp: string;
    user: string;
}

export interface Attachment {
    id: string;
    name: string;
    type: string;
    url: string;
    uploadedAt: string;
}

/**
 * Equipment types supported by the system
 */
export interface EquipmentTypeDetail {
    id: number;
    value: string;
    description: string;
}

// Equipment type values from the server enum
export type EquipmentType =
    | 'HPLC'
    | 'Centrifuge'
    | 'Microscope'
    | 'PCR'
    | 'Spectrophotometer'
    | 'Balance'
    | 'pH Meter';

/**
 * Available equipment statuses
 */
export type EquipmentStatus =
  | 'Available'
  | 'In Use'
  | 'Under Maintenance'
  | 'Out of Service'
  | 'Quarantined';
