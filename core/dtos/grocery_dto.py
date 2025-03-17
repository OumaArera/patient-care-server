from datetime import datetime
from typing import Union

from core.utils.format_null_values import format_value

class GroceryResponseDTO:
    """DTO for transforming Grocery model responses."""

    @staticmethod
    def transform_grocery(grocery: Union[dict, object]) -> dict:
        """Converts a Grocery model instance or dictionary into a structured response."""

        if isinstance(grocery, dict):
            return {
                "groceryId": grocery.get("groceryId"),
                "staffId": grocery.get("staff__id"),
                "staffName": format_value(
                    grocery.get("staff__firstName"),
                    grocery.get("staff__lastName")
                ),
                "details": grocery.get("details", []),
                "feedback": grocery.get("feedback"),
                "status": grocery.get("status"),
                "createdAt": grocery.get("createdAt"),
                "modifiedAt": grocery.get("modifiedAt"),
            }

        # Handling model instance
        return {
            "groceryId": grocery.groceryId,
            "staffId": grocery.staff.id if grocery.staff else None,
            "staffName": format_value(
                grocery.staff.firstName if grocery.staff else None,
                grocery.staff.lastName if grocery.staff else None
            ),
            "details": grocery.details,
            "feedback": grocery.feedback,
            "status": grocery.status,
            "createdAt": grocery.createdAt.strftime("%Y-%m-%d %H:%M:%S"),
            "modifiedAt": grocery.modifiedAt.strftime("%Y-%m-%d %H:%M:%S"),
        }
