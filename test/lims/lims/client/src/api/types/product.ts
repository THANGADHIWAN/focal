import { ApiResponse, PaginatedResponse } from '../types';

// Product Status Enum (must match backend enum values)
export type ProductStatus = 'NOT_STARTED' | 'IN_PROGRESS' | 'COMPLETED';

// Base Product Interface
export interface Product {
    id: number;
    product_code: string;
    name: string;
    description?: string;
    status: ProductStatus;
    created_at: string;
    updated_at: string;
    sample_count?: number;
    test_count?: number;
}

// Product Create Request
export interface ProductCreateRequest {
    product_name: string;
    description?: string;
    status?: ProductStatus;
}

// Product Update Request
export interface ProductUpdateRequest {
    name?: string;
    description?: string;
    status?: ProductStatus;
}

// Product Summary (for dropdowns)
export interface ProductSummary {
    id: number;
    product_code: string;
    name: string;
    status: ProductStatus;
}

// API Response Types
export interface ProductResponse extends Product {}

export interface ProductListResponse {
    items: Product[];
    total: number;
    page: number;
    size: number;
    pages: number;
}

export interface ProductApiResponse extends ApiResponse {
    data: Product;
}

export interface ProductListApiResponse extends ApiResponse {
    data: ProductListResponse;
}