import logging
from core.db_exceptions import *
from django.db import IntegrityError, DatabaseError
from django.core.exceptions import ValidationError
from core.dtos.patient_manager_dto import PatientManagerResponseDTO
from custom_admin.models.patient_manager import PatientManager
from custom_admin.models.patient import Patient
from users.models import User

logger = logging.getLogger(__name__)

class PatientManagerRepository:
    """Handles CRUD operations on the PatientManager model."""

    @staticmethod
    def create_or_update_patient_manager(validated_data):
        """Creates or updates a PatientManager record based on patient assignment."""
        try:
            patient_id = validated_data.get("patient")
            care_giver_id = validated_data.get("careGiver")

            # Fetch patient instance
            try:
                patient = Patient.objects.get(pk=patient_id)
            except Patient.DoesNotExist:
                raise NotFoundException(entity_name=f"Resident with ID {patient_id} not found")

            # Fetch care_giver instance
            try:
                care_giver = User.objects.get(pk=care_giver_id)
            except User.DoesNotExist:
                raise NotFoundException(entity_name=f"CareGiver with ID {care_giver_id} not found")
            
            # Create new manager
            new_manager = PatientManager.create_patient_manager(
                validated_data={"patient": patient, "careGiver": care_giver}
            )
            new_manager.full_clean()
            new_manager.save()
            return new_manager
        except NotFoundException as ex:
            raise ex
        except ValidationError as ex:
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while creating/updating resident manager: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to create/update resident manager.")
        except Exception as ex:
            logger.error(f"Unexpected error while creating/updating resident manager: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while creating/updating resident manager.")

    
    @staticmethod
    def get_patient_manager_by_id(manager_id):
        """Fetches a PatientManager by ID."""
        try:
            manager = PatientManager.objects.select_related("patient", "careGiver").get(pk=manager_id)
            return manager
        except PatientManager.DoesNotExist:
            raise NotFoundException(entity_name=f"PatientManager with ID: {manager_id}")
        except DatabaseError as ex:
            logger.error(f"Database error while fetching patient manager by ID: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch resident manager by ID.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching patient manager by ID: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching resident manager by ID.")

    @staticmethod
    def get_all_patient_managers(query_params):
        """Fetches PatientManager records with optional filtering."""
        try:
            field_mapping = {
                "patient": "patient__patientId",
                "careGiver": "careGiver__id",
            }

            adjusted_filters = {
                field_mapping.get(key, key): value
                for key, value in query_params.items()
                if value
            }

            managers = PatientManager.objects.select_related(
                "patient", "careGiver"
            ).filter(
                **adjusted_filters
            ).values(
                "patientManagerId",
                "patient__patientId",
                "patient__firstName",
                "patient__lastName",
                "patient__allergies",
                "patient__dateOfBirth",
                "patient__diagnosis",
                "patient__physicianName",
                "patient__pcpOrDoctor",
                "patient__branch__branchName",
                "patient__branch__facility__facilityName",
                "patient__room",
                "patient__cart",
                "careGiver__id",
                "careGiver__firstName",
                "careGiver__lastName",
                "createdAt",
                "modifiedAt"
            ).order_by("createdAt")

            # managers = paginator.paginate_queryset(queryset=managers, request=request)
            return [PatientManagerResponseDTO.transform_patient_manager(manager) for manager in managers]
        except DatabaseError as ex:
            logger.error(f"Database error while fetching patient managers: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch resident managers.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching patient managers: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching resident managers.")

    @staticmethod
    def delete_patient_manager(manager_id):
        """Deletes a PatientManager record by ID."""
        try:
            manager = PatientManagerRepository.get_patient_manager_by_id(manager_id=manager_id)
            manager.delete()
            return True
        except NotFoundException as ex:
            raise ex
        except IntegrityError as ex:
            logger.error(f"Integrity error while deleting patient manager: {ex}", exc_info=True)
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while deleting resident manager: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to delete resident manager.")
        except Exception as ex:
            logger.error(f"Unexpected error while deleting resident manager: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while deleting resident manager.")
