from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas import ApiResponse, AliquotCreate, AliquotUpdate
from app.services.aliquot_service import AliquotService
from app.utils.constants import Location

router = APIRouter(
    prefix="/samples/{sample_id}/aliquots",
    tags=["aliquots"],
    responses={404: {"description": "Not found"}}
)

@router.get("/", response_model=ApiResponse)
def get_all_aliquots(
    sample_id: str = Path(..., description="The ID of the sample"),
    db: Session = Depends(get_db)
):
    """
    Get all aliquots for a sample
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
        
        aliquots = AliquotService.get_all_aliquots(db=db, sample_id=sample_id_int)
        
        return {
            "data": aliquots,
            "status": 200,
            "success": True
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get aliquots: {str(e)}"
        )

@router.get("/{aliquot_id}", response_model=ApiResponse)
def get_aliquot_by_id(
    sample_id: str = Path(..., description="The ID of the sample"),
    aliquot_id: str = Path(..., description="The ID of the aliquot"),
    db: Session = Depends(get_db)
):
    """
    Get a specific aliquot by its ID
    """
    try:
        # Convert string IDs to integers
        try:
            sample_id_int = int(sample_id)
            aliquot_id_int = int(aliquot_id)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid ID format. Expected numeric IDs."
            )
        
        aliquot = AliquotService.get_aliquot_by_id(
            db=db,
            aliquot_id=aliquot_id_int,
            sample_id=sample_id_int
        )
        
        if aliquot is None:
            raise HTTPException(
                status_code=404,
                detail=f"Aliquot with ID {aliquot_id} not found for sample {sample_id}"
            )
        
        return {
            "data": aliquot,
            "status": 200,
            "success": True
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get aliquot: {str(e)}"
        )

@router.post("/", response_model=ApiResponse)
def create_aliquot(
    aliquot_data: AliquotCreate,
    sample_id: str = Path(..., description="The ID of the sample"),
    db: Session = Depends(get_db)
):
    """
    Create a new aliquot for a sample
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
        
        # Ensure the provided sample_id matches the path parameter
        if aliquot_data.sample_id != sample_id_int:
            raise HTTPException(
                status_code=400,
                detail="The sample_id in the request body must match the sample_id in the URL path"
            )
        
        aliquot = AliquotService.create_aliquot(db=db, aliquot_data=aliquot_data)
        
        if aliquot is None:
            raise HTTPException(
                status_code=404,
                detail=f"Sample with ID {sample_id} not found or not enough volume left"
            )
        
        return {
            "data": aliquot,
            "status": 201,
            "success": True
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create aliquot: {str(e)}"
        )

@router.patch("/{aliquot_id}/location", response_model=ApiResponse)
def update_aliquot_location(
    location_update: AliquotUpdate,
    sample_id: str = Path(..., description="The ID of the sample"),
    aliquot_id: str = Path(..., description="The ID of the aliquot"),
    db: Session = Depends(get_db)
):
    """
    Update an aliquot's location
    """
    try:
        # Convert string IDs to integers
        try:
            sample_id_int = int(sample_id)
            aliquot_id_int = int(aliquot_id)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid ID format. Expected numeric IDs."
            )
        
        updated_aliquot = AliquotService.update_aliquot_location(
            db=db,
            sample_id=sample_id_int,
            aliquot_id=aliquot_id_int,
            location=location_update.location
        )
        
        if updated_aliquot is None:
            raise HTTPException(
                status_code=404,
                detail=f"Aliquot with ID {aliquot_id} not found for sample {sample_id}"
            )
        
        return {
            "data": updated_aliquot,
            "status": 200,
            "success": True
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update aliquot location: {str(e)}"
        )

@router.delete("/{aliquot_id}", response_model=ApiResponse)
def delete_aliquot(
    sample_id: str = Path(..., description="The ID of the sample"),
    aliquot_id: str = Path(..., description="The ID of the aliquot"),
    db: Session = Depends(get_db)
):
    """
    Delete an aliquot
    """
    try:
        # Convert string IDs to integers
        try:
            sample_id_int = int(sample_id)
            aliquot_id_int = int(aliquot_id)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid ID format. Expected numeric IDs."
            )
        
        success = AliquotService.delete_aliquot(
            db=db,
            sample_id=sample_id_int,
            aliquot_id=aliquot_id_int
        )
        
        if not success:
            raise HTTPException(
                status_code=404,
                detail=f"Aliquot with ID {aliquot_id} not found for sample {sample_id}"
            )
        
        return {
            "message": f"Aliquot with ID {aliquot_id} deleted successfully",
            "status": 200,
            "success": True
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete aliquot: {str(e)}"
        )
