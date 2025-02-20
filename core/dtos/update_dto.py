from datetime import datetime
from typing import Union

from core.utils.format_null_values import format_value

class UpdateResponseDTO:
    """DTO for transforming Update model responses."""

    @staticmethod
    def transform_update(update: Union[dict, object]) -> dict:
        """Converts an Update model instance or dictionary into a structured response."""

        if isinstance(update, dict):
            return {
                "updateId": update.get("updateId"),
                "patientId": update.get("patient__patientId"),
                "patientName": format_value(
                    update.get("patient__firstName"),
                    update.get("patient__lastName")
                ),
                "type": update.get("type"),
                "weight": update.get("weight"),
                "weightDeviation": update.get("weightDeviation"),
                "facilityName": update.get('patient__branch__facility__facilityName'),
                "branchName": update.get('patient__branch__branchName'),
                "careGiverId": update.get("careGiver"),
                "careGiverName": format_value(
                    update.get("careGiver__firstName"),
                    update.get("careGiver__lastName")
                ),
                "notes": update.get("notes"),
                "dateTaken": update.get("dateTaken"),
                "createdAt": update.get("createdAt"),
                "modifiedAt": update.get("modifiedAt"),
            }
        
        # Handling model instance
        return {
            "updateId": update.updateId,
            "patientId": update.patient.patientId if update.patient else None,
            "patientName": format_value(
                    update.patient.firstName if update.patient else None,
                    update.patient.lastName if update.patient else None
                ),
            "type": update.type,
            "weight": update.weight,
            "weightDeviation": update.weightDeviation,
            "facilityName": update.patient.branch.facility.facilityName\
                if update.patient and update.patient.branch and\
                update.patient.branch.facility else None,
            "branchName": update.patient.branch.branchName\
                if update.patient and update.patient.branch else None,
            "careGiverId": update.careGiver.id if update.careGiver else None,
            "notes": update.notes,
            "dateTaken": update.dateTaken.strftime("%Y-%m-%d")\
                if isinstance(update.dateTaken, datetime) else update.dateTaken,
            "createdAt": update.createdAt.strftime("%Y-%m-%d %H:%M:%S"),
            "modifiedAt": update.modifiedAt.strftime("%Y-%m-%d %H:%M:%S"),
        }
