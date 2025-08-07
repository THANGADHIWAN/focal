"""
Sample service for the Sample Management API
"""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, or_, and_
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime
import pandas as pd
from io import StringIO
import csv
from fastapi import HTTPException
import logging

from app.db.models.sample import Sample, SampleType, Aliquot
from app.db.models.test import Test
from app.schemas import SampleCreate, SampleUpdate, SampleFilter, SampleResponse, AliquotSummary

# Set up logging
logger = logging.getLogger(__name__)

class SampleService:
    @staticmethod
    def get_all_samples(
        db: Session,
        page: int = 1,
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> Tuple[List[SampleResponse], int, int]:
        """
        Get all samples with pagination and filtering options
        """
        try:
            # Query samples with sample type join
            query = (
                db.query(Sample, SampleType.name.label('type_name'))
                .join(SampleType, Sample.sample_type_id == SampleType.id)
            )
        
            # Apply filters if provided
            if filters:
                if filters.get("type"):
                    if isinstance(filters["type"], list):
                        # Convert string IDs to integers for database query
                        type_ids = []
                        for type_id in filters["type"]:
                            try:
                                type_ids.append(int(type_id))
                            except (ValueError, TypeError):
                                continue
                        if type_ids:
                            query = query.filter(Sample.sample_type_id.in_(type_ids))
                    else:
                        try:
                            type_id = int(filters["type"])
                            query = query.filter(Sample.sample_type_id == type_id)
                        except (ValueError, TypeError):
                            pass
                        
                if filters.get("status"):
                    if isinstance(filters["status"], list):
                        query = query.filter(Sample.status.in_(filters["status"]))
                    else:
                        query = query.filter(Sample.status == filters["status"])
                        
                if filters.get("location"):
                    if isinstance(filters["location"], list):
                        # Convert string IDs to integers for database query
                        location_ids = []
                        for location_id in filters["location"]:
                            try:
                                location_ids.append(int(location_id))
                            except (ValueError, TypeError):
                                continue
                        if location_ids:
                            query = query.filter(Sample.box_id.in_(location_ids))
                    else:
                        try:
                            location_id = int(filters["location"])
                            query = query.filter(Sample.box_id == location_id)
                        except (ValueError, TypeError):
                            pass
                        
                if filters.get("owner"):
                    if isinstance(filters["owner"], list):
                        query = query.filter(Sample.created_by.in_(filters["owner"]))
                    else:
                        query = query.filter(Sample.created_by == filters["owner"])
                        
                if filters.get("search"):
                    search_term = f"%{filters['search']}%"
                    query = query.filter(
                        or_(
                            Sample.sample_name.ilike(search_term),
                            Sample.sample_code.ilike(search_term),
                            Sample.created_by.ilike(search_term)
                        )
                    )
          
            # Count total results for pagination
            total_count = query.count()
            print(f"Total samples found: {total_count}")
            total_pages = (total_count + limit - 1) // limit if total_count > 0 else 0
            
            # Apply pagination
            query = query.offset((page - 1) * limit).limit(limit)
            
            # Get results with related aliquots
            samples = query.options(
                joinedload(Sample.aliquots)
            ).all()
            
            # Convert SQLAlchemy models to Pydantic models
            sample_responses = []
            for sample, type_name in samples:
                # Convert aliquots to AliquotSummary
                aliquot_summaries = []
                for aliquot in sample.aliquots:
                    aliquot_summary = AliquotSummary(
                        id=aliquot.id,
                        aliquot_code=aliquot.aliquot_code,
                        volume_ml=aliquot.volume_ml,
                        status=aliquot.status,
                        created_at=aliquot.created_at
                    )
                    aliquot_summaries.append(aliquot_summary)
                
                # Create sample response with aliquots
                sample_response = SampleResponse(
                    id=sample.id,
                    sample_code=sample.sample_code,
                    sample_name=sample.sample_name,
                    sample_type_id=sample.sample_type_id,
                    type_name=type_name,
                    status=sample.status,
                    box_id=sample.box_id,
                    volume_ml=sample.volume_ml,
                    received_date=sample.received_date,
                    due_date=sample.due_date,
                    priority=sample.priority,
                    quantity=sample.quantity,
                    is_aliquot=sample.is_aliquot,
                    number_of_aliquots=sample.number_of_aliquots,
                    created_by=sample.created_by,
                    created_at=sample.created_at,
                    updated_at=sample.updated_at,
                    purpose=sample.purpose,
                    aliquots=aliquot_summaries
                )
                sample_responses.append(sample_response)
            
            return sample_responses, total_count, total_pages
            
        except Exception as e:
            logger.error(f"Error in get_all_samples: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Database error: {str(e)}"
            )

    @staticmethod
    def get_sample_by_id(db: Session, sample_id: int) -> Optional[SampleResponse]:
        """
        Get a specific sample by its ID
        """
        try:
            result = (
                db.query(Sample, SampleType.name.label('type_name'))
                .join(SampleType, Sample.sample_type_id == SampleType.id)
                .options(joinedload(Sample.aliquots))
                .filter(Sample.id == sample_id)
                .first()
            )
            
            if result:
                sample, type_name = result
                # Convert aliquots to AliquotSummary
                aliquot_summaries = []
                for aliquot in sample.aliquots:
                    aliquot_summary = AliquotSummary(
                        id=aliquot.id,
                        aliquot_code=aliquot.aliquot_code,
                        volume_ml=aliquot.volume_ml,
                        status=aliquot.status,
                        created_at=aliquot.created_at
                    )
                    aliquot_summaries.append(aliquot_summary)
                
                # Create sample response with aliquots
                sample_response = SampleResponse(
                    id=sample.id,
                    sample_code=sample.sample_code,
                    sample_name=sample.sample_name,
                    sample_type_id=sample.sample_type_id,
                    type_name=type_name,
                    status=sample.status,
                    box_id=sample.box_id,
                    volume_ml=sample.volume_ml,
                    received_date=sample.received_date,
                    due_date=sample.due_date,
                    priority=sample.priority,
                    quantity=sample.quantity,
                    is_aliquot=sample.is_aliquot,
                    number_of_aliquots=sample.number_of_aliquots,
                    created_by=sample.created_by,
                    created_at=sample.created_at,
                    updated_at=sample.updated_at,
                    purpose=sample.purpose,
                    aliquots=aliquot_summaries
                )
                return sample_response
            return None
            
        except Exception as e:
            logger.error(f"Error in get_sample_by_id: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Database error: {str(e)}"
            )

    @staticmethod
    def create_sample(db: Session, sample_data: SampleCreate) -> SampleResponse:
        """
        Create a new sample
        """
        try:
            # Create new sample object
            sample = Sample(
                sample_code=sample_data.sample_code,
                sample_name=sample_data.sample_name,
                sample_type_id=sample_data.sample_type_id,
                status=sample_data.status,
                box_id=sample_data.box_id,
                volume_ml=sample_data.volume_ml,
                received_date=sample_data.received_date,
                due_date=sample_data.due_date,
                priority=sample_data.priority,
                quantity=sample_data.quantity,
                is_aliquot=sample_data.is_aliquot,
                number_of_aliquots=sample_data.number_of_aliquots,
                created_by=sample_data.created_by,
                purpose=sample_data.purpose
            )
            
            db.add(sample)
            db.commit()
            db.refresh(sample)
            
            # Get sample type name
            type_name = db.query(SampleType).filter(SampleType.id == sample.sample_type_id).first().name
            
            # Create sample response without aliquots (new sample won't have any)
            sample_response = SampleResponse(
                id=sample.id,
                sample_code=sample.sample_code,
                sample_name=sample.sample_name,
                sample_type_id=sample.sample_type_id,
                type_name=type_name,
                status=sample.status,
                box_id=sample.box_id,
                volume_ml=sample.volume_ml,
                received_date=sample.received_date,
                due_date=sample.due_date,
                priority=sample.priority,
                quantity=sample.quantity,
                is_aliquot=sample.is_aliquot,
                number_of_aliquots=sample.number_of_aliquots,
                created_by=sample.created_by,
                created_at=sample.created_at,
                updated_at=sample.updated_at,
                purpose=sample.purpose,
                aliquots=[]
            )
            
            return sample_response
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error in create_sample: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to create sample: {str(e)}"
            )

    @staticmethod
    def update_sample(db: Session, sample_id: int, sample_data: SampleUpdate) -> Optional[SampleResponse]:
        """
        Update an existing sample
        """
        try:
            result = (
                db.query(Sample, SampleType.name.label('type_name'))
                .join(SampleType, Sample.sample_type_id == SampleType.id)
                .options(joinedload(Sample.aliquots))
                .filter(Sample.id == sample_id)
                .first()
            )
            
            if not result:
                return None
                
            sample, type_name = result
            
            # Update fields if provided
            update_data = sample_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(sample, field, value)
            
            db.commit()
            db.refresh(sample)
            
            # Convert aliquots to AliquotSummary
            aliquot_summaries = []
            for aliquot in sample.aliquots:
                aliquot_summary = AliquotSummary(
                    id=aliquot.id,
                    aliquot_code=aliquot.aliquot_code,
                    volume_ml=aliquot.volume_ml,
                    status=aliquot.status,
                    created_at=aliquot.created_at
                )
                aliquot_summaries.append(aliquot_summary)
            
            # Create sample response with aliquots
            sample_response = SampleResponse(
                id=sample.id,
                sample_code=sample.sample_code,
                sample_name=sample.sample_name,
                sample_type_id=sample.sample_type_id,
                type_name=type_name,
                status=sample.status,
                box_id=sample.box_id,
                volume_ml=sample.volume_ml,
                received_date=sample.received_date,
                due_date=sample.due_date,
                priority=sample.priority,
                quantity=sample.quantity,
                is_aliquot=sample.is_aliquot,
                number_of_aliquots=sample.number_of_aliquots,
                created_by=sample.created_by,
                created_at=sample.created_at,
                updated_at=sample.updated_at,
                purpose=sample.purpose,
                aliquots=aliquot_summaries
            )
            
            return sample_response
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error in update_sample: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to update sample: {str(e)}"
            )

    @staticmethod
    def delete_sample(db: Session, sample_id: int) -> bool:
        """
        Delete a sample
        """
        try:
            sample = db.query(Sample).filter(Sample.id == sample_id).first()
            
            if not sample:
                return False
            
            db.delete(sample)
            db.commit()
            
            return True
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error in delete_sample: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to delete sample: {str(e)}"
            )

    @staticmethod
    def export_samples_csv(db: Session, filters: Optional[Dict[str, Any]] = None) -> str:
        """
        Export samples as CSV
        """
        try:
            # Query samples with sample type join
            query = (
                db.query(Sample, SampleType.name.label('type_name'))
                .join(SampleType, Sample.sample_type_id == SampleType.id)
            )
            
            # Apply filters if provided
            if filters:
                if filters.get("type"):
                    if isinstance(filters["type"], list):
                        type_ids = []
                        for type_id in filters["type"]:
                            try:
                                type_ids.append(int(type_id))
                            except (ValueError, TypeError):
                                continue
                        if type_ids:
                            query = query.filter(Sample.sample_type_id.in_(type_ids))
                    else:
                        try:
                            type_id = int(filters["type"])
                            query = query.filter(Sample.sample_type_id == type_id)
                        except (ValueError, TypeError):
                            pass
                        
                if filters.get("status"):
                    if isinstance(filters["status"], list):
                        query = query.filter(Sample.status.in_(filters["status"]))
                    else:
                        query = query.filter(Sample.status == filters["status"])
                        
                if filters.get("location"):
                    if isinstance(filters["location"], list):
                        location_ids = []
                        for location_id in filters["location"]:
                            try:
                                location_ids.append(int(location_id))
                            except (ValueError, TypeError):
                                continue
                        if location_ids:
                            query = query.filter(Sample.box_id.in_(location_ids))
                    else:
                        try:
                            location_id = int(filters["location"])
                            query = query.filter(Sample.box_id == location_id)
                        except (ValueError, TypeError):
                            pass
                        
                if filters.get("owner"):
                    if isinstance(filters["owner"], list):
                        query = query.filter(Sample.created_by.in_(filters["owner"]))
                    else:
                        query = query.filter(Sample.created_by == filters["owner"])
                        
                if filters.get("search"):
                    search_term = f"%{filters['search']}%"
                    query = query.filter(
                        or_(
                            Sample.sample_name.ilike(search_term),
                            Sample.sample_code.ilike(search_term),
                            Sample.created_by.ilike(search_term)
                        )
                    )
            
            samples = query.all()
            
            # Create CSV data
            output = StringIO()
            writer = csv.writer(output)
            
            # Write header
            writer.writerow([
                'ID', 'Sample Code', 'Sample Name', 'Sample Type ID', 'Status',
                'Box ID', 'Volume (mL)', 'Received Date', 'Due Date', 'Priority',
                'Quantity', 'Is Aliquot', 'Number of Aliquots', 'Created By',
                'Created At', 'Updated At', 'Purpose'
            ])
            
            # Write data rows
            for sample in samples:
                writer.writerow([
                    sample.id, sample.sample_code, sample.sample_name,
                    sample.sample_type_id, sample.status, sample.box_id,
                    sample.volume_ml, sample.received_date, sample.due_date,
                    sample.priority, sample.quantity, sample.is_aliquot,
                    sample.number_of_aliquots, sample.created_by,
                    sample.created_at, sample.updated_at, sample.purpose
                ])
            
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"Error in export_samples_csv: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to export samples: {str(e)}"
            )
