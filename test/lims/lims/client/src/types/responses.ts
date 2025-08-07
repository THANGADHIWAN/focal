import { Sample } from './api';

export interface PaginatedResponse<T> {
    items: T[];
    total: number;
    page: number;
    limit: number;
    totalPages: number;
}

export type SampleListResponse = PaginatedResponse<Sample>;
export type SampleResponse = Sample;

export interface ApiError {
    message: string;
    status: number;
    errors?: Record<string, string[]>;
}
