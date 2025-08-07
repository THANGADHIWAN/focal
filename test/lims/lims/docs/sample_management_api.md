# Sample Management Module API Documentation

This document provides comprehensive information about the Sample Management module APIs, including data types, request/response structures, and endpoints.

## Table of Contents
1. [Data Models](#data-models)
2. [API Services](#api-services)
   - [Sample Service](#sample-service)
   - [Aliquot Service](#aliquot-service)
   - [Test Service](#test-service)
   - [Metadata Service](#metadata-service)
3. [API Endpoints](#api-endpoints)
4. [Request/Response Examples](#requestresponse-examples)

## Data Models

### Sample
```typescript
interface Sample {
    id: string;                  // Unique identifier for the sample
    name: string;                // Name/identifier of the sample
    type: string;                // Type of sample (blood, tissue, etc.)
    submissionDate: string;      // ISO date string of when sample was submitted
    status: 'submitted' | 'aliquots_created' | 'aliquots_plated' | 'testing_completed' | 'in_storage';  // Current status
    owner: string;               // Person who submitted/owns the sample
    boxId: string;               // Storage box identifier
    location: string;            // Physical location of the sample
    lastMovement: string;        // ISO date string of last time sample was moved
    volumeLeft: number;          // Remaining volume after aliquots created
    totalVolume: number;         // Original total volume
    aliquotsCreated: number;     // Number of aliquots created from this sample
    aliquots: Aliquot[];         // List of aliquots associated with this sample
}
```

### Aliquot
```typescript
interface Aliquot {
    id: string;                  // Unique identifier for the aliquot
    volume: number;              // Volume of the aliquot
    createdAt: string;           // ISO date string of when aliquot was created
    location: string;            // Physical location of the aliquot
    tests: Test[];               // List of tests performed on this aliquot
}
```

### Test
```typescript
interface Test {
    id: string;                  // Unique identifier for the test
    name: string;                // Name of the test
    status: 'Pending' | 'In Progress' | 'Completed' | 'Failed';  // Current status of the test
    assignedTo: string;          // Person assigned to perform the test
    startDate: string;           // ISO date string of when test was started
    completionDate?: string;     // Optional ISO date string of when test was completed
    method: string;              // Method used for the test
    results?: string;            // Optional test results
    notes?: string;              // Optional notes about the test
}
```

### Box Location
```typescript
interface BoxLocation {
  drawer: string;                // Drawer identifier
  rack: string;                  // Rack identifier
  shelf: string;                 // Shelf identifier
  freezer: string;               // Freezer identifier
  lab: string;                   // Lab location
}
```

### Metadata Types
```typescript
interface SampleType {
    id: string;                  // Unique identifier for the sample type
    name: string;                // Name of the sample type (e.g., "Blood", "Tissue")
    description?: string;        // Optional description of the sample type
}

interface SampleStatus {
    id: string;                  // Unique identifier for the status
    name: string;                // Name of the status (e.g., "submitted", "in_storage")
    description?: string;        // Optional description of what the status means
}

interface LabLocation {
    id: string;                  // Unique identifier for the lab location
    name: string;                // Name of the lab location (e.g., "Lab 1", "Lab 2")
    description?: string;        // Optional description of the lab location
}

interface User {
    id: string;                  // Unique identifier for the user
    name: string;                // User's full name
    email: string;               // User's email address
    role: string;                // User's role in the system
}

interface StorageLocation extends BoxLocation {
    id: string;                  // Unique identifier for the storage location
    name: string;                // Name of the storage location
    capacity: number;            // Total capacity of this storage location
    availableSpaces: number;     // Number of available spaces in this location
}
```

### Request/Response Types

#### Sample Requests
```typescript
interface SampleCreateRequest {
    name: string;                // Name/identifier of the sample
    type: string;                // Type of sample (blood, tissue, etc.)
    owner: string;               // Person who submitted/owns the sample
    boxId?: string;              // Optional storage box identifier
    volume: number;              // Original total volume
    notes?: string;              // Optional notes about the sample
}

interface SampleUpdateRequest {
    name?: string;               // Optional updated name
    type?: string;               // Optional updated type
    status?: string;             // Optional updated status
    owner?: string;              // Optional updated owner
    boxId?: string;              // Optional updated box identifier
    location?: string;           // Optional updated location
    notes?: string;              // Optional updated notes
}
```

#### Aliquot Requests
```typescript
interface AliquotCreateRequest {
    sampleId: string;            // ID of the parent sample
    volume: number;              // Volume of the aliquot
    location?: string;           // Optional location for the aliquot
}
```

#### Test Requests
```typescript
interface TestCreateRequest {
    name: string;                // Name of the test
    method: string;              // Method used for the test
    assignedTo?: string;         // Optional person assigned to the test
    notes?: string;              // Optional notes about the test
}

interface TestUpdateRequest {
    status?: 'Pending' | 'In Progress' | 'Completed' | 'Failed';  // Optional updated status
    results?: string;            // Optional test results
    notes?: string;              // Optional updated notes
    completionDate?: string;     // Optional completion date
}
```

#### API Response
```typescript
interface ApiResponse<T> {
    data?: T;                    // Response data of generic type T
    message?: string;            // Optional message from the server
    status: number;              // HTTP status code
    success: boolean;            // Whether the request was successful
}
```

#### Paginated Response
```typescript
interface PaginatedResponse<T> {
    data: T[];                   // Array of items of type T
    totalCount: number;          // Total number of items
    totalPages: number;          // Total number of pages
    currentPage: number;         // Current page number
    pageSize: number;            // Number of items per page
    hasMore: boolean;            // Whether there are more pages
}
```

## Pagination and Filtering

The Sample Management API supports comprehensive filtering and pagination options:

### Pagination Parameters
- **page**: Page number (default: 1)
- **limit**: Number of items per page (default: 10)

### Filter Parameters
- **type**: Filter samples by type (array of strings)
- **status**: Filter samples by status (array of strings)
- **location**: Filter samples by location (array of strings)
- **owner**: Filter samples by owner (array of strings)
- **search**: Text search across sample name, type, and owner fields (string)

Sample API endpoints that support these filters:
- `GET /samples` (getAllSamples)
- `GET /samples/export` (exportSamples)

### Example Filter Query
```
GET /samples?page=1&limit=20&type=Blood&status=submitted&owner=John%20Doe&search=A123
```

This would return the first page (20 items per page) of blood samples in submitted status, owned by John Doe, with "A123" in their name, type, or owner.

## API Services

### Sample Service

#### Methods

1. **getAllSamples**
   - **Purpose**: Get all samples with pagination and filtering options
   - **Parameters**:
     - page (number, default: 1): Page number for pagination
     - limit (number, default: 10): Number of items per page
     - filters (optional): Object containing filter criteria
       - type (string[]): Filter by sample types
       - status (string[]): Filter by sample statuses
       - location (string[]): Filter by locations
       - owner (string[]): Filter by sample owners
       - search (string): Search term for sample name, type or owner
   - **Returns**: Promise<SampleListResponse> (Paginated list of samples)
   - **Endpoint**: GET /samples

2. **getSampleById**
   - **Purpose**: Get a specific sample by its ID
   - **Parameters**:
     - id (string): Sample ID
   - **Returns**: Promise<SampleResponse> (Single sample)
   - **Endpoint**: GET /samples/{id}

3. **createSample**
   - **Purpose**: Create a new sample
   - **Parameters**:
     - sampleData (SampleCreateRequest): Data for new sample
   - **Returns**: Promise<SampleResponse> (Created sample)
   - **Endpoint**: POST /samples

4. **updateSample**
   - **Purpose**: Update an existing sample
   - **Parameters**:
     - id (string): Sample ID
     - sampleData (SampleUpdateRequest): Data to update
   - **Returns**: Promise<SampleResponse> (Updated sample)
   - **Endpoint**: PATCH /samples/{id}

5. **deleteSample**
   - **Purpose**: Delete a sample
   - **Parameters**:
     - id (string): Sample ID
   - **Returns**: Promise<void>
   - **Endpoint**: DELETE /samples/{id}

6. **exportSamples**
   - **Purpose**: Export sample data as CSV
   - **Parameters**:
     - filters (optional): Same filter options as getAllSamples
   - **Returns**: Promise<Blob> (CSV file as blob)
   - **Endpoint**: GET /samples/export (with query parameters)

7. **searchSamples** (implemented via getAllSamples with search parameter)
   - **Purpose**: Search for samples by name, type, or owner
   - **Parameters**:
     - search (string): Search term to match against sample fields
     - page (number, default: 1): Page number for pagination
     - limit (number, default: 10): Number of items per page
   - **Returns**: Promise<SampleListResponse> (Paginated list of matching samples)
   - **Endpoint**: GET /samples?search={searchTerm}

### Aliquot Service

#### Methods

1. **getAllAliquots**
   - **Purpose**: Get all aliquots for a sample
   - **Parameters**:
     - sampleId (string): Parent sample ID
   - **Returns**: Promise<AliquotResponse[]> (Array of aliquots)
   - **Endpoint**: GET /samples/{sampleId}/aliquots

2. **getAliquotById**
   - **Purpose**: Get a specific aliquot by its ID
   - **Parameters**:
     - sampleId (string): Parent sample ID
     - aliquotId (string): Aliquot ID
   - **Returns**: Promise<AliquotResponse> (Single aliquot)
   - **Endpoint**: GET /samples/{sampleId}/aliquots/{aliquotId}

3. **createAliquot**
   - **Purpose**: Create a new aliquot for a sample
   - **Parameters**:
     - aliquotData (AliquotCreateRequest): Data for new aliquot
   - **Returns**: Promise<AliquotResponse> (Created aliquot)
   - **Endpoint**: POST /samples/{sampleId}/aliquots

4. **updateAliquotLocation**
   - **Purpose**: Update an aliquot's location
   - **Parameters**:
     - sampleId (string): Parent sample ID
     - aliquotId (string): Aliquot ID
     - location (string): New location
   - **Returns**: Promise<AliquotResponse> (Updated aliquot)
   - **Endpoint**: PATCH /samples/{sampleId}/aliquots/{aliquotId}/location

5. **deleteAliquot**
   - **Purpose**: Delete an aliquot
   - **Parameters**:
     - sampleId (string): Parent sample ID
     - aliquotId (string): Aliquot ID
   - **Returns**: Promise<void>
   - **Endpoint**: DELETE /samples/{sampleId}/aliquots/{aliquotId}

### Test Service

#### Methods

1. **getAllTests**
   - **Purpose**: Get all tests for an aliquot
   - **Parameters**:
     - sampleId (string): Parent sample ID
     - aliquotId (string): Parent aliquot ID
   - **Returns**: Promise<TestResponse[]> (Array of tests)
   - **Endpoint**: GET /samples/{sampleId}/aliquots/{aliquotId}/tests

2. **getTestById**
   - **Purpose**: Get a specific test by its ID
   - **Parameters**:
     - sampleId (string): Parent sample ID
     - aliquotId (string): Parent aliquot ID
     - testId (string): Test ID
   - **Returns**: Promise<TestResponse> (Single test)
   - **Endpoint**: GET /samples/{sampleId}/aliquots/{aliquotId}/tests/{testId}

3. **createTest**
   - **Purpose**: Create a new test for an aliquot
   - **Parameters**:
     - sampleId (string): Parent sample ID
     - aliquotId (string): Parent aliquot ID
     - testData (TestCreateRequest): Data for new test
   - **Returns**: Promise<TestResponse> (Created test)
   - **Endpoint**: POST /samples/{sampleId}/aliquots/{aliquotId}/tests

4. **updateTest**
   - **Purpose**: Update an existing test
   - **Parameters**:
     - sampleId (string): Parent sample ID
     - aliquotId (string): Parent aliquot ID
     - testId (string): Test ID
     - testData (TestUpdateRequest): Data to update
   - **Returns**: Promise<TestResponse> (Updated test)
   - **Endpoint**: PATCH /samples/{sampleId}/aliquots/{aliquotId}/tests/{testId}

5. **deleteTest**
   - **Purpose**: Delete a test
   - **Parameters**:
     - sampleId (string): Parent sample ID
     - aliquotId (string): Parent aliquot ID
     - testId (string): Test ID
   - **Returns**: Promise<void>
   - **Endpoint**: DELETE /samples/{sampleId}/aliquots/{aliquotId}/tests/{testId}

6. **getTestMethods**
   - **Purpose**: Get all available test methods
   - **Parameters**: None
   - **Returns**: Promise<string[]> (Array of method names)
   - **Endpoint**: GET /tests/methods

### Metadata Service

#### Methods

1. **getSampleTypes**
   - **Purpose**: Get all sample types for dropdown
   - **Returns**: Promise<SampleType[]> (Array of sample types)
   - **Endpoint**: GET /metadata/sample-types

2. **getSampleStatuses**
   - **Purpose**: Get all sample statuses for dropdown
   - **Returns**: Promise<SampleStatus[]> (Array of sample statuses)
   - **Endpoint**: GET /metadata/sample-statuses

3. **getLabLocations**
   - **Purpose**: Get all lab locations for dropdown
   - **Returns**: Promise<LabLocation[]> (Array of lab locations)
   - **Endpoint**: GET /metadata/lab-locations

4. **getUsers**
   - **Purpose**: Get all users for assignment dropdown
   - **Returns**: Promise<User[]> (Array of users)
   - **Endpoint**: GET /metadata/users

5. **getStorageLocations**
   - **Purpose**: Get all storage locations/freezers
   - **Returns**: Promise<StorageLocation[]> (Array of storage locations)
   - **Endpoint**: GET /storage/locations

6. **getAvailableBoxes**
   - **Purpose**: Get available storage boxes
   - **Returns**: Promise<StorageLocation[]> (Array of box locations)
   - **Endpoint**: GET /storage/boxes

## API Endpoints

### Sample Endpoints
- `GET /samples`: Get all samples with pagination and filtering
- `GET /samples/{id}`: Get a specific sample by ID
- `POST /samples`: Create a new sample
- `PATCH /samples/{id}`: Update an existing sample
- `DELETE /samples/{id}`: Delete a sample
- `GET /samples/export`: Export samples as CSV

### Aliquot Endpoints
- `GET /samples/{sampleId}/aliquots`: Get all aliquots for a sample
- `GET /samples/{sampleId}/aliquots/{aliquotId}`: Get a specific aliquot
- `POST /samples/{sampleId}/aliquots`: Create a new aliquot
- `PATCH /samples/{sampleId}/aliquots/{aliquotId}/location`: Update aliquot location
- `DELETE /samples/{sampleId}/aliquots/{aliquotId}`: Delete an aliquot

### Test Endpoints
- `GET /samples/{sampleId}/aliquots/{aliquotId}/tests`: Get all tests for an aliquot
- `GET /samples/{sampleId}/aliquots/{aliquotId}/tests/{testId}`: Get a specific test
- `POST /samples/{sampleId}/aliquots/{aliquotId}/tests`: Create a new test
- `PATCH /samples/{sampleId}/aliquots/{aliquotId}/tests/{testId}`: Update an existing test
- `DELETE /samples/{sampleId}/aliquots/{aliquotId}/tests/{testId}`: Delete a test
- `GET /tests/methods`: Get all available test methods

### Bulk Operations Endpoints
- `GET /samples/export`: Export all samples matching filters as CSV
- `POST /samples/import`: Import samples from CSV (future implementation)
- `POST /samples/bulk-update`: Update multiple samples at once (future implementation)
- `POST /samples/bulk-delete`: Delete multiple samples at once (future implementation)

### Metadata Endpoints
- `GET /metadata/sample-types`: Get all sample types
- `GET /metadata/sample-statuses`: Get all sample statuses
- `GET /metadata/lab-locations`: Get all lab locations
- `GET /metadata/users`: Get all users
- `GET /storage/locations`: Get all storage locations
- `GET /storage/boxes`: Get available boxes

## Request/Response Examples

### Sample Creation

**Request:**
```json
POST /samples
{
  "name": "Blood Sample A",
  "type": "Blood",
  "owner": "John Doe",
  "boxId": "box-001",
  "volume": 15,
  "notes": "Collected from patient #12345"
}
```

**Response:**
```json
{
  "data": {
    "id": "sample-001",
    "name": "Blood Sample A",
    "type": "Blood",
    "submissionDate": "2025-07-03T10:00:00.000Z",
    "status": "submitted",
    "owner": "John Doe",
    "boxId": "box-001",
    "location": "Lab Storage",
    "lastMovement": "2025-07-03T10:00:00.000Z",
    "volumeLeft": 15,
    "totalVolume": 15,
    "aliquotsCreated": 0,
    "aliquots": []
  },
  "status": 201,
  "success": true
}
```

### Aliquot Creation

**Request:**
```json
POST /samples/sample-001/aliquots
{
  "sampleId": "sample-001",
  "volume": 5,
  "location": "Freezer 1, Rack 3"
}
```

**Response:**
```json
{
  "data": {
    "id": "aliquot-001",
    "volume": 5,
    "createdAt": "2025-07-03T11:00:00.000Z",
    "location": "Freezer 1, Rack 3",
    "tests": []
  },
  "status": 201,
  "success": true
}
```

### Test Creation

**Request:**
```json
POST /samples/sample-001/aliquots/aliquot-001/tests
{
  "name": "CBC",
  "method": "Automated Analysis",
  "assignedTo": "Lab Technician 1",
  "notes": "Priority test"
}
```

**Response:**
```json
{
  "data": {
    "id": "test-001",
    "name": "CBC",
    "status": "Pending",
    "assignedTo": "Lab Technician 1",
    "startDate": "2025-07-03T11:30:00.000Z",
    "method": "Automated Analysis",
    "notes": "Priority test"
  },
  "status": 201,
  "success": true
}
```

### Retrieving Sample with Related Data

**Request:**
```
GET /samples/sample-001
```

**Response:**
```json
{
  "data": {
    "id": "sample-001",
    "name": "Blood Sample A",
    "type": "Blood",
    "submissionDate": "2025-07-03T10:00:00.000Z",
    "status": "aliquots_created",
    "owner": "John Doe",
    "boxId": "box-001",
    "location": "Lab Storage",
    "lastMovement": "2025-07-03T10:00:00.000Z",
    "volumeLeft": 10,
    "totalVolume": 15,
    "aliquotsCreated": 1,
    "aliquots": [
      {
        "id": "aliquot-001",
        "volume": 5,
        "createdAt": "2025-07-03T11:00:00.000Z",
        "location": "Freezer 1, Rack 3",
        "tests": [
          {
            "id": "test-001",
            "name": "CBC",
            "status": "Pending",
            "assignedTo": "Lab Technician 1",
            "startDate": "2025-07-03T11:30:00.000Z",
            "method": "Automated Analysis",
            "notes": "Priority test"
          }
        ]
      }
    ]
  },
  "status": 200,
  "success": true
}
```

### Sample Export to CSV

**Request:**
```
GET /samples/export?type=Blood&status=submitted&owner=John%20Doe
```

**Response:**
```
Content-Type: text/csv;charset=utf-8
Content-Disposition: attachment; filename="samples_export.csv"

ID,Name,Type,Status,Owner,Submission Date,Location,Volume
sample-001,Blood Sample A,Blood,submitted,John Doe,2025-07-03T10:00:00.000Z,Lab Storage,15
sample-003,Blood Sample C,Blood,submitted,John Doe,2025-07-01T14:30:00.000Z,Lab Storage,20
```

The CSV export includes all samples matching the provided filters and contains the following columns:
- ID
- Name
- Type
- Status
- Owner
- Submission Date
- Location
- Volume (totalVolume)

## Common Workflows

### Complete Sample Lifecycle

1. **Register new sample**
   ```
   POST /samples
   ```

2. **Create aliquot from sample**
   ```
   POST /samples/{sampleId}/aliquots
   ```

3. **Create test for an aliquot**
   ```
   POST /samples/{sampleId}/aliquots/{aliquotId}/tests
   ```

4. **Update test with results**
   ```
   PATCH /samples/{sampleId}/aliquots/{aliquotId}/tests/{testId}
   {
     "status": "Completed",
     "results": "Test results data",
     "completionDate": "2025-07-05T10:30:00.000Z"
   }
   ```

5. **Update sample status after testing**
   ```
   PATCH /samples/{sampleId}
   {
     "status": "testing_completed"
   }
   ```

6. **Move sample to storage**
   ```
   PATCH /samples/{sampleId}
   {
     "status": "in_storage",
     "location": "Freezer 2, Shelf 3"
   }
   ```

### Sample Search and Filtering

For complex searching across samples:

```
GET /samples?type=Blood,Tissue&status=submitted,aliquots_created&owner=John%20Doe&search=patient&page=1&limit=20
```

This request would:
- Search for samples containing "patient" in name, type or owner
- Filter to include only Blood and Tissue samples
- Filter to include only samples with status "submitted" or "aliquots_created"
- Filter to include only samples owned by John Doe
- Return the first page with 20 results per page
