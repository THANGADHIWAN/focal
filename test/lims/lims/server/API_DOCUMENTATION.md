# LIMS API Documentation

This document provides comprehensive documentation for all API endpoints in the LIMS (Laboratory Information Management System) application.

## Base URL
```
http://localhost:8000
```

## Authentication
Most endpoints require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

---

## Health & Status Endpoints

### 1. Health Check
**GET** `/health`

**Description**: Check application and database status

**Response**:
```json
{
  "status": "healthy",
  "database": "connected",
  "message": "Application is running and database is accessible"
}
```

**Error Response**:
```json
{
  "status": "unhealthy",
  "database": "disconnected",
  "message": "Database connection failed: connection refused",
  "error": "connection refused"
}
```

### 2. Root Endpoint
**GET** `/`

**Description**: Get API information and links

**Response**:
```json
{
  "message": "LIMS Sample Management API",
  "version": "1.0.0",
  "docs": "/docs",
  "health": "/health"
}
```

---

## Sample Management Endpoints

### 3. Get All Samples
**GET** `/samples`

**Description**: Retrieve all samples with pagination and filtering

**Query Parameters**:
- `page` (integer, default: 1): Page number
- `limit` (integer, default: 10, max: 100): Items per page
- `type` (array of strings, optional): Filter by sample type IDs
- `status` (array of strings, optional): Filter by sample statuses
- `location` (array of strings, optional): Filter by storage locations
- `owner` (array of strings, optional): Filter by created_by field
- `search` (string, optional): Search term for sample name or code

**Example Request**:
```
GET /samples?page=1&limit=10&status=Completed&search=sample123
```

**Response**:
```json
{
  "data": {
    "data": [
      {
        "id": 1,
        "sample_code": "SAM-20241201-0001",
        "sample_name": "Blood Sample 001",
        "sample_type_id": 1,
        "status": "Completed",
        "box_id": 1,
        "volume_ml": 10,
        "received_date": "2024-12-01T10:00:00",
        "due_date": "2024-12-08T10:00:00",
        "priority": "Medium",
        "quantity": 10.5,
        "is_aliquot": false,
        "number_of_aliquots": 3,
        "created_by": "John Doe",
        "created_at": "2024-12-01T10:00:00",
        "updated_at": "2024-12-01T10:00:00",
        "purpose": "Clinical testing",
        "aliquots": [
          {
            "id": 1,
            "aliquot_code": "ALQ-001",
            "volume_ml": 3.5,
            "status": "Logged_In",
            "creation_date": "2024-12-01T10:30:00"
          }
        ]
      }
    ],
    "total_count": 25,
    "total_pages": 3,
    "current_page": 1,
    "page_size": 10,
    "has_more": true
  },
  "status": 200,
  "success": true
}
```

### 4. Get Sample by ID
**GET** `/samples/{sample_id}`

**Description**: Retrieve a specific sample by its ID

**Path Parameters**:
- `sample_id` (integer): Sample ID

**Example Request**:
```
GET /samples/1
```

**Response**:
```json
{
  "data": {
    "id": 1,
    "sample_code": "SAM-20241201-0001",
    "sample_name": "Blood Sample 001",
    "sample_type_id": 1,
    "status": "Completed",
    "box_id": 1,
    "volume_ml": 10,
    "received_date": "2024-12-01T10:00:00",
    "due_date": "2024-12-08T10:00:00",
    "priority": "Medium",
    "quantity": 10.5,
    "is_aliquot": false,
    "number_of_aliquots": 3,
    "created_by": "John Doe",
    "created_at": "2024-12-01T10:00:00",
    "updated_at": "2024-12-01T10:00:00",
    "purpose": "Clinical testing",
    "aliquots": [
      {
        "id": 1,
        "aliquot_code": "ALQ-001",
        "volume_ml": 3.5,
        "status": "Logged_In",
        "creation_date": "2024-12-01T10:30:00"
      }
    ]
  },
  "status": 200,
  "success": true
}
```

**Error Response** (404):
```json
{
  "detail": "Sample with ID 999 not found"
}
```

### 5. Create Sample
**POST** `/samples`

**Description**: Create a new sample

