from datetime import datetime
from typing import Union

from core.utils.format_null_values import format_value

class UtilityResponseDTO:
    """DTO for transforming Utility model responses."""

    @staticmethod
    def transform_utility(utility: Union[dict, object]) -> dict:
        """Converts a Utility model instance or dictionary into a structured response."""

        if isinstance(utility, dict):
            return {
                "utilityId": utility.get("utilityId"),
                "staffId": utility.get("staff__id"),
                "staffName": format_value(
                    utility.get("staff__firstName"),
                    utility.get("staff__lastName")
                ),
                "item": utility.get("item"),
                "details": utility.get("details"),
                "status": utility.get("status"),
                "createdAt": utility.get("createdAt"),
                "modifiedAt": utility.get("modifiedAt"),
            }

        # Handling model instance
        return {
            "utilityId": utility.utilityId,
            "staffId": utility.staff.id if utility.staff else None,
            "staffName": format_value(
                utility.staff.firstName if utility.staff else None,
                utility.staff.lastName if utility.staff else None
            ),
            "item": utility.item,
            "details": utility.details,
            "status": utility.status,
            "createdAt": utility.createdAt.strftime("%Y-%m-%d %H:%M:%S"),
            "modifiedAt": utility.modifiedAt.strftime("%Y-%m-%d %H:%M:%S"),
        }
