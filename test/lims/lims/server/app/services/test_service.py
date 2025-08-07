"""
Test service for the Sample Management API
"""
from sqlalchemy.orm import Session
from app.db.models.sample import Aliquot, Sample
from app.db.models.test import Test, TestMethod
from app.schemas.test import TestCreate, TestUpdate, TestResponse, TestMethodResponse
from typing import List, Optional
from datetime import datetime

class TestService:
    @staticmethod
    def get_all_tests(db: Session, sample_id: int, aliquot_id: int) -> List[TestResponse]:
        """
        Get all tests for an aliquot
        """
        tests = db.query(Test).join(Aliquot).filter(
            Aliquot.id == aliquot_id,
            Aliquot.sample_id == sample_id
        ).all()

        # Convert SQLAlchemy models to Pydantic models
        return [
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
            )
            for test in tests
        ]
    
    @staticmethod
    def get_test_by_id(db: Session, sample_id: int, aliquot_id: int, test_id: int) -> Optional[TestResponse]:
        """
        Get a specific test by its ID
        """
        test = db.query(Test).join(Aliquot).filter(
            Test.id == test_id,
            Aliquot.id == aliquot_id,
            Aliquot.sample_id == sample_id
        ).first()

        if test is None:
            return None

        return TestResponse(
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
        )
    
    @staticmethod
    def create_test(db: Session, sample_id: int, aliquot_id: int, test_data: TestCreate) -> Optional[TestResponse]:
        """
        Create a new test for an aliquot
        """
        # Verify aliquot exists and belongs to the sample
        aliquot = db.query(Aliquot).filter(
            Aliquot.id == aliquot_id,
            Aliquot.sample_id == sample_id
        ).first()
        
        if aliquot is None:
            return None
        
        # Create the test
        db_test = Test(
            sample_id=sample_id,
            aliquot_id=aliquot_id,
            test_master_id=test_data.test_master_id,
            analyst_id=test_data.analyst_id,
            instrument_id=test_data.instrument_id,
            status=test_data.status,
            scheduled_date=test_data.scheduled_date,
            remarks=test_data.remarks,
            start_date=datetime.utcnow()
        )
        
        # When a test is created, update the sample status
        sample = db.query(Sample).filter(Sample.id == sample_id).first()
        if sample and sample.status == "aliquots_created":
            sample.status = "aliquots_plated"
        
        db.add(db_test)
        db.commit()
        db.refresh(db_test)

        return TestResponse(
            id=db_test.id,
            sample_id=db_test.sample_id,
            aliquot_id=db_test.aliquot_id,
            test_master_id=db_test.test_master_id,
            analyst_id=db_test.analyst_id,
            instrument_id=db_test.instrument_id,
            scheduled_date=db_test.scheduled_date,
            start_date=db_test.start_date,
            end_date=db_test.end_date,
            status=db_test.status,
            remarks=db_test.remarks,
            sample=None,
            aliquot=None,
            test_results=[]
        )
    
    @staticmethod
    def update_test(db: Session, sample_id: int, aliquot_id: int, test_id: int, test_data: TestUpdate) -> Optional[TestResponse]:
        """
        Update an existing test
        """
        db_test = db.query(Test).join(Aliquot).filter(
            Test.id == test_id,
            Aliquot.id == aliquot_id,
            Aliquot.sample_id == sample_id
        ).first()
        
        if db_test is None:
            return None
        
        # Update only the fields that are provided
        update_data = test_data.model_dump(exclude_unset=True)
        
        # If status is being changed to "Completed" and end_date isn't provided, set it
        if update_data.get("status") == "Completed" and not update_data.get("end_date"):
            update_data["end_date"] = datetime.utcnow()
            
            # Check if all tests for this sample are now completed
            sample = db.query(Sample).filter(Sample.id == sample_id).first()
            if sample:
                # Count total and completed tests for the sample
                all_aliquots = db.query(Aliquot).filter(Aliquot.sample_id == sample_id).all()
                aliquot_ids = [a.id for a in all_aliquots]
                
                total_tests = db.query(Test).filter(Test.aliquot_id.in_(aliquot_ids)).count()
                completed_tests = db.query(Test).filter(
                    Test.aliquot_id.in_(aliquot_ids),
                    Test.status == "Completed"
                ).count()
                
                # If all tests are completed, update the sample status
                if total_tests > 0 and total_tests == completed_tests:
                    sample.status = "testing_completed"
        
        for key, value in update_data.items():
            setattr(db_test, key, value)
            
        db.commit()
        db.refresh(db_test)

        return TestResponse(
            id=db_test.id,
            sample_id=db_test.sample_id,
            aliquot_id=db_test.aliquot_id,
            test_master_id=db_test.test_master_id,
            analyst_id=db_test.analyst_id,
            instrument_id=db_test.instrument_id,
            scheduled_date=db_test.scheduled_date,
            start_date=db_test.start_date,
            end_date=db_test.end_date,
            status=db_test.status,
            remarks=db_test.remarks,
            sample=None,
            aliquot=None,
            test_results=[]
        )
    
    @staticmethod
    def delete_test(db: Session, sample_id: int, aliquot_id: int, test_id: int) -> bool:
        """
        Delete a test
        """
        db_test = db.query(Test).join(Aliquot).filter(
            Test.id == test_id,
            Aliquot.id == aliquot_id,
            Aliquot.sample_id == sample_id
        ).first()
        
        if db_test is None:
            return False
        
        db.delete(db_test)
        db.commit()
        return True
    
    @staticmethod
    def get_test_methods(db: Session) -> List[TestMethodResponse]:
        """
        Get all available test methods
        """
        methods = db.query(TestMethod).all()
        return [
            TestMethodResponse(
                id=method.id,
                name=method.name,
                version=method.version,
                description=method.description,
                validated=method.validated
            )
            for method in methods
        ]
