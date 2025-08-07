import apiClient from '../axiosConfig';
import { API_ENDPOINTS } from '../constants';
import {
    ProductResponse,
    ProductListResponse,
    ProductCreateRequest,
    ProductUpdateRequest,
    ProductSummary,
    ProductListApiResponse,
    ProductApiResponse,
    ApiResponse
} from '../types/product';

class ProductService {
    /**
     * Test API connection
     */
    async testConnection(): Promise<boolean> {
        try {
            // Test connection with minimal parameters
            await apiClient.get(API_ENDPOINTS.PRODUCTS.BASE, { 
                params: { page: 1, limit: 1 },
                timeout: 5000 
            });
            return true;
        } catch (error: any) {
            // Only consider it a connection failure if it's a network/timeout error
            // Don't treat 4xx errors as connection failures
            if (error.code === 'ECONNREFUSED' || error.code === 'ENOTFOUND' || error.code === 'TIMEOUT') {
                console.error('[ProductService] Connection test failed:', error);
                return false;
            }
            // For other errors (like 400, 401, etc.), consider connection successful
            return true;
        }
    }

    /**
     * Get all products with pagination and filtering options
     */
    async getAllProducts(
        page = 1,
        limit = 10,
        filters?: {
            status?: string[],
            search?: string,
            created_from?: string,
            created_to?: string
        }
    ): Promise<ProductListResponse> {
        // Prepare parameters for the API call
        const params = new URLSearchParams();
        params.append('page', page.toString());
        params.append('limit', limit.toString());

        // Add filters if provided
        if (filters) {
            if (filters.status && filters.status.length > 0) {
                filters.status.forEach(status => params.append('status', status));
            }
            if (filters.search) {
                params.append('search', filters.search);
            }
            if (filters.created_from) {
                params.append('created_from', filters.created_from);
            }
            if (filters.created_to) {
                params.append('created_to', filters.created_to);
            }
        }

        try {
            console.log('[ProductService] Fetching products with params:', params.toString());
            const response = await apiClient.get<ProductListApiResponse>(
                API_ENDPOINTS.PRODUCTS.BASE,
                { params }
            );
            console.log('[ProductService] Products response:', response.data);
            
            // Return empty list response if no data
            if (!response.data.data) {
                return {
                    items: [],
                    total: 0,
                    page: page,
                    size: limit,
                    pages: 0
                };
            }
            
            return response.data.data;
        } catch (error: any) {
            if (error.response?.data?.error) {
                console.error('[ProductService] API error:', error.response.data.error);
                throw new Error(error.response.data.error);
            }
            console.error('[ProductService] Error fetching products:', error);
            throw error;
        }
    }

    /**
     * Get a specific product by ID
     */
    async getProductById(productId: string): Promise<ProductResponse | null> {
        try {
            const response = await apiClient.get<ProductApiResponse>(
                API_ENDPOINTS.PRODUCTS.BY_ID(productId)
            );
            return response.data.data;
        } catch (error: any) {
            if (error.response?.status === 404) {
                console.info('[ProductService] Product not found:', productId);
                return null;
            }
            if (error.response?.data?.error) {
                console.error('[ProductService] API error:', error.response.data.error);
                throw new Error(error.response.data.error);
            }
            console.error('[ProductService] Error fetching product:', error);
            throw error;
        }
    }

    /**
     * Create a new product
     */
    async createProduct(productData: ProductCreateRequest): Promise<ProductResponse> {
        try {
            const response = await apiClient.post<ProductApiResponse>(
                API_ENDPOINTS.PRODUCTS.BASE,
                productData
            );
            return response.data.data;
        } catch (error) {
            console.error('[ProductService] Error creating product:', error);
            throw error;
        }
    }

    /**
     * Update an existing product
     */
    async updateProduct(productId: string, productData: ProductUpdateRequest): Promise<ProductResponse> {
        try {
            const response = await apiClient.put<ProductApiResponse>(
                API_ENDPOINTS.PRODUCTS.BY_ID(productId),
                productData
            );
            return response.data.data;
        } catch (error) {
            console.error('[ProductService] Error updating product:', error);
            throw error;
        }
    }

    /**
     * Delete a product
     */
    async deleteProduct(productId: string): Promise<boolean> {
        try {
            await apiClient.delete(API_ENDPOINTS.PRODUCTS.BY_ID(productId));
            return true;
        } catch (error) {
            console.error('[ProductService] Error deleting product:', error);
            throw error;
        }
    }

    /**
     * Get product summaries (for dropdowns)
     */
    async getProductSummaries(): Promise<ProductSummary[]> {
        try {
            const response = await apiClient.get<ApiResponse>(
                API_ENDPOINTS.PRODUCTS.SUMMARIES
            );
            return response.data.data;
        } catch (error) {
            console.error('[ProductService] Error fetching product summaries:', error);
            throw error;
        }
    }

    /**
     * Get all samples for a specific product
     */
    async getProductSamples(productId: string): Promise<any[]> {
        try {
            const response = await apiClient.get<ApiResponse>(
                API_ENDPOINTS.PRODUCTS.SAMPLES(productId)
            );
            return response.data.data.samples || [];
        } catch (error) {
            console.error('[ProductService] Error fetching product samples:', error);
            throw error;
        }
    }

    /**
     * Get all tests for a specific product
     */
    async getProductTests(productId: string): Promise<any[]> {
        try {
            const response = await apiClient.get<ApiResponse>(
                API_ENDPOINTS.PRODUCTS.TESTS(productId)
            );
            return response.data.data.tests || [];
        } catch (error) {
            console.error('[ProductService] Error fetching product tests:', error);
            throw error;
        }
    }
}

export default new ProductService();