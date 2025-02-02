from datetime import datetime
from typing import Union

class UpdateResponseDTO:
    """DTO for transforming Update model responses."""

    @staticmethod
    def transform_update(update: Union[dict, object]) -> dict:
        """Converts an Update model instance or dictionary into a structured response."""

        if isinstance(update, dict):
            return {
                "updateId": update.get("updateId"),
                "patientId": update.get("patient__patientId"),
                "careGiverId": update.get("careGiver"),
                "notes": update.get("notes"),
                "dateTaken": update.get("dateTaken"),
                "createdAt": update.get("createdAt"),
                "modifiedAt": update.get("modifiedAt"),
            }
        
        # Handling model instance
        return {
            "updateId": update.updateId,
            "patientId": update.patient.patientId if update.patient else None,
            "careGiverId": update.careGiver.id if update.careGiver else None,
            "notes": update.notes,
            "dateTaken": update.dateTaken.strftime("%Y-%m-%d") if isinstance(update.dateTaken, datetime) else update.dateTaken,
            "createdAt": update.createdAt.strftime("%Y-%m-%d %H:%M:%S"),
            "modifiedAt": update.modifiedAt.strftime("%Y-%m-%d %H:%M:%S"),
        }
