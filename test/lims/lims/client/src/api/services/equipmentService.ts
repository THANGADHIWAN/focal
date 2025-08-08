import apiClient from '../axiosConfig';
import { API_ENDPOINTS } from '../constants';
import { Equipment, EquipmentType, EquipmentStatus } from '../../types/equipment';

class EquipmentService {
    /**
     * Get all equipment with pagination and filtering
     */
    async getAllEquipment(params: {
        page?: number;
        limit?: number;
        type?: string;
        status?: string;
        location?: string;
        manufacturer?: string;
        search?: string;
        sortBy?: string;
        sortOrder?: 'asc' | 'desc';
    } = {}): Promise<{ 
        data: Equipment[],
        pagination: {
            currentPage: number;
            totalPages: number;
            totalItems: number;
            itemsPerPage: number;
            hasMore: boolean;
        } 
    }> {
        const response = await apiClient.get<{
            data: Equipment[],
            pagination: {
                currentPage: number;
                totalPages: number;
                totalItems: number;
                itemsPerPage: number;
                hasMore: boolean;
            },
            status: number,
            success: boolean
        }>(
            API_ENDPOINTS.METADATA.EQUIPMENT,
            { params }
        );
        return {
            data: response.data.data,
            pagination: response.data.pagination
        };
    }

    /**
     * Create new equipment
     */
    async createEquipment(data: Partial<Equipment>): Promise<Equipment> {
        const response = await apiClient.post<{ data: Equipment, status: number, success: boolean }>(
            API_ENDPOINTS.METADATA.EQUIPMENT,
            data
        );
        return response.data.data;
    }

    /**
     * Update equipment
     */
    async updateEquipment(id: string, updates: Partial<Equipment>): Promise<Equipment> {
        const response = await apiClient.put<{ data: Equipment, status: number, success: boolean }>(
            `${API_ENDPOINTS.METADATA.EQUIPMENT}/${id}`,
            updates
        );
        return response.data.data;
    }

    /**
     * Delete equipment
     */
    async deleteEquipment(id: string): Promise<void> {
        await apiClient.delete(`${API_ENDPOINTS.METADATA.EQUIPMENT}/${id}`);
    }

    /**
     * Get equipment types
     */
    async getEquipmentTypes(): Promise<EquipmentType[]> {
        const response = await apiClient.get<{ data: EquipmentType[], status: number, success: boolean }>(
            API_ENDPOINTS.METADATA.EQUIPMENT_TYPES
        );
        return response.data.data;
    }

    /**
     * Get equipment statuses
     */
    async getEquipmentStatuses(): Promise<EquipmentStatus[]> {
        const response = await apiClient.get<{ data: EquipmentStatus[], status: number, success: boolean }>(
            API_ENDPOINTS.METADATA.EQUIPMENT_STATUSES
        );
        return response.data.data;
    }

    /**
     * Add maintenance record
     */
    async addMaintenanceRecord(
        equipmentId: string,
        record: {
            date: string;
            performedBy: string;
            task: string;
            status: string;
            notes?: string;
        }
    ): Promise<Equipment> {
        const response = await apiClient.post<{ data: Equipment, status: number, success: boolean }>(
            `${API_ENDPOINTS.METADATA.EQUIPMENT}/${equipmentId}/maintenance`,
            record
        );
        return response.data.data;
    }

    /**
     * Add note to equipment
     */
    async addNote(equipmentId: string, note: { content: string, user: string }): Promise<Equipment> {
        const response = await apiClient.post<{ data: Equipment, status: number, success: boolean }>(
            `${API_ENDPOINTS.METADATA.EQUIPMENT}/${equipmentId}/notes`,
            note
        );
        return response.data.data;
    }

    /**
     * Add attachment to equipment
     */
    async addAttachment(equipmentId: string, attachment: FormData): Promise<Equipment> {
        const response = await apiClient.post<{ data: Equipment, status: number, success: boolean }>(
            `${API_ENDPOINTS.METADATA.EQUIPMENT}/${equipmentId}/attachments`,
            attachment,
            {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            }
        );
        return response.data.data;
    }
}

export default new EquipmentService();
