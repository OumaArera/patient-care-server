from custom_admin.repositories.patient_repo import PatientRepository
from core.dtos.patient_dto import PatientResponseDTO


class PatientService:
    """Handles the business logic for patients."""

    @staticmethod
    def create_patient(data):
        """Creates a patient in the database."""
        try:
            new_patient = PatientRepository.create_patient(patient_data=data)
            return PatientResponseDTO.transform_patient(patient=new_patient)
        except Exception as ex:
            raise ex

    @staticmethod
    def get_patient_by_id(patient_id):
        """Fetches details of a patient by ID."""
        try:
            patient = PatientRepository.get_patient_by_id(patient_id=patient_id)
            return PatientResponseDTO.transform_patient(patient=patient)
        except Exception as ex:
            raise ex

    @staticmethod
    def get_all_patients(request, query_params):
        """Fetches and returns all patients."""
        try:
            query_params.pop("pageSize", None)
            query_params.pop("pageNumber", None)
            patients = PatientRepository.get_all_patients(
                request=request, query_params=query_params
            )
            return patients
        except Exception as ex:
            raise ex

    @staticmethod
    def update_patient(patient_id, patient_data):
        """Updates an existing patient."""
        try:
            updated_patient = PatientRepository.update_patient(
                patient_id=patient_id, patient_data=patient_data
            )
            return PatientResponseDTO.transform_patient(patient=updated_patient)
        except Exception as ex:
            raise ex

    @staticmethod
    def delete_patient(patient_id):
        """Deletes a patient by ID."""
        try:
            return PatientRepository.delete_patient(patient_id=patient_id)
        except Exception as ex:
            raise ex
