# """
# Database initialization script for the comprehensive LIMS schema.

# This module provides functionality to initialize the database with all necessary
# tables, enums, and extensions. It includes proper error handling and logging.
# """

# import sys
# import os
# from typing import List
# from sqlalchemy import create_engine, text
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.exc import SQLAlchemyError, ProgrammingError
# from dotenv import load_dotenv

# # Add parent directory to path for imports
# sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# from app.core.database import db_manager, get_logger
# from app.db.database import Base

# load_dotenv()
# logger = get_logger(__name__)

# class DatabaseInitializer:
#     """Database initialization class with comprehensive error handling."""
    
#     def __init__(self):
#         self.engine = None
        
#     def _get_engine(self):
#         """Get database engine."""
#         if not self.engine:
#             if not db_manager._initialized:
#                 db_manager.initialize()
#             self.engine = db_manager.engine
#         return self.engine

#     def create_extensions(self) -> bool:
#         """Create PostgreSQL extensions."""
#         try:
#             with self._get_engine().connect() as conn:
#                 conn.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'))
#                 conn.commit()
#                 logger.info("✓ PostgreSQL extensions created successfully")
#                 return True
#         except SQLAlchemyError as e:
#             logger.error(f"Failed to create extensions: {e}")
#             return False

#     def create_enums(self) -> bool:
#         """Create all enum types."""
#         enum_definitions = [
#             ("sample_priority", ["Low", "Medium", "High", "Urgent"]),
#             ("sample_status", ["Logged_In", "In_Progress", "Completed", "Archived"]),
#             ("specification_type_enum", ["Exact", "Range", "Less_Than", "Greater_Than"]),
#             ("parameter_type_enum", ["Numeric", "Text", "Boolean", "DateTime"]),
#             ("step_result_enum", ["Pass", "Fail", "NA"]),
#             ("test_status_enum", ["Pending", "In_Progress", "Completed", "Cancelled"]),
#             ("result_status_enum", ["Pass", "Fail", "OOS", "Invalid"]),
#             ("investigation_phase", ["phase1_lab", "phase2_qc", "phase3_qa"]),
#             ("deviation_severity", ["minor", "major", "critical"]),
#             ("deviation_status", ["open", "under_investigation", "closed"]),
#             ("capa_action_type", ["corrective", "preventive", "both"]),
#             ("capa_status", ["open", "in_progress", "closed", "verified", "cancelled"]),
#             ("capa_task_status", ["pending", "in_progress", "completed"])
#         ]
        
#         try:
#             with self._get_engine().connect() as conn:
#                 for enum_name, enum_values in enum_definitions:
#                     enum_values_str = "','".join(enum_values)
#                     conn.execute(text(f"""
#                         DO $$ BEGIN
#                             CREATE TYPE {enum_name} AS ENUM ('{enum_values_str}');
#                         EXCEPTION
#                             WHEN duplicate_object THEN null;
#                         END $$;
#                     """))
#                 conn.commit()
#                 logger.info(f"✓ Created {len(enum_definitions)} enum types successfully")
#                 return True
#         except SQLAlchemyError as e:
#             logger.error(f"Failed to create enums: {e}")
#             return False

#     def create_tables(self) -> bool:
#         """Create all database tables."""
#         try:
#             Base.metadata.create_all(bind=self._get_engine())
#             logger.info("✓ Database tables created successfully")
#             return True
#         except SQLAlchemyError as e:
#             logger.error(f"Failed to create tables: {e}")
#             return False
    
#     def verify_database(self) -> bool:
#         """Verify database connection and basic functionality."""
#         try:
#             with self._get_engine().connect() as conn:
#                 result = conn.execute(text("SELECT 1"))
#                 if result.fetchone()[0] == 1:
#                     logger.info("✓ Database connection verified")
#                     return True
#                 return False
#         except SQLAlchemyError as e:
#             logger.error(f"Database verification failed: {e}")
#             return False
    
#     def initialize_database(self) -> bool:
#         """Initialize the complete database schema."""
#         logger.info("Starting database initialization...")
        
#         steps = [
#             ("Verifying database connection", self.verify_database),
#             ("Creating PostgreSQL extensions", self.create_extensions),
#             ("Creating enum types", self.create_enums),
#             ("Creating database tables", self.create_tables),
#             ("Final verification", self.verify_database)
#         ]
        
#         for step_name, step_func in steps:
#             logger.info(f"Step: {step_name}...")
#             if not step_func():
#                 logger.error(f"Failed at step: {step_name}")
#                 return False
        
#         logger.info("🎉 Database initialization completed successfully!")
#         return True


# def init_database() -> bool:
#     """Main function to initialize the database."""
#     try:
#         initializer = DatabaseInitializer()
#         return initializer.initialize_database()
#     except Exception as e:
#         logger.error(f"Critical error during database initialization: {e}")
#         return False


# def verify_initialization() -> bool:
#     """Verify that database initialization was successful."""
#     try:
#         initializer = DatabaseInitializer()
#         return initializer.verify_database()
#     except Exception as e:
#         logger.error(f"Database verification failed: {e}")
#         return False


# if __name__ == "__main__":
#     success = init_database()
#     if not success:
#         logger.error("Database initialization failed!")
#         sys.exit(1)
#     logger.info("Database is ready for use.")
