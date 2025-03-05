import logging
from django.db import IntegrityError, DatabaseError  # type: ignore
from django.core.exceptions import ValidationError  # type: ignore
from core.db_exceptions import *
from core.paginator import paginator
from core.dtos.vital_dto import VitalResponseDTO  # Import the DTO
from custom_admin.models.vitals import Vital

logger = logging.getLogger(__name__)

class VitalRepository:
    """Handles CRUD operations on the Vital model."""

    @staticmethod
    def create_vital(vital_data):
        """Creates a new vital entry in the database."""
        try:
            new_vital = Vital.create_vital(validated_data=vital_data)
            new_vital.full_clean()
            new_vital.save()
            return new_vital
        except ValidationError as ex:
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while creating a new vital: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to create vital.")
        except Exception as ex:
            logger.error(f"Unexpected error while creating a new vital: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while creating vital.")

    @staticmethod
    def get_vital_by_id(vital_id):
        """Fetches details of a vital by ID."""
        try:
            vital = Vital.objects.get(pk=vital_id)
            return vital
        except Vital.DoesNotExist:
            raise NotFoundException(entity_name=f"Vital with ID: {vital_id}")
        except DatabaseError as ex:
            logger.error(f"Database error while fetching vital by ID: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch vital by ID.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching vital by ID: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching vital by ID.")

    @staticmethod
    def get_all_vitals(request, query_params):
        """Fetches and returns all vitals with optional filtering."""
        try:
            field_mapping = {
                "patient": "patient_id",
                "dateTaken": "dateTaken",
                "bloodPressure": "bloodPressure__icontains",
                "temperature": "temperature",
                "pulse": "pulse",
                "oxygenSaturation": "oxygenSaturation"
            }

            adjusted_filters = {
                field_mapping.get(key, key): value
                for key, value in query_params.items()
                if value
            }

            vitals = Vital.objects.select_related("patient").filter(
                **adjusted_filters
            ).values(
                "vitalId",
                "bloodPressure",
                "temperature",
                "pulse",
                "oxygenSaturation",
                "pain",
                "dateTaken",
                "createdAt",
                "modifiedAt",
                "patient__patientId",
                "patient__firstName",
                "patient__lastName"
            ).order_by("dateTaken")

            # vitals = paginator.paginate_queryset(queryset=vitals, request=request)
            return [VitalResponseDTO.transform_vital(vital) for vital in vitals]
        except DatabaseError as ex:
            logger.error(f"Database error while fetching vitals: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch vitals.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching vitals: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching vitals.")

    @staticmethod
    def update_vital(vital_id, vital_data):
        """Updates the details of an existing vital."""
        try:
            vital = VitalRepository.get_vital_by_id(vital_id=vital_id)
            for field, value in vital_data.items():
                if hasattr(vital, field):
                    setattr(vital, field, value)
            vital.full_clean()
            vital.save()
            return vital
        except NotFoundException as ex:
            raise ex
        except ValidationError as ex:
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while updating vital: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to update vital.")
        except Exception as ex:
            logger.error(f"Unexpected error while updating vital: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while updating vital.")

    @staticmethod
    def delete_vital(vital_id):
        """Deletes a vital record by ID."""
        try:
            vital = VitalRepository.get_vital_by_id(vital_id=vital_id)
            vital.delete()
            return True
        except NotFoundException as ex:
            raise ex
        except IntegrityError as ex:
            logger.error(f"Integrity error while deleting vital: {ex}", exc_info=True)
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while deleting vital: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to delete vital.")
        except Exception as ex:
            logger.error(f"Unexpected error while deleting vital: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while deleting vital.")
