# LIMS Full Workflow Validation Guide

This guide provides a step-by-step process to validate the complete workflow from metadata to sample/test/aliquot CRUD operations.

## Prerequisites

- Backend server running
- Frontend development server running
- User logged in (if authentication is implemented)

## 1. Metadata Workflow Validation

### Step 1: Validate Metadata API Endpoints

1. Open your browser's developer tools (F12)
2. Navigate to the Network tab
3. Verify the following API calls return valid data:
   - `GET /metadata/sample-types`
   - `GET /metadata/sample-statuses` 
   - `GET /metadata/lab-locations`
   - `GET /metadata/users`

Each response should have:
- `success: true`
- `status: 200`
- `data` array containing objects with at least `value` and `label` properties

### Step 2: Verify Frontend Dropdown Population

1. Navigate to any form that has dropdowns (e.g., sample creation form)
2. Verify that the dropdowns for these fields are populated with values from metadata endpoints:
   - Sample Type dropdown → values from `/metadata/sample-types`
   - Owner dropdown → values from `/metadata/users`
   - Location dropdown → values from `/metadata/lab-locations`

## 2. Sample Management Workflow

### Step 1: Create a Sample

1. Navigate to the sample creation form
2. Fill in required fields:
   - Name: "Test Sample 001"
   - Type: Select a type from the dropdown (e.g., "Blood")
   - Owner: Select an owner from the dropdown
   - Volume: 20.0 mL
3. Submit the form
4. Verify in the Network tab that a `POST /samples` request is made with the correct data
5. Verify the response includes a new sample ID and status is "submitted"
6. Verify the sample appears in the samples list/table

### Step 2: View Sample Details

1. Click on the newly created sample to view its details
2. Verify a `GET /samples/{sample_id}` request is made
3. Verify all sample details display correctly:
   - Basic information (name, type, owner)
   - Status ("submitted")
   - Volume information
   - No aliquots should be present yet

### Step 3: Update Sample Information

1. Edit the sample (click edit button or similar)
2. Change some fields:
   - Update the name to "Updated Test Sample 001"
   - Change the location (if editable)
3. Save the changes
4. Verify a `PATCH /samples/{sample_id}` request is made
5. Verify the updated information appears in the UI

## 3. Aliquot Management Workflow

### Step 1: Create Aliquots

1. Navigate to the sample details page for your test sample
2. Find the "Create Aliquot" button/form
3. Create an aliquot with:
   - Volume: 5.0 mL
   - Location: Select a location from dropdown
4. Submit the form
5. Verify a `POST /samples/{sample_id}/aliquots` request is made
6. Verify the aliquot appears in the UI under the sample
7. Verify the sample status has changed to "aliquots_created"
8. Verify the sample's remaining volume has decreased by 5.0 mL

### Step 2: Create Another Aliquot

1. Create another aliquot:
   - Volume: 5.0 mL
   - Location: Select a different location
2. Verify the same process as above
3. Verify the sample now has 2 aliquots listed
4. Verify the sample's remaining volume has decreased by another 5.0 mL

## 4. Test Management Workflow

### Step 1: Add Tests to Aliquots

1. Navigate to one of the aliquots
2. Find the "Add Test" button/form
3. Create a test with:
   - Name: "Test CBC"
   - Method: Select a method
   - Assigned To: Select a user
4. Submit the form
5. Verify a `POST /samples/{sample_id}/aliquots/{aliquot_id}/tests` request is made
6. Verify the test appears under the aliquot with "pending" status

### Step 2: Update Test Status

1. Find the test you just created
2. Update its status to "in_progress"
3. Verify a `PATCH /samples/{sample_id}/aliquots/{aliquot_id}/tests/{test_id}` request is made
4. Verify the test status changes in the UI

### Step 3: Complete a Test

1. Update the test status to "completed"
2. Add test results: "Normal range detected"
3. Verify the same PATCH request is made with the updated information
4. Verify all tests for an aliquot are shown properly

## 5. Sample Status Workflow

### Step 1: Complete All Tests

1. If you have multiple tests, update them all to "completed" status
2. Verify that when all tests are completed, a request is made to update the sample status
3. Verify the sample status changes to "testing_completed"

### Step 2: Final Storage

1. Update the sample location to indicate final storage (e.g., "Freezer")
2. Verify the sample status changes to "in_storage"

## 6. Filtering and Search

### Step 1: Test Filter By Sample Type

1. Navigate to the samples list view
2. Apply a filter for sample type (e.g., "Blood")
3. Verify a `GET /samples?type=Blood` request is made
4. Verify only samples with that type are shown

### Step 2: Test Multiple Filter Values

1. Select multiple sample types as filters
2. Verify a request like `GET /samples?type=Blood&type=Tissue` is made
3. Verify the results include samples with any of those types

### Step 3: Test Combination of Filters

1. Apply filters for both type and status
2. Verify the correct query parameters are sent
3. Verify the results match the filter criteria

## 7. Export Functionality

1. Navigate to the samples list view
2. Apply any filters you want to test
3. Click the "Export" button
4. Verify a request to `/samples/export` with the correct filter parameters is made
5. Verify the CSV/Excel file downloads correctly and contains the expected data

## Common Issues to Check

1. **Case Transformation Issues**: Watch for snake_case vs camelCase mismatches in the Network tab
2. **Enum Value Consistency**: Verify that enum values sent by the frontend match those expected by the backend
3. **Filter Parameter Encoding**: Make sure array parameters are properly encoded in URL
4. **Error Handling**: Intentionally cause an error (e.g., submit invalid data) to test error handling

## Documentation Verification

1. Compare actual API behavior against documented behavior in:
   - `docs/api_documentation.md`
   - Backend code comments
   - Swagger documentation (if available)

2. Note any discrepancies for updating documentation

By following this validation guide, you'll thoroughly test the complete LIMS workflow and ensure proper integration between frontend and backend.
