import logging
from core.db_exceptions import *
from django.db import IntegrityError, DatabaseError # type: ignore
from django.core.exceptions import ValidationError # type: ignore
from core.dtos.medication_admin_dto import MedicationAdministrationResponseDTO
from core.paginator import paginator
from custom_admin.models.medical_administration import MedicationAdministration

logger = logging.getLogger(__name__)

class MedicationAdministrationRepository:
    """Handles CRUD operations on the MedicationAdministration model."""

    @staticmethod
    def create_medication_administration(administration_data):
        """Creates a medication administration entry in the database."""
        try:
            new_admin = MedicationAdministration.create_administration_medication(validated_data=administration_data)
            new_admin.full_clean()
            new_admin.save()
            return new_admin
        except ValidationError as ex:
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while creating medication administration: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to create medication administration.")
        except Exception as ex:
            logger.error(f"Unexpected error while creating medication administration: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while creating medication administration.")

    @staticmethod
    def get_medication_administration_by_id(administration_id):
        """Fetches details of a medication administration by ID."""
        try:
            administration = MedicationAdministration.objects.get(pk=administration_id)
            return administration
        except MedicationAdministration.DoesNotExist:
            raise NotFoundException(entity_name=f"Medication Administration with ID: {administration_id}")
        except DatabaseError as ex:
            logger.error(f"Database error while fetching medication administration by ID: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch medication administration by ID.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching medication administration by ID: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching medication administration by ID.")

    @staticmethod
    def get_all_medication_administrations(request, query_params):
        """Fetches and returns all medication administrations with optional filtering."""
        try:
            field_mapping = {
                "medication": "medication__medicationId",
                "patient": "patient__patientId",
                "careGiver": "careGiver__id",
                "status": "status__icontains"
            }

            adjusted_filters = {
                field_mapping.get(key, key): value
                for key, value in query_params.items()
                if value
            }

            administrations = MedicationAdministration.objects.select_related(
                "patient", "medication", "careGiver"
            ).filter(
                **adjusted_filters
            ).values(
                "medicationAdministrationId",
                "patient__patientId", 
                "patient__firstName",
                "patient__lastName",
                "patient__branch__branchName",
                "patient__branch__facility__facilityName",
                "medication__medicationId",
                "careGiver", 
                "careGiver__firstName",
                "careGiver__lastName",
                "status",
                "reasonNotFiled",
                "timeAdministered", 
                "createdAt", 
                "modifiedAt"
            ).order_by("createdAt")

            administrations = paginator.paginate_queryset(queryset=administrations, request=request)
            return [MedicationAdministrationResponseDTO.transform_medication_administration(admin) for admin in administrations]
        except DatabaseError as ex:
            logger.error(f"Database error while fetching medication administrations: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch medication administrations.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching medication administrations: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching medication administrations.")

    @staticmethod
    def update_medication_administration(administration_id, administration_data):
        """Updates an existing medication administration record."""
        try:
            administration = MedicationAdministrationRepository.get_medication_administration_by_id(
                administration_id=administration_id
            )
            for field, value in administration_data.items():
                if hasattr(administration, field):
                    setattr(administration, field, value)
            administration.full_clean()
            administration.save()
            return administration
        except ValidationError as ex:
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while updating medication administration: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to update medication administration.")
        except Exception as ex:
            logger.error(f"Unexpected error while updating medication administration: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while updating medication administration.")

    @staticmethod
    def delete_medication_administration(administration_id):
        """Deletes a medication administration record by ID."""
        try:
            administration = MedicationAdministrationRepository.get_medication_administration_by_id(
                administration_id=administration_id
            )
            administration.delete()
            return True
        except NotFoundException as ex:
            raise ex
        except IntegrityError as ex:
            logger.error(f"Integrity error while deleting medication administration: {ex}", exc_info=True)
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while deleting medication administration: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to delete medication administration.")
        except Exception as ex:
            logger.error(f"Unexpected error while deleting medication administration: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while deleting medication administration.")
