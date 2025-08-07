import apiClient from '../axiosConfig';
import { API_ENDPOINTS } from '../constants';
import {
    TestResponse,
    TestCreateRequest,
    TestUpdateRequest
} from '../types';

class TestService {
    /**
     * Get all tests for an aliquot
     */
    async getAllTests(sampleId: string, aliquotId: string): Promise<TestResponse[]> {
        const response = await apiClient.get<{ data: TestResponse[], status: number, success: boolean }>(
            API_ENDPOINTS.SAMPLES.TESTS(sampleId, aliquotId)
        );

        return response.data.data;
    }

    /**
     * Get a test by ID
     */
    async getTestById(sampleId: string, aliquotId: string, testId: string): Promise<TestResponse | null> {
        const response = await apiClient.get<{ data: TestResponse, status: number, success: boolean }>(
            API_ENDPOINTS.SAMPLES.TEST(sampleId, aliquotId, testId)
        );

        return response.data.data || null;
    }

    /**
     * Create a new test for an aliquot
     */
    async createTest(
        sampleId: string,
        aliquotId: string,
        testData: TestCreateRequest
    ): Promise<TestResponse> {
        const response = await apiClient.post<{ data: TestResponse, status: number, success: boolean }>(
            API_ENDPOINTS.SAMPLES.TESTS(sampleId, aliquotId),
            { 
                ...testData, 
                sample_id: parseInt(sampleId),
                aliquot_id: parseInt(aliquotId),
                status: "Pending"
            }
        );

        return response.data.data;
    }

    /**
     * Update an existing test
     */
    async updateTest(
        sampleId: string,
        aliquotId: string,
        testId: string,
        updates: TestUpdateRequest
    ): Promise<TestResponse> {
        const response = await apiClient.patch<{ data: TestResponse, status: number, success: boolean }>(
            API_ENDPOINTS.SAMPLES.TEST(sampleId, aliquotId, testId),
            updates
        );

        return response.data.data;
    }

    /**
     * Delete a test
     */
    async deleteTest(
        sampleId: string,
        aliquotId: string,
        testId: string
    ): Promise<void> {
        await apiClient.delete(
            API_ENDPOINTS.SAMPLES.TEST(sampleId, aliquotId, testId)
        );
    }

    /**
     * Get all available test methods
     */
    async getTestMethods(): Promise<any[]> {
        const response = await apiClient.get<{ data: any[], status: number, success: boolean }>(
            API_ENDPOINTS.TESTS.METHODS
        );

        return response.data.data;
    }
}

export default new TestService();
