# Database Package Documentation

## Overview

This package provides comprehensive database management for the LIMS (Laboratory Information Management System) application. It includes database models, initialization scripts, and seeding utilities designed for production use.

## Package Structure

```
server/app/db/
├── __init__.py          # Package exports and model registration
├── init_db.py           # Database initialization with error handling
├── seed.py              # Production-ready database seeding
├── models/              # SQLAlchemy model definitions
│   ├── __init__.py      # Model exports
│   ├── base.py          # Base model class
│   ├── user.py          # User and authentication models
│   ├── sample.py        # Sample management models
│   ├── test.py          # Test and analysis models
│   ├── storage.py       # Storage location models
│   ├── storage_hierarchy.py  # Storage hierarchy and tracking
│   ├── material.py      # Material and inventory models
│   ├── instrument.py    # Instrument management models
│   ├── quality_events.py     # Quality events (OOS, CAPA, etc.)
│   ├── audit.py         # Audit trail and signatures
│   └── product.py       # Product management models
└── README.md           # This documentation
```

## Key Features

### Database Initialization (`init_db.py`)
- **Production-ready error handling**: Comprehensive exception handling with detailed logging
- **Step-by-step validation**: Each initialization step is verified before proceeding
- **PostgreSQL extensions**: Automatic creation of required extensions (uuid-ossp)
- **Enum types**: Systematic creation of all required enum types
- **Connection verification**: Database connectivity tests before and after initialization

### Database Seeding (`seed.py`)
- **Transaction management**: All seeding operations wrapped in transactions
- **Comprehensive test data**: Realistic pharmaceutical lab data including:
  - User accounts with proper roles
  - Storage hierarchy (locations → rooms → freezers → boxes)
  - Sample types for pharmaceutical testing
  - Test methods (HPLC, dissolution, microbial testing, etc.)
  - Materials and reagents with lot tracking
  - Instruments with calibration tracking
  - Sample workflow data
- **Error handling**: Proper rollback on failures with detailed logging
- **Idempotent operations**: Safe to run multiple times without data duplication

### Package Exports (`__init__.py`)
- **Organized imports**: Clean separation of database utilities and models
- **Model registration**: All models properly registered with SQLAlchemy
- **Type safety**: Proper exports for IDE support and type checking

## Usage

### Initialize Database
```python
from app.db import init_database

# Initialize complete database schema
success = init_database()
if success:
    print("Database ready!")
```

### Seed Database
```python
from app.db import seed_database

# Seed with comprehensive test data
seed_database()
```

### Use Database Session
```python
from app.db import get_db

# Get database session
db = get_db()

# Or use context manager
from app.db import db_manager
with db_manager.get_db_session() as session:
    # Your database operations
    pass
```

### Import Models
```python
from app.db import Sample, Test, Users, StorageLocation
# All models available as clean imports
```

## Production Considerations

### Logging
- All database operations include comprehensive logging
- Error messages provide actionable information for troubleshooting
- Success messages confirm completion of operations

### Error Handling
- Database connection failures are handled gracefully
- Transaction rollbacks prevent partial data states
- Clear error messages for debugging

### Performance
- Connection pooling configured in core database manager
- Efficient bulk operations for seeding
- Proper indexing through model definitions

### Security
- Password hashing using bcrypt
- No sensitive data in logs
- Proper transaction isolation

## Development Workflow

1. **First Setup**:
   ```bash
   # Initialize database schema
   python -m app.db.init_db
   
   # Seed with test data
   python -m app.db.seed
   ```

2. **Regular Development**:
   - Use the seeded data for testing
   - Models are automatically available through package imports
   - Database sessions managed by core database manager

3. **Adding New Models**:
   - Create model in appropriate file under `models/`
   - Add import to `models/__init__.py`
   - Add export to main `__init__.py`
   - Run database initialization to create new tables

## Quality Assurance

### Code Standards
- Type hints throughout for better IDE support
- Comprehensive docstrings for all functions and classes
- Clean separation of concerns
- Production-ready error handling

### Testing
- Seeded data provides comprehensive test scenarios
- All database operations are transactional
- Proper cleanup mechanisms in place

### Maintainability
- Modular structure for easy maintenance
- Clear documentation and code comments
- Consistent naming conventions
- Centralized configuration through core database manager

This database package provides a solid foundation for the LIMS application with production-ready features, comprehensive error handling, and maintainable code structure.