// Define types for sample data
export interface Sample {
    id: number;
    sample_code: string;
    sample_name: string;
    sample_type_id: number;
    type_name: string;
    status: string;
    box_id?: number;
    volume_ml?: number;
    received_date?: string;
    due_date?: string;
    priority?: string;
    quantity?: number;
    is_aliquot?: boolean;
    number_of_aliquots?: number;
    created_by: string;
    created_at: string;
    updated_at?: string;
    purpose?: string;
    aliquots: Aliquot[];
}

export interface Aliquot {
    id: number;
    aliquot_code: string;
    volume_ml?: number;
    status: string;
    created_at: string;
    sample_id?: number;
    creation_date?: string;
    assigned_to?: string;
    created_by?: string;
    purpose?: string;
    tests: Test[];
}

export interface Test {
    id: string;
    sample_id?: string;
    aliquot_id?: string;
    test_master_id: string;
    test_name: string;
    analyst_id?: string;
    instrument_id?: string;
    scheduled_date?: string;
    start_date?: string;
    end_date?: string;
    status: string;
    remarks?: string;
    test_results: TestResult[];
}

export interface TestResult {
    id: number;
    test_id: number;
    test_parameter_id: number;
    result_value?: string;
    unit?: string;
    specification_limit?: string;
    result_status: string;
    result_date: string;
    remarks?: string;
}

// Sample create/update request types
export interface SampleCreateRequest {
    name: string;
    type: number;            // Sample type ID
    owner: string;           // Owner name
    box_id?: number;         // Box ID
    volume: number;          // Volume in mL
    notes?: string;          // Optional notes
}

export interface SampleUpdateRequest {
    name?: string;
    type?: number;
    status?: string;
    owner?: string;
    box_id?: number;
    volume?: number;
    notes?: string;
}

// Aliquot create/update request types
export interface AliquotCreateRequest {
    volume: number;
    purpose?: string;
    location?: string;
}

// Test create/update request types
export interface TestCreateRequest {
    test_master_id: number;
    analyst_id?: string;
    instrument_id?: number;
    scheduled_date?: string;
    remarks?: string;
}

export interface TestUpdateRequest {
    status?: string;
    start_date?: string;
    end_date?: string;
    remarks?: string;
}

// Response types
export interface ApiResponse<T> {
    data?: T;
    message?: string;
    status: number;
    success: boolean;
}
