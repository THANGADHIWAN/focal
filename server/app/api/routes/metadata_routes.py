from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from app.db.database import get_db
from app.api.schemas import ApiResponse
from app.services.metadata_service import MetadataService
from app.api.routes.equipment import router as equipment_router

# Set up logging
logger = logging.getLogger(__name__)

metadata_router = APIRouter(
    prefix="/metadata",
    tags=["metadata"]
)

# Include equipment routes
metadata_router.include_router(equipment_router)

# Storage router moved to storage_routes.py

@metadata_router.get("/sample_types", response_model=ApiResponse)
def get_sample_types(db: Session = Depends(get_db)):
    """Get all sample types"""
    try:
        sample_types = MetadataService.get_sample_types(db)
        return {
            "data": sample_types,
            "status": 200,
            "success": True
        }
    except Exception as e:
        logger.error(f"Error in get_sample_types: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@metadata_router.get("/sample_statuses", response_model=ApiResponse)
def get_sample_statuses(db: Session = Depends(get_db)):
    """Get all sample statuses"""
    try:
        sample_statuses = MetadataService.get_sample_statuses(db)
        return {
            "data": sample_statuses,
            "status": 200,
            "success": True
        }
    except Exception as e:
        logger.error(f"Error in get_sample_statuses: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@metadata_router.get("/lab_locations", response_model=ApiResponse)
def get_lab_locations(db: Session = Depends(get_db)):
    """Get all lab locations"""
    try:
        lab_locations = MetadataService.get_lab_locations(db)
        return {
            "data": lab_locations,
            "status": 200,
            "success": True
        }
    except Exception as e:
        logger.error(f"Error in get_lab_locations: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@metadata_router.get("/users", response_model=ApiResponse)
def get_users(db: Session = Depends(get_db)):
    """Get all users"""
    try:
        users = MetadataService.get_users(db)
        return {
            "data": users,
            "status": 200,
            "success": True
        }
    except Exception as e:
        logger.error(f"Error in get_users: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@metadata_router.get("/storage_locations", response_model=ApiResponse)
def get_storage_locations(db: Session = Depends(get_db)):
    """Get all storage locations"""
    try:
        locations = MetadataService.get_storage_locations(db)
        return {
            "data": locations,
            "status": 200,
            "success": True
        }
    except Exception as e:
        logger.error(f"Error in get_storage_locations: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@metadata_router.get("/equipment", response_model=ApiResponse)
def get_equipment(db: Session = Depends(get_db)):
    """Get all equipment"""
    try:
        equipment = MetadataService.get_equipment(db)
        return {
            "data": equipment,
            "status": 200,
            "success": True
        }
    except Exception as e:
        logger.error(f"Error in get_equipment: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@metadata_router.get("/equipment_types", response_model=ApiResponse)
def get_equipment_types():
    """Get all available equipment types from enum"""
    try:
        equipment_types = MetadataService.get_equipment_types()
        return {
            "data": equipment_types,
            "status": 200,
            "success": True
        }
    except Exception as e:
        logger.error(f"Error in get_equipment_types: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@metadata_router.get("/equipment_statuses", response_model=ApiResponse)
def get_equipment_statuses():
    """Get all available equipment statuses from enum"""
    try:
        equipment_statuses = MetadataService.get_equipment_statuses()
        return {
            "data": equipment_statuses,
            "status": 200,
            "success": True
        }
    except Exception as e:
        logger.error(f"Error in get_equipment_statuses: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


