import {
    Sample,
    Aliquot,
    Test,
    ApiResponse,
    SampleCreateRequest,
    SampleUpdateRequest,
    AliquotCreateRequest,
    TestCreateRequest,
    TestUpdateRequest
} from '../types/api';
import { BoxLocation } from '../types/sample';
import {
    Product,
    ProductCreateRequest,
    ProductUpdateRequest,
    ProductResponse,
    ProductListResponse,
    ProductSummary,
    ProductStatus,
    ProductApiResponse,
    ProductListApiResponse
} from './types/product';

// Re-export types
export type {
    Sample,
    Aliquot,
    Test,
    ApiResponse,
    SampleCreateRequest,
    SampleUpdateRequest,
    AliquotCreateRequest,
    TestCreateRequest,
    TestUpdateRequest,
    BoxLocation,
    Product,
    ProductCreateRequest,
    ProductUpdateRequest,
    ProductResponse,
    ProductListResponse,
    ProductSummary,
    ProductStatus,
    ProductApiResponse,
    ProductListApiResponse
};

// Paginated API Response
export interface PaginatedResponse<T> {
    data: T[];
    totalCount: number;
    totalPages: number;
    currentPage: number;
    pageSize: number;
    hasMore: boolean;
}

// Error Response
export interface ErrorResponse {
    message: string;
    errors?: Record<string, string[]>;
    status: number;
}

// Sample Related Types
export interface SampleResponse extends Sample { }
export interface SampleListResponse extends PaginatedResponse<Sample> { }

// Aliquot Related Types
export interface AliquotResponse extends Aliquot { }
export interface AliquotListResponse extends PaginatedResponse<Aliquot> { }

// Test Related Types
export interface TestResponse extends Test { }
export interface TestListResponse extends PaginatedResponse<Test> { }

// Metadata Types
export interface SampleType {
    id: number;
    value: string;
    description?: string;
}

export interface SampleStatus {
    id: number;
    value: string;
    description?: string;
}

export interface TestMethod {
    id: number;
    value: string;
    description?: string;
}

export interface TestStatus {
    id: number;
    value: string;
    description?: string;
}

export interface LabLocation {
    id: number;
    value: string;
    description?: string;
}

export interface User {
    id: number;
    value: string;
    email?: string;
}

export interface StorageLocation extends BoxLocation {
    id: number;
    name: string;
    capacity: number;
    availableSpaces: number;
}

export interface SampleVolume {
    sampleId: string;
    volume: number;
    location?: string;
}
