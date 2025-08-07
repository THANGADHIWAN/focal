# Frontend-Backend Data Transformation Guide

This guide provides specific examples of data transformations needed between the frontend and backend.

## Key Data Transformation Issues

The backend uses snake_case (Python convention) while the frontend uses camelCase (JavaScript convention). This causes integration issues that need to be handled systematically.

## Common Backend to Frontend Transformations

| Backend (snake_case)  | Frontend (camelCase) |
|-----------------------|----------------------|
| `submission_date`     | `submissionDate`     |
| `volume_left`         | `volumeLeft`         |
| `total_volume`        | `totalVolume`        |
| `aliquots_created`    | `aliquotsCreated`    |
| `box_id`              | `boxId`              |
| `last_movement`       | `lastMovement`       |
| `created_at`          | `createdAt`          |
| `assigned_to`         | `assignedTo`         |
| `start_date`          | `startDate`          |
| `completion_date`     | `completionDate`     |
| `total_count`         | `totalCount`         |
| `total_pages`         | `totalPages`         |
| `current_page`        | `currentPage`        |
| `page_size`           | `pageSize`           |
| `has_more`            | `hasMore`            |

## Implementation Solutions

### 1. Utility Functions Approach

Create utility functions to automatically transform objects between snake_case and camelCase:

```typescript
// src/utils/caseTransform.ts

/**
 * Transforms an object's keys from snake_case to camelCase
 */
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

/**
 * Transforms an object's keys from camelCase to snake_case
 */
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

### 2. Axios Interceptors Approach

Add interceptors to automatically transform data on API requests and responses:

```typescript
// Add to src/api/axiosConfig.ts

import { snakeToCamel, camelToSnake } from '../utils/caseTransform';

// Response interceptor for backend→frontend transformation
apiClient.interceptors.response.use(
  response => {
    // Only transform if we have a successful response with data
    if (response.status >= 200 && response.status < 300 && response.data) {
      // Transform the data property which contains our actual response
      if (response.data.data) {
        response.data.data = snakeToCamel(response.data.data);
      }
    }
    return response;
  }
);

// Request interceptor for frontend→backend transformation
apiClient.interceptors.request.use(
  config => {
    // Only transform the request body, not query parameters
    if (config.data) {
      config.data = camelToSnake(config.data);
    }
    return config;
  }
);
```

### 3. Type Definitions with Transformation

Update your type definitions to account for the transformations:

```typescript
// src/types/api.ts

// Backend response types (snake_case)
export interface SampleResponse {
  id: string;
  name: string;
  type: string;
  submission_date: string;
  status: string;
  owner: string;
  box_id: string;
  location: string;
  last_movement: string;
  volume_left: number;
  total_volume: number;
  aliquots_created: number;
  aliquots: AliquotResponse[];
}

// Frontend model types (camelCase)
export interface Sample {
  id: string;
  name: string;
  type: string;
  submissionDate: string;
  status: string;
  owner: string;
  boxId: string;
  location: string;
  lastMovement: string;
  volumeLeft: number;
  totalVolume: number;
  aliquotsCreated: number;
  aliquots: Aliquot[];
}

// Type guard to convert SampleResponse to Sample
export function transformSample(response: SampleResponse): Sample {
  return {
    id: response.id,
    name: response.name,
    type: response.type,
    submissionDate: response.submission_date,
    status: response.status,
    owner: response.owner,
    boxId: response.box_id,
    location: response.location,
    lastMovement: response.last_movement,
    volumeLeft: response.volume_left,
    totalVolume: response.total_volume,
    aliquotsCreated: response.aliquots_created,
    aliquots: response.aliquots.map(transformAliquot)
  };
}
```

## Which Approach to Choose?

1. **Axios Interceptors**: Best for most applications as it centralizes transformation logic and works automatically.
   
2. **Utility Functions**: Good when you need manual control over transformations or have edge cases.
   
3. **Type Definitions**: Most verbose but provides the strongest type safety.

For this LIMS application, we recommend the Axios Interceptors approach because:

- It's centralized and requires minimal code changes
- It works automatically for all API calls
- It maintains clean data models in your application code

## Implementation Steps

1. Create the `caseTransform.ts` utility file
2. Add the interceptors to your Axios configuration
3. Update your mock API handler to work with camelCase on the frontend side
4. Test the transformations with real API calls

By implementing these changes, you'll ensure consistent data formats between your frontend and backend.