**Request Body**:
```json
{
  "sample_code": "SAM-20241201-0002",
  "sample_name": "Blood Sample 002",
  "sample_type_id": 1,
  "status": "Logged_In",
  "box_id": 1,
  "volume_ml": 15,
  "received_date": "2024-12-01T11:00:00",
  "due_date": "2024-12-08T11:00:00",
  "priority": "High",
  "quantity": 15.0,
  "is_aliquot": false,
  "number_of_aliquots": 0,
  "created_by": "Jane Smith",
  "purpose": "Research study"
}
```

**Response**:
```json
{
  "data": {
    "id": 2,
    "sample_code": "SAM-20241201-0002",
    "sample_name": "Blood Sample 002",
    "sample_type_id": 1,
    "status": "Logged_In",
    "box_id": 1,
    "volume_ml": 15,
    "received_date": "2024-12-01T11:00:00",
    "due_date": "2024-12-08T11:00:00",
    "priority": "High",
    "quantity": 15.0,
    "is_aliquot": false,
    "number_of_aliquots": 0,
    "created_by": "Jane Smith",
    "created_at": "2024-12-01T11:00:00",
    "updated_at": null,
    "purpose": "Research study"
  },
  "status": 201,
  "success": true,
  "message": "Sample created successfully"
}
```

### 6. Update Sample
**PATCH** `/samples/{sample_id}`

**Description**: Update an existing sample

**Path Parameters**:
- `sample_id` (integer): Sample ID

**Request Body** (partial update):
```json
{
  "status": "In_Progress",
  "priority": "Urgent",
  "purpose": "Updated research purpose"
}
```

**Response**:
```json
{
  "data": {
    "id": 1,
    "sample_code": "SAM-20241201-0001",
    "sample_name": "Blood Sample 001",
    "sample_type_id": 1,
    "status": "In_Progress",
    "box_id": 1,
    "volume_ml": 10,
    "received_date": "2024-12-01T10:00:00",
    "due_date": "2024-12-08T10:00:00",
    "priority": "Urgent",
    "quantity": 10.5,
    "is_aliquot": false,
    "number_of_aliquots": 3,
    "created_by": "John Doe",
    "created_at": "2024-12-01T10:00:00",
    "updated_at": "2024-12-01T12:00:00",
    "purpose": "Updated research purpose"
  },
  "status": 200,
  "success": true,
  "message": "Sample updated successfully"
}
```

### 7. Delete Sample
**DELETE** `/samples/{sample_id}`

**Description**: Delete a sample

**Path Parameters**:
- `sample_id` (integer): Sample ID

**Example Request**:
```
DELETE /samples/1
```

**Response**:
```json
{
  "data": null,
  "status": 200,
  "success": true,
  "message": "Sample deleted successfully"
}
```

### 8. Export Samples
**GET** `/samples/export`

**Description**: Export samples as CSV

**Query Parameters** (same as Get All Samples):
- `type` (array of strings, optional)
- `status` (array of strings, optional)
- `location` (array of strings, optional)
- `owner` (array of strings, optional)
- `search` (string, optional)

**Example Request**:
```
GET /samples/export?status=Completed
```

**Response**: CSV file download with headers:
```
ID,Sample Code,Sample Name,Type ID,Status,Box ID,Volume (ml),Received Date,Due Date,Priority,Quantity,Is Aliquot,Number of Aliquots,Created By,Created At,Updated At,Purpose
1,SAM-20241201-0001,Blood Sample 001,1,Completed,1,10,2024-12-01T10:00:00,2024-12-08T10:00:00,Medium,10.5,false,3,John Doe,2024-12-01T10:00:00,2024-12-01T10:00:00,Clinical testing
```

---

## Aliquot Management Endpoints

### 9. Get All Aliquots
**GET** `/aliquots`

**Description**: Retrieve all aliquots with pagination and filtering

**Query Parameters**:
- `page` (integer, default: 1): Page number
- `limit` (integer, default: 10, max: 100): Items per page
- `sample_id` (integer, optional): Filter by sample ID
- `status` (array of strings, optional): Filter by aliquot status
- `search` (string, optional): Search term for aliquot code

**Example Request**:
```
GET /aliquots?page=1&limit=10&sample_id=1
```

