# Inventory Management API Documentation

## Overview
This document describes the API endpoints available for managing inventory in the LIMS system. The API provides functionality for managing materials, material lots, usage logs, and inventory adjustments.

## Base URL
All API endpoints are prefixed with `/api/inventory`

## Authentication
All endpoints require authentication. Include the authentication token in the Authorization header:
```
Authorization: Bearer <your_token>
```

## Endpoints

### Materials

#### GET /materials
Get a list of materials with optional filtering.

**Query Parameters:**
- `skip` (integer, optional): Number of records to skip (default: 0)
- `limit` (integer, optional): Maximum number of records to return (default: 100)
- `search` (string, optional): Search term to filter materials by name, CAS number, or manufacturer
- `material_type` (string, optional): Filter by material type

**Response:** Array of Material objects

#### POST /materials
Create a new material.

**Request Body:**
```json
{
    "name": "string",
    "material_type": "string",
    "cas_number": "string",
    "manufacturer": "string",
    "grade": "string",
    "unit_of_measure": "string",
    "shelf_life_days": "integer",
    "is_controlled": "boolean"
}
```

**Response:** Created Material object

#### GET /materials/{material_id}
Get a specific material by ID.

**Response:** Material object

#### PUT /materials/{material_id}
Update a specific material.

**Request Body:** Same as POST /materials
**Response:** Updated Material object

### Material Lots

#### GET /material-lots
Get a list of material lots with optional filtering.

**Query Parameters:**
- `skip` (integer, optional): Number of records to skip
- `limit` (integer, optional): Maximum number of records to return
- `material_id` (integer, optional): Filter by material ID
- `status` (string, optional): Filter by lot status

**Response:** Array of MaterialLot objects

#### POST /material-lots
Create a new material lot.

**Request Body:**
```json
{
    "material_id": "integer",
    "lot_number": "string",
    "received_date": "datetime",
    "expiry_date": "datetime",
    "received_quantity": "decimal",
    "current_quantity": "decimal",
    "storage_location_id": "integer",
    "status": "string",
    "remarks": "string"
}
```

**Response:** Created MaterialLot object

#### GET /material-lots/{lot_id}
Get a specific material lot by ID.

**Response:** MaterialLot object

#### PUT /material-lots/{lot_id}
Update a specific material lot.

**Request Body:** Partial MaterialLot object (only include fields to update)
**Response:** Updated MaterialLot object

### Usage Logs

#### POST /usage-logs
Record material usage.

**Request Body:**
```json
{
    "material_lot_id": "integer",
    "used_by": "string",
    "used_quantity": "decimal",
    "purpose": "string",
    "associated_sample_id": "integer",
    "remarks": "string"
}
```

**Response:** Created MaterialUsageLog object

#### GET /usage-logs
Get material usage logs with optional filtering.

**Query Parameters:**
- `skip` (integer, optional): Number of records to skip
- `limit` (integer, optional): Maximum number of records to return
- `material_lot_id` (integer, optional): Filter by material lot ID
- `start_date` (datetime, optional): Filter by usage date range start
- `end_date` (datetime, optional): Filter by usage date range end

**Response:** Array of MaterialUsageLog objects

### Inventory Adjustments

#### POST /inventory-adjustments
Create an inventory adjustment record.

**Request Body:**
```json
{
    "material_lot_id": "integer",
    "adjusted_by": "string",
    "adjustment_type": "string",
    "quantity": "decimal",
    "reason": "string",
    "remarks": "string"
}
```

**Response:** Created MaterialInventoryAdjustment object

#### GET /inventory-adjustments
Get inventory adjustments with optional filtering.

**Query Parameters:**
- `skip` (integer, optional): Number of records to skip
- `limit` (integer, optional): Maximum number of records to return
- `material_lot_id` (integer, optional): Filter by material lot ID
- `adjustment_type` (string, optional): Filter by adjustment type
- `start_date` (datetime, optional): Filter by adjustment date range start
- `end_date` (datetime, optional): Filter by adjustment date range end

**Response:** Array of MaterialInventoryAdjustment objects

## Error Responses

All endpoints may return the following error responses:

- `400 Bad Request`: Invalid request parameters or payload
- `401 Unauthorized`: Missing or invalid authentication token
- `403 Forbidden`: Insufficient permissions to perform the action
- `404 Not Found`: Requested resource not found
- `422 Unprocessable Entity`: Request validation error
- `500 Internal Server Error`: Server-side error

## Pagination

List endpoints support pagination through `skip` and `limit` parameters. The default page size is 100 records.

## Filtering

Many endpoints support filtering through query parameters. Multiple filters can be combined to narrow down the results.

## Data Types

- `integer`: Whole number
- `string`: Text value
- `boolean`: True/false value
- `decimal`: Numeric value with decimal places
- `datetime`: ISO 8601 formatted date-time string (e.g., "2025-08-05T14:30:00Z")

## Best Practices

1. Always include appropriate error handling in your client application
2. Use filtering parameters to reduce the amount of data transferred
3. Implement pagination when displaying large datasets
4. Handle datetime values in UTC to avoid timezone issues
5. Validate input data before sending requests
6. Include appropriate content-type headers (application/json)
