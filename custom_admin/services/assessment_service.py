from custom_admin.repositories.assessment_repo import AssessmentRepository
from core.dtos.assessment_dto import AssessmentResponseDTO

class AssessmentService:
    """Handles the business logic for assessments."""

    @staticmethod
    def create_assessment(data):
        """Creates a new assessment entry in the database."""
        try:
            new_assessment = AssessmentRepository.create_assessment(assessment_data=data)
            return AssessmentResponseDTO.transform_assessment(assessment=new_assessment)
        except Exception as ex:
            raise ex

    @staticmethod
    def get_assessment_by_id(assessment_id):
        """Fetches details of an assessment by ID."""
        try:
            assessment = AssessmentRepository.get_assessment_by_id(assessment_id=assessment_id)
            return AssessmentResponseDTO.transform_assessment(assessment=assessment)
        except Exception as ex:
            raise ex

    @staticmethod
    def get_due_assessments():
        """Fetches assessments that are due in the next 20 days."""
        try:
            assessments = AssessmentRepository.get_due_assessments()
            return assessments
        except Exception as ex:
            raise ex

    @staticmethod
    def update_assessment(assessment_id, assessment_data):
        """Updates an existing assessment entry."""
        try:
            updated_assessment = AssessmentRepository.update_assessment(
                assessment_id=assessment_id,
                assessment_data=assessment_data
            )
            return AssessmentResponseDTO.transform_assessment(assessment=updated_assessment)
        except Exception as ex:
            raise ex

    @staticmethod
    def delete_assessment(assessment_id):
        """Deletes an assessment entry by ID."""
        try:
            return AssessmentRepository.delete_assessment(assessment_id=assessment_id)
        except Exception as ex:
            raise ex

    @staticmethod
    def schedule_assessment_notifications():
        """Triggers scheduled email notifications for assessments."""
        try:
            AssessmentRepository.schedule_assessment_notifications()
        except Exception as ex:
            raise ex
