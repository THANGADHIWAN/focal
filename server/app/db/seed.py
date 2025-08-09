# """
# Database seeding module for the LIMS application.

# This module provides functionality to seed the database with initial data
# for development and testing purposes. It includes comprehensive error handling,
# logging, and transaction management.
# """

# import sys
# import os
# from datetime import datetime, timedelta
# from typing import List, Optional
# from uuid import uuid4

# from sqlalchemy.orm import Session
# from sqlalchemy.exc import IntegrityError, SQLAlchemyError
# from passlib.context import CryptContext

# # Add parent directory to path for imports
# sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# from app.core.database import db_manager, get_logger
# from app.db.models import (
#     Users, SampleType, Sample, Aliquot, ChainOfCustody, SampleStatusLog, StorageTransactionLog,
#     Material, MaterialLot, MaterialUsageLog, MaterialInventoryAdjustment,
#     StorageLocation, StorageRoom, Freezer, Box, InventorySlot,
#     Instrument, InstrumentCalibration, InstrumentMaintenanceLog,
#     TestMethod, TestParameter, TestSpecification, TestProcedure, TestStep, 
#     TestStepExecution, TestMaster, Test, TestResult,
#     OOS, OOSInvestigation, Deviation, CAPA, CAPAAction,
#     AuditTrail, ElectronicSignature
# )
# from app.utils.constants import SampleStatusEnum, TestStatusEnum

# logger = get_logger(__name__)

# # Password hashing configuration
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# def get_password_hash(password: str) -> str:
#     """Hash a password using bcrypt."""
#     return pwd_context.hash(password)


# def random_str(prefix: str) -> str:
#     """Generate a random string with prefix."""
#     return f"{prefix}_{uuid4().hex[:8].upper()}"


# class DatabaseSeeder:
#     """Main database seeding class with transaction management."""
    
#     def __init__(self):
#         self.db: Optional[Session] = None
        
#     def __enter__(self):
#         """Enter context manager and get database session."""
#         self.db = db_manager.get_session()
#         return self
        
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         """Exit context manager and close database session."""
#         if self.db:
#             if exc_type is not None:
#                 self.db.rollback()
#                 logger.error(f"Transaction rolled back due to error: {exc_val}")
#             self.db.close()
    
#     def check_existing_data(self) -> bool:
#         """Check if database already contains seeded data."""
#         try:
#             user_count = self.db.query(Users).count()
#             if user_count > 0:
#                 logger.info(f"Database already contains {user_count} users. Skipping seed.")
#                 return True
#             return False
#         except SQLAlchemyError as e:
#             logger.error(f"Error checking existing data: {e}")
#             return True
    
#     def seed_users(self) -> List[Users]:
#         """Seed user accounts."""
#         users_data = [
#             {
#                 "full_name": "System Administrator",
#                 "email": "admin@lims.local",
#                 "role": "admin",
#                 "department": "IT",
#                 "password": "admin123"
#             },
#             {
#                 "full_name": "Lab Manager",
#                 "email": "labmanager@lims.local", 
#                 "role": "lab_manager",
#                 "department": "Laboratory",
#                 "password": "manager123"
#             },
#             {
#                 "full_name": "Senior Analyst",
#                 "email": "analyst1@lims.local",
#                 "role": "analyst",
#                 "department": "Quality Control",
#                 "password": "analyst123"
#             },
#             {
#                 "full_name": "Lab Technician",
#                 "email": "tech1@lims.local",
#                 "role": "technician", 
#                 "department": "Laboratory",
#                 "password": "tech123"
#             },
#             {
#                 "full_name": "QA Reviewer",
#                 "email": "qa@lims.local",
#                 "role": "qa_reviewer",
#                 "department": "Quality Assurance",
#                 "password": "qa123"
#             }
#         ]
        
