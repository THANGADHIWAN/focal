from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.db.database import get_db
from app.schemas import ApiResponse
from app.services.audit_service import AuditService

router = APIRouter(
    prefix="/samples/{sample_id}/timeline",
    tags=["audit"],
    responses={404: {"description": "Not found"}}
)

@router.get("/", response_model=ApiResponse)
def get_sample_timeline(
    sample_id: str = Path(..., description="The ID of the sample"),
    limit: int = Query(50, ge=1, le=100, description="Number of timeline events to return"),
    db: Session = Depends(get_db)
):
    """
    Get timeline/audit trail for a specific sample
    """
    try:
        timeline_events = AuditService.get_sample_timeline(
            db=db,
            sample_id=sample_id,
            limit=limit
        )
        
        return {
            "data": timeline_events,
            "status": 200,
            "success": True
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve timeline: {str(e)}"
        )

@router.get("/aliquots/{aliquot_id}", response_model=ApiResponse)
def get_aliquot_timeline(
    sample_id: str = Path(..., description="The ID of the sample"),
    aliquot_id: str = Path(..., description="The ID of the aliquot"),
    limit: int = Query(50, ge=1, le=100, description="Number of timeline events to return"),
    db: Session = Depends(get_db)
):
    """
    Get timeline/audit trail for a specific aliquot
    """
    try:
        timeline_events = AuditService.get_aliquot_timeline(
            db=db,
            sample_id=sample_id,
            aliquot_id=aliquot_id,
            limit=limit
        )
        
        return {
            "data": timeline_events,
            "status": 200,
            "success": True
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve aliquot timeline: {str(e)}"
        )

@router.get("/tests/{test_id}", response_model=ApiResponse)
def get_test_timeline(
    sample_id: str = Path(..., description="The ID of the sample"),
    test_id: str = Path(..., description="The ID of the test"),
    limit: int = Query(50, ge=1, le=100, description="Number of timeline events to return"),
    db: Session = Depends(get_db)
):
    """
    Get timeline/audit trail for a specific test
    """
    try:
        timeline_events = AuditService.get_test_timeline(
            db=db,
            sample_id=sample_id,
            test_id=test_id,
            limit=limit
        )
        
        return {
            "data": timeline_events,
            "status": 200,
            "success": True
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve test timeline: {str(e)}"
        ) 