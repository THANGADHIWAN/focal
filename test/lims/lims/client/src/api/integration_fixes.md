# Frontend-Backend Integration Fixes

This document outlines the necessary changes to fix the integration issues between the frontend and backend.

## 1. Enum Usage

The backend uses string enums in `constants.py` for validation in schemas, while the frontend uses string literals. We should create TypeScript enums to match the backend.

```typescript
// Create this file at: src/types/enums.ts

export enum SampleType {
  BLOOD = "Blood",
  TISSUE = "Tissue",
  URINE = "Urine",
  SALIVA = "Saliva",
  CULTURE = "Culture",
  ENVIRONMENTAL = "Environmental",
  OTHER = "Other"
}

export enum SampleStatus {
  SUBMITTED = "submitted",
  ALIQUOTS_CREATED = "aliquots_created",
  ALIQUOTS_PLATED = "aliquots_plated",
  TESTING_COMPLETED = "testing_completed",
  IN_STORAGE = "in_storage"
}

export enum TestStatus {
  PENDING = "pending",
  IN_PROGRESS = "in_progress",
  COMPLETED = "completed",
  FAILED = "failed"
}

export enum Location {
  LAB_1 = "Lab 1",
  LAB_2 = "Lab 2",
  LAB_3 = "Lab 3",
  STORAGE_ROOM = "Storage Room",
  FREEZER = "Freezer",
  REFRIGERATOR = "Refrigerator"
}
```

Then update the API types to use these enums:

```typescript
// Update src/types/api.ts
import { SampleType, SampleStatus, TestStatus, Location } from './enums';

export interface Sample {
  id: string;
  name: string;
  type: SampleType;  // Use enum instead of string
  submissionDate: string;
  status: SampleStatus;  // Use enum instead of string literal union
  owner: string;
  boxId: string;
  location: Location;  // Use enum instead of string
  lastMovement: string;
  volumeLeft: number;
  totalVolume: number;
  aliquotsCreated: number;
  aliquots: Aliquot[];
}

// Update other interfaces similarly
```

## 2. API Structure & Error Handling

Create a consistent error handler for API responses:

```typescript
// Add to src/api/axiosConfig.ts

interface ApiErrorResponse {
  detail?: string | Record<string, string[]>;
  status: number;
  success: false;
}

// Enhance the response interceptor
apiClient.interceptors.response.use(
  response => response,
  error => {
    // If the error has a response from our mock API, return it as a successful response
    if (error.response && error.config && USE_MOCK_API) {
      console.log('[Mock API Response] Returning mock response:', error.response);
      return error.response;
    }

    // Standardize error format for frontend
    const errorResponse: ApiErrorResponse = {
      status: error.response?.status || 500,
      success: false,
      detail: error.response?.data?.detail || 'An unknown error occurred'
    };

    console.error('[API Error]', errorResponse);
    return Promise.reject(errorResponse);
  }
);

// Create a utility function for API response handling
export function handleApiResponse<T>(promise: Promise<any>): Promise<T> {
  return promise.then(response => {
    if (response.data.success === false) {
      return Promise.reject(response.data);
    }
    return response.data.data;
  });
}
```

## 3. Mock Data Structure

Update mock data to match backend responses:

```typescript
// Update src/api/mockData.ts

export const mockSampleTypes = [
  { value: "Blood", label: "Blood", description: "Blood sample" },
  { value: "Tissue", label: "Tissue", description: "Tissue sample" },
  // ...other types
];

export const mockSampleStatuses = [
  { value: "submitted", label: "Submitted", description: "Sample has been submitted" },
  { value: "aliquots_created", label: "Aliquots Created", description: "Aliquots have been created from this sample" },
  // ...other statuses
];
```

Update the mock handler to return the correct structure:

```typescript
// Update in mockApiHandler.ts

// For metadata endpoints
if (url.includes('/metadata/sample-types')) {
  return {
    data: mockSampleTypes,
    status: 200,
    success: true
  };
}
```

## 4. Data Model Transformations

Create a utility to handle snake_case to camelCase conversions:

```typescript
// Create at: src/utils/apiTransform.ts

export function snakeToCamel(obj: any): any {
  if (obj === null || typeof obj !== 'object') {
    return obj;
  }

  if (Array.isArray(obj)) {
    return obj.map(item => snakeToCamel(item));
  }

  return Object.keys(obj).reduce((acc, key) => {
    const camelKey = key.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase());
    acc[camelKey] = snakeToCamel(obj[key]);
    return acc;
  }, {} as Record<string, any>);
}

export function camelToSnake(obj: any): any {
  if (obj === null || typeof obj !== 'object') {
    return obj;
  }

  if (Array.isArray(obj)) {
    return obj.map(item => camelToSnake(item));
  }

  return Object.keys(obj).reduce((acc, key) => {
    const snakeKey = key.replace(/([A-Z])/g, "_$1").toLowerCase();
    acc[snakeKey] = camelToSnake(obj[key]);
    return acc;
  }, {} as Record<string, any>);
}
```

Then add an axios interceptor to transform data:

```typescript
// Add to axiosConfig.ts

import { snakeToCamel, camelToSnake } from '../utils/apiTransform';

// Add response interceptor for case transformation
apiClient.interceptors.response.use(
  response => {
    if (response.data && response.data.data) {
      // Transform snake_case to camelCase
      response.data.data = snakeToCamel(response.data.data);
    }
    return response;
  }
);

// Add request interceptor for case transformation
apiClient.interceptors.request.use(
  config => {
    if (config.data) {
      // Transform camelCase to snake_case
      config.data = camelToSnake(config.data);
    }
    return config;
  }
);
```

## 5. Filter Parameters

Update the sample service to correctly handle array parameters:

```typescript
// Update src/api/services/sampleService.ts

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
  // Create URLSearchParams object
  const params = new URLSearchParams();
  params.append('page', page.toString());
  params.append('limit', limit.toString());

  // Add filters with proper array handling
  if (filters) {
    // For arrays, add multiple entries with the same key
    if (filters.type?.length) {
      filters.type.forEach(type => params.append('type', type));
    }
    if (filters.status?.length) {
      filters.status.forEach(status => params.append('status', status));
    }
    if (filters.location?.length) {
      filters.location.forEach(location => params.append('location', location));
    }
    if (filters.owner?.length) {
      filters.owner.forEach(owner => params.append('owner', owner));
    }
    if (filters.search) {
      params.append('search', filters.search);
    }
  }

  // Use the URLSearchParams object directly
  const response = await apiClient.get<{ data: SampleListResponse, status: number, success: boolean }>(
    API_ENDPOINTS.SAMPLES.BASE,
    { params }
  );

  return response.data.data;
}
```

## Implementation Plan

1. Create the enums file first
2. Update the API types to use these enums
3. Add the API transformation utilities
4. Update the axios interceptors
5. Fix the mock data structure
6. Update service methods to properly handle array parameters

These changes will ensure proper integration between the frontend and backend APIs.
