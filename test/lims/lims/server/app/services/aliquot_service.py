"""
Aliquot service for handling business logic related to aliquots
"""
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

from app.db.models.sample import Sample, Aliquot
from app.db.models.test import Test
from app.api.schemas.aliquot import AliquotCreate, AliquotUpdate, AliquotResponse
from app.api.schemas.test import TestResponse
from app.core.exceptions import (
    NotFoundError,
    ValidationError,
    DatabaseError,
    InvalidOperationError,
    UnexpectedError,
    RelatedResourceError
)
from app.utils.constants import SampleStatus, AliquotStatus

# Set up logging
logger = logging.getLogger(__name__)

class AliquotService:
    @staticmethod
    def get_all_aliquots(db: Session, sample_id: str) -> List[AliquotResponse]:
        """
        Get all aliquots for a sample
        """
        try:
            # First check if sample exists
            sample = db.query(Sample).filter(Sample.id == sample_id).first()
            if not sample:
                raise NotFoundError("Sample", sample_id)

            aliquots = db.query(Aliquot).filter(
                Aliquot.sample_id == sample_id
            ).options(
                joinedload(Aliquot.tests)
            ).all()
            
            # Convert SQLAlchemy models to Pydantic models
            return [AliquotService._format_aliquot_response(aliquot) for aliquot in aliquots]
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error in get_all_aliquots: {str(e)}")
            raise UnexpectedError("retrieving aliquots", e)
    
    @staticmethod
    def get_aliquot_by_id(db: Session, aliquot_id: str, sample_id: str) -> AliquotResponse:
        """
        Get a specific aliquot by its ID
        """
        try:
            aliquot = db.query(Aliquot).filter(
                Aliquot.id == aliquot_id,
                Aliquot.sample_id == sample_id
            ).options(
                joinedload(Aliquot.tests)
            ).first()
            
            if aliquot is None:
                raise NotFoundError("Aliquot", aliquot_id)
                
            return AliquotService._format_aliquot_response(aliquot)
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error in get_aliquot_by_id: {str(e)}")
            raise UnexpectedError("retrieving aliquot", e)
    
    @staticmethod
    def create_aliquot(db: Session, aliquot_data: AliquotCreate) -> AliquotResponse:
        """
        Create a new aliquot for a sample
        """
        try:
            # Get the parent sample
            sample = db.query(Sample).filter(Sample.id == aliquot_data.sample_id).first()
            if sample is None:
                raise NotFoundError("Sample", aliquot_data.sample_id)
            
            # Validate volume
            if sample.volume_left < aliquot_data.volume_ml:
                raise InvalidOperationError(
                    "create aliquot",
                    f"Insufficient volume. Available: {sample.volume_left}ml, Requested: {aliquot_data.volume_ml}ml"
                )
            
            # Create the aliquot
            db_aliquot = Aliquot(
                sample_id=aliquot_data.sample_id,
                aliquot_code=aliquot_data.aliquot_code,
                volume_ml=aliquot_data.volume_ml,
                status=aliquot_data.status,
                created_by=aliquot_data.created_by,
                assigned_to=aliquot_data.assigned_to,
                purpose=aliquot_data.purpose,
                created_at=datetime.utcnow()
            )
            
            # Update the parent sample's volume and aliquot count
            sample.volume_left = sample.volume_left - aliquot_data.volume_ml
            sample.aliquots_created = sample.aliquots_created + 1
            
            # If this is the first aliquot, update the sample status
            if sample.aliquots_created == 1:
                sample.status = SampleStatus.ALIQUOTED
            
            try:
                db.add(db_aliquot)
                db.commit()
                db.refresh(db_aliquot)
            except Exception as e:
                db.rollback()
                raise DatabaseError("creating aliquot", {"error": str(e)})
            
            return AliquotService._format_aliquot_response(db_aliquot)
            
        except (NotFoundError, InvalidOperationError, DatabaseError):
            raise
        except Exception as e:
            logger.error(f"Error in create_aliquot: {str(e)}")
            raise UnexpectedError("creating aliquot", e)
    
    @staticmethod
    def update_aliquot_location(db: Session, sample_id: str, aliquot_id: str, location: str) -> AliquotResponse:
        """
        Update an aliquot's location
        """
        try:
            db_aliquot = db.query(Aliquot).filter(
                Aliquot.id == aliquot_id,
                Aliquot.sample_id == sample_id
            ).options(
                joinedload(Aliquot.tests)
            ).first()
            
            if db_aliquot is None:
                raise NotFoundError("Aliquot", aliquot_id)
            
            # Validate location status
            if location not in AliquotStatus:
                raise ValidationError(
                    f"Invalid location status: {location}",
                    {"valid_statuses": list(AliquotStatus)}
                )
            
            try:
                db_aliquot.status = location
                db.commit()
                db.refresh(db_aliquot)
            except Exception as e:
                db.rollback()
                raise DatabaseError("updating aliquot location", {"error": str(e)})
            
            return AliquotService._format_aliquot_response(db_aliquot)
            
        except (NotFoundError, ValidationError, DatabaseError):
            raise
        except Exception as e:
            logger.error(f"Error in update_aliquot_location: {str(e)}")
            raise UnexpectedError("updating aliquot location", e)
    
    @staticmethod
    def delete_aliquot(db: Session, sample_id: str, aliquot_id: str) -> bool:
        """
        Delete an aliquot
        """
        try:
            # Find the aliquot
            db_aliquot = db.query(Aliquot).filter(
                Aliquot.id == aliquot_id,
                Aliquot.sample_id == sample_id
            ).first()
            
            if db_aliquot is None:
                raise NotFoundError("Aliquot", aliquot_id)
            
            # Check if aliquot has tests
            test_count = db.query(Test).filter(Test.aliquot_id == aliquot_id).count()
            if test_count > 0:
                raise RelatedResourceError("aliquot", {"tests": test_count})
            
            # Get the parent sample to update its volume and aliquot count
            sample = db.query(Sample).filter(Sample.id == sample_id).first()
            if not sample:
                raise NotFoundError("Sample", sample_id)
            
            try:
                # Return the volume back to the parent sample
                sample.volume_left = sample.volume_left + db_aliquot.volume_ml
                sample.aliquots_created = sample.aliquots_created - 1
                
                # If no more aliquots, update the sample status back to submitted
                if sample.aliquots_created <= 0:
                    sample.status = SampleStatus.SUBMITTED
                    sample.aliquots_created = 0  # Make sure it's not negative
                
                # Delete the aliquot
                db.delete(db_aliquot)
                db.commit()
                
                return True

    @staticmethod
    def _format_aliquot_response(aliquot: Aliquot) -> AliquotResponse:
        """Helper method to format aliquot response"""
        return AliquotResponse(
            id=aliquot.id,
            sample_id=aliquot.sample_id,
            aliquot_code=aliquot.aliquot_code,
            volume_ml=aliquot.volume_ml,
            creation_date=aliquot.created_at,
            status=aliquot.status,
            assigned_to=aliquot.assigned_to,
            created_by=aliquot.created_by,
            created_at=aliquot.created_at,
            purpose=aliquot.purpose,
            sample=None,  # Can add sample details if needed
            tests=[
                TestResponse(
                    id=test.id,
                    sample_id=test.sample_id,
                    aliquot_id=test.aliquot_id,
                    test_master_id=test.test_master_id,
                    analyst_id=test.analyst_id,
                    instrument_id=test.instrument_id,
                    scheduled_date=test.scheduled_date,
                    start_date=test.start_date,
                    end_date=test.end_date,
                    status=test.status,
                    remarks=test.remarks,
                    sample=None,
                    aliquot=None,
                    test_results=[]
                ) for test in aliquot.tests
            ]
        )
                
            except Exception as e:
                db.rollback()
                raise DatabaseError("deleting aliquot", {"error": str(e)})
            
        except (NotFoundError, RelatedResourceError, DatabaseError):
            raise
        except Exception as e:
            logger.error(f"Error in delete_aliquot: {str(e)}")
            raise UnexpectedError("deleting aliquot", e)
