from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import logging

# Import models from their respective modules
from app.db.models.user import Users
from app.db.models.storage_hierarchy import StorageLocation, Box, StorageRoom, Freezer
from app.db.models.sample import SampleType
from app.db.models.instrument import Instrument
from app.db.models.test import TestMaster, TestMethod
from app.utils.constants import EquipmentType, EquipmentStatus, SampleType, SampleStatus

# Set up logging
logger = logging.getLogger(__name__)

class MetadataService:
    @staticmethod
    def get_sample_types(db: Session) -> List[Dict[str, Any]]:
        """
        Get all sample types for dropdown with enum validation
        """
        try:
            return [
            {
                "id": i + 1,
                "value": enum_item.value,
                "description": f"{enum_item.value} sample"
            }
            for i, enum_item in enumerate(SampleType)
            ]
        except Exception as e:
            logger.error(f"Error in get_sample_types: {str(e)}")
            raise



    @staticmethod
    def validate_sample_type(sample_type: str) -> str:
        """
        Validate sample type against enum and return valid value
        """
        if not sample_type:
            return None
        
        try:
            # Check if the type exists in our enum (case-insensitive)
            for enum_item in SampleType:
                if enum_item.value.lower() == sample_type.lower():
                    return enum_item.value
            
            # If not found in enum, log a warning but return the original value
            logger.warning(f"Sample type '{sample_type}' not found in SampleTypeEnum")
            return sample_type
        except Exception as e:
            logger.error(f"Error validating sample type '{sample_type}': {str(e)}")
            return sample_type

    @staticmethod
    def get_sample_statuses(db: Session) -> List[Dict[str, Any]]:
        """
        Get all sample statuses for dropdown
        """
        # Since we're using string statuses in the new schema, return common statuses
        statuses = [
            {
            "id": i + 1,
            "value": enum_item.value,
            "description": f"Sample status: {enum_item.value}"
            }
            for i, enum_item in enumerate(SampleStatus)
        ]
        return statuses
    
    @staticmethod
    def get_lab_locations(db: Session) -> List[Dict[str, Any]]:
        """
        Get all storage locations for dropdown
        """
        try:
            locations = db.query(StorageLocation).all()
            # Return as a list of dictionaries with id and value for dropdown
            return [
                {
                    "id": location.id,
                    "value": location.location_name,
                    "description": location.description
                }
                for location in locations
            ]
        except Exception as e:
            logger.error(f"Error in get_lab_locations: {str(e)}")
            raise
    
    @staticmethod
    def get_users(db: Session) -> List[Dict[str, Any]]:
        """
        Get all users for assignment dropdown
        """
        try:
            logger.info("Fetching users from DB in service...")
            users = db.query(Users).all()
            logger.info(f"Found {len(users)} users")
            
            # Return as a list of dictionaries with id and value for dropdown
            result = [
                {
                    "id": user.id,
                    "value": user.full_name,
                    "email": user.email
                }
                for user in users
            ]
            logger.info(f"Formatted user data: {result}")
            return result
        except Exception as e:
            logger.error(f"Error fetching users: {e}")
            raise
    
    @staticmethod
    def get_storage_locations(db: Session) -> List[Dict[str, Any]]:
        """
        Get all storage locations/freezers
        """
        try:
            locations = db.query(StorageLocation).all()
            
            return [
                {
                    "id": location.id,
                    "name": location.location_name,
                    "description": location.description,
                    "temperature": location.temperature_celsius,
                    "humidity": location.humidity_percent
                }
                for location in locations
            ]
        except Exception as e:
            logger.error(f"Error in get_storage_locations: {str(e)}")
            raise
    
    @staticmethod
    def get_available_boxes(db: Session) -> List[Dict[str, Any]]:
        """
        Get all available storage boxes
        """
        try:
            boxes = db.query(Box).all()
            
            return [
                {
                    "id": box.id,
                    "name": box.box_code,
                    "type": box.box_type,
                    "capacity": box.capacity,
                    "freezer_id": box.freezer_id,
                    "rack": box.rack,
                    "shelf": box.shelf,
                    "drawer": box.drawer
                }
                for box in boxes
            ]
        except Exception as e:
            logger.error(f"Error in get_available_boxes: {str(e)}")
            raise

    @staticmethod
    def get_equipment(db: Session) -> List[Dict[str, Any]]:
        """
        Get all equipment with enum validation
        """
        try:
            equipment = db.query(Instrument).all()
            
            equipment_list = []
            for item in equipment:
                # Validate equipment type against enum if it exists
                equipment_type = item.instrument_type
                if equipment_type:
                    # Check if the type exists in our enum
                    try:
                        # Try to find the enum value (case-insensitive)
                        enum_value = None
                        for enum_item in EquipmentType:
                            if enum_item.value.lower() == equipment_type.lower():
                                enum_value = enum_item.value
                                break
                        
                        # If not found in enum, use the original value but log a warning
                        if not enum_value:
                            logger.warning(f"Equipment type '{equipment_type}' not found in EquipmentTypeEnum")
                            enum_value = equipment_type
                    except Exception as e:
                        logger.error(f"Error validating equipment type '{equipment_type}': {str(e)}")
                        enum_value = equipment_type
                else:
                    enum_value = None

                equipment_data = {
                    "id": item.id,
                    "name": item.name,
                    "instrument_type": enum_value,
                    "serial_number": item.serial_number,
                    "manufacturer": item.manufacturer,
                    "model_number": item.model_number,
                    "purchase_date": item.purchase_date.isoformat() if item.purchase_date else None,
                    "location_id": item.location_id,
                    "status": item.status,
                    "qualification_status": item.qualification_status,
                    "maintenance_type": item.maintenance_type,
                    "remarks": item.remarks
                }
                equipment_list.append(equipment_data)
            
            return equipment_list
        except Exception as e:
            logger.error(f"Error in get_equipment: {str(e)}")
            raise

    @staticmethod
    def get_storage_hierarchy(db: Session) -> Dict[str, Any]:
        """
        Get complete storage hierarchy
        """
        try:
            # Get all storage locations with their rooms, freezers, and boxes
            locations = db.query(StorageLocation).all()
            
            hierarchy = []
            for location in locations:
                location_data = {
                    "id": location.id,
                    "location_name": location.location_name,
                    "location_code": location.location_code,
                    "storage_rooms": []
                }
                
                # Get rooms for this location
                rooms = db.query(StorageRoom).filter(StorageRoom.storage_location_id == location.id).all()
                for room in rooms:
                    room_data = {
                        "id": room.id,
                        "room_name": room.room_name,
                        "floor": room.floor,
                        "building": room.building,
                        "freezers": []
                    }
                    
                    # Get freezers for this room
                    freezers = db.query(Freezer).filter(Freezer.storage_room_id == room.id).all()
                    for freezer in freezers:
                        freezer_data = {
                            "id": freezer.id,
                            "freezer_name": freezer.freezer_name,
                            "freezer_type": freezer.freezer_type,
                            "boxes": []
                        }
                        
                        # Get boxes for this freezer
                        boxes = db.query(Box).filter(Box.freezer_id == freezer.id).all()
                        for box in boxes:
                            box_data = {
                                "id": box.id,
                                "box_code": box.box_code,
                                "box_type": box.box_type,
                                "capacity": box.capacity,
                                "inventory_slots": []
                            }
                            
                            # Get inventory slots for this box (if implemented)
                            # For now, we'll create placeholder slots
                            for i in range(1, min(box.capacity + 1, 11)):  # Show first 10 slots
                                slot_data = {
                                    "id": i,
                                    "slot_code": f"SLOT-{box.box_code}-{i:03d}",
                                    "is_occupied": False,
                                    "aliquot_id": None
                                }
                                box_data["inventory_slots"].append(slot_data)
                            
                            freezer_data["boxes"].append(box_data)
                        
                        room_data["freezers"].append(freezer_data)
                    
                    location_data["storage_rooms"].append(room_data)
                
                hierarchy.append(location_data)
            
            return {"storage_locations": hierarchy}
        except Exception as e:
            logger.error(f"Error in get_storage_hierarchy: {str(e)}")
            raise

    @staticmethod
    def get_available_slots(db: Session) -> List[Dict[str, Any]]:
        """
        Get all available storage slots
        """
        try:
            # Get all boxes
            boxes = db.query(Box).all()
            
            available_slots = []
            for box in boxes:
                # For now, we'll create placeholder available slots
                # In a real implementation, you'd check actual occupancy
                for i in range(1, min(box.capacity + 1, 6)):  # Show first 5 available slots
                    slot_data = {
                        "id": i,
                        "slot_code": f"SLOT-{box.box_code}-{i:03d}",
                        "is_occupied": False,
                        "box_id": box.id,
                        "box": {
                            "id": box.id,
                            "box_code": box.box_code,
                            "freezer": {
                                "id": box.freezer_id,
                                "freezer_name": "Freezer"  # You'd get this from the relationship
                            }
                        }
                    }
                    available_slots.append(slot_data)
            
            return available_slots
        except Exception as e:
            logger.error(f"Error in get_available_slots: {str(e)}")
            raise

    @staticmethod
    def check_database_connection(db: Session) -> bool:
        """
        Check if database is accessible and tables exist
        """
        try:
            # Try to query a simple table to check connectivity
            db.execute("SELECT 1")
            return True
        except Exception as e:
            logger.error(f"Database connection check failed: {str(e)}")
            return False

    @staticmethod
    def validate_equipment_type(equipment_type: str) -> str:
        """
        Validate equipment type against enum and return valid value
        """
        if not equipment_type:
            return None
        
        try:
            # Check if the type exists in our enum (case-insensitive)
            for enum_item in EquipmentType:
                if enum_item.value.lower() == equipment_type.lower():
                    return enum_item.value
            
            # If not found in enum, log a warning but return the original value
            logger.warning(f"Equipment type '{equipment_type}' not found in EquipmentTypeEnum")
            return equipment_type
        except Exception as e:
            logger.error(f"Error validating equipment type '{equipment_type}': {str(e)}")
            return equipment_type

    @staticmethod
    def get_equipment_types() -> List[Dict[str, Any]]:
        """
        Get all available equipment types from enum
        """
        try:
            return [
                {
                    "id": i + 1,
                    "value": enum_item.value,
                    "description": f"{enum_item.value} equipment"
                }
                for i, enum_item in enumerate(EquipmentType)
            ]
        except Exception as e:
            logger.error(f"Error in get_equipment_types: {str(e)}")
            raise

    @staticmethod
    def get_equipment_statuses() -> List[Dict[str, Any]]:
        """
        Get all available equipment statuses from enum
        """
        try:
            return [
                {
                    "id": i + 1,
                    "value": enum_item.value,
                    "description": f"Equipment is {enum_item.value.lower()}"
                }
                for i, enum_item in enumerate(EquipmentStatus)
            ]
        except Exception as e:
            logger.error(f"Error in get_equipment_statuses: {str(e)}")
            raise

    @staticmethod
    def create_sample_type(db: Session, name: str, description: Optional[str] = None) -> SampleType:
        """
        Create a new sample type
        """
        try:
            sample_type = SampleType(name=name, description=description)
            db.add(sample_type)
            db.commit()
            db.refresh(sample_type)
            return sample_type
        except Exception as e:
            logger.error(f"Error in create_sample_type: {str(e)}")
            db.rollback()
            raise
    
    @staticmethod
    def create_storage_location(
        db: Session,
        name: str,
        description: Optional[str] = None,
        temperature: Optional[float] = None,
        humidity: Optional[float] = None
    ) -> StorageLocation:
        """
        Create a new storage location
        """
        try:
            location = StorageLocation(
                location_name=name,
                description=description,
                temperature_celsius=temperature,
                humidity_percent=humidity
            )
            db.add(location)
            db.commit()
            db.refresh(location)
            return location
        except Exception as e:
            logger.error(f"Error in create_storage_location: {str(e)}")
            db.rollback()
            raise
