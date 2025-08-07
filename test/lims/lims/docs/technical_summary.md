# LIMS API Integration Technical Summary

This document summarizes the technical approach to resolving the integration issues between the frontend and backend.

## Integration Issues Resolved

### 1. Enum Usage

**Problem:** Backend uses string enums in `constants.py` for validation in schemas, while the frontend uses string literals.

**Solution:** 
- Created TypeScript enums in `src/types/enums.ts` that mirror the Python enums
- Updated frontend types to use these enums instead of string literals
- This provides better type safety and autocomplete in the frontend

**Implementation Files:**
- New: `client/src/types/enums.ts`
- Updated: `client/src/types/api.ts`

### 2. API Structure & Error Handling

**Problem:** Backend returns API responses in consistent format `{ data, status, success }`, but frontend doesn't handle errors consistently.

**Solution:**
- Enhanced axios interceptors to standardize error handling
- Created a utility function `handleApiResponse` to process API responses consistently
- Improved error handling in all API service methods

**Implementation Files:**
- Updated: `client/src/api/axiosConfig.ts`

### 3. Mock Integration

**Problem:** Frontend uses mock API handler with `USE_MOCK_API = true`, but the mock data structure doesn't match the actual backend responses.

**Solution:**
- Updated mock data to match the backend response structure
- Ensured all metadata endpoints return the correct value/label/description structure
- Updated mock handler to correctly simulate pagination and filtering

**Implementation Files:**
- Updated: `client/src/api/mockData.ts`
- Updated: `client/src/api/mockApiHandler.ts`

### 4. Data Model Transformations

**Problem:** Backend uses snake_case for field names (Python convention), while frontend uses camelCase (JavaScript/TypeScript convention).

**Solution:**
- Created utility functions for automatic transformation between cases
- Added axios interceptors to transform data on all requests and responses
- Created a comprehensive data transformation guide

**Implementation Files:**
- New: `client/src/utils/caseTransform.ts`
- Updated: `client/src/api/axiosConfig.ts`
- Documentation: `docs/data_transformation_guide.md`

### 5. Filter Parameters

**Problem:** Backend accepts multiple values for filters, but frontend URL encoding for arrays might not be correct.

**Solution:**
- Updated service methods to correctly handle array parameters
- Used URLSearchParams for proper query parameter encoding
- Added examples in the API documentation

**Implementation Files:**
- Updated: `client/src/api/services/sampleService.ts`
- Documentation: `docs/api_documentation.md`

## API Testing and Documentation

To validate the integration and provide comprehensive documentation, we've created:

1. **Enhanced API Test Script:**
   - `server/test_api.py`: Tests all endpoints and validates data formats
   - Tests proper handling of enums, case transformations, and filter parameters

2. **API Documentation:**
   - `docs/api_documentation.md`: Comprehensive documentation of all API endpoints
   - Includes request/response examples for all endpoints
   - Documents error handling and common response structures

3. **Workflow Validation Guide:**
   - `docs/workflow_validation_guide.md`: Step-by-step guide to test the full workflow
   - Validates the complete process from metadata to sample/test/aliquot CRUD

## Technical Implementation Overview

### Automatic Case Transformation

The most significant improvement is the automatic transformation between snake_case and camelCase:

```typescript
// Example of how axios interceptors handle case transformation

// Response interceptor (backend → frontend)
apiClient.interceptors.response.use(
  response => {
    if (response.data?.data) {
      response.data.data = snakeToCamel(response.data.data);
    }
    return response;
  }
);

// Request interceptor (frontend → backend)
apiClient.interceptors.request.use(
  config => {
    if (config.data) {
      config.data = camelToSnake(config.data);
    }
    return config;
  }
);
```

This approach allows the frontend to use camelCase and the backend to use snake_case without manual transformation in each service method.

### TypeScript Enum Integration

Created TypeScript enums that mirror the Python enums:

```typescript
// Python enum in constants.py
class SampleTypeEnum(str, enum.Enum):
    BLOOD = "Blood"
    TISSUE = "Tissue"
    # ...

// TypeScript enum in types/enums.ts
export enum SampleType {
    BLOOD = "Blood",
    TISSUE = "Tissue",
    // ...
}
```

This ensures type safety and consistency between frontend and backend.

### Proper Array Parameter Handling

Updated sample service to correctly handle array parameters:

```typescript
// For arrays, add multiple entries with the same key
if (filters.type?.length) {
  filters.type.forEach(type => params.append('type', type));
}
```

This correctly sends requests like `?type=Blood&type=Tissue` for array parameters.

## Conclusion

These changes ensure proper integration between the frontend and backend, with:

1. Type safety through consistent enum usage
2. Automatic data transformation between snake_case and camelCase
3. Proper handling of array parameters in API requests
4. Consistent error handling across all API calls
5. Comprehensive API documentation and testing

The implementation has been validated through:
- Automated API tests
- Manual workflow validation
- Documentation of API endpoints and examples

This approach significantly improves code maintainability and reduces integration issues.