**Response**:
```json
{
  "data": {
    "data": [
      {
        "id": 1,
        "sample_id": 1,
        "aliquot_code": "ALQ-001",
        "volume_ml": 3.5,
        "creation_date": "2024-12-01T10:30:00",
        "status": "Logged_In",
        "assigned_to": "user-uuid-here",
        "created_by": "John Doe",
        "created_at": "2024-12-01T10:30:00",
        "purpose": "Testing aliquot"
      }
    ],
    "total_count": 5,
    "total_pages": 1,
    "current_page": 1,
    "page_size": 10,
    "has_more": false
  },
  "status": 200,
  "success": true
}
```

### 10. Get Aliquot by ID
**GET** `/aliquots/{aliquot_id}`

**Description**: Retrieve a specific aliquot by its ID

**Path Parameters**:
- `aliquot_id` (integer): Aliquot ID

**Example Request**:
```
GET /aliquots/1
```

**Response**:
```json
{
  "data": {
    "id": 1,
    "sample_id": 1,
    "aliquot_code": "ALQ-001",
    "volume_ml": 3.5,
    "creation_date": "2024-12-01T10:30:00",
    "status": "Logged_In",
    "assigned_to": "user-uuid-here",
    "created_by": "John Doe",
    "created_at": "2024-12-01T10:30:00",
    "purpose": "Testing aliquot",
    "sample": {
      "id": 1,
      "sample_code": "SAM-20241201-0001",
      "sample_name": "Blood Sample 001"
    }
  },
  "status": 200,
  "success": true
}
```

### 11. Create Aliquot
**POST** `/aliquots`

**Description**: Create a new aliquot

**Request Body**:
```json
{
  "sample_id": 1,
  "aliquot_code": "ALQ-002",
  "volume_ml": 2.5,
  "status": "Logged_In",
  "assigned_to": "user-uuid-here",
  "created_by": "John Doe",
  "purpose": "Second testing aliquot"
}
```

**Response**:
```json
{
  "data": {
    "id": 2,
    "sample_id": 1,
    "aliquot_code": "ALQ-002",
    "volume_ml": 2.5,
    "creation_date": "2024-12-01T12:00:00",
    "status": "Logged_In",
    "assigned_to": "user-uuid-here",
    "created_by": "John Doe",
    "created_at": "2024-12-01T12:00:00",
    "purpose": "Second testing aliquot"
  },
  "status": 201,
  "success": true,
  "message": "Aliquot created successfully"
}
```

### 12. Update Aliquot
**PATCH** `/aliquots/{aliquot_id}`

**Description**: Update an existing aliquot

**Path Parameters**:
- `aliquot_id` (integer): Aliquot ID

**Request Body** (partial update):
```json
{
  "status": "In_Progress",
  "volume_ml": 2.0,
  "purpose": "Updated testing purpose"
}
```

**Response**:
```json
{
  "data": {
    "id": 1,
    "sample_id": 1,
    "aliquot_code": "ALQ-001",
    "volume_ml": 2.0,
    "creation_date": "2024-12-01T10:30:00",
    "status": "In_Progress",
    "assigned_to": "user-uuid-here",
    "created_by": "John Doe",
    "created_at": "2024-12-01T10:30:00",
    "purpose": "Updated testing purpose"
  },
  "status": 200,
  "success": true,
  "message": "Aliquot updated successfully"
}
```

### 13. Delete Aliquot
**DELETE** `/aliquots/{aliquot_id}`

**Description**: Delete an aliquot

**Path Parameters**:
- `aliquot_id` (integer): Aliquot ID

**Example Request**:
```
DELETE /aliquots/1
```

**Response**:
```json
{
  "data": null,
  "status": 200,
  "success": true,
  "message": "Aliquot deleted successfully"
}
```

---

## Test Management Endpoints

### 14. Get All Tests
**GET** `/tests`

**Description**: Retrieve all tests with pagination and filtering

**Query Parameters**:
- `page` (integer, default: 1): Page number
- `limit` (integer, default: 10, max: 100): Items per page
- `sample_id` (integer, optional): Filter by sample ID
- `aliquot_id` (integer, optional): Filter by aliquot ID
- `status` (array of strings, optional): Filter by test status
- `search` (string, optional): Search term for test name

**Example Request**:
```
GET /tests?page=1&limit=10&status=In_Progress
```

