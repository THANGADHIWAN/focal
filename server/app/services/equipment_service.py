"""
Equipment/Instrument service layer handling business logic
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, UploadFile
from app.db.models.instrument import (
    Instrument, InstrumentCalibration,
    InstrumentMaintenanceLog, Note
)
from app.api.schemas.equipment import (
    InstrumentCreate, InstrumentUpdate, CalibrationCreate,
    MaintenanceCreate, NoteCreate
)
from app.core.config import settings
from app.core.constants.equipment import (
    EquipmentType, EquipmentStatus,
    MaintenanceStatus, CalibrationStatus
)
from app.core.utils.file_handling import save_upload_file

class EquipmentService:
    @staticmethod
    def get_all_equipment(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get all equipment with pagination and filtering"""
        query = db.query(Instrument)

        # Apply filters
        if filters:
            if filters.get("type"):
                query = query.filter(Instrument.instrument_type == filters["type"])
            if filters.get("status"):
                query = query.filter(Instrument.status == filters["status"])
            if filters.get("location_id"):
                query = query.filter(Instrument.location_id == filters["location_id"])
            if filters.get("manufacturer"):
                query = query.filter(Instrument.manufacturer == filters["manufacturer"])

        # Apply search
        if search:
            search_filter = or_(
                Instrument.name.ilike(f"%{search}%"),
                Instrument.description.ilike(f"%{search}%"),
                Instrument.serial_number.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)

        total = query.count()
        items = query.offset(skip).limit(limit).all()

        return {
            "items": items,
            "total": total,
            "page": skip // limit + 1,
            "size": limit,
            "pages": (total + limit - 1) // limit
        }

    @staticmethod
    def get_equipment_by_id(db: Session, equipment_id: int) -> Instrument:
        """Get equipment by ID"""
        equipment = db.query(Instrument).filter(Instrument.id == equipment_id).first()
        if not equipment:
            raise HTTPException(status_code=404, detail="Equipment not found")
        return equipment

    @staticmethod
    def create_equipment(db: Session, equipment: InstrumentCreate) -> Instrument:
        """Create new equipment"""
        # Check for duplicate serial number
        existing = db.query(Instrument).filter(
            Instrument.serial_number == equipment.serial_number
        ).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Equipment with this serial number already exists"
            )

        db_equipment = Instrument(**equipment.dict())
        db.add(db_equipment)
        db.commit()
        db.refresh(db_equipment)
        return db_equipment

    @staticmethod
    def update_equipment(
        db: Session,
        equipment_id: int,
        updates: InstrumentUpdate
    ) -> Instrument:
        """Update equipment"""
        equipment = EquipmentService.get_equipment_by_id(db, equipment_id)
        
        update_data = updates.dict(exclude_unset=True)
        
        # Check serial number uniqueness if being updated
        if "serial_number" in update_data:
            existing = db.query(Instrument).filter(
                Instrument.serial_number == update_data["serial_number"],
                Instrument.id != equipment_id
            ).first()
            if existing:
                raise HTTPException(
                    status_code=400,
                    detail="Equipment with this serial number already exists"
                )

        for field, value in update_data.items():
            setattr(equipment, field, value)

        db.commit()
        db.refresh(equipment)
        return equipment

    @staticmethod
    def delete_equipment(db: Session, equipment_id: int) -> None:
        """Delete equipment"""
        equipment = EquipmentService.get_equipment_by_id(db, equipment_id)
        db.delete(equipment)
        db.commit()

    @staticmethod
    def add_calibration(
        db: Session,
        equipment_id: int,
        calibration: CalibrationCreate
    ) -> InstrumentCalibration:
        """Add calibration record"""
        equipment = EquipmentService.get_equipment_by_id(db, equipment_id)
        
        db_calibration = InstrumentCalibration(
            **calibration.dict(),
            instrument_id=equipment_id,
            calibration_date=datetime.utcnow()
        )
        
        db.add(db_calibration)
        EquipmentService.check_calibration_status(equipment)
        db.commit()
        db.refresh(db_calibration)
        return db_calibration

    @staticmethod
    def add_maintenance(
        db: Session,
        equipment_id: int,
        maintenance: MaintenanceCreate
    ) -> InstrumentMaintenanceLog:
        """Add maintenance record"""
        equipment = EquipmentService.get_equipment_by_id(db, equipment_id)
        
        db_maintenance = InstrumentMaintenanceLog(
            **maintenance.dict(),
            instrument_id=equipment_id,
            maintenance_date=datetime.utcnow()
        )
        
        db.add(db_maintenance)
        db.commit()
        db.refresh(db_maintenance)
        return db_maintenance

    @staticmethod
    async def add_attachment(
        db: Session,
        equipment_id: int,
        file: UploadFile
    ) -> Dict[str, Any]:
        """Add attachment to equipment"""
        equipment = EquipmentService.get_equipment_by_id(db, equipment_id)
        
        # Save file and get URL
        file_url = await save_upload_file(
            file,
            folder=f"equipment/{equipment_id}/attachments"
        )
        
        attachment_data = {
            "name": file.filename,
            "type": file.content_type,
            "url": file_url,
            "uploaded_at": datetime.utcnow()
        }
        
        return attachment_data

    @staticmethod
    def get_equipment_types() -> List[Dict[str, Any]]:
        """Get all equipment types"""
        return [
            {"id": i, "value": t.value, "description": t.value}
            for i, t in enumerate(EquipmentType, 1)
        ]

    @staticmethod
    def get_equipment_statuses() -> List[Dict[str, Any]]:
        """Get all equipment statuses"""
        return [
            {"id": i, "value": s.value, "description": s.value}
            for i, s in enumerate(EquipmentStatus, 1)
        ]

    @staticmethod
    def add_note(
        db: Session,
        equipment_id: int,
        note: NoteCreate
    ) -> Dict[str, Any]:
        """Add note to equipment"""
        equipment = EquipmentService.get_equipment_by_id(db, equipment_id)
        
        db_note = Note(
            content=note.content,
            user=note.user,
            instrument_id=equipment_id,
            timestamp=datetime.utcnow()
        )
        
        db.add(db_note)
        db.commit()
        db.refresh(db_note)
        return db_note

    @staticmethod
    def check_calibration_status(equipment: Instrument) -> None:
        """Update equipment calibration status"""
        if not equipment.calibrations:
            return
        
        latest = max(equipment.calibrations, key=lambda c: c.calibration_date)
        if datetime.utcnow() > latest.due_date:
            equipment.status = EquipmentStatus.OUT_OF_SERVICE
