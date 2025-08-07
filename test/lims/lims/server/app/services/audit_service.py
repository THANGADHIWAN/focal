"""
Audit service for handling timeline and audit trail functionality
"""
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Dict, Any
from datetime import datetime
import uuid

from app.db.models.audit import AuditTrail
from app.db.models.sample import Sample, Aliquot
from app.db.models.test import Test


class AuditService:
    @staticmethod
    def get_sample_timeline(db: Session, sample_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get timeline events for a specific sample
        """
        try:
            # Get audit trails for the sample
            audit_trails = db.query(AuditTrail).filter(
                AuditTrail.entity_type == "sample",
                AuditTrail.entity_id == sample_id
            ).order_by(desc(AuditTrail.performed_at)).limit(limit).all()
            
            timeline_events = []
            
            for audit in audit_trails:
                # Get user information
                user_name = audit.user.name if audit.user else "System"
                
                timeline_events.append({
                    "id": str(audit.id),
                    "event": audit.action,
                    "date": audit.performed_at.isoformat() if audit.performed_at else None,
                    "user": user_name,
                    "entity_type": audit.entity_type,
                    "entity_id": str(audit.entity_id),
                    "old_value": audit.old_value,
                    "new_value": audit.new_value,
                    "justification": audit.justification,
                    "ip_address": audit.ip_address
                })
            
            # Add sample creation event if no audit trails exist
            if not timeline_events:
                sample = db.query(Sample).filter(Sample.id == sample_id).first()
                if sample:
                    timeline_events.append({
                        "id": "sample_created",
                        "event": "Sample Created",
                        "date": sample.created_at.isoformat() if sample.created_at else None,
                        "user": sample.created_by,
                        "entity_type": "sample",
                        "entity_id": str(sample.id),
                        "old_value": None,
                        "new_value": {
                            "sample_code": sample.sample_code,
                            "sample_name": sample.sample_name,
                            "status": sample.status
                        },
                        "justification": "Sample registered in the system",
                        "ip_address": None
                    })
            
            return timeline_events
            
        except Exception as e:
            print(f"Error getting sample timeline: {e}")
            return []

    @staticmethod
    def get_aliquot_timeline(db: Session, sample_id: str, aliquot_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get timeline events for a specific aliquot
        """
        try:
            # Get audit trails for the aliquot
            audit_trails = db.query(AuditTrail).filter(
                AuditTrail.entity_type == "aliquot",
                AuditTrail.entity_id == aliquot_id
            ).order_by(desc(AuditTrail.performed_at)).limit(limit).all()
            
            timeline_events = []
            
            for audit in audit_trails:
                # Get user information
                user_name = audit.user.name if audit.user else "System"
                
                timeline_events.append({
                    "id": str(audit.id),
                    "event": audit.action,
                    "date": audit.performed_at.isoformat() if audit.performed_at else None,
                    "user": user_name,
                    "entity_type": audit.entity_type,
                    "entity_id": str(audit.entity_id),
                    "old_value": audit.old_value,
                    "new_value": audit.new_value,
                    "justification": audit.justification,
                    "ip_address": audit.ip_address
                })
            
            # Add aliquot creation event if no audit trails exist
            if not timeline_events:
                aliquot = db.query(Aliquot).filter(
                    Aliquot.id == aliquot_id,
                    Aliquot.sample_id == sample_id
                ).first()
                if aliquot:
                    timeline_events.append({
                        "id": "aliquot_created",
                        "event": "Aliquot Created",
                        "date": aliquot.created_at.isoformat() if aliquot.created_at else None,
                        "user": aliquot.created_by,
                        "entity_type": "aliquot",
                        "entity_id": str(aliquot.id),
                        "old_value": None,
                        "new_value": {
                            "aliquot_code": aliquot.aliquot_code,
                            "volume_ml": aliquot.volume_ml,
                            "status": aliquot.status
                        },
                        "justification": "Aliquot created from sample",
                        "ip_address": None
                    })
            
            return timeline_events
            
        except Exception as e:
            print(f"Error getting aliquot timeline: {e}")
            return []

    @staticmethod
    def get_test_timeline(db: Session, sample_id: str, test_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get timeline events for a specific test
        """
        try:
            # Get audit trails for the test
            audit_trails = db.query(AuditTrail).filter(
                AuditTrail.entity_type == "test",
                AuditTrail.entity_id == test_id
            ).order_by(desc(AuditTrail.performed_at)).limit(limit).all()
            
            timeline_events = []
            
            for audit in audit_trails:
                # Get user information
                user_name = audit.user.name if audit.user else "System"
                
                timeline_events.append({
                    "id": str(audit.id),
                    "event": audit.action,
                    "date": audit.performed_at.isoformat() if audit.performed_at else None,
                    "user": user_name,
                    "entity_type": audit.entity_type,
                    "entity_id": str(audit.entity_id),
                    "old_value": audit.old_value,
                    "new_value": audit.new_value,
                    "justification": audit.justification,
                    "ip_address": audit.ip_address
                })
            
            # Add test creation event if no audit trails exist
            if not timeline_events:
                test = db.query(Test).filter(
                    Test.id == test_id,
                    Test.sample_id == sample_id
                ).first()
                if test:
                    timeline_events.append({
                        "id": "test_created",
                        "event": "Test Created",
                        "date": test.created_at.isoformat() if hasattr(test, 'created_at') and test.created_at else None,
                        "user": test.created_by if hasattr(test, 'created_by') else "System",
                        "entity_type": "test",
                        "entity_id": str(test.id),
                        "old_value": None,
                        "new_value": {
                            "test_master_id": test.test_master_id,
                            "status": test.status,
                            "scheduled_date": test.scheduled_date.isoformat() if test.scheduled_date else None
                        },
                        "justification": "Test scheduled for aliquot",
                        "ip_address": None
                    })
            
            return timeline_events
            
        except Exception as e:
            print(f"Error getting test timeline: {e}")
            return []

    @staticmethod
    def create_audit_trail(
        db: Session,
        entity_type: str,
        entity_id: str,
        action: str,
        user_id: str,
        old_value: Dict[str, Any] = None,
        new_value: Dict[str, Any] = None,
        justification: str = None,
        ip_address: str = None
    ) -> AuditTrail:
        """
        Create a new audit trail entry
        """
        try:
            audit_trail = AuditTrail(
                entity_type=entity_type,
                entity_id=uuid.UUID(entity_id),
                action=action,
                user_id=uuid.UUID(user_id),
                old_value=old_value,
                new_value=new_value,
                justification=justification,
                ip_address=ip_address,
                performed_at=datetime.utcnow()
            )
            
            db.add(audit_trail)
            db.commit()
            db.refresh(audit_trail)
            
            return audit_trail
            
        except Exception as e:
            db.rollback()
            print(f"Error creating audit trail: {e}")
            raise 