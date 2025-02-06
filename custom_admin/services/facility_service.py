from custom_admin.repositories.facility_repo import FacilityRepository
from core.dtos.facility_dto import FacilityResponseDTO


class FacilityService:
    """Handles the business logic for facilities."""

    @staticmethod
    def create_facility(data):
        """Creates a facility in the database."""
        try:
            new_facility = FacilityRepository.create_facility(facility_data=data)
            return FacilityResponseDTO.transform_facility(facility=new_facility)
        except Exception as ex:
            raise ex

    @staticmethod
    def get_facility_by_id(facility_id):
        """Fetches details of a facility by ID."""
        try:
            facility = FacilityRepository.get_facility_by_id(facility_id=facility_id)
            return FacilityResponseDTO.transform_facility(facility=facility)
        except Exception as ex:
            raise ex

    @staticmethod
    def get_all_facilities(query_params):
        """Fetches and returns all facilities."""
        try:
            query_params.pop("pageSize", None)
            query_params.pop("pageNumber", None)
            facilities = FacilityRepository.get_all_facilities(
                query_params=query_params
            )
            return facilities
        except Exception as ex:
            raise ex

    @staticmethod
    def update_facility(facility_id, facility_data):
        """Updates an existing facility."""
        try:
            updated_facility = FacilityRepository.update_facility(
                facility_id=facility_id, 
                facility_data=facility_data
            )
            return FacilityResponseDTO.transform_facility(facility=updated_facility)
        except Exception as ex:
            raise ex

    @staticmethod
    def delete_facility(facility_id):
        """Deletes a facility by ID."""
        try:
            return FacilityRepository.delete_facility(facility_id=facility_id)
        except Exception as ex:
            raise ex
