import apiClient from '../axiosConfig';
import { API_ENDPOINTS } from '../constants';
import { ApiResponse } from '../types';

export interface StorageBox {
    id: number;
    name: string;
    code: string;
    freezer_id: number;
    drawer_number: number;
    rack_number: number;
    shelf_number: number;
    capacity: number;
    is_full: boolean;
    temperature?: string;
    notes?: string;
    created_by: string;
    created_at: string;
    updated_at?: string;
    freezer_name?: string;
    freezer_location?: string;
}

export interface Freezer {
    id: number;
    name: string;
    code: string;
    location: string;
    temperature_range?: string;
    maintenance_status?: string;
    notes?: string;
    created_by: string;
    created_at: string;
    updated_at?: string;
    boxes: StorageBox[];
}

export interface StorageHierarchy {
    hierarchy: {
        id: number;
        name: string;
        code: string;
        location: string;
        temperature_range?: string;
        boxes: {
            id: number;
            name: string;
            code: string;
            drawer_number: number;
            rack_number: number;
            shelf_number: number;
            capacity: number;
            is_full: boolean;
        }[];
    }[];
}

class StorageService {
    /**
     * Get all storage boxes with optional filtering
     */
    async getAllBoxes(
        skip = 0,
        limit = 100,
        freezerId?: number,
        search?: string
    ) {
        try {
            const params = new URLSearchParams();
            params.append('skip', skip.toString());
            params.append('limit', limit.toString());
            if (freezerId) params.append('freezer_id', freezerId.toString());
            if (search) params.append('search', search);

            const response = await apiClient.get<ApiResponse<StorageBox[]>>(
                `${API_ENDPOINTS.STORAGE.BOXES}`,
                { params }
            );
            return response.data;
        } catch (error) {
            console.error('Error fetching boxes:', error);
            throw error;
        }
    }

    /**
     * Get a box by ID
     */
    async getBoxById(id: number) {
        try {
            const response = await apiClient.get<ApiResponse<StorageBox>>(
                `${API_ENDPOINTS.STORAGE.BOXES}/${id}`
            );
            return response.data;
        } catch (error) {
            console.error('Error fetching box:', error);
            throw error;
        }
    }

    /**
     * Get all freezers with optional filtering
     */
    async getAllFreezers(
        skip = 0,
        limit = 100,
        location?: string,
        search?: string
    ) {
        try {
            const params = new URLSearchParams();
            params.append('skip', skip.toString());
            params.append('limit', limit.toString());
            if (location) params.append('location', location);
            if (search) params.append('search', search);

            const response = await apiClient.get<ApiResponse<Freezer[]>>(
                `${API_ENDPOINTS.STORAGE.FREEZERS}`,
                { params }
            );
            return response.data;
        } catch (error) {
            console.error('Error fetching freezers:', error);
            throw error;
        }
    }

    /**
     * Get complete storage hierarchy
     */
    async getStorageHierarchy() {
        try {
            const response = await apiClient.get<ApiResponse<StorageHierarchy>>(
                `${API_ENDPOINTS.STORAGE.HIERARCHY}`
            );
            return response.data;
        } catch (error) {
            console.error('Error fetching storage hierarchy:', error);
            throw error;
        }
    }
}
