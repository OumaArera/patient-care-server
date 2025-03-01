from custom_admin.repositories.vitals_repo import VitalRepository
from core.dtos.vital_dto import VitalResponseDTO

class VitalService:
    """Handles the business logic for patient vitals."""

    @staticmethod
    def create_vital(data):
        """Creates a new vital entry in the database."""
        try:
            new_vital = VitalRepository.create_vital(vital_data=data)
            return VitalResponseDTO.transform_vital(vital=new_vital)
        except Exception as ex:
            raise ex

    @staticmethod
    def get_vital_by_id(vital_id):
        """Fetches details of a vital by ID."""
        try:
            vital = VitalRepository.get_vital_by_id(vital_id=vital_id)
            return VitalResponseDTO.transform_vital(vital=vital)
        except Exception as ex:
            raise ex

    @staticmethod
    def get_all_vitals(request, query_params):
        """Fetches and returns all vitals with optional filtering."""
        try:
            query_params.pop("pageSize", None)
            query_params.pop("pageNumber", None)
            vitals = VitalRepository.get_all_vitals(
                request=request, 
                query_params=query_params
            )
            return vitals
        except Exception as ex:
            raise ex

    @staticmethod
    def update_vital(vital_id, vital_data):
        """Updates an existing vital entry."""
        try:
            updated_vital = VitalRepository.update_vital(
                vital_id=vital_id, 
                vital_data=vital_data
            )
            return VitalResponseDTO.transform_vital(
                vital=updated_vital
            )
        except Exception as ex:
            raise ex

    @staticmethod
    def delete_vital(vital_id):
        """Deletes a vital entry by ID."""
        try:
            return VitalRepository.delete_vital(
                vital_id=vital_id
            )
        except Exception as ex:
            raise ex
