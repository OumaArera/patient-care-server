from typing import Union

from core.utils.format_null_values import format_value

class IncidentResponseDTO:
    """DTO for transforming Incident model responses."""

    @staticmethod
    def transform_incident(incident: Union[dict, object]) -> dict:
        """Converts an Incident model instance or dictionary into a structured response."""

        if isinstance(incident, dict):
            return {
                "incidentId": incident.get("incidentId"),
                "staffId": incident.get("staff__id"),
                "staffName": format_value(
                    incident.get("staff__firstName"),
                    incident.get("staff__lastName")
                ),
                "filePath": incident.get("filePath"),
                "details": incident.get("details"),
                "status": incident.get("status"),
                "createdAt": incident.get("createdAt"),
                "modifiedAt": incident.get("modifiedAt"),
            }

        # Handling model instance
        return {
            "incidentId": incident.incidentId,
            "staffId": incident.staff.id if incident.staff else None,
            "staffName": format_value(
                incident.staff.firstName if incident.staff else None,
                incident.staff.lastName if incident.staff else None
            ),
            "filePath": incident.filePath,
            "details": incident.details,
            "status": incident.status,
            "createdAt": incident.createdAt.strftime("%Y-%m-%d %H:%M:%S"),
            "modifiedAt": incident.modifiedAt.strftime("%Y-%m-%d %H:%M:%S"),
        }
