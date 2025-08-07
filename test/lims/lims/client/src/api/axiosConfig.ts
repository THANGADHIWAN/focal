import axios from 'axios';
import mockApiHandler from './mockApiHandler';

// Set USE_MOCK_API to true for development mode
export const USE_MOCK_API = false;

// Get the API base URL from environment or use default
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
    timeout: 10000,
});

// Add request interceptor for logging
apiClient.interceptors.request.use(
    (config) => {
        console.log(`[API Request] ${config.method?.toUpperCase()} ${config.url}`, {
            baseURL: config.baseURL,
            data: config.data,
            params: config.params
        });
        return config;
    },
    (error) => {
        console.error('[API Request Error]', error);
        return Promise.reject(error);
    }
);

// Add mock interceptor if USE_MOCK_API is true
if (USE_MOCK_API) {
    apiClient.interceptors.request.use(
        async (config) => {
            try {
                console.log(`[Mock API Interceptor] Intercepting ${config.method} request to ${config.url}`);
                const response = await mockApiHandler(config);
                console.log('[Mock API Interceptor] Mock response:', response);
                return Promise.reject({
                    config,
                    response: { data: response, status: 200 }
                });
            } catch (error) {
                console.error('[Mock API Interceptor] Error:', error);
                return config;
            }
        }
    );
}

// Add response interceptor for error handling
apiClient.interceptors.response.use(
    response => {
        console.log(`[API Response] ${response.status} ${response.config.url}`, response.data);
        return response;
    },
    error => {
        // If the error has a response from our mock API, return it as a successful response
        if (error.response && error.config && USE_MOCK_API) {
            console.log('[Mock API Response] Returning mock response:', error.response);
            return error.response;
        }
        
        console.error('[API Error]', {
            message: error.message,
            status: error.response?.status,
            data: error.response?.data,
            url: error.config?.url,
            method: error.config?.method
        });
        
        return Promise.reject(error);
    }
);

export default apiClient;
