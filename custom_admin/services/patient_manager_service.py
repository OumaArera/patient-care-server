from custom_admin.repositories.patient_manager_repo import PatientManagerRepository
from core.dtos.patient_manager_dto import PatientManagerResponseDTO

class PatientManagerService:
    """Handles the business logic for patient managers."""

    @staticmethod
    def create_or_update_patient_manager(data):
        """Creates or updates a patient manager record."""
        try:
            manager = PatientManagerRepository.\
                create_or_update_patient_manager(
                    validated_data=data
                )
            return PatientManagerResponseDTO.\
                transform_patient_manager(
                    manager=manager
                )
        except Exception as ex:
            raise ex

    @staticmethod
    def get_patient_manager_by_id(manager_id):
        """Fetches a patient manager by ID."""
        try:
            manager = PatientManagerRepository.\
                get_patient_manager_by_id(
                    manager_id=manager_id
                )
            return PatientManagerResponseDTO.\
                transform_patient_manager(
                    manager=manager
                )
        except Exception as ex:
            raise ex

    @staticmethod
    def get_all_patient_managers(request, query_params):
        """Fetches and returns all patient managers with optional filtering."""
        try:
            query_params.pop("pageSize", None)
            query_params.pop("pageNumber", None)
            managers = PatientManagerRepository.\
                get_all_patient_managers(
                    request=request, 
                    query_params=query_params
                )
            return managers
        except Exception as ex:
            raise ex

    @staticmethod
    def delete_patient_manager(manager_id):
        """Deletes a patient manager by ID."""
        try:
            return PatientManagerRepository.\
                delete_patient_manager(
                    manager_id=manager_id
                )
        except Exception as ex:
            raise ex