#         users = []
#         for user_data in users_data:
#             password = user_data.pop("password")
#             user = Users(
#                 id=uuid4(),
#                 hashed_password=get_password_hash(password),
#                 is_active=True,
#                 created_at=datetime.utcnow(),
#                 **user_data
#             )
#             users.append(user)
        
#         self.db.add_all(users)
#         self.db.commit()
#         logger.info(f"✓ Created {len(users)} users")
#         return users
    
#     def seed_storage_hierarchy(self) -> tuple:
#         """Seed storage hierarchy (locations, rooms, freezers, boxes)."""
#         # Storage Locations
#         locations = [
#             StorageLocation(
#                 location_name=f"Building A - Floor {i}",
#                 location_code=random_str("LOC"),
#                 temperature_celsius=-20.0 if i <= 2 else 4.0,
#                 humidity_percent=45.0,
#                 description=f"Temperature controlled storage - Floor {i}"
#             ) for i in range(1, 4)
#         ]
        
#         self.db.add_all(locations)
#         self.db.commit()
        
#         # Storage Rooms
#         rooms = []
#         for i, location in enumerate(locations):
#             room = StorageRoom(
#                 room_name=f"Storage Room {i+1}",
#                 floor=i+1,
#                 building="A",
#                 access_control=True,
#                 temperature_range="-25 to -15" if i <= 1 else "2 to 8",
#                 humidity_range="40-50",
#                 notes=f"Secure storage room {i+1}",
#                 storage_location_id=location.id
#             )
#             rooms.append(room)
        
#         self.db.add_all(rooms)
#         self.db.commit()
        
#         # Freezers
#         freezers = []
#         for i, room in enumerate(rooms):
#             freezer = Freezer(
#                 freezer_name=f"Ultra-Low Freezer {i+1}",
#                 freezer_type="Ultra-Low" if i <= 1 else "Standard",
#                 storage_room_id=room.id,
#                 temperature_range="-80 to -70" if i <= 1 else "-25 to -15",
#                 notes=f"High-capacity freezer {i+1}"
#             )
#             freezers.append(freezer)
        
#         self.db.add_all(freezers)
#         self.db.commit()
        
#         # Boxes
#         boxes = []
#         for i, freezer in enumerate(freezers):
#             for j in range(3):  # 3 boxes per freezer
#                 box = Box(
#                     box_code=random_str("BOX"),
#                     box_type="Standard 100-slot",
#                     rack=f"R{j+1}",
#                     shelf=f"S{(j%2)+1}",
#                     drawer=f"D{j+1}",
#                     capacity=100,
#                     freezer_id=freezer.id
#                 )
#                 boxes.append(box)
        
#         self.db.add_all(boxes)
#         self.db.commit()
        
#         logger.info(f"✓ Created storage hierarchy: {len(locations)} locations, {len(rooms)} rooms, {len(freezers)} freezers, {len(boxes)} boxes")
#         return locations, rooms, freezers, boxes
    
#     def seed_sample_types_and_test_methods(self) -> tuple:
#         """Seed sample types and test methods."""
#         # Sample Types for pharmaceutical lab
#         sample_types = [
#             SampleType(
#                 name="Active Pharmaceutical Ingredient (API)",
#                 description="Raw active ingredient for drug manufacturing",
#                 matrix_type="Solid"
#             ),
#             SampleType(
#                 name="Finished Drug Product",
#                 description="Final manufactured pharmaceutical product",
#                 matrix_type="Solid"
#             ),
#             SampleType(
#                 name="Excipient",
#                 description="Inactive ingredient used in drug formulation",
#                 matrix_type="Solid"
#             ),
#             SampleType(
#                 name="Injectable Solution",
#                 description="Sterile solution for injection",
#                 matrix_type="Liquid"
#             ),
#             SampleType(
#                 name="Stability Sample",
#                 description="Sample for stability testing",
#                 matrix_type="Mixed"
#             )
#         ]
        
