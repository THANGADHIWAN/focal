"""
Storage management service.
"""
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Optional, Dict, Any
from fastapi import HTTPException
import logging

from app.db.models.storage_hierarchy import Box, Freezer
from app.api.schemas.storage import BoxCreate, BoxUpdate, FreezerCreate, FreezerUpdate

# Set up logging
logger = logging.getLogger(__name__)

class StorageService:
    @staticmethod
    def get_all_boxes(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Box]:
        """Get all storage boxes."""
        try:
            query = db.query(Box)
            
            if filters:
                if filters.get("freezer_id"):
                    query = query.filter(Box.freezer_id == filters["freezer_id"])
                if filters.get("search"):
                    search = f"%{filters['search']}%"
                    query = query.filter(
                        or_(
                            Box.box_code.ilike(search),
                            Box.box_type.ilike(search)
                        )
                    )
                    
            boxes = query.offset(skip).limit(limit).all()
            return boxes
        except Exception as e:
            logger.error(f"Error getting boxes: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_box_by_id(db: Session, box_id: int) -> Optional[Box]:
        """Get a box by its ID."""
        try:
            return db.query(Box).filter(Box.id == box_id).first()
        except Exception as e:
            logger.error(f"Error getting box {box_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def create_box(db: Session, box: BoxCreate) -> Box:
        """Create a new storage box."""
        try:
            db_box = Box(**box.model_dump())
            db.add(db_box)
            db.commit()
            db.refresh(db_box)
            return db_box
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating box: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def update_box(db: Session, box_id: int, box: BoxUpdate) -> Optional[Box]:
        """Update a storage box."""
        try:
            db_box = StorageService.get_box_by_id(db, box_id)
            if not db_box:
                return None
                
            update_data = box.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_box, field, value)
                
            db.commit()
            db.refresh(db_box)
            return db_box
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating box {box_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def delete_box(db: Session, box_id: int) -> bool:
        """Delete a storage box."""
        try:
            db_box = StorageService.get_box_by_id(db, box_id)
            if not db_box:
                return False
                
            db.delete(db_box)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting box {box_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_all_freezers(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Freezer]:
        """Get all freezers."""
        try:
            query = db.query(Freezer)
            
            if filters:
                if filters.get("location"):
                    query = query.filter(Freezer.location.ilike(f"%{filters['location']}%"))
                if filters.get("search"):
                    search = f"%{filters['search']}%"
                    query = query.filter(
                        or_(
                            Freezer.name.ilike(search),
                            Freezer.code.ilike(search)
                        )
                    )
                    
            freezers = query.offset(skip).limit(limit).all()
            return freezers
        except Exception as e:
            logger.error(f"Error getting freezers: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_freezer_by_id(db: Session, freezer_id: int) -> Optional[Freezer]:
        """Get a freezer by its ID."""
        try:
            return db.query(Freezer).filter(Freezer.id == freezer_id).first()
        except Exception as e:
            logger.error(f"Error getting freezer {freezer_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def create_freezer(db: Session, freezer: FreezerCreate) -> Freezer:
        """Create a new freezer."""
        try:
            db_freezer = Freezer(**freezer.model_dump())
            db.add(db_freezer)
            db.commit()
            db.refresh(db_freezer)
            return db_freezer
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating freezer: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def update_freezer(db: Session, freezer_id: int, freezer: FreezerUpdate) -> Optional[Freezer]:
        """Update a freezer."""
        try:
            db_freezer = StorageService.get_freezer_by_id(db, freezer_id)
            if not db_freezer:
                return None
                
            update_data = freezer.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_freezer, field, value)
                
            db.commit()
            db.refresh(db_freezer)
            return db_freezer
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating freezer {freezer_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def delete_freezer(db: Session, freezer_id: int) -> bool:
        """Delete a freezer."""
        try:
            db_freezer = StorageService.get_freezer_by_id(db, freezer_id)
            if not db_freezer:
                return False
                
            db.delete(db_freezer)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting freezer {freezer_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_storage_hierarchy(db: Session) -> Dict[str, Any]:
        """Get complete storage hierarchy (freezers, boxes, etc.)."""
        try:
            freezers = db.query(Freezer).all()
            hierarchy = []
            
            for freezer in freezers:
                freezer_data = {
                    "id": freezer.id,
                    "name": freezer.name,
                    "code": freezer.code,
                    "location": freezer.location,
                    "temperature_range": freezer.temperature_range,
                    "boxes": []
                }
                
                boxes = db.query(Box).filter(Box.freezer_id == freezer.id).all()
                for box in boxes:
                    box_data = {
                        "id": box.id,
                        "name": box.name,
                        "code": box.code,
                        "drawer_number": box.drawer_number,
                        "rack_number": box.rack_number,
                        "shelf_number": box.shelf_number,
                        "capacity": box.capacity,
                        "is_full": box.is_full
                    }
                    freezer_data["boxes"].append(box_data)
                    
                hierarchy.append(freezer_data)
                
            return {"hierarchy": hierarchy}
        except Exception as e:
            logger.error(f"Error getting storage hierarchy: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
