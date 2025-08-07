# LIMS API Documentation

## Metadata Endpoints

### GET /metadata/sample-types

Returns a list of sample types for dropdown menus.

**Response:**
```json
{
  "data": [
    {
      "value": "Blood",
      "label": "Blood",
      "description": "Blood sample"
    },
    {
      "value": "Tissue",
      "label": "Tissue",
      "description": "Tissue sample"
    },
    {
      "value": "Urine",
      "label": "Urine",
      "description": "Urine sample"
    }
  ],
  "status": 200,
  "success": true
}
```

### GET /metadata/sample-statuses

Returns a list of sample statuses for dropdown menus.

**Response:**
```json
{
  "data": [
    {
      "value": "submitted",
      "label": "Submitted",
      "description": "Sample has been submitted to the system"
    },
    {
      "value": "aliquots_created",
      "label": "Aliquots Created",
      "description": "Aliquots have been created from this sample"
    },
    {
      "value": "testing_completed",
      "label": "Testing Completed",
      "description": "All testing has been completed for this sample"
    }
  ],
  "status": 200,
  "success": true
}
```

### GET /metadata/lab-locations

Returns a list of lab locations for dropdown menus.

**Response:**
```json
{
  "data": [
    {
      "value": "Lab 1",
      "label": "Lab 1",
      "description": "Main laboratory"
    },
    {
      "value": "Lab 2",
      "label": "Lab 2",
      "description": "Secondary laboratory"
    }
  ],
  "status": 200,
  "success": true
}
```

### GET /metadata/users

Returns a list of users for assignment dropdowns.

**Response:**
```json
{
  "data": [
    {
      "value": "john_doe",
      "label": "John Doe",
      "email": "john.doe@example.com"
    },
    {
      "value": "jane_smith",
      "label": "Jane Smith",
      "email": "jane.smith@example.com"
    }
  ],
  "status": 200,
  "success": true
}
```

## Sample Endpoints

### GET /samples

Get all samples with pagination and filtering options.

**Query Parameters:**
- `page` (integer, default=1): Page number
- `limit` (integer, default=10): Number of items per page
- `type` (array): Filter by sample types (can specify multiple)
- `status` (array): Filter by sample statuses (can specify multiple)
- `location` (array): Filter by lab locations (can specify multiple)
- `owner` (array): Filter by sample owners (can specify multiple)
- `search` (string): Search term for sample name or ID

**Example Request:**
```
GET /samples?page=1&limit=10&type=Blood&type=Tissue&status=submitted
```

**Response:**
```json
{
  "data": {
    "data": [
      {
        "id": "sample-001",
        "name": "Blood Sample A",
        "type": "Blood",
        "submission_date": "2025-06-15T00:00:00",
        "status": "submitted",
        "owner": "John Doe",
        "box_id": "box-001",
        "location": "Lab 1",
        "last_movement": "2025-06-15T00:00:00",
        "volume_left": 10.0,
        "total_volume": 15.0,
        "aliquots_created": 2,
        "aliquots": []
      }
    ],
    "total_count": 1,
    "total_pages": 1,
    "current_page": 1,
    "page_size": 10,
    "has_more": false
  },
  "status": 200,
  "success": true
}
```

### POST /samples

Create a new sample.

**Request Body:**
```json
{
  "name": "Blood Sample B",
  "type": "Blood",
  "owner": "Jane Smith",
  "volume": 20.0,
  "box_id": "box-002",
  "notes": "Morning collection"
}
```

**Response:**
```json
{
  "data": {
    "id": "sample-002",
    "name": "Blood Sample B",
    "type": "Blood",
    "submission_date": "2025-07-08T10:30:00",
    "status": "submitted",
    "owner": "Jane Smith",
    "box_id": "box-002",
    "location": null,
    "last_movement": "2025-07-08T10:30:00",
    "volume_left": 20.0,
    "total_volume": 20.0,
    "aliquots_created": 0,
    "aliquots": []
  },
  "status": 201,
  "success": true
}
```

### GET /samples/{sample_id}

Get a specific sample by its ID.

