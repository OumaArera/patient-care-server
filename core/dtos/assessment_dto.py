from typing import Union
from core.utils.format_null_values import format_value

class AssessmentResponseDTO:
    """DTO for transforming Assessment model responses."""

    @staticmethod
    def transform_assessment(assessment: Union[dict, object]) -> dict:
        """Converts an Assessment model instance or dictionary into a structured response."""

        if isinstance(assessment, dict):
            return {
                "assessmentId": assessment.get("assessmentId"),
                "residentId": assessment.get("resident__patientId"),
                "residentName": format_value(
                    assessment.get("resident__firstName"),
                    assessment.get("resident__lastName")
                ),
                "assessmentStartDate": assessment.get("assessmentStartDate"),
                "assessmentNextDate": assessment.get("assessmentNextDate"),
                "NCPStartDate": assessment.get("NCPStartDate"),
                "NCPNextDate": assessment.get("NCPNextDate"),
                "socialWorker": assessment.get("socialWorker"),
                "createdAt": assessment.get("createdAt"),
                "modifiedAt": assessment.get("modifiedAt"),
            }

        # Handling model instance
        return {
            "assessmentId": assessment.assessmentId,
            "residentId": assessment.resident.patientId if assessment.resident else None,
            "residentName": format_value(
                assessment.resident.firstName if assessment.resident else None,
                assessment.resident.lastName if assessment.resident else None
            ),
            "assessmentStartDate": assessment.assessmentStartDate,
            "assessmentNextDate": assessment.assessmentNextDate,
            "NCPStartDate": assessment.NCPStartDate,
            "NCPNextDate": assessment.NCPNextDate,
            "socialWorker": assessment.socialWorker,
            "createdAt": assessment.createdAt.strftime("%Y-%m-%d %H:%M:%S"),
            "modifiedAt": assessment.modifiedAt.strftime("%Y-%m-%d %H:%M:%S"),
        }
