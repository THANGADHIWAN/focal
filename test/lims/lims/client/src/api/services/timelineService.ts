import apiClient from '../axiosConfig';
import { API_ENDPOINTS } from '../constants';

export interface TimelineEvent {
    id: string;
    event: string;
    date: string;
    user: string;
    entity_type: string;
    entity_id: string;
    old_value?: any;
    new_value?: any;
    justification?: string;
    ip_address?: string;
}

export interface TimelineResponse {
    data: TimelineEvent[];
    status: number;
    success: boolean;
}

class TimelineService {
    /**
     * Get timeline events for a sample
     */
    async getSampleTimeline(sampleId: string, limit: number = 50): Promise<TimelineEvent[]> {
        try {
            const response = await apiClient.get<TimelineResponse>(
                `${API_ENDPOINTS.SAMPLES.TIMELINE(sampleId)}?limit=${limit}`
            );
            return response.data.data;
        } catch (error) {
            console.error('Error fetching sample timeline:', error);
            throw error;
        }
    }

    /**
     * Get timeline events for an aliquot
     */
    async getAliquotTimeline(sampleId: string, aliquotId: string, limit: number = 50): Promise<TimelineEvent[]> {
        try {
            const response = await apiClient.get<TimelineResponse>(
                `${API_ENDPOINTS.SAMPLES.ALIQUOT_TIMELINE(sampleId, aliquotId)}?limit=${limit}`
            );
            return response.data.data;
        } catch (error) {
            console.error('Error fetching aliquot timeline:', error);
            throw error;
        }
    }

    /**
     * Get timeline events for a test
     */
    async getTestTimeline(sampleId: string, testId: string, limit: number = 50): Promise<TimelineEvent[]> {
        try {
            const response = await apiClient.get<TimelineResponse>(
                `${API_ENDPOINTS.SAMPLES.TEST_TIMELINE(sampleId, testId)}?limit=${limit}`
            );
            return response.data.data;
        } catch (error) {
            console.error('Error fetching test timeline:', error);
            throw error;
        }
    }
}

export default new TimelineService(); 