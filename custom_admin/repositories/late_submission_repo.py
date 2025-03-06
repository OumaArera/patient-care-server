import logging
from django.db import IntegrityError, DatabaseError  # type: ignore
from django.core.exceptions import ValidationError  # type: ignore
from core.db_exceptions import *
from core.dtos.late_submission_dto import LateSubmissionResponseDTO
from core.paginator import paginator
from custom_admin.models.late_submission import LateSubmission

logger = logging.getLogger(__name__)

class LateSubmissionRepository:
    """Handles CRUD operations on the LateSubmission model."""

    @staticmethod
    def create_late_submission(submission_data):
        """Creates a new late submission entry in the database."""
        try:
            new_submission = LateSubmission.create_late_submission(validated_data=submission_data)
            new_submission.full_clean()
            new_submission.save()
            return new_submission
        except ValidationError as ex:
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while creating a new late submission: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to create late submission.")
        except Exception as ex:
            logger.error(f"Unexpected error while creating a new late submission: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while creating late submission.")

    @staticmethod
    def get_late_submission_by_id(submission_id):
        """Fetches details of a late submission by ID."""
        try:
            submission = LateSubmission.objects.get(pk=submission_id)
            return submission
        except LateSubmission.DoesNotExist:
            raise NotFoundException(entity_name=f"LateSubmission with ID: {submission_id}")
        except DatabaseError as ex:
            logger.error(f"Database error while fetching late submission by ID: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch late submission by ID.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching late submission by ID: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching late submission by ID.")

    @staticmethod
    def get_all_late_submissions(request, query_params):
        """Fetches and returns all late submissions with optional filtering."""
        try:
            field_mapping = {
                "patient": "patient_id",
                "manager": "manager_id",
                "careGiver": "careGiver_id",
                "type": "type",
                "start": "start",
                "duration": "duration"
            }

            adjusted_filters = {
                field_mapping.get(key, key): value
                for key, value in query_params.items()
                if value
            }

            submissions = LateSubmission.objects.select_related(
                "patient", "manager", "careGiver"
            ).filter(
                **adjusted_filters
            ).values(
                "lateSubmissionId",
                "type",
                "start",
                "duration",
                "reasonForLateSubmission",
                "createdAt",
                "modifiedAt",
                "patient__patientId",
                "patient__firstName",
                "patient__lastName",
                "manager__id",
                "manager__first_name",
                "manager__last_name",
                "careGiver__id",
                "careGiver__first_name",
                "careGiver__last_name"
            ).order_by("start")
            return [LateSubmissionResponseDTO.transform_late_submission(submission)\
                for submission in submissions]
        except DatabaseError as ex:
            logger.error(f"Database error while fetching late submissions: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch late submissions.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching late submissions: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching late submissions.")

    @staticmethod
    def update_late_submission(submission_id, submission_data):
        """Updates the details of an existing late submission."""
        try:
            submission = LateSubmissionRepository.get_late_submission_by_id(submission_id=submission_id)
            for field, value in submission_data.items():
                if hasattr(submission, field):
                    setattr(submission, field, value)
            submission.full_clean()
            submission.save()
            return submission
        except NotFoundException as ex:
            raise ex
        except ValidationError as ex:
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while updating late submission: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to update late submission.")
        except Exception as ex:
            logger.error(f"Unexpected error while updating late submission: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while updating late submission.")

    @staticmethod
    def delete_late_submission(submission_id):
        """Deletes a late submission record by ID."""
        try:
            submission = LateSubmissionRepository.get_late_submission_by_id(submission_id=submission_id)
            submission.delete()
            return True
        except NotFoundException as ex:
            raise ex
        except IntegrityError as ex:
            logger.error(f"Integrity error while deleting late submission: {ex}", exc_info=True)
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while deleting late submission: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to delete late submission.")
        except Exception as ex:
            logger.error(f"Unexpected error while deleting late submission: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while deleting late submission.")
