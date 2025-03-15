import logging
from custom_admin.repositories.utility_repo import UtilityRepository
from core.dtos.utility_dto import UtilityResponseDTO

logger = logging.getLogger(__name__)

class UtilityService:
    """Handles the business logic for utility management."""

    @staticmethod
    def create_utility(data):
        """Creates a new utility entry in the database."""
        try:
            new_utility = UtilityRepository.create_utility(utility_data=data)
            return UtilityResponseDTO.transform_utility(utility=new_utility)
        except Exception as ex:
            logger.error(f"Error while creating utility: {ex}", exc_info=True)
            raise ex

    @staticmethod
    def get_utility_by_id(utility_id):
        """Fetches details of a utility by ID."""
        try:
            utility = UtilityRepository.get_utility_by_id(utility_id=utility_id)
            return UtilityResponseDTO.transform_utility(utility=utility)
        except Exception as ex:
            logger.error(f"Error while fetching utility by ID {utility_id}: {ex}", exc_info=True)
            raise ex

    @staticmethod
    def get_all_utilities(query_params):
        """Fetches and returns all utilities with optional filtering."""
        try:
            return UtilityRepository.get_all_utilities(query_params=query_params)
        except Exception as ex:
            logger.error(f"Error while fetching all utilities: {ex}", exc_info=True)
            raise ex

    @staticmethod
    def update_utility(utility_id, utility_data):
        """Updates an existing utility entry."""
        try:
            updated_utility = UtilityRepository.update_utility(utility_id=utility_id, utility_data=utility_data)
            return UtilityResponseDTO.transform_utility(utility=updated_utility)
        except Exception as ex:
            logger.error(f"Error while updating utility {utility_id}: {ex}", exc_info=True)
            raise ex

    @staticmethod
    def delete_utility(utility_id):
        """Deletes a utility entry by ID."""
        try:
            return UtilityRepository.delete_utility(utility_id=utility_id)
        except Exception as ex:
            logger.error(f"Error while deleting utility {utility_id}: {ex}", exc_info=True)
            raise ex
