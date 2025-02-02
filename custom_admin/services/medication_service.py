from custom_admin.repositories.medication_repo import MedicationRepository
from core.dtos.medication_dto import MedicationResponseDTO


class MedicationService:
    """Handles the business logic for medications."""

    @staticmethod
    def create_medication(data):
        """Creates a medication entry in the database."""
        try:
            new_medication = MedicationRepository.create_medication(medication_data=data)
            return MedicationResponseDTO.transform_medication(medication=new_medication)
        except Exception as ex:
            raise ex

    @staticmethod
    def get_medication_by_id(medication_id):
        """Fetches details of a medication by ID."""
        try:
            medication = MedicationRepository.get_medication_by_id(medication_id=medication_id)
            return MedicationResponseDTO.transform_medication(medication=medication)
        except Exception as ex:
            raise ex

    @staticmethod
    def get_all_medications(request, query_params):
        """Fetches and returns all medications."""
        try:
            query_params.pop("pageSize", None)
            query_params.pop("pageNumber", None)
            medications = MedicationRepository.get_all_medications(
                request=request,
                query_params=query_params
            )
            return medications
        except Exception as ex:
            raise ex

    @staticmethod
    def update_medication(medication_id, medication_data):
        """Updates an existing medication."""
        try:
            updated_medication = MedicationRepository.update_medication(
                medication_id=medication_id,
                medication_data=medication_data
            )
            return MedicationResponseDTO.transform_medication(medication=updated_medication)
        except Exception as ex:
            raise ex

    @staticmethod
    def delete_medication(medication_id):
        """Deletes a medication by ID."""
        try:
            return MedicationRepository.delete_medication(medication_id=medication_id)
        except Exception as ex:
            raise ex
