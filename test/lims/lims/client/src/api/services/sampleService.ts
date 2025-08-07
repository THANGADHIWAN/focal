import apiClient from '../axiosConfig';
import { API_ENDPOINTS } from '../constants';
import {
    ApiResponse,
    SampleResponse,
    SampleListResponse,
    SampleCreateRequest,
    SampleUpdateRequest,
    Sample
} from '../types';

class SampleService {
    /**
     * Get all samples with pagination and filtering options
     */
    async getAllSamples(
        page = 1,
        limit = 10,
        filters?: {
            type?: string[],
            status?: string[],
            location?: string[],
            owner?: string[],
            search?: string
        }
    ): Promise<SampleListResponse> {
        // Prepare parameters for the API call
        const params = new URLSearchParams();
        params.append('page', page.toString());
        params.append('limit', limit.toString());

        // Add filters if provided
        if (filters) {
            if (filters.type && filters.type.length > 0) {
                filters.type.forEach(type => params.append('type', type));
            }
            if (filters.status && filters.status.length > 0) {
                filters.status.forEach(status => params.append('status', status));
            }
            if (filters.location && filters.location.length > 0) {
                filters.location.forEach(location => params.append('location', location));
            }
            if (filters.owner && filters.owner.length > 0) {
                filters.owner.forEach(owner => params.append('owner', owner));
            }
            if (filters.search) {
                params.append('search', filters.search);
            }
        }

        try {
            console.log('[SampleService] Fetching samples with params:', params.toString());
            const response = await apiClient.get<{ data: SampleListResponse, status: number, success: boolean }>(
                API_ENDPOINTS.SAMPLES.BASE,
                { params }
            );

            console.log('[SampleService] Samples response:', response.data);
            return response.data.data;
        } catch (error) {
            console.error('[SampleService] Error fetching samples:', error);
            throw error;
        }
    }

    /**
     * Get a sample by ID
     */
    async getSampleById(id: string): Promise<SampleResponse> {
        try {
            console.log('[SampleService] Fetching sample by ID:', id);
            const response = await apiClient.get<{ data: SampleResponse, status: number, success: boolean }>(
                API_ENDPOINTS.SAMPLES.BY_ID(id)
            );

            console.log('[SampleService] Sample response:', response.data);
            return response.data.data;
        } catch (error) {
            console.error('[SampleService] Error fetching sample by ID:', id, error);
            throw error;
        }
    }

    /**
     * Create a new sample
     */
    async createSample(sampleData: SampleCreateRequest): Promise<SampleResponse> {
        try {
            console.log('[SampleService] Creating sample:', sampleData);
            const response = await apiClient.post<{ data: SampleResponse, status: number, success: boolean }>(
                API_ENDPOINTS.SAMPLES.BASE,
                sampleData
            );

            console.log('[SampleService] Create sample response:', response.data);
            return response.data.data;
        } catch (error) {
            console.error('[SampleService] Error creating sample:', error);
            throw error;
        }
    }

    /**
     * Update an existing sample
     */
    async updateSample(id: string, sampleData: SampleUpdateRequest): Promise<SampleResponse> {
        try {
            console.log('[SampleService] Updating sample:', id, sampleData);
            const response = await apiClient.patch<{ data: SampleResponse, status: number, success: boolean }>(
                API_ENDPOINTS.SAMPLES.BY_ID(id),
                sampleData
            );

            console.log('[SampleService] Update sample response:', response.data);
            return response.data.data;
        } catch (error) {
            console.error('[SampleService] Error updating sample:', id, error);
            throw error;
        }
    }

    /**
     * Delete a sample by ID
     */
    async deleteSample(id: string): Promise<void> {
        try {
            console.log('[SampleService] Deleting sample:', id);
            await apiClient.delete(API_ENDPOINTS.SAMPLES.BY_ID(id));
            console.log('[SampleService] Sample deleted successfully:', id);
        } catch (error) {
            console.error('[SampleService] Error deleting sample:', id, error);
            throw error;
        }
    }

    /**
     * Export samples data as CSV
     */
    async exportSamples(
        filters?: {
            type?: string[],
            status?: string[],
            location?: string[],
            owner?: string[],
            search?: string
        }
    ): Promise<Blob> {
        const params = new URLSearchParams();

        // Add filters if provided
        if (filters) {
            if (filters.type && filters.type.length > 0) {
                filters.type.forEach(type => params.append('type', type));
            }
            if (filters.status && filters.status.length > 0) {
                filters.status.forEach(status => params.append('status', status));
            }
            if (filters.location && filters.location.length > 0) {
                filters.location.forEach(location => params.append('location', location));
            }
            if (filters.owner && filters.owner.length > 0) {
                filters.owner.forEach(owner => params.append('owner', owner));
            }
            if (filters.search) {
                params.append('search', filters.search);
            }
        }

        try {
            console.log('[SampleService] Exporting samples with params:', params.toString());
            const response = await apiClient.get(
                API_ENDPOINTS.SAMPLES.EXPORT,
                {
                    params,
                    responseType: 'blob'
                }
            );

            console.log('[SampleService] Export response received');
            return response.data;
        } catch (error) {
            console.error('[SampleService] Error exporting samples:', error);
            throw error;
        }
    }

    /**
     * Test API connection
     */
    async testConnection(): Promise<boolean> {
        try {
            console.log('[SampleService] Testing API connection...');
            const response = await apiClient.get('/health');
            console.log('[SampleService] Health check response:', response.data);
            return response.status === 200;
        } catch (error) {
            console.error('[SampleService] API connection test failed:', error);
            return false;
        }
    }
}

export default new SampleService();
