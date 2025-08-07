"""
Storage routes for managing boxes and freezers.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from app.db.database import get_db
from app.services.storage_service import StorageService
from app.schemas import ApiResponse
from app.schemas.storage import (
    BoxCreate, BoxUpdate, BoxResponse,
    FreezerCreate, FreezerUpdate, FreezerResponse
)

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/storage",
    tags=["storage"],
    responses={404: {"description": "Not found"}}
)

@router.get("/boxes", response_model=ApiResponse)
def get_boxes(
    skip: int = 0,
    limit: int = 100,
    freezer_id: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all storage boxes."""
    try:
        filters = {}
        if freezer_id:
            filters["freezer_id"] = freezer_id
        if search:
            filters["search"] = search
            
        boxes = StorageService.get_all_boxes(db, skip, limit, filters)
        return {
            "data": boxes,
            "status": 200,
            "success": True
        }
    except Exception as e:
        logger.error(f"Error in get_boxes: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/boxes/{box_id}", response_model=ApiResponse)
def get_box(box_id: int, db: Session = Depends(get_db)):
    """Get a specific box by ID."""
    try:
        box = StorageService.get_box_by_id(db, box_id)
        if not box:
            raise HTTPException(status_code=404, detail="Box not found")
            
        return {
            "data": box,
            "status": 200,
            "success": True
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_box: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/boxes", response_model=ApiResponse)
def create_box(box: BoxCreate, db: Session = Depends(get_db)):
    """Create a new storage box."""
    try:
        new_box = StorageService.create_box(db, box)
        return {
            "data": new_box,
            "status": 201,
            "success": True,
            "message": "Box created successfully"
        }
    except Exception as e:
        logger.error(f"Error in create_box: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/boxes/{box_id}", response_model=ApiResponse)
def update_box(box_id: int, box: BoxUpdate, db: Session = Depends(get_db)):
    """Update a storage box."""
    try:
        updated_box = StorageService.update_box(db, box_id, box)
        if not updated_box:
            raise HTTPException(status_code=404, detail="Box not found")
            
        return {
            "data": updated_box,
            "status": 200,
            "success": True,
            "message": "Box updated successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in update_box: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/boxes/{box_id}", response_model=ApiResponse)
def delete_box(box_id: int, db: Session = Depends(get_db)):
    """Delete a storage box."""
    try:
        success = StorageService.delete_box(db, box_id)
        if not success:
            raise HTTPException(status_code=404, detail="Box not found")
            
        return {
            "data": None,
            "status": 200,
            "success": True,
            "message": "Box deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in delete_box: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/freezers", response_model=ApiResponse)
def get_freezers(
    skip: int = 0,
    limit: int = 100,
    location: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all freezers."""
    try:
        filters = {}
        if location:
            filters["location"] = location
        if search:
            filters["search"] = search
            
        freezers = StorageService.get_all_freezers(db, skip, limit, filters)
        return {
            "data": freezers,
            "status": 200,
            "success": True
        }
    except Exception as e:
        logger.error(f"Error in get_freezers: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/freezers/{freezer_id}", response_model=ApiResponse)
def get_freezer(freezer_id: int, db: Session = Depends(get_db)):
    """Get a specific freezer by ID."""
    try:
        freezer = StorageService.get_freezer_by_id(db, freezer_id)
        if not freezer:
            raise HTTPException(status_code=404, detail="Freezer not found")
            
        return {
            "data": freezer,
            "status": 200,
            "success": True
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_freezer: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/freezers", response_model=ApiResponse)
def create_freezer(freezer: FreezerCreate, db: Session = Depends(get_db)):
    """Create a new freezer."""
    try:
        new_freezer = StorageService.create_freezer(db, freezer)
        return {
            "data": new_freezer,
            "status": 201,
            "success": True,
            "message": "Freezer created successfully"
        }
    except Exception as e:
        logger.error(f"Error in create_freezer: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/freezers/{freezer_id}", response_model=ApiResponse)
def update_freezer(freezer_id: int, freezer: FreezerUpdate, db: Session = Depends(get_db)):
    """Update a freezer."""
    try:
        updated_freezer = StorageService.update_freezer(db, freezer_id, freezer)
        if not updated_freezer:
            raise HTTPException(status_code=404, detail="Freezer not found")
            
        return {
            "data": updated_freezer,
            "status": 200,
            "success": True,
            "message": "Freezer updated successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in update_freezer: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/freezers/{freezer_id}", response_model=ApiResponse)
def delete_freezer(freezer_id: int, db: Session = Depends(get_db)):
    """Delete a freezer."""
    try:
        success = StorageService.delete_freezer(db, freezer_id)
        if not success:
            raise HTTPException(status_code=404, detail="Freezer not found")
            
        return {
            "data": None,
            "status": 200,
            "success": True,
            "message": "Freezer deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in delete_freezer: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/hierarchy", response_model=ApiResponse)
def get_storage_hierarchy(db: Session = Depends(get_db)):
    """Get complete storage hierarchy (freezers, boxes, etc.)."""
    try:
        hierarchy = StorageService.get_storage_hierarchy(db)
        return {
            "data": hierarchy,
            "status": 200,
            "success": True
        }
    except Exception as e:
        logger.error(f"Error in get_storage_hierarchy: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/available_slots", response_model=ApiResponse)
def get_available_slots(db: Session = Depends(get_db)):
    """Get all available storage slots"""
    try:
        available_slots = StorageService.get_available_slots(db)
        return {
            "data": available_slots,
            "status": 200,
            "success": True
        }
    except Exception as e:
        logger.error(f"Error in get_available_slots: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
