from sqlalchemy.orm import Session, joinedload
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.db.models.sample import Sample, Aliquot
from app.db.models.test import Test
from app.schemas import AliquotCreate, AliquotUpdate, AliquotResponse, TestResponse
from typing import List, Optional, Dict, Any

class AliquotService:
    @staticmethod
    def get_all_aliquots(db: Session, sample_id: str) -> List[AliquotResponse]:
        """
        Get all aliquots for a sample
        """
        aliquots = db.query(Aliquot).filter(
            Aliquot.sample_id == sample_id
        ).options(
            joinedload(Aliquot.tests)
        ).all()
        
        # Convert SQLAlchemy models to Pydantic models
        return [
            AliquotResponse(
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
            for aliquot in aliquots
        ]
    
    @staticmethod
    def get_aliquot_by_id(db: Session, aliquot_id: str, sample_id: str) -> Optional[AliquotResponse]:
        """
        Get a specific aliquot by its ID
        """
        aliquot = db.query(Aliquot).filter(
            Aliquot.id == aliquot_id,
            Aliquot.sample_id == sample_id
        ).options(
            joinedload(Aliquot.tests)
        ).first()
        
        if aliquot is None:
            return None
            
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
    
    @staticmethod
    def create_aliquot(db: Session, aliquot_data: AliquotCreate) -> Optional[AliquotResponse]:
        """
        Create a new aliquot for a sample
        """
        # Get the parent sample
        sample = db.query(Sample).filter(Sample.id == aliquot_data.sample_id).first()
        
        if sample is None:
            return None
        
        # Check if there's enough volume left
        if sample.volume_left < aliquot_data.volume_ml:
            return None
        
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
        if sample.aliquots_created == 0:
            sample.status = "aliquots_created"
        
        db.add(db_aliquot)
        db.commit()
        db.refresh(db_aliquot)
        
        return AliquotResponse(
            id=db_aliquot.id,
            sample_id=db_aliquot.sample_id,
            aliquot_code=db_aliquot.aliquot_code,
            volume_ml=db_aliquot.volume_ml,
            creation_date=db_aliquot.created_at,
            status=db_aliquot.status,
            assigned_to=db_aliquot.assigned_to,
            created_by=db_aliquot.created_by,
            created_at=db_aliquot.created_at,
            purpose=db_aliquot.purpose,
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
                ) for test in db_aliquot.tests
            ]
        )
    
    @staticmethod
    def update_aliquot_location(db: Session, sample_id: str, aliquot_id: str, location: str) -> Optional[AliquotResponse]:
        """
        Update an aliquot's location
        """
        db_aliquot = db.query(Aliquot).filter(
            Aliquot.id == aliquot_id,
            Aliquot.sample_id == sample_id
        ).options(
            joinedload(Aliquot.tests)
        ).first()
        
        if db_aliquot is None:
            return None
        
        db_aliquot.status = location  # In this case location maps to status
        db.commit()
        db.refresh(db_aliquot)
        
        return AliquotResponse(
            id=db_aliquot.id,
            sample_id=db_aliquot.sample_id,
            aliquot_code=db_aliquot.aliquot_code,
            volume_ml=db_aliquot.volume_ml,
            creation_date=db_aliquot.created_at,
            status=db_aliquot.status,
            assigned_to=db_aliquot.assigned_to,
            created_by=db_aliquot.created_by,
            created_at=db_aliquot.created_at,
            purpose=db_aliquot.purpose,
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
                ) for test in db_aliquot.tests
            ]
        )
    
    @staticmethod
    def delete_aliquot(db: Session, sample_id: str, aliquot_id: str) -> bool:
        """
        Delete an aliquot
        """
        # Find the aliquot
        db_aliquot = db.query(Aliquot).filter(
            Aliquot.id == aliquot_id,
            Aliquot.sample_id == sample_id
        ).first()
        
        if db_aliquot is None:
            return False
        
        # Get the parent sample to update its volume and aliquot count
        sample = db.query(Sample).filter(Sample.id == sample_id).first()
        
        if sample:
            # Return the volume back to the parent sample
            sample.volume_left = sample.volume_left + db_aliquot.volume
            sample.aliquots_created = sample.aliquots_created - 1
            
            # If no more aliquots, update the sample status back to submitted
            if sample.aliquots_created <= 0:
                sample.status = "submitted"
                sample.aliquots_created = 0  # Make sure it's not negative
        
        # Delete the aliquot
        db.delete(db_aliquot)
        db.commit()
        return True
