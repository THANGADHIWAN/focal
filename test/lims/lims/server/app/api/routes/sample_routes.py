from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any, Union
from io import StringIO
import logging

from app.db.database import get_db
from app.schemas import ApiResponse, PaginatedResponse, SampleCreate, SampleUpdate, SampleFilter
from app.services.sample_service import SampleService
from app.db.models.sample import Sample

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/samples",
    tags=["samples"],
    responses={404: {"description": "Not found"}}
)

@router.get("", response_model=ApiResponse)
def get_all_samples(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Number of items per page"),
    type: Optional[List[str]] = Query(
        None, 
        description="Filter by sample type IDs - Get values from /metadata/sample_types API"
    ),
    status: Optional[List[str]] = Query(
        None, 
        description="Filter by sample statuses"
    ),
    location: Optional[List[str]] = Query(
        None, 
        description="Filter by storage locations"
    ),
    owner: Optional[List[str]] = Query(
        None, 
        description="Filter by created_by field",
        examples=[["John Doe", "Jane Smith"]]
    ),
    search: Optional[str] = Query(
        None, 
        description="Search term for sample name or code",
        examples=["sample123"]
    ),
    db: Session = Depends(get_db)
):
    """
    Get all samples with pagination and filtering options
    """
    try:
        # Build filter dict from query parameters
        filters = {}
        if type:
            filters["type"] = type
        if status:
            filters["status"] = status
        if location:
            filters["location"] = location
        if owner:
            filters["owner"] = owner
        if search:
            filters["search"] = search
        
        samples, total_count, total_pages = SampleService.get_all_samples(
            db=db,
            page=page,
            limit=limit,
            filters=filters
        )
        
        # Create paginated response
        paginated_response = {
            "data": samples,
            "total_count": total_count,
            "total_pages": total_pages,
            "current_page": page,
            "page_size": limit,
            "has_more": page < total_pages
        }
        
        return {
            "data": paginated_response,
            "status": 200,
            "success": True
        }
    except Exception as e:
        logger.error(f"Error in get_all_samples: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/{sample_id}", response_model=ApiResponse)
def get_sample_by_id(
    sample_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a specific sample by its ID
    """
    try:
        # Convert string sample_id to integer
        try:
            sample_id_int = int(sample_id)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid sample ID format: {sample_id}. Expected a numeric ID."
            )
        
        sample = SampleService.get_sample_by_id(db=db, sample_id=sample_id_int)
        
        if sample is None:
            raise HTTPException(
                status_code=404,
                detail=f"Sample with ID {sample_id} not found"
            )
        
        return {
            "data": sample,
            "status": 200,
            "success": True
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_sample_by_id: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.post("", response_model=ApiResponse)
def create_sample(
    sample_data: SampleCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new sample
    """
    try:
        sample = SampleService.create_sample(db=db, sample_data=sample_data)
        
        return {
            "data": sample,
            "status": 201,
            "success": True,
            "message": "Sample created successfully"
        }
    except Exception as e:
        logger.error(f"Error in create_sample: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create sample: {str(e)}"
        )

@router.patch("/{sample_id}", response_model=ApiResponse)
def update_sample(
    sample_id: str,
    sample_data: SampleUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing sample
    """
    try:
        # Convert string sample_id to integer
        try:
            sample_id_int = int(sample_id)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid sample ID format: {sample_id}. Expected a numeric ID."
            )
        
        sample = SampleService.update_sample(
            db=db, 
            sample_id=sample_id_int, 
            sample_data=sample_data
        )
        
        if sample is None:
            raise HTTPException(
                status_code=404,
                detail=f"Sample with ID {sample_id} not found"
            )
        
        return {
            "data": sample,
            "status": 200,
            "success": True,
            "message": "Sample updated successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in update_sample: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update sample: {str(e)}"
        )

@router.delete("/{sample_id}", response_model=ApiResponse)
def delete_sample(
    sample_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a sample by its ID
    """
    try:
        # Convert string sample_id to integer
        try:
            sample_id_int = int(sample_id)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid sample ID format: {sample_id}. Expected a numeric ID."
            )
        
        success = SampleService.delete_sample(db=db, sample_id=sample_id_int)
        
        if not success:
            raise HTTPException(
                status_code=404,
                detail=f"Sample with ID {sample_id} not found"
            )
        
        return {
            "data": None,
            "status": 200,
            "success": True,
            "message": "Sample deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in delete_sample: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete sample: {str(e)}"
        )

@router.get("/export_csv", response_class=Response)
def export_samples(
    type: Optional[List[str]] = Query(
        None, 
        description="Filter by sample types"
    ),
    status: Optional[List[str]] = Query(
        None, 
        description="Filter by sample statuses"
    ),
    location: Optional[List[str]] = Query(
        None, 
        description="Filter by storage locations"
    ),
    owner: Optional[List[str]] = Query(
        None, 
        description="Filter by sample owners",
        examples=[["John Doe", "Jane Smith"]]
    ),
    search: Optional[str] = Query(
        None, 
        description="Search term for sample name or code",
        examples=["sample123"]
    ),
    db: Session = Depends(get_db)
):
    """
    Export samples as CSV
    """
    try:
        # Build filter dict from query parameters
        filters = {}
        if type:
            filters["type"] = type
        if status:
            filters["status"] = status
        if location:
            filters["location"] = location
        if owner:
            filters["owner"] = owner
        if search:
            filters["search"] = search
        
        csv_data = SampleService.export_samples_csv(db=db, filters=filters)
        
        return Response(
            content=csv_data,
            media_type="text/csv",
            headers={
                "Content-Disposition": "attachment; filename=samples_export.csv"
            }
        )
    except Exception as e:
        logger.error(f"Error in export_samples: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to export samples: {str(e)}"
        )