**Response**:
```json
{
  "data": {
    "data": [
      {
        "id": 1,
        "sample_id": 1,
        "aliquot_id": 1,
        "test_master_id": 1,
        "analyst_id": "user-uuid-here",
        "instrument_id": 1,
        "scheduled_date": "2024-12-02T09:00:00",
        "start_date": "2024-12-02T09:00:00",
        "end_date": "2024-12-02T11:00:00",
        "status": "In_Progress",
        "remarks": "Standard blood test"
      }
    ],
    "total_count": 8,
    "total_pages": 1,
    "current_page": 1,
    "page_size": 10,
    "has_more": false
  },
  "status": 200,
  "success": true
}
```

### 15. Get Test by ID
**GET** `/tests/{test_id}`

**Description**: Retrieve a specific test by its ID

**Path Parameters**:
- `test_id` (integer): Test ID

**Example Request**:
```
GET /tests/1
```

**Response**:
```json
{
  "data": {
    "id": 1,
    "sample_id": 1,
    "aliquot_id": 1,
    "test_master_id": 1,
    "analyst_id": "user-uuid-here",
    "instrument_id": 1,
    "scheduled_date": "2024-12-02T09:00:00",
    "start_date": "2024-12-02T09:00:00",
    "end_date": "2024-12-02T11:00:00",
    "status": "In_Progress",
    "remarks": "Standard blood test",
    "sample": {
      "id": 1,
      "sample_code": "SAM-20241201-0001",
      "sample_name": "Blood Sample 001"
    },
    "aliquot": {
      "id": 1,
      "aliquot_code": "ALQ-001"
    },
    "test_results": [
      {
        "id": 1,
        "test_parameter_id": 1,
        "result_value": "120",
        "unit": "mg/dL",
        "specification_limit": "70-140",
        "result_status": "Pass",
        "result_date": "2024-12-02T10:30:00"
      }
    ]
  },
  "status": 200,
  "success": true
}
```

### 16. Create Test
**POST** `/tests`

**Description**: Create a new test

**Request Body**:
```json
{
  "sample_id": 1,
  "aliquot_id": 1,
  "test_master_id": 1,
  "analyst_id": "user-uuid-here",
  "instrument_id": 1,
  "scheduled_date": "2024-12-03T09:00:00",
  "status": "Pending",
  "remarks": "New blood test"
}
```

**Response**:
```json
{
  "data": {
    "id": 2,
    "sample_id": 1,
    "aliquot_id": 1,
    "test_master_id": 1,
    "analyst_id": "user-uuid-here",
    "instrument_id": 1,
    "scheduled_date": "2024-12-03T09:00:00",
    "start_date": null,
    "end_date": null,
    "status": "Pending",
    "remarks": "New blood test"
  },
  "status": 201,
  "success": true,
  "message": "Test created successfully"
}
```

### 17. Update Test
**PATCH** `/tests/{test_id}`

**Description**: Update an existing test

**Path Parameters**:
- `test_id` (integer): Test ID

**Request Body** (partial update):
```json
{
  "status": "Completed",
  "start_date": "2024-12-02T09:00:00",
  "end_date": "2024-12-02T11:00:00",
  "remarks": "Test completed successfully"
}
```

**Response**:
```json
{
  "data": {
    "id": 1,
    "sample_id": 1,
    "aliquot_id": 1,
    "test_master_id": 1,
    "analyst_id": "user-uuid-here",
    "instrument_id": 1,
    "scheduled_date": "2024-12-02T09:00:00",
    "start_date": "2024-12-02T09:00:00",
    "end_date": "2024-12-02T11:00:00",
    "status": "Completed",
    "remarks": "Test completed successfully"
  },
  "status": 200,
  "success": true,
  "message": "Test updated successfully"
}
```

### 18. Delete Test
**DELETE** `/tests/{test_id}`

**Description**: Delete a test

**Path Parameters**:
- `test_id` (integer): Test ID

**Example Request**:
```
DELETE /tests/1
```

**Response**:
```json
{
  "data": null,
  "status": 200,
  "success": true,
  "message": "Test deleted successfully"
}
```

---

## Authentication Endpoints

### 19. Login
**POST** `/auth/login`

