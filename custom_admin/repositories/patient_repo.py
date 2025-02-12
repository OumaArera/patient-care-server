import logging
from core.db_exceptions import *
from django.db import IntegrityError, DatabaseError  # type: ignore
from django.core.exceptions import ValidationError  # type: ignore
from core.dtos.patient_dto import PatientResponseDTO
from core.paginator import paginator
from custom_admin.models.patient import Patient

logger = logging.getLogger(__name__)

class PatientRepository:
    """Handles the CRUD operations on the Patient model."""

    @staticmethod
    def create_patient(patient_data):
        """Creates a new patient in the database."""
        try:
            new_patient = Patient.create_patient(validated_data=patient_data)
            new_patient.full_clean()
            new_patient.save()
            return new_patient
        except ValidationError as ex:
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while creating a new patient: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to create patient.")
        except Exception as ex:
            logger.error(f"Unexpected error while creating a new patient: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while creating patient.")

    @staticmethod
    def get_patient_by_id(patient_id):
        """Fetches details of a patient by ID."""
        try:
            patient = Patient.objects.select_related("branch").get(pk=patient_id)
            return patient
        except Patient.DoesNotExist:
            raise NotFoundException(entity_name=f"Patient with ID: {patient_id}")
        except DatabaseError as ex:
            logger.error(f"Database error while fetching patient by ID: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch patient by ID.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching patient by ID: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching patient by ID.")

    @staticmethod
    def get_all_patients(query_params):
        """Fetches and returns all patients with optional filtering."""
        try:
            field_mapping = {
                "firstName": "firstName__icontains",
                "lastName": "lastName__icontains",
                "dateOfBirth": "dateOfBirth__lte",
                "physicianName": "physicianName__icontains",
                "pcpOrDoctor": "pcpOrDoctor__icontains",
                "branch": "branch",
                "room": "room__icontains",
                "cart": "cart__icontains",
            }

            adjusted_filters = {
                field_mapping.get(key, key): value
                for key, value in query_params.items()
                if value
            }

            patients = Patient.objects.select_related(
                "branch"
            ).filter(
                **adjusted_filters
            ).values(
                "patientId", 
                "firstName", 
                "middleNames", 
                "lastName", 
                "dateOfBirth",
                "diagnosis", 
                "allergies", 
                "physicianName", 
                "pcpOrDoctor", 
                "room", 
                "cart",
                "branch__branchId", 
                "branch__branchName", 
                "createdAt"
            ).order_by(
                "createdAt"
            )
            
            # patients = paginator.paginate_queryset(queryset=patients, request=request)
            return [PatientResponseDTO.transform_patient(patient) for patient in patients]
        except DatabaseError as ex:
            logger.error(f"Database error while fetching patients: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch patients.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching patients: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching patients.")

    @staticmethod
    def update_patient(patient_id, patient_data):
        """Updates an existing patient's details."""
        try:
            patient = PatientRepository.get_patient_by_id(patient_id=patient_id)
            for field, value in patient_data.items():
                if hasattr(patient, field):  
                    setattr(patient, field, value)
            patient.full_clean()
            patient.save()
            return patient
        except ValidationError as ex:
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while updating resident: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to update resident.")
        except Exception as ex:
            logger.error(f"Unexpected error while updating resident: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while updating resident.")

    @staticmethod
    def delete_patient(patient_id):
        """Deletes a patient by ID."""
        try:
            patient = PatientRepository.get_patient_by_id(patient_id=patient_id)
            patient.delete()
            return True
        except NotFoundException as ex:
            raise ex
        except IntegrityError as ex:
            logger.error(f"Integrity error while deleting resident: {ex}", exc_info=True)
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while deleting resident: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to delete resident.")
        except Exception as ex:
            logger.error(f"Unexpected error while deleting resident: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while deleting resident.")
