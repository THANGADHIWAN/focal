import { Equipment, EquipmentType, EquipmentStatus } from '../../types/equipment';

export interface BaseEquipment {
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
}

export interface NewEquipment extends BaseEquipment {
    calibration?: {
        lastDate: string;
        nextDate: string;
        calibratedBy: string;
    };
}

export interface EquipmentFilters {
    type?: EquipmentType[];
    status?: EquipmentStatus[];
    location?: string[];
    manufacturer?: string[];
    search?: string;
}
