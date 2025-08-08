"""
API Service layer for aliquot operations
Handles request validation, error formatting, and response structure
"""
from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, List
import logging

from app.api.schemas.aliquot import AliquotCreate, AliquotUpdate, AliquotResponse
from app.services.aliquot_service import AliquotService
from app.utils.responses import format_success_response
from app.core.exceptions import LIMSException

# Set up logging
logger = logging.getLogger(__name__)


class AliquotAPIService:
    """
    API Service layer for Aliquot operations
    Handles request validation, error formatting, and response structure
    """

    @staticmethod
    def get_all_aliquots(db: Session, sample_id: str) -> Dict[str, Any]:
        """
        Handle GET /samples/{sample_id}/aliquots endpoint
        """
        try:
            aliquots = AliquotService.get_all_aliquots(db, sample_id)
            return format_success_response(
                data=aliquots,
                status_code=200
            )
        except LIMSException as e:
            raise HTTPException(
                status_code=e.status_code,
                detail=e.detail
            )

    @staticmethod
    def get_aliquot_by_id(db: Session, sample_id: str, aliquot_id: str) -> Dict[str, Any]:
        """
        Handle GET /samples/{sample_id}/aliquots/{aliquot_id} endpoint
        """
        try:
            aliquot = AliquotService.get_aliquot_by_id(db, aliquot_id, sample_id)
            return format_success_response(
                data=aliquot,
                status_code=200
            )
        except LIMSException as e:
            raise HTTPException(
                status_code=e.status_code,
                detail=e.detail
            )

    @staticmethod
    def create_aliquot(db: Session, aliquot_data: AliquotCreate) -> Dict[str, Any]:
        """
        Handle POST /samples/{sample_id}/aliquots endpoint
        """
        try:
            aliquot = AliquotService.create_aliquot(db, aliquot_data)
            return format_success_response(
                data=aliquot,
                status_code=201,
                message="Aliquot created successfully"
            )
        except LIMSException as e:
            raise HTTPException(
                status_code=e.status_code,
                detail=e.detail
            )

    @staticmethod
    def update_aliquot_location(
        db: Session,
        sample_id: str,
        aliquot_id: str,
        location: str
    ) -> Dict[str, Any]:
        """
        Handle PUT /samples/{sample_id}/aliquots/{aliquot_id}/location endpoint
        """
        try:
            aliquot = AliquotService.update_aliquot_location(db, sample_id, aliquot_id, location)
            return format_success_response(
                data=aliquot,
                status_code=200,
                message="Aliquot location updated successfully"
            )
        except LIMSException as e:
            raise HTTPException(
                status_code=e.status_code,
                detail=e.detail
            )

    @staticmethod
    def delete_aliquot(db: Session, sample_id: str, aliquot_id: str) -> Dict[str, Any]:
        """
        Handle DELETE /samples/{sample_id}/aliquots/{aliquot_id} endpoint
        """
        try:
            AliquotService.delete_aliquot(db, sample_id, aliquot_id)
            return format_success_response(
                data={"message": f"Aliquot {aliquot_id} deleted successfully"},
                status_code=200
            )
        except LIMSException as e:
            raise HTTPException(
                status_code=e.status_code,
                detail=e.detail
            )