#         # Test Methods for pharmaceutical testing
#         test_methods = [
#             TestMethod(
#                 name="HPLC Assay",
#                 version="1.0",
#                 description="High Performance Liquid Chromatography for potency determination",
#                 validated=True,
#                 created_by="System",
#                 created_at=datetime.utcnow()
#             ),
#             TestMethod(
#                 name="Dissolution Test",
#                 version="1.0", 
#                 description="Drug release rate measurement",
#                 validated=True,
#                 created_by="System",
#                 created_at=datetime.utcnow()
#             ),
#             TestMethod(
#                 name="Microbial Limit Test",
#                 version="1.0",
#                 description="Microbial contamination testing",
#                 validated=True,
#                 created_by="System",
#                 created_at=datetime.utcnow()
#             ),
#             TestMethod(
#                 name="Water Content by KF",
#                 version="1.0",
#                 description="Karl Fischer water content determination",
#                 validated=True,
#                 created_by="System",
#                 created_at=datetime.utcnow()
#             ),
#             TestMethod(
#                 name="Related Substances",
#                 version="1.0",
#                 description="Impurity profile analysis by HPLC",
#                 validated=True,
#                 created_by="System",
#                 created_at=datetime.utcnow()
#             )
#         ]
        
#         self.db.add_all(sample_types + test_methods)
#         self.db.commit()
        
#         logger.info(f"✓ Created {len(sample_types)} sample types and {len(test_methods)} test methods")
#         return sample_types, test_methods
    
#     def seed_materials_and_instruments(self, locations: List[StorageLocation]) -> tuple:
#         """Seed materials and instruments."""
#         # Materials
#         materials = [
#             Material(
#                 name="Acetonitrile HPLC Grade",
#                 material_type="Solvent",
#                 cas_number="75-05-8",
#                 manufacturer="Fisher Scientific",
#                 grade="HPLC",
#                 unit_of_measure="L",
#                 shelf_life_days=730,
#                 is_controlled=False,
#                 created_at=datetime.utcnow()
#             ),
#             Material(
#                 name="Potassium Dihydrogen Phosphate",
#                 material_type="Buffer",
#                 cas_number="7778-77-0",
#                 manufacturer="Sigma-Aldrich",
#                 grade="ACS",
#                 unit_of_measure="kg",
#                 shelf_life_days=1095,
#                 is_controlled=False,
#                 created_at=datetime.utcnow()
#             ),
#             Material(
#                 name="Reference Standard API-001",
#                 material_type="Reference Standard",
#                 cas_number="REF-001",
#                 manufacturer="Internal",
#                 grade="Primary",
#                 unit_of_measure="mg",
#                 shelf_life_days=365,
#                 is_controlled=True,
#                 created_at=datetime.utcnow()
#             )
#         ]
        
#         # Material Lots
#         material_lots = []
#         for i, material in enumerate(materials):
#             lot = MaterialLot(
#                 material_id=material.id,
#                 lot_number=random_str("LOT"),
#                 received_date=datetime.utcnow() - timedelta(days=30),
#                 expiry_date=datetime.utcnow() + timedelta(days=material.shelf_life_days),
#                 received_quantity=1000.0 if material.unit_of_measure != "mg" else 100.0,
#                 current_quantity=950.0 if material.unit_of_measure != "mg" else 95.0,
#                 storage_location_id=locations[i % len(locations)].id,
#                 status="Available",
#                 remarks=f"Initial stock for {material.name}"
#             )
#             material_lots.append(lot)
        