**Example Request:**
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
    "submission_date": "2025-06-15T00:00:00",
    "status": "submitted",
    "owner": "John Doe",
    "box_id": "box-001",
    "location": "Lab 1",
    "last_movement": "2025-06-15T00:00:00",
    "volume_left": 10.0,
    "total_volume": 15.0,
    "aliquots_created": 2,
    "aliquots": [
      {
        "id": "aliquot-001",
        "volume": 5.0,
        "created_at": "2025-06-16T00:00:00",
        "location": "Freezer 1, Rack 3",
        "tests": []
      }
    ]
  },
  "status": 200,
  "success": true
}
```

### PATCH /samples/{sample_id}

Update a specific sample.

**Example Request:**
```
PATCH /samples/sample-001
```

**Request Body:**
```json
{
  "name": "Updated Blood Sample A",
  "status": "aliquots_created",
  "location": "Lab 2"
}
```

**Response:**
```json
{
  "data": {
    "id": "sample-001",
    "name": "Updated Blood Sample A",
    "type": "Blood",
    "submission_date": "2025-06-15T00:00:00",
    "status": "aliquots_created",
    "owner": "John Doe",
    "box_id": "box-001",
    "location": "Lab 2",
    "last_movement": "2025-07-08T11:00:00",
    "volume_left": 10.0,
    "total_volume": 15.0,
    "aliquots_created": 2,
    "aliquots": []
  },
  "status": 200,
  "success": true
}
```

### DELETE /samples/{sample_id}

Delete a sample.

**Example Request:**
```
DELETE /samples/sample-001
```

**Response:**
```json
{
  "data": {
    "message": "Sample deleted successfully"
  },
  "status": 200,
  "success": true
}
```

## Aliquot Endpoints

### GET /samples/{sample_id}/aliquots

Get all aliquots for a specific sample.

**Response:**
```json
{
  "data": [
    {
      "id": "aliquot-001",
      "sample_id": "sample-001",
      "volume": 5.0,
      "created_at": "2025-06-16T00:00:00",
      "location": "Freezer 1, Rack 3",
      "tests": []
    }
  ],
  "status": 200,
  "success": true
}
```

### POST /samples/{sample_id}/aliquots

Create a new aliquot for a sample.

**Request Body:**
```json
{
  "volume": 5.0,
  "location": "Freezer 2, Rack 1"
}
```

**Response:**
```json
{
  "data": {
    "id": "aliquot-003",
    "sample_id": "sample-001",
    "volume": 5.0,
    "created_at": "2025-07-08T11:30:00",
    "location": "Freezer 2, Rack 1",
    "tests": []
  },
  "status": 201,
  "success": true
}
```

## Test Endpoints

### POST /samples/{sample_id}/aliquots/{aliquot_id}/tests

Add a test to an aliquot.

**Request Body:**
```json
{
  "name": "CBC",
  "method": "Automated Analysis",
  "assigned_to": "Lab Technician 1",
  "notes": "Priority test"
}
```

**Response:**
```json
{
  "data": {
    "id": "test-002",
    "name": "CBC",
    "status": "pending",
    "assigned_to": "Lab Technician 1",
    "start_date": "2025-07-08T12:00:00",
    "completion_date": null,
    "method": "Automated Analysis",
    "results": null,
    "notes": "Priority test"
  },
  "status": 201,
  "success": true
}
```

### PATCH /samples/{sample_id}/aliquots/{aliquot_id}/tests/{test_id}

Update a test.

**Request Body:**
```json
{
  "status": "completed",
  "results": "Normal values",
  "completion_date": "2025-07-09T14:30:00"
}
```

**Response:**
```json
{
  "data": {
    "id": "test-002",
    "name": "CBC",
    "status": "completed",
    "assigned_to": "Lab Technician 1",
    "start_date": "2025-07-08T12:00:00",
    "completion_date": "2025-07-09T14:30:00",
    "method": "Automated Analysis",
    "results": "Normal values",
    "notes": "Priority test"
  },
  "status": 200,
  "success": true
}
```

## Full Workflow

1. Get metadata for dropdowns via `/metadata/sample-types`, `/metadata/sample-statuses`, etc.
2. Create a sample via `POST /samples`
3. Create aliquots from the sample via `POST /samples/{sample_id}/aliquots`
4. Verify sample status has updated to "aliquots_created"
5. Add tests to aliquots via `POST /samples/{sample_id}/aliquots/{aliquot_id}/tests`
6. Update test status and results via `PATCH /samples/{sample_id}/aliquots/{aliquot_id}/tests/{test_id}`
7. When all tests are completed, the sample status should update to "testing_completed"

## Common Error Responses

### Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ],
  "status": 422,
  "success": false
}
```

### Not Found Error
```json
{
  "detail": "Sample with ID 'invalid-id' not found",
  "status": 404,
  "success": false
}
```

### Internal Server Error
```json
{
  "detail": "An internal server error occurred",
  "status": 500,
  "success": false
}
```
