from custom_admin.repositories.leave_repo import LeaveRepository
from core.dtos.leave_dto import LeaveResponseDTO
import logging

logger = logging.getLogger(__name__)

class LeaveService:
    """Handles the business logic for leave management."""

    @staticmethod
    def create_leave(data):
        """Creates a new leave entry in the database."""
        try:
            new_leave = LeaveRepository.create_leave(leave_data=data)
            return LeaveResponseDTO.transform_leave(leave=new_leave)
        except Exception as ex:
            logger.error(f"Error while creating leave: {ex}", exc_info=True)
            raise ex

    @staticmethod
    def get_leave_by_id(leave_id):
        """Fetches details of a leave by ID."""
        try:
            leave = LeaveRepository.get_leave_by_id(leave_id=leave_id)
            return LeaveResponseDTO.transform_leave(leave=leave)
        except Exception as ex:
            logger.error(f"Error while fetching leave by ID {leave_id}: {ex}", exc_info=True)
            raise ex

    @staticmethod
    def get_all_leaves(query_params):
        """Fetches and returns all leaves with optional filtering."""
        try:
            return LeaveRepository.get_all_leaves(query_params=query_params)
        except Exception as ex:
            logger.error(f"Error while fetching all leaves: {ex}", exc_info=True)
            raise ex

    @staticmethod
    def update_leave(leave_id, leave_data):
        """Updates an existing leave entry."""
        try:
            updated_leave = LeaveRepository.update_leave(leave_id=leave_id, leave_data=leave_data)
            return LeaveResponseDTO.transform_leave(leave=updated_leave)
        except Exception as ex:
            logger.error(f"Error while updating leave {leave_id}: {ex}", exc_info=True)
            raise ex

    @staticmethod
    def delete_leave(leave_id):
        """Deletes a leave entry by ID."""
        try:
            return LeaveRepository.delete_leave(leave_id=leave_id)
        except Exception as ex:
            logger.error(f"Error while deleting leave {leave_id}: {ex}", exc_info=True)
            raise ex