#         # Instruments
#         instruments = [
#             Instrument(
#                 name="HPLC System 1",
#                 instrument_type="HPLC",
#                 serial_number=random_str("SN"),
#                 manufacturer="Agilent",
#                 model_number="1260 Infinity",
#                 purchase_date=datetime.utcnow() - timedelta(days=365),
#                 location_id=locations[0].id,
#                 status="Active",
#                 qualification_status="Qualified",
#                 maintenance_type="Preventive",
#                 remarks="Primary HPLC system for routine analysis"
#             ),
#             Instrument(
#                 name="Dissolution Tester",
#                 instrument_type="Dissolution",
#                 serial_number=random_str("SN"),
#                 manufacturer="Distek",
#                 model_number="2500 SELECT",
#                 purchase_date=datetime.utcnow() - timedelta(days=200),
#                 location_id=locations[1].id,
#                 status="Active",
#                 qualification_status="Qualified",
#                 maintenance_type="Preventive",
#                 remarks="8-vessel dissolution system"
#             ),
#             Instrument(
#                 name="Karl Fischer Titrator",
#                 instrument_type="Titrator",
#                 serial_number=random_str("SN"),
#                 manufacturer="Metrohm",
#                 model_number="917 Coulometer",
#                 purchase_date=datetime.utcnow() - timedelta(days=150),
#                 location_id=locations[2].id,
#                 status="Active",
#                 qualification_status="Qualified",
#                 maintenance_type="Preventive",
#                 remarks="Coulometric KF for water content"
#             )
#         ]
        
#         self.db.add_all(materials + material_lots + instruments)
#         self.db.commit()
        
#         logger.info(f"✓ Created {len(materials)} materials, {len(material_lots)} lots, and {len(instruments)} instruments")
#         return materials, material_lots, instruments
    
#     def seed_sample_data(self, sample_types: List[SampleType], boxes: List[Box], users: List[Users]) -> List[Sample]:
#         """Seed sample data."""
#         samples = []
        
#         for i in range(10):
#             sample = Sample(
#                 sample_code=random_str("SMP"),
#                 sample_name=f"Batch {random_str('BTH')} Sample {i+1}",
#                 sample_type_id=sample_types[i % len(sample_types)].id,
#                 status="Logged_In",
#                 box_id=boxes[i % len(boxes)].id,
#                 volume_ml=10.0,
#                 received_date=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
#                 due_date=datetime.utcnow() + timedelta(days=random.randint(7, 21)),
#                 priority="HIGH" if i < 2 else "MEDIUM" if i < 6 else "LOW",
#                 quantity=5.0,
#                 is_aliquot=False,
#                 number_of_aliquots=0,
#                 created_by=users[i % len(users)].full_name,
#                 created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
#                 purpose="Quality Control Testing"
#             )
#             samples.append(sample)
        
#         self.db.add_all(samples)
#         self.db.commit()
        
#         logger.info(f"✓ Created {len(samples)} samples")
#         return samples
    
#     def seed_complete_workflow(self) -> None:
#         """Seed complete workflow with all related data."""
#         try:
#             # Check if data already exists
#             if self.check_existing_data():
#                 return
            
#             logger.info("Starting comprehensive database seeding...")
            
#             # Seed core entities
#             users = self.seed_users()
#             locations, rooms, freezers, boxes = self.seed_storage_hierarchy()
#             sample_types, test_methods = self.seed_sample_types_and_test_methods()
#             materials, material_lots, instruments = self.seed_materials_and_instruments(locations)
#             samples = self.seed_sample_data(sample_types, boxes, users)
            
#             logger.info("🎉 Database seeding completed successfully!")
#             logger.info("Database is now ready for development and testing.")
            
#         except IntegrityError as e:
#             self.db.rollback()
#             logger.error(f"Data integrity error during seeding: {e}")
#             raise
#         except SQLAlchemyError as e:
#             self.db.rollback()
#             logger.error(f"Database error during seeding: {e}")
#             raise
#         except Exception as e:
#             self.db.rollback()
#             logger.error(f"Unexpected error during seeding: {e}")
#             raise


# def seed_database():
#     """Main function to seed the database."""
#     try:
#         with DatabaseSeeder() as seeder:
#             seeder.seed_complete_workflow()
#     except Exception as e:
#         logger.error(f"Failed to seed database: {e}")
#         sys.exit(1)


# if __name__ == "__main__":
#     seed_database()