**Description**: Authenticate user and get JWT token

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "id": "user-uuid-here",
    "full_name": "John Doe",
    "email": "user@example.com",
    "role": "analyst",
    "department": "Laboratory"
  }
}
```

**Error Response** (401):
```json
{
  "detail": "Invalid credentials"
}
```

### 20. Register
**POST** `/auth/register`

**Description**: Register a new user

**Request Body**:
```json
{
  "full_name": "Jane Smith",
  "email": "jane.smith@example.com",
  "password": "password123",
  "role": "analyst",
  "department": "Laboratory"
}
```

**Response**:
```json
{
  "data": {
    "id": "new-user-uuid-here",
    "full_name": "Jane Smith",
    "email": "jane.smith@example.com",
    "role": "analyst",
    "department": "Laboratory",
    "is_active": true,
    "created_at": "2024-12-01T10:00:00"
  },
  "status": 201,
  "success": true,
  "message": "User registered successfully"
}
```

### 21. Get Current User
**GET** `/auth/me`

**Description**: Get current user information

**Headers**:
```
Authorization: Bearer <jwt_token>
```

**Response**:
```json
{
  "data": {
    "id": "user-uuid-here",
    "full_name": "John Doe",
    "email": "user@example.com",
    "role": "analyst",
    "department": "Laboratory",
    "is_active": true,
    "created_at": "2024-12-01T10:00:00",
    "updated_at": "2024-12-01T10:00:00"
  },
  "status": 200,
  "success": true
}
```

---

## Metadata Endpoints

### 22. Get Sample Types
**GET** `/metadata/sample_types`

**Description**: Get all sample types

**Response**:
```json
{
  "data": [
    {
      "id": 1,
      "name": "Blood",
      "description": "Blood samples",
      "matrix_type": "Liquid"
    },
    {
      "id": 2,
      "name": "Tissue",
      "description": "Tissue samples",
      "matrix_type": "Solid"
    }
  ],
  "status": 200,
  "success": true
}
```

### 23. Get Storage Locations
**GET** `/metadata/storage_locations`

**Description**: Get all storage locations

**Response**:
```json
{
  "data": [
    {
      "id": 1,
      "location_name": "Main Laboratory",
      "location_code": "LAB-001",
      "temperature_celsius": 22.0,
      "humidity_percent": 45.0,
      "description": "Main laboratory storage"
    },
    {
      "id": 2,
      "location_name": "Freezer Room",
      "location_code": "FREEZER-001",
      "temperature_celsius": -20.0,
      "humidity_percent": 30.0,
      "description": "Freezer storage for samples"
    }
  ],
  "status": 200,
  "success": true
}
```

### 24. Get Equipment
**GET** `/metadata/equipment`

**Description**: Get all equipment

**Response**:
```json
{
  "data": [
    {
      "id": 1,
      "name": "HPLC System",
      "equipment_type": "HPLC",
      "serial_number": "HPLC-001",
      "manufacturer": "Agilent",
      "model_number": "1260",
      "status": "Available",
      "location_id": 1
    },
    {
      "id": 2,
      "name": "Centrifuge",
      "equipment_type": "Centrifuge",
      "serial_number": "CENT-001",
      "manufacturer": "Eppendorf",
      "model_number": "5810R",
      "status": "In Use",
      "location_id": 1
    }
  ],
  "status": 200,
  "success": true
}
```

---

## Storage Management Endpoints

### 25. Get Storage Hierarchy
**GET** `/storage/hierarchy`

**Description**: Get complete storage hierarchy

**Response**:
```json
{
  "data": {
    "storage_locations": [
      {
        "id": 1,
        "location_name": "Main Laboratory",
        "location_code": "LAB-001",
        "storage_rooms": [
          {
            "id": 1,
            "room_name": "Lab Room 1",
            "floor": 1,
            "building": "Main Building",
            "freezers": [
              {
                "id": 1,
                "freezer_name": "Freezer A",
                "freezer_type": "Ultra-low",
                "boxes": [
                  {
                    "id": 1,
                    "box_code": "BOX-001",
                    "box_type": "Standard",
                    "capacity": 100,
                    "inventory_slots": [
                      {
                        "id": 1,
                        "slot_code": "SLOT-001",
                        "is_occupied": true,
                        "aliquot_id": 1
                      }
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  },
  "status": 200,
  "success": true
}
```

### 26. Get Available Slots
**GET** `/storage/available_slots`

**Description**: Get all available storage slots

**Response**:
```json
{
  "data": [
    {
      "id": 2,
      "slot_code": "SLOT-002",
      "is_occupied": false,
      "box_id": 1,
      "box": {
        "id": 1,
        "box_code": "BOX-001",
        "freezer": {
          "id": 1,
          "freezer_name": "Freezer A"
        }
      }
    }
  ],
  "status": 200,
  "success": true
}
```

---

## Error Responses

### Common Error Formats

**400 Bad Request**:
```json
{
  "detail": "Validation error",
  "errors": [
    {
      "field": "sample_code",
      "message": "Sample code is required"
    }
  ]
}
```

**401 Unauthorized**:
```json
{
  "detail": "Not authenticated"
}
```

**403 Forbidden**:
```json
{
  "detail": "Insufficient permissions"
}
```

**404 Not Found**:
```json
{
  "detail": "Resource not found"
}
```

**422 Unprocessable Entity**:
```json
{
  "detail": [
    {
      "loc": ["body", "sample_code"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**500 Internal Server Error**:
```json
{
  "detail": "Internal server error"
}
```

---

## Data Types and Enums

### Sample Status Values
- `Logged_In`
- `In_Progress`
- `Completed`
- `Archived`

### Sample Priority Values
- `Low`
- `Medium`
- `High`
- `Urgent`

### Test Status Values
- `Pending`
- `In_Progress`
- `Completed`
- `Cancelled`

### Equipment Status Values
- `Available`
- `In Use`
- `Under Maintenance`
- `Out of Service`
- `Quarantined`

### Equipment Type Values
- `HPLC`
- `Centrifuge`
- `Microscope`
- `PCR`
- `Spectrophotometer`
- `Balance`
- `pH Meter`

### Sample Type Values
- `Blood`
- `Tissue`
- `Urine`
- `Saliva`
- `Culture`
- `Environmental`
- `Other`

---

## Rate Limiting

The API implements rate limiting to prevent abuse:
- **General endpoints**: 100 requests per minute
- **Authentication endpoints**: 10 requests per minute
- **Export endpoints**: 20 requests per minute

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```

---

## Pagination

All list endpoints support pagination with the following response format:
```json
{
  "data": [...],
  "total_count": 100,
  "total_pages": 10,
  "current_page": 1,
  "page_size": 10,
  "has_more": true
}
```

---

## File Upload/Download

### Export Endpoints
Export endpoints return CSV files with appropriate headers:
```
Content-Type: text/csv
Content-Disposition: attachment; filename=samples_export.csv
```

### File Upload (Future)
File upload endpoints will support:
- Sample attachments
- Test result files
- Documentation uploads

---

## WebSocket Endpoints (Future)

### Real-time Updates
WebSocket endpoints will be available for:
- Real-time test status updates
- Sample processing notifications
- Equipment status changes

---

## API Versioning

The API uses URL versioning:
- Current version: `/api/v1/`
- Future versions: `/api/v2/`, `/api/v3/`, etc.

---

## SDKs and Libraries

### Python SDK
```python
from lims_client import LIMSClient

client = LIMSClient(base_url="http://localhost:8000")
samples = client.samples.get_all(page=1, limit=10)
```

### JavaScript SDK
```javascript
import { LIMSClient } from '@lims/client';

const client = new LIMSClient('http://localhost:8000');
const samples = await client.samples.getAll({ page: 1, limit: 10 });
```

---

## Testing

### Test Environment
- **Base URL**: `http://localhost:8000`
- **Database**: PostgreSQL with test data
- **Authentication**: Test JWT tokens provided

### Example Test Requests
```bash
# Health check
curl http://localhost:8000/health

# Get samples
curl -H "Authorization: Bearer <token>" http://localhost:8000/samples

# Create sample
curl -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"sample_code":"TEST-001","sample_name":"Test Sample"}' \
  http://localhost:8000/samples
```

---

This documentation covers all the main API endpoints in the LIMS system. For interactive documentation, visit the Swagger UI at `/docs` when the server is running. 