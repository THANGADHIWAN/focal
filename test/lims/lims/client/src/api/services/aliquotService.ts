import apiClient from '../axiosConfig';
import { API_ENDPOINTS } from '../constants';
import {
    AliquotResponse,
    AliquotCreateRequest
} from '../types';

class AliquotService {
    /**
     * Get all aliquots for a sample
     */
    async getAllAliquots(sampleId: string): Promise<AliquotResponse[]> {
        const response = await apiClient.get<{ data: AliquotResponse[], status: number, success: boolean }>(
            API_ENDPOINTS.SAMPLES.ALIQUOTS(sampleId)
        );

        return response.data.data;
    }

    /**
     * Get an aliquot by ID
     */
    async getAliquotById(sampleId: string, aliquotId: string): Promise<AliquotResponse | null> {
        const response = await apiClient.get<{ data: AliquotResponse, status: number, success: boolean }>(
            API_ENDPOINTS.SAMPLES.ALIQUOT(sampleId, aliquotId)
        );

        return response.data.data || null;
    }

    /**
     * Create a new aliquot for a sample
     */
    async createAliquot(sampleId: string, aliquotData: AliquotCreateRequest): Promise<AliquotResponse> {
        const response = await apiClient.post<{ data: AliquotResponse, status: number, success: boolean }>(
            API_ENDPOINTS.SAMPLES.ALIQUOTS(sampleId),
            { 
                ...aliquotData, 
                sample_id: parseInt(sampleId),
                aliquot_code: `ALQ-${Date.now()}`,
                status: "Logged_In",
                created_by: "Current User" // This should come from auth context
            }
        );

        return response.data.data;
    }

    /**
     * Update an aliquot's location
     */
    async updateAliquotLocation(
        sampleId: string,
        aliquotId: string,
        location: string
    ): Promise<AliquotResponse> {
        const response = await apiClient.patch<{ data: AliquotResponse, status: number, success: boolean }>(
            API_ENDPOINTS.SAMPLES.ALIQUOT_LOCATION(sampleId, aliquotId),
            { location }
        );

        return response.data.data;
    }

    /**
     * Delete an aliquot
     */
    async deleteAliquot(sampleId: string, aliquotId: string): Promise<void> {
        await apiClient.delete(API_ENDPOINTS.SAMPLES.ALIQUOT(sampleId, aliquotId));
    }
}

export default new AliquotService();
