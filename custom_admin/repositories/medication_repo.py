import logging
from core.db_exceptions import *
from django.db import IntegrityError, DatabaseError  # type: ignore
from django.core.exceptions import ValidationError  # type: ignore
from core.dtos.medication_dto import MedicationResponseDTO
from core.paginator import paginator
from custom_admin.models.medication import Medication

logger = logging.getLogger(__name__)

class MedicationRepository:
    """Handles CRUD operations on the Medication model."""

    @staticmethod
    def create_medication(medication_data):
        """Creates a medication entry in the database."""
        try:
            new_medication = Medication.create_medication(validated_data=medication_data)
            new_medication.full_clean()
            new_medication.save()
            return new_medication
        except ValidationError as ex:
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while creating a new medication: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to create medication.")
        except Exception as ex:
            logger.error(f"Unexpected error while creating a new medication: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while creating medication.")

    @staticmethod
    def get_medication_by_id(medication_id):
        """Fetches details of a medication by ID."""
        try:
            medication = Medication.objects.get(pk=medication_id)
            return medication
        except Medication.DoesNotExist:
            raise NotFoundException(entity_name=f"Medication with ID: {medication_id}")
        except DatabaseError as ex:
            logger.error(f"Database error while fetching medication by ID: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch medication by ID.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching medication by ID: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching medication by ID.")

    @staticmethod
    def get_all_medications(query_params):
        """Fetches and returns all medications with optional filtering."""
        try:
            field_mapping = {
                "medicationName": "medicationName__icontains",
                "medicationCode": "medicationCode__icontains",
                "status": "status",
                "patient": "patient",
            }

            adjusted_filters = {
                field_mapping.get(key, key): value
                for key, value in query_params.items()
                if value
            }

            medications = Medication.objects.select_related(
                "patient"
            ).filter(**adjusted_filters).values(
                "medicationId", "medicationName", "medicationCode", "equivalentTo",
                "instructions", "quantity", "diagnosis", "medicationTime",
                "patient__patientId", "createdAt", "modifiedAt", "patient__firstName",
                "patient__lastName",
            ).order_by("createdAt")

            # medications = paginator.paginate_queryset(queryset=medications, request=request)
            return [MedicationResponseDTO.transform_medication(medication) for medication in medications]
        except DatabaseError as ex:
            logger.error(f"Database error while fetching medications: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch medications.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching medications: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching medications.")

    @staticmethod
    def update_medication(medication_id, medication_data):
        """Updates the details of an existing medication."""
        try:
            medication = MedicationRepository.get_medication_by_id(medication_id=medication_id)
            for field, value in medication_data.items():
                if hasattr(medication, field):
                    setattr(medication, field, value)
            medication.full_clean()
            medication.save()
            return medication
        except NotFoundException as ex:
            raise ex
        except ValidationError as ex:
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while updating medication: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to update medication.")
        except Exception as ex:
            logger.error(f"Unexpected error while updating medication: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while updating medication.")

    @staticmethod
    def delete_medication(medication_id):
        """Deletes a medication record by ID."""
        try:
            medication = MedicationRepository.get_medication_by_id(medication_id=medication_id)
            medication.delete()
            return True
        except NotFoundException as ex:
            raise ex
        except IntegrityError as ex:
            logger.error(f"Integrity error while deleting medication: {ex}", exc_info=True)
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while deleting medication: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to delete medication.")
        except Exception as ex:
            logger.error(f"Unexpected error while deleting medication: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while deleting medication.")
