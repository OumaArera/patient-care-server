import logging
from datetime import timedelta, date
from django.db import IntegrityError, DatabaseError
from django.core.exceptions import ValidationError
from django.db import models
from core.db_exceptions import *
from core.dtos.assessment_dto import AssessmentResponseDTO
from core.utils.scheduling import schedule_email_notifications
from custom_admin.models.assessment import Assessment

logger = logging.getLogger(__name__)

class AssessmentRepository:
    """Handles CRUD operations for the Assessment model."""

    @staticmethod
    def create_assessment(assessment_data):
        """Creates a new assessment entry in the database."""
        try:
            new_assessment = Assessment.create_assessment(validated_data=assessment_data)
            new_assessment.full_clean()
            new_assessment.save()
            return new_assessment
        except ValidationError as ex:
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while creating a new assessment: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to create assessment.")
        except Exception as ex:
            logger.error(f"Unexpected error while creating a new assessment: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while creating assessment.")

    @staticmethod
    def get_assessment_by_id(assessment_id):
        """Fetches details of an assessment by ID."""
        try:
            assessment = Assessment.objects.get(pk=assessment_id)
            return assessment
        except Assessment.DoesNotExist:
            raise NotFoundException(entity_name=f"Assessment with ID: {assessment_id}")
        except DatabaseError as ex:
            logger.error(f"Database error while fetching assessment by ID: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch assessment by ID.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching assessment by ID: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching assessment by ID.")

    @staticmethod
    def get_due_assessments():
        """Fetches assessments due in the next 10 days."""
        try:
            today = date.today()
            due_date = today + timedelta(days=10)

            assessments = Assessment.objects.filter(
                models.Q(assessmentNextDate__gte=today, assessmentNextDate__lte=due_date) |
                models.Q(NCPNextDate__gte=today, NCPNextDate__lte=due_date)
            ).values(
                "assessmentId", "resident__patientId", "resident__firstName",
                "resident__lastName", "assessmentStartDate", "assessmentNextDate",
                "NCPStartDate", "NCPNextDate", "socialWorker", "createdAt", "modifiedAt"
            ).order_by("assessmentNextDate")

            return [AssessmentResponseDTO.transform_assessment(assessment) for assessment in assessments]
        
        except DatabaseError as ex:
            logger.error(f"Database error while fetching due assessments: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch due assessments.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching due assessments: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching due assessments.")

    @staticmethod
    def update_assessment(assessment_id, assessment_data):
        """Updates the details of an existing assessment."""
        try:
            assessment = AssessmentRepository.get_assessment_by_id(assessment_id=assessment_id)
            for field, value in assessment_data.items():
                if hasattr(assessment, field):
                    setattr(assessment, field, value)
            assessment.full_clean()
            assessment.save()
            return assessment
        except NotFoundException as ex:
            raise ex
        except ValidationError as ex:
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while updating assessment: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to update assessment.")
        except Exception as ex:
            logger.error(f"Unexpected error while updating assessment: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while updating assessment.")

    @staticmethod
    def delete_assessment(assessment_id):
        """Deletes an assessment record by ID."""
        try:
            assessment = AssessmentRepository.get_assessment_by_id(assessment_id=assessment_id)
            assessment.delete()
            return True
        except NotFoundException as ex:
            raise ex
        except IntegrityError as ex:
            logger.error(f"Integrity error while deleting assessment: {ex}", exc_info=True)
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while deleting assessment: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to delete assessment.")
        except Exception as ex:
            logger.error(f"Unexpected error while deleting assessment: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while deleting assessment.")

    @staticmethod
    def schedule_assessment_notifications():
        """Triggers scheduled email notifications for assessments."""
        schedule_email_notifications()
