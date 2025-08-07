"""
Main application entry point for the LIMS Sample Management API.

This module initializes the FastAPI application with proper configuration,
middleware, and route registration.
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

# Import core modules
from app.core.config import settings, get_settings
from app.core.logging import setup_logging
from app.core.database import initialize_database, close_database, test_database_connection
from app.core.exceptions import LIMSException, lims_exception_handler

# Import routes
from app.api.routes.sample_routes import router as sample_router
from app.api.routes.aliquot_routes import router as aliquot_router
from app.api.routes.test_routes import router as test_router, test_methods_router
from app.api.routes.audit_routes import router as audit_router
from app.api.routes.product_routes import router as product_router
# from app.api.routes.auth_routes import router as auth_router
from app.api.routes.metadata_routes import metadata_router
from app.api.routes.storage_routes import router as storage_router

# Import enums for OpenAPI schema
from app.utils.constants import (
    SampleStatus as SampleStatusEnum, 
    TestStatus as TestStatusEnum, 
    SampleType as SampleTypeEnum,
    Location as LocationEnum, 
    EquipmentType as EquipmentTypeEnum,
    EquipmentStatus as EquipmentStatusEnum,
    SpecificationType as SpecificationTypeEnum,
    InventoryCategory as InventoryCategoryEnum,
    InventoryStatus as InventoryStatusEnum
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    try:
        
        
        # Initialize database
        initialize_database()
        
        # Test database connection
        if not test_database_connection():
            raise Exception("Database connection failed")
        
        yield
        
    except Exception as e:
        print(f"Application startup error: {e}")
        raise
    finally:
        # Shutdown
        close_database()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    
    app = FastAPI(
        title=settings.app_name,
        description="API for managing laboratory samples, aliquots and tests.",
        version=settings.app_version,
        # docs_url=settings.docs_url,
        # redoc_url=settings.redoc_url,
        lifespan=lifespan
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add exception handlers
    app.add_exception_handler(LIMSException, lims_exception_handler)
    
    # Register routes
    app.include_router(sample_router, prefix=settings.api_prefix)
    app.include_router(aliquot_router, prefix=settings.api_prefix)
    app.include_router(test_router, prefix=settings.api_prefix)
    app.include_router(test_methods_router, prefix=settings.api_prefix)
    app.include_router(audit_router, prefix=settings.api_prefix)
    app.include_router(product_router, prefix=settings.api_prefix)
    # app.include_router(auth_router, prefix=settings.api_prefix)
    app.include_router(metadata_router, prefix=settings.api_prefix)
    app.include_router(storage_router, prefix=settings.api_prefix)
    
    return app


# Create application instance
app = create_app()


@app.get("/health")
async def health_check():
    """Health check endpoint to verify application and database status."""
    try:
        # Test database connection
        if not test_database_connection():
            return JSONResponse(
                status_code=503,
                content={
                    "status": "unhealthy",
                    "database": "disconnected",
                    "message": "Database connection failed"
                }
            )
        
        return {
            "status": "healthy",
            "database": "connected",
            "message": "Application is running and database is accessible",
            "version": settings.app_version
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "database": "disconnected",
                "message": f"Application error: {str(e)}",
                "error": str(e)
            }
        )


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": settings.app_name,
        "version": settings.app_version,
        "docs": settings.docs_url,
        "health": "/health"
    }


def custom_openapi():
    """Generate custom OpenAPI schema with enum definitions."""
    if app.openapi_schema:
        return app.openapi_schema
        
    openapi_schema = get_openapi(
        title=settings.app_name,
        version=settings.app_version,
        description="API for managing laboratory samples, aliquots and tests",
        routes=app.routes,
    )
    
    # Add enum definitions to schema components
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}
    if "schemas" not in openapi_schema["components"]:
        openapi_schema["components"]["schemas"] = {}
    
    # Define enum schemas
    enum_schemas = {
        "SampleTypeEnum": {
            "type": "string",
            "enum": [e.value for e in SampleTypeEnum],
            "title": "SampleTypeEnum",
            "description": "Types of samples in the system",
            "x-enumNames": [e.name for e in SampleTypeEnum]
        },
        "SampleStatusEnum": {
            "type": "string",
            "enum": [e.value for e in SampleStatusEnum],
            "title": "SampleStatusEnum",
            "description": "Status values for samples in the system",
            "x-enumNames": [e.name for e in SampleStatusEnum]
        },
        "TestStatusEnum": {
            "type": "string",
            "enum": [e.value for e in TestStatusEnum],
            "title": "TestStatusEnum",
            "description": "Status values for tests in the system",
            "x-enumNames": [e.name for e in TestStatusEnum]
        },
        "LocationEnum": {
            "type": "string",
            "enum": [e.value for e in LocationEnum],
            "title": "LocationEnum",
            "description": "Lab locations in the system",
            "x-enumNames": [e.name for e in LocationEnum]
        },
        "EquipmentTypeEnum": {
            "type": "string",
            "enum": [e.value for e in EquipmentTypeEnum],
            "title": "EquipmentTypeEnum",
            "description": "Types of equipment available in the system",
            "x-enumNames": [e.name for e in EquipmentTypeEnum]
        },
        "EquipmentStatusEnum": {
            "type": "string",
            "enum": [e.value for e in EquipmentStatusEnum],
            "title": "EquipmentStatusEnum",
            "description": "Status values for equipment in the system",
            "x-enumNames": [e.name for e in EquipmentStatusEnum]
        },
        "InventoryCategoryEnum": {
            "type": "string", 
            "enum": [e.value for e in InventoryCategoryEnum],
            "title": "InventoryCategoryEnum",
            "description": "Categories for inventory items",
            "x-enumNames": [e.name for e in InventoryCategoryEnum]
        },
        "InventoryStatusEnum": {
            "type": "string",
            "enum": [e.value for e in InventoryStatusEnum],
            "title": "InventoryStatusEnum",
            "description": "Status values for inventory items",
            "x-enumNames": [e.name for e in InventoryStatusEnum]
        },
        "SpecificationTypeEnum": {
            "type": "string",
            "enum": [e.value for e in SpecificationTypeEnum],
            "title": "SpecificationTypeEnum",
            "description": "Types of specifications in the system",
            "x-enumNames": [e.name for e in SpecificationTypeEnum]
        }
    }
    
    # Add enum schemas to OpenAPI schema
    openapi_schema["components"]["schemas"].update(enum_schemas)
    
    # Update query parameter schemas for enum arrays
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            if "parameters" in openapi_schema["paths"][path][method]:
                for i, param in enumerate(openapi_schema["paths"][path][method]["parameters"]):
                    if param.get("name") in ["type", "status", "location"]:
                        if param["name"] == "type":
                            openapi_schema["paths"][path][method]["parameters"][i]["schema"] = {
                                "type": "array",
                                "items": {"$ref": "#/components/schemas/SampleTypeEnum"},
                                "title": "Type"
                            }
                        elif param["name"] == "status":
                            openapi_schema["paths"][path][method]["parameters"][i]["schema"] = {
                                "type": "array",
                                "items": {"$ref": "#/components/schemas/SampleStatusEnum"},
                                "title": "Status"
                            }
                        elif param["name"] == "location":
                            openapi_schema["paths"][path][method]["parameters"][i]["schema"] = {
                                "type": "array",
                                "items": {"$ref": "#/components/schemas/LocationEnum"},
                                "title": "Location"
                            }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Override the default OpenAPI schema
app.openapi = custom_openapi


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host=settings.host, 
        port=settings.port, 
        reload=True
    )
