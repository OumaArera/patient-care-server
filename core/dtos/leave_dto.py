from datetime import datetime
from typing import Union

from core.utils.format_null_values import format_value

class LeaveResponseDTO:
    """DTO for transforming Leave model responses."""

    @staticmethod
    def transform_leave(leave: Union[dict, object]) -> dict:
        """Converts a Leave model instance or dictionary into a structured response."""

        if isinstance(leave, dict):
            return {
                "leaveId": leave.get("leaveId"),
                "staffId": leave.get("staff__id"),
                "staffName": format_value(
                    leave.get("staff__firstName"),
                    leave.get("staff__lastName")
                ),
                "reasonForLeave": leave.get("reasonForLeave"),
                "startDate": leave.get("startDate"),
                "endDate": leave.get("endDate"),
                "status": leave.get("status"),
                "declineReason": leave.get("declineReason"),
                "createdAt": leave.get("createdAt"),
                "modifiedAt": leave.get("modifiedAt"),
            }
        
        # Handling model instance
        return {
            "leaveId": leave.leaveId,
            "staffId": leave.staff.id if leave.staff else None,
            "staffName": format_value(
                leave.staff.firstName if leave.staff else None,
                leave.staff.lastName if leave.staff else None
            ),
            "reasonForLeave": leave.reasonForLeave,
            "startDate": leave.startDate.strftime("%Y-%m-%d") 
                if isinstance(leave.startDate, datetime) else leave.startDate,
            "endDate": leave.endDate.strftime("%Y-%m-%d") 
                if isinstance(leave.endDate, datetime) else leave.endDate,
            "status": leave.status,
            "declineReason": leave.declineReason,
            "createdAt": leave.createdAt.strftime("%Y-%m-%d %H:%M:%S"),
            "modifiedAt": leave.modifiedAt.strftime("%Y-%m-%d %H:%M:%S"),
        }