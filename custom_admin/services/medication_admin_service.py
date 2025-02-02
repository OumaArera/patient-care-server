from custom_admin.repositories.medication_admin_repo import *
from core.dtos.medication_admin_dto import *

class MedicationAdministrationService:
    """Handles the business logic for medication administrations."""

    @staticmethod
    def create_medication_administration(data):
        """Creates a medication administration entry in the database."""
        try:
            new_administration =\
                MedicationAdministrationRepository.\
                    create_medication_administration(
                    administration_data=data
            )
            return MedicationAdministrationResponseDTO.\
                transform_medication_administration(
                    data=new_administration
            )
        except Exception as ex:
            raise ex

    @staticmethod
    def get_medication_administration_by_id(administration_id):
        """Fetches details of a medication administration by ID."""
        try:
            administration =\
                MedicationAdministrationRepository.\
                    get_medication_administration_by_id(
                    administration_id=administration_id
            )
            return MedicationAdministrationResponseDTO.\
                transform_medication_administration(
                    data=administration
                )
        except Exception as ex:
            raise ex

    @staticmethod
    def get_all_medications_administrations(request, query_params):
        """Fetches and returns all medication administrations with optional filtering."""
        try:
            query_params.pop("pageSize", None)
            query_params.pop("pageNumber", None)
            administrations =\
                MedicationAdministrationRepository.\
                get_all_medication_administrations(
                request=request,
                query_params=query_params
            )
            return administrations
        except Exception as ex:
            raise ex

    @staticmethod
    def update_medication_administration(administration_id, administration_data):
        """Updates an existing medication administration."""
        try:
            updated_administration =\
                MedicationAdministrationRepository.\
                update_medication_administration(
                administration_id=administration_id,
                administration_data=administration_data
            )
            return MedicationAdministrationResponseDTO.\
                transform_medication_administration(
                    data=updated_administration
                )
        except Exception as ex:
            raise ex

    @staticmethod
    def delete_medication_administration(administration_id):
        """Deletes a medication administration by ID."""
        try:
            return MedicationAdministrationRepository.\
                delete_medication_administration(
                    administration_id=administration_id
                )
        except Exception as ex:
            raise ex
