import logging
from core.db_exceptions import *
from django.db import IntegrityError, DatabaseError  # type: ignore
from django.core.exceptions import ValidationError  # type: ignore
from core.paginator import paginator
from core.dtos.facility_dto import FacilityResponseDTO  # Assuming a DTO exists
from custom_admin.models.facility import Facility

logger = logging.getLogger(__name__)

class FacilityRepository:
    """Handles the CRUD operations on the Facility model."""

    @staticmethod
    def create_facility(facility_data):
        """Creates a facility in the database."""
        try:
            new_facility = Facility.create_facility(validated_data=facility_data)
            new_facility.full_clean()
            new_facility.save()
            return new_facility
        except ValidationError as ex:
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while creating a new facility: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to create facility.")
        except Exception as ex:
            logger.error(f"Unexpected error while creating a new facility: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while creating facility.")

    @staticmethod
    def get_facility_by_id(facility_id):
        """Fetches details of a facility by ID."""
        try:
            facility = Facility.objects.get(pk=facility_id)
            return facility
        except Facility.DoesNotExist:
            raise NotFoundException(entity_name=f"Facility with ID: {facility_id}")
        except DatabaseError as ex:
            logger.error(f"Database error while fetching facility by ID: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch facility by ID.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching facility by ID: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching facility by ID.")

    @staticmethod
    def get_all_facilities(query_params):
        """Fetches and returns all the facilities with optional filtering."""
        try:
            field_mapping = {
                "facilityName": "facilityName__icontains",
                "facilityAddress": "facilityAddress__icontains",
            }

            adjusted_filters = {
                field_mapping.get(key, key): value
                for key, value in query_params.items()
                if value
            }

            facilities = Facility.objects.filter(**adjusted_filters).values(
                "facilityId", "facilityName", "facilityAddress", "createdAt"
            ).order_by("createdAt")
            
            # facilities = paginator.paginate_queryset(queryset=facilities, request=request)
            return [FacilityResponseDTO.transform_facility(facility) for facility in facilities]
        except DatabaseError as ex:
            logger.error(f"Database error while fetching facilities: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch facilities.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching facilities: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching facilities.")

    @staticmethod
    def update_facility(facility_id, facility_data):
        """Updates the details of an existing facility."""
        try:
            facility = FacilityRepository.get_facility_by_id(facility_id=facility_id)
            for field, value in facility_data.items():
                if hasattr(facility, field):  
                    setattr(facility, field, value)
            facility.clean_fields()
            facility.save()
            return facility
        except ValidationError as ex:
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while updating facility: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to update facility.")
        except Exception as ex:
            logger.error(f"Unexpected error while updating facility: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while updating facility.")

    @staticmethod
    def delete_facility(facility_id):
        """Deletes a facility record by ID."""
        try:
            facility = FacilityRepository.get_facility_by_id(facility_id=facility_id)
            facility.delete()
            return True
        except NotFoundException as ex:
            raise ex
        except IntegrityError as ex:
            logger.error(f"Integrity error while deleting facility: {ex}", exc_info=True)
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while deleting facility: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to delete facility.")
        except Exception as ex:
            logger.error(f"Unexpected error while deleting facility: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while deleting facility.")
