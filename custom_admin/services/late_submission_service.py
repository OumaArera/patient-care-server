from custom_admin.repositories.late_submission_repo import LateSubmissionRepository
from core.dtos.late_submission_dto import LateSubmissionResponseDTO

class LateSubmissionService:
    """Handles the business logic for late submissions."""

    @staticmethod
    def create_late_submission(data):
        """Creates a new late submission entry in the database."""
        try:
            new_submission = LateSubmissionRepository.create_late_submission(submission_data=data)
            return LateSubmissionResponseDTO.transform_late_submission(late_submission=new_submission)
        except Exception as ex:
            raise ex

    @staticmethod
    def get_late_submission_by_id(submission_id):
        """Fetches details of a late submission by ID."""
        try:
            submission = LateSubmissionRepository.get_late_submission_by_id(submission_id=submission_id)
            return LateSubmissionResponseDTO.transform_late_submission(late_submission=submission)
        except Exception as ex:
            raise ex

    @staticmethod
    def get_all_late_submissions(request, query_params):
        """Fetches and returns all late submissions with optional filtering."""
        try:
            query_params.pop("pageSize", None)
            query_params.pop("pageNumber", None)
            submissions = LateSubmissionRepository.get_all_late_submissions(
                request=request, query_params=query_params
            )
            return submissions
        except Exception as ex:
            raise ex

    @staticmethod
    def update_late_submission(submission_id, submission_data):
        """Updates an existing late submission entry."""
        try:
            updated_submission = LateSubmissionRepository.update_late_submission(
                submission_id=submission_id, submission_data=submission_data
            )
            return LateSubmissionResponseDTO.transform_late_submission(
                late_submission=updated_submission
            )
        except Exception as ex:
            raise ex

    @staticmethod
    def delete_late_submission(submission_id):
        """Deletes a late submission entry by ID."""
        try:
            return LateSubmissionRepository.delete_late_submission(
                submission_id=submission_id
            )
        except Exception as ex:
            raise ex