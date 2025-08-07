# LIMS Database Setup Guide

This guide explains how to set up the comprehensive LIMS database schema.

## Prerequisites

1. **PostgreSQL** installed and running
2. **Python** with required dependencies
3. **Database credentials** configured

## Database Configuration

### 1. Environment Variables

Create a `.env` file in the server directory with the following configuration:

```env
# Database Configuration
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=lims

# Application Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### 2. Create Database

First, create the database:

```bash
# Connect to PostgreSQL as superuser
psql -U postgres

# Create the database
CREATE DATABASE lims;

# Exit psql
\q
```

### 3. Run Schema Creation

You have two options to create the schema:

#### Option A: Using SQL Script (Recommended)

```bash
# Run the SQL script directly
psql -U postgres -d lims -f create_schema.sql
```

#### Option B: Using Python Script

```bash
# Install dependencies if not already installed
pip install psycopg2-binary python-dotenv sqlalchemy

# Run the database creation script
python create_database.py
```

## Schema Overview

The LIMS database includes the following main components:

### Core Tables
- **users** - User management with UUID primary keys
- **audit_trail** - Complete audit logging
- **electronic_signature** - Digital signatures

### Storage Hierarchy
- **storage_location** - Top-level storage locations
- **storage_room** - Rooms within locations
- **freezer** - Freezers within rooms
- **box** - Storage boxes within freezers
- **inventory_slot** - Individual slots within boxes

### Sample Management
- **sample_type** - Types of samples
- **sample** - Main sample records
- **aliquot** - Sample aliquots
- **chain_of_custody** - Sample transfer tracking
- **sample_status_log** - Status change history
- **storage_transaction_log** - Storage movement history

### Material Management
- **material** - Materials and reagents
- **material_lot** - Specific lots of materials
- **material_usage_log** - Usage tracking
- **material_inventory_adjustment** - Inventory adjustments

### Instrument Management
- **instrument** - Laboratory instruments
- **instrument_calibration** - Calibration records
- **instrument_maintenance_log** - Maintenance history

### Testing & Methods
- **test_method** - Test methods and procedures
- **test_parameter** - Parameters for tests
- **test_specification** - Specifications for parameters
- **test_procedure** - Step-by-step procedures
- **test_step** - Individual test steps
- **test_step_execution** - Step execution records
- **test_master** - Master test definitions
- **test** - Individual test instances
- **test_result** - Test results

### Quality Events
- **oos** - Out of Specification events
- **oos_investigation** - OOS investigation records
- **deviation** - Deviation management
- **capa** - Corrective and Preventive Actions
- **capa_action** - CAPA action items

## Enum Types

The schema includes comprehensive enum types for:

- **sample_priority** - Low, Medium, High, Urgent
- **sample_status** - Logged_In, In_Progress, Completed, Archived
- **specification_type_enum** - Exact, Range, Less_Than, Greater_Than
- **parameter_type_enum** - Numeric, Text, Boolean, DateTime
- **step_result_enum** - Pass, Fail, NA
- **test_status_enum** - Pending, In_Progress, Completed, Cancelled
- **result_status_enum** - Pass, Fail, OOS, Invalid
- **investigation_phase** - phase1_lab, phase2_qc, phase3_qa
- **deviation_severity** - minor, major, critical
- **deviation_status** - open, under_investigation, closed
- **capa_action_type** - corrective, preventive, both
- **capa_status** - open, in_progress, closed, verified, cancelled
- **capa_task_status** - pending, in_progress, completed

## Indexes

The schema includes comprehensive indexing for optimal performance:

- Foreign key indexes
- Unique constraint indexes
- Search optimization indexes
- Status-based query indexes

## Sample Data

The schema includes basic sample data:

- Default users (John Doe, Jane Smith, Bob Wilson)
- Sample types (Blood, Urine, Tissue, Environmental)
- Basic storage hierarchy (Main Lab → Storage Room 1 → Freezer 1 → Box 1)

## Verification

To verify the database setup:

```bash
# Connect to the database
psql -U postgres -d lims

# Check tables
\dt

# Check enums
\dT

# Check sample data
SELECT * FROM users;
SELECT * FROM sample_type;
SELECT * FROM storage_location;

# Exit
\q
```

## Troubleshooting

### Common Issues

1. **Permission denied**: Ensure your PostgreSQL user has CREATE privileges
2. **Database doesn't exist**: Create the database first using `CREATE DATABASE lims;`
3. **Extension not found**: Ensure `uuid-ossp` extension is available
4. **Connection refused**: Check PostgreSQL service is running

### Reset Database

To completely reset the database:

```sql
-- Drop all tables (run in psql)
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;

-- Then re-run the schema creation script
```

## Next Steps

After setting up the database:

1. Configure your application to connect to the database
2. Set up Alembic migrations for future schema changes
3. Create API endpoints for the new models
4. Update the frontend to work with the new schema

## Support

For issues with database setup, check:

1. PostgreSQL logs
2. Connection string format
3. User permissions
4. Extension availability 