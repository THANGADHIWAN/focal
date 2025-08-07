from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.database import get_db
from app.schemas import ApiResponse, TestCreate, TestUpdate, TestMethodResponse
from app.services.test_service import TestService
from app.utils.constants import TestStatus

router = APIRouter(
    prefix="/samples/{sample_id}/aliquots/{aliquot_id}/tests",
    tags=["tests"],
    responses={404: {"description": "Not found"}}
)

# Separate router for test methods
test_methods_router = APIRouter(
    prefix="/tests",
    tags=["tests"],
    responses={404: {"description": "Not found"}}
)

@router.get("/", response_model=ApiResponse)
def get_all_tests(
    sample_id: str = Path(..., description="The ID of the sample"),
    aliquot_id: str = Path(..., description="The ID of the aliquot"),
    db: Session = Depends(get_db)
):
    """
    Get all tests for an aliquot
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
        
        tests = TestService.get_all_tests(
            db=db,
            sample_id=sample_id_int,
            aliquot_id=aliquot_id_int
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get tests: {str(e)}"
        )
    finally:
        db.close()
    
    return {
        "data": tests,
        "status": 200,
        "success": True
    }

@router.get("/{test_id}", response_model=ApiResponse)
def get_test_by_id(
    sample_id: str = Path(..., description="The ID of the sample"),
    aliquot_id: str = Path(..., description="The ID of the aliquot"),
    test_id: str = Path(..., description="The ID of the test"),
    db: Session = Depends(get_db)
):
    """
    Get a specific test by its ID
    """
    try:
        # Convert string IDs to integers
        try:
            sample_id_int = int(sample_id)
            aliquot_id_int = int(aliquot_id)
            test_id_int = int(test_id)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid ID format. Expected numeric IDs."
            )
        
        test = TestService.get_test_by_id(
            db=db,
            sample_id=sample_id_int,
            aliquot_id=aliquot_id_int,
            test_id=test_id_int
        )
        
        if test is None:
            raise HTTPException(
                status_code=404,
                detail=f"Test with ID {test_id} not found for aliquot {aliquot_id}"
            )
        
        return {
            "data": test,
            "status": 200,
            "success": True
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get test: {str(e)}"
        )

@router.post("/", response_model=ApiResponse)
def create_test(
    test_data: TestCreate,
    sample_id: str = Path(..., description="The ID of the sample"),
    aliquot_id: str = Path(..., description="The ID of the aliquot"),
    db: Session = Depends(get_db)
):
    """
    Create a new test for an aliquot
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
        
        test = TestService.create_test(
            db=db,
            sample_id=sample_id_int,
            aliquot_id=aliquot_id_int,
            test_data=test_data
        )
        
        if test is None:
            raise HTTPException(
                status_code=404,
                detail=f"Aliquot with ID {aliquot_id} not found for sample {sample_id}"
            )
        
        return {
            "data": test,
            "status": 201,
            "success": True
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create test: {str(e)}"
        )

@router.patch("/{test_id}", response_model=ApiResponse)
def update_test(
    test_data: TestUpdate,
    sample_id: str = Path(..., description="The ID of the sample"),
    aliquot_id: str = Path(..., description="The ID of the aliquot"),
    test_id: str = Path(..., description="The ID of the test"),
    db: Session = Depends(get_db)
):
    """
    Update an existing test
    """
    try:
        # Convert string IDs to integers
        try:
            sample_id_int = int(sample_id)
            aliquot_id_int = int(aliquot_id)
            test_id_int = int(test_id)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid ID format. Expected numeric IDs."
            )
        
        updated_test = TestService.update_test(
            db=db,
            sample_id=sample_id_int,
            aliquot_id=aliquot_id_int,
            test_id=test_id_int,
            test_data=test_data
        )
        
        if updated_test is None:
            raise HTTPException(
                status_code=404,
                detail=f"Test with ID {test_id} not found for aliquot {aliquot_id}"
            )
        
        return {
            "data": updated_test,
            "status": 200,
            "success": True
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update test: {str(e)}"
        )

@router.delete("/{test_id}", response_model=ApiResponse)
def delete_test(
    sample_id: str = Path(..., description="The ID of the sample"),
    aliquot_id: str = Path(..., description="The ID of the aliquot"),
    test_id: str = Path(..., description="The ID of the test"),
    db: Session = Depends(get_db)
):
    """
    Delete a test
    """
    try:
        # Convert string IDs to integers
        try:
            sample_id_int = int(sample_id)
            aliquot_id_int = int(aliquot_id)
            test_id_int = int(test_id)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid ID format. Expected numeric IDs."
            )
        
        success = TestService.delete_test(
            db=db,
            sample_id=sample_id_int,
            aliquot_id=aliquot_id_int,
            test_id=test_id_int
        )
        
        if not success:
            raise HTTPException(
                status_code=404,
                detail=f"Test with ID {test_id} not found for aliquot {aliquot_id}"
            )
        
        return {
            "message": f"Test with ID {test_id} deleted successfully",
            "status": 200,
            "success": True
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete test: {str(e)}"
        )

@test_methods_router.get("/methods", response_model=ApiResponse)
def get_test_methods(db: Session = Depends(get_db)):
    """
    Get all available test methods
    """
    methods = TestService.get_test_methods(db=db)
    
    return {
        "data": methods,
        "status": 200,
        "success": True
    }
