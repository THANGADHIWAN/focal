import apiClient from '../axiosConfig';
import { API_ENDPOINTS } from '../constants';
import {
    SampleType,
    SampleStatus,
    LabLocation,
    User,
    StorageLocation
} from '../types';

// Add new types for equipment
export interface Equipment {
    id: number;
    name: string;
    instrument_type: string;
    serial_number: string;
    manufacturer: string;
    model_number: string;
    purchase_date: string | null;
    location_id: number | null;
    status: string;
    qualification_status: string | null;
    maintenance_type: string | null;
    remarks: string | null;
}

export interface EquipmentType {
    id: number;
    value: string;
    description: string;
}

export interface EquipmentStatus {
    id: number;
    value: string;
    description: string;
}

export interface StorageHierarchy {
    storage_locations: Array<{
        id: number;
        location_name: string;
        location_code: string;
        storage_rooms: Array<{
            id: number;
            room_name: string;
            floor: number;
            building: string;
            freezers: Array<{
                id: number;
                freezer_name: string;
                freezer_type: string;
                boxes: Array<{
                    id: number;
                    box_code: string;
                    box_type: string;
                    capacity: number;
                    inventory_slots: Array<{
                        id: number;
                        slot_code: string;
                        is_occupied: boolean;
                        aliquot_id: number | null;
                    }>;
                }>;
            }>;
        }>;
    }>;
}

export interface AvailableSlot {
    id: number;
    slot_code: string;
    is_occupied: boolean;
    box_id: number;
    box: {
        id: number;
        box_code: string;
        freezer: {
            id: number;
            freezer_name: string;
        };
    };
}

export interface HealthStatus {
    database_connected: boolean;
    service_status: string;
}

class MetadataService {
    /**
     * Get all sample types for dropdown
     */
    async getSampleTypes(): Promise<SampleType[]> {
        const response = await apiClient.get<{ data: SampleType[], status: number, success: boolean }>(
            API_ENDPOINTS.METADATA.SAMPLE_TYPES
        );
        return response.data.data;
    }

    /**
     * Get all sample types from enum only
     */
    async getSampleTypesFromEnum(): Promise<SampleType[]> {
        const response = await apiClient.get<{ data: SampleType[], status: number, success: boolean }>(
            API_ENDPOINTS.METADATA.SAMPLE_TYPES_ENUM
        );
        return response.data.data;
    }

    /**
     * Get all sample statuses for dropdown
     */
    async getSampleStatuses(): Promise<SampleStatus[]> {
        const response = await apiClient.get<{ data: SampleStatus[], status: number, success: boolean }>(
            API_ENDPOINTS.METADATA.SAMPLE_STATUSES
        );
        return response.data.data;
    }

    /**
     * Get all lab locations for dropdown
     */
    async getLabLocations(): Promise<LabLocation[]> {
        const response = await apiClient.get<{ data: LabLocation[], status: number, success: boolean }>(
            API_ENDPOINTS.METADATA.LAB_LOCATIONS
        );
        return response.data.data;
    }

    /**
     * Get all users for dropdown
     */
    async getUsers(): Promise<User[]> {
        const response = await apiClient.get<{ data: User[], status: number, success: boolean }>(
            API_ENDPOINTS.METADATA.USERS
        );
        return response.data.data;
    }

    /**
     * Get all storage locations for dropdown
     */
    async getStorageLocations(): Promise<StorageLocation[]> {
        const response = await apiClient.get<{ data: StorageLocation[], status: number, success: boolean }>(
            API_ENDPOINTS.METADATA.STORAGE_LOCATIONS
        );
        return response.data.data;
    }

    /**
     * Get all equipment
     */
    async getEquipment(): Promise<Equipment[]> {
        const response = await apiClient.get<{ data: Equipment[], status: number, success: boolean }>(
            API_ENDPOINTS.METADATA.EQUIPMENT
        );
        return response.data.data;
    }

    /**
     * Get all equipment types from enum
     */
    async getEquipmentTypes(): Promise<EquipmentType[]> {
        const response = await apiClient.get<{ data: EquipmentType[], status: number, success: boolean }>(
            API_ENDPOINTS.METADATA.EQUIPMENT_TYPES
        );
        return response.data.data;
    }

    /**
     * Get all equipment statuses from enum
     */
    async getEquipmentStatuses(): Promise<EquipmentStatus[]> {
        const response = await apiClient.get<{ data: EquipmentStatus[], status: number, success: boolean }>(
            API_ENDPOINTS.METADATA.EQUIPMENT_STATUSES
        );
        return response.data.data;
    }

    /**
     * Get storage hierarchy
     */
    async getStorageHierarchy(): Promise<StorageHierarchy> {
        const response = await apiClient.get<{ data: StorageHierarchy, status: number, success: boolean }>(
            API_ENDPOINTS.STORAGE.HIERARCHY
        );
        return response.data.data;
    }

    /**
     * Get available storage slots
     */
    async getAvailableSlots(): Promise<AvailableSlot[]> {
        const response = await apiClient.get<{ data: AvailableSlot[], status: number, success: boolean }>(
            API_ENDPOINTS.STORAGE.AVAILABLE_SLOTS
        );
        return response.data.data;
    }

    /**
     * Check service health
     */
    async checkHealth(): Promise<HealthStatus> {
        const response = await apiClient.get<{ data: HealthStatus, status: number, success: boolean }>(
            API_ENDPOINTS.METADATA.HEALTH
        );
        return response.data.data;
    }

    /**
     * Get available storage boxes
     */
    async getAvailableBoxes(): Promise<StorageLocation[]> {
        const response = await apiClient.get<{ data: StorageLocation[], status: number, success: boolean }>(
            API_ENDPOINTS.STORAGE.BOXES
        );
        return response.data.data;
    }

    /**
     * Get all metadata in one call (for initialization)
     */
    async getAllMetadata(): Promise<{
        sampleTypes: SampleType[];
        sampleStatuses: SampleStatus[];
        labLocations: LabLocation[];
        users: User[];
        storageLocations: StorageLocation[];
        equipment: Equipment[];
        equipmentTypes: EquipmentType[];
        equipmentStatuses: EquipmentStatus[];
    }> {
        const response = await apiClient.get(
            API_ENDPOINTS.METADATA.ALL
        );
        return response.data;
    }
}

export default new MetadataService();
