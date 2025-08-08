# Equipment API Documentation

This document describes the API endpoints and data types for the Equipment Management module.

## Base URL
```
/api/metadata
```

## Data Types

### Equipment
```typescript
interface Equipment {
  id: string;                 // Unique identifier for the equipment
  name: string;              // Name of the equipment
  description?: string;      // Optional description
  type: EquipmentType;       // Type of equipment (from enum)
  model: string;             // Equipment model number
  manufacturer: string;      // Manufacturer name
  serialNumber: string;      // Serial number
  location: string;         // Physical location
  status: EquipmentStatus;   // Current status (from enum)
  assignedTo?: string;      // Optional user assignment
  team?: string;           // Optional team assignment
  calibration: {
    lastDate: string;      // ISO date string
    nextDate: string;      // ISO date string
    calibratedBy: string;  // Name of calibration provider
    certificate?: string;  // Optional certificate file reference
  };
  maintenanceHistory: MaintenanceRecord[];
  notes: Note[];
  attachments: Attachment[];
}
```

### MaintenanceRecord
```typescript
interface MaintenanceRecord {
  id: string;           // Unique identifier for the maintenance record
  date: string;         // ISO date string
  performedBy: string;  // Name of person who performed maintenance
  task: string;         // Description of maintenance task
  status: string;       // Status of maintenance (Completed, In Progress, etc.)
  notes?: string;       // Optional notes about maintenance
}
```

### Note
```typescript
interface Note {
  id: string;           // Unique identifier for the note
  content: string;      // Note content
  timestamp: string;    // ISO date string
  user: string;        // User who created the note
}
```

### Attachment
```typescript
interface Attachment {
  id: string;           // Unique identifier for the attachment
  name: string;         // File name
  type: string;         // MIME type
  url: string;         // File URL
  uploadedAt: string;  // ISO date string
}
```

### Enums
```typescript
type EquipmentType =
  | 'HPLC'
  | 'Centrifuge'
  | 'Microscope'
  | 'PCR'
  | 'Spectrophotometer'
  | 'Balance'
  | 'pH Meter';

type EquipmentStatus =
  | 'Available'
  | 'In Use'
  | 'Under Maintenance'
  | 'Out of Service'
  | 'Quarantined';
```

## Endpoints

### Get All Equipment
```
GET /equipment
```
Returns a list of all equipment.

**Response**
```typescript
{
  data: Equipment[];
  status: number;
  success: boolean;
}
```

### Get Equipment Types
```
GET /equipment_types
```
Returns list of available equipment types.

**Response**
```typescript
{
  data: Array<{
    id: number;
    value: EquipmentType;
    description: string;
  }>;
  status: number;
  success: boolean;
}
```

### Get Equipment Statuses
```
GET /equipment_statuses
```
Returns list of available equipment statuses.

**Response**
```typescript
{
  data: Array<{
    id: number;
    value: EquipmentStatus;
    description: string;
  }>;
  status: number;
  success: boolean;
}
```

### Create Equipment
```
POST /equipment
```
Creates a new equipment record.

**Request Body**
```typescript
Omit<Equipment, 'id' | 'maintenanceHistory' | 'notes' | 'attachments'>
```

**Response**
```typescript
{
  data: Equipment;
  status: number;
  success: boolean;
}
```

### Update Equipment
```
PUT /equipment/{id}
```
Updates an existing equipment record.

**Parameters**
- `id`: string (path parameter)

**Request Body**
```typescript
Partial<Equipment>
```

**Response**
```typescript
{
  data: Equipment;
  status: number;
  success: boolean;
}
```

### Delete Equipment
```
DELETE /equipment/{id}
```
Deletes an equipment record.

**Parameters**
- `id`: string (path parameter)

**Response**
```typescript
{
  status: number;
  success: boolean;
}
```

### Add Maintenance Record
```
POST /equipment/{id}/maintenance
```
Adds a maintenance record to equipment.

**Parameters**
- `id`: string (path parameter)

**Request Body**
```typescript
Omit<MaintenanceRecord, 'id'>
```

**Response**
```typescript
{
  data: Equipment;
  status: number;
  success: boolean;
}
```

### Add Note
```
POST /equipment/{id}/notes
```
Adds a note to equipment.

**Parameters**
- `id`: string (path parameter)

**Request Body**
```typescript
{
  content: string;
  user: string;
}
```

**Response**
```typescript
{
  data: Equipment;
  status: number;
  success: boolean;
}
```

### Add Attachment
```
POST /equipment/{id}/attachments
```
Adds an attachment to equipment.

**Parameters**
- `id`: string (path parameter)

**Request Body**
```
FormData containing file
```

**Response**
```typescript
{
  data: Equipment;
  status: number;
  success: boolean;
}
```

## Error Responses

All endpoints may return the following error response:

```typescript
{
  status: number;
  success: false;
  detail: string;
}
```

Common error status codes:
- 400: Bad Request (invalid input)
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

## Pagination and Filtering

For the GET /equipment endpoint, the following query parameters are supported:

```typescript
interface EquipmentQueryParams {
  page?: number;        // Page number (default: 1)
  limit?: number;       // Items per page (default: 20)
  type?: string;        // Filter by equipment type
  status?: string;      // Filter by status
  location?: string;    // Filter by location
  manufacturer?: string; // Filter by manufacturer
  search?: string;      // Search in name, description, and serial number
  sortBy?: string;      // Field to sort by
  sortOrder?: 'asc' | 'desc'; // Sort order
}
```

When using pagination, the response includes additional metadata:

```typescript
{
  data: Equipment[];
  status: number;
  success: boolean;
  pagination: {
    currentPage: number;
    totalPages: number;
    totalItems: number;
    itemsPerPage: number;
    hasMore: boolean;
  }
}
```
