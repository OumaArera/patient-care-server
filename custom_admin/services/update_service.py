from custom_admin.repositories.update_repository import UpdateRepository
from core.dtos.update_dto import UpdateResponseDTO

class UpdateService:
    """Handles the business logic for patient updates."""

    @staticmethod
    def create_update(data):
        """Creates a new update entry in the database."""
        try:
            new_update = UpdateRepository.create_update(update_data=data)
            return UpdateResponseDTO.transform_update(update=new_update)
        except Exception as ex:
            raise ex

    @staticmethod
    def get_update_by_id(update_id):
        """Fetches details of an update by ID."""
        try:
            update = UpdateRepository.get_update_by_id(update_id=update_id)
            return UpdateResponseDTO.transform_update(update=update)
        except Exception as ex:
            raise ex

    @staticmethod
    def get_all_updates(request, query_params):
        """Fetches and returns all updates with optional filtering."""
        try:
            query_params.pop("pageSize", None)
            query_params.pop("pageNumber", None)
            updates = UpdateRepository.get_all_updates(
                request=request, 
                query_params=query_params
            )
            return updates
        except Exception as ex:
            raise ex

    @staticmethod
    def update_update(update_id, update_data):
        """Updates an existing update entry."""
        try:
            updated_update = UpdateRepository.update_update(
                update_id=update_id, 
                update_data=update_data
            )
            return UpdateResponseDTO.transform_update(
                update=updated_update
            )
        except Exception as ex:
            raise ex

    @staticmethod
    def delete_update(update_id):
        """Deletes an update entry by ID."""
        try:
            return UpdateRepository.delete_update(
                update_id=update_id
            )
        except Exception as ex:
            raise ex
