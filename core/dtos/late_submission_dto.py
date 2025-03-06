from datetime import datetime
from typing import Union

from core.utils.format_null_values import format_value

class LateSubmissionResponseDTO:
    """DTO for transforming LateSubmission model responses."""

    @staticmethod
    def transform_late_submission(late_submission: Union[dict, object]) -> dict:
        """Converts a LateSubmission model instance or dictionary into a structured response."""

        if isinstance(late_submission, dict):
            return {
                "lateSubmissionId": late_submission.get("lateSubmissionId"),
                "patientId": late_submission.get("patient__patientId"),
                "patientName": format_value(
                    late_submission.get("patient__firstName"),
                    late_submission.get("patient__lastName")
                ),
                "managerId": late_submission.get("manager__id"),
                "careGiverId": late_submission.get("careGiver__id"),
                "type": late_submission.get("type"),
                "start": late_submission.get("start"),
                "duration": late_submission.get("duration"),
                "reasonForLateSubmission": late_submission.get("reasonForLateSubmission"),
                "createdAt": late_submission.get("createdAt"),
                "modifiedAt": late_submission.get("modifiedAt"),
            }

        # Handling model instance
        return {
            "lateSubmissionId": late_submission.lateSubmissionId,
            "patientId": late_submission.patient.patientId if late_submission.patient else None,
            "patientName": format_value(
                late_submission.patient.firstName if late_submission.patient else None,
                late_submission.patient.lastName if late_submission.patient else None
            ),
            "managerId": late_submission.manager.id if late_submission.manager else None,
            "careGiverId": late_submission.careGiver.id if late_submission.careGiver else None,
            "type": late_submission.type,
            "start": late_submission.start.strftime("%Y-%m-%d %H:%M:%S")
                if isinstance(late_submission.start, datetime) else late_submission.start,
            "duration": late_submission.duration,
            "reasonForLateSubmission": late_submission.reasonForLateSubmission,
            "createdAt": late_submission.createdAt.strftime("%Y-%m-%d %H:%M:%S"),
            "modifiedAt": late_submission.modifiedAt.strftime("%Y-%m-%d %H:%M:%S"),
        }
