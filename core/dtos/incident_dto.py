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
                "raisedById": incident.get("raisedBy__id"),
                "raisedBy": format_value(
                    incident.get("raisedBy__firstName"),
                    incident.get("raisedBy__lastName")
                ),
                "assignedToId": incident.get("assignedTo__id"),
                "assignedTo": format_value(
                    incident.get("assignedTo__firstName"),
                    incident.get("assignedTo__lastName")
                ),
                "incident": incident.get("incident"),
                "type": incident.get("type"),
                "comments": incident.get("comments"),
                "status": incident.get("status"),
                "priority": incident.get("priority"),
                "resolvedAt": incident.get("resolvedAt"),
                "createdAt": incident.get("createdAt"),
                "modifiedAt": incident.get("modifiedAt"),
            }

        # Handling model instance
        return {
            "incidentId": incident.incidentId,
            "raisedById": incident.raisedBy.id if incident.raisedBy else None,
            "raisedBy": format_value(
                incident.raisedBy.firstName,
                incident.raisedBy.lastName
            ),
            "assignedToId": incident.assignedTo.id if incident.assignedTo else None,
            "assignedTo": format_value(
                incident.assignedTo.firstName if incident.assignedTo else None,
                incident.assignedTo.lastName if incident.assignedTo else None
            ),
            "incident": incident.incident,
            "type": incident.type,
            "comments": incident.comments,
            "status": incident.status,
            "priority": incident.priority,
            "resolvedAt": incident.resolvedAt,
            "createdAt": incident.createdAt.strftime("%Y-%m-%d %H:%M:%S"),
            "modifiedAt": incident.modifiedAt.strftime("%Y-%m-%d %H:%M:%S"),
        }
