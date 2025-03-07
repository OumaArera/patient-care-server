from datetime import datetime
from typing import Union

from core.utils.format_null_values import format_value

class VitalResponseDTO:
    """DTO for transforming Vital model responses."""

    @staticmethod
    def transform_vital(vital: Union[dict, object]) -> dict:
        """Converts a Vital model instance or dictionary into a structured response."""

        if isinstance(vital, dict):
            return {
                "vitalId": vital.get("vitalId"),
                "patientId": vital.get("patient__patientId"),
                "patientName": format_value(
                    vital.get("patient__firstName"),
                    vital.get("patient__lastName")
                ),
                "bloodPressure": vital.get("bloodPressure"),
                "temperature": vital.get("temperature"),
                "pulse": vital.get("pulse"),
                "oxygenSaturation": vital.get("oxygenSaturation"),
                "pain": vital.get("pain"),
                "reasonEdited": vital.get("reasonEdited"),
                "dateTaken": vital.get("dateTaken"),
                "createdAt": vital.get("createdAt"),
                "modifiedAt": vital.get("modifiedAt"),
            }
        
        # Handling model instance
        return {
            "vitalId": vital.vitalId,
            "patientId": vital.patient.patientId if vital.patient else None,
            "patientName": format_value(
                vital.patient.firstName if vital.patient else None,
                vital.patient.lastName if vital.patient else None
            ),
            "bloodPressure": vital.bloodPressure,
            "temperature": vital.temperature,
            "pulse": vital.pulse,
            "oxygenSaturation": vital.oxygenSaturation,
            "pain": vital.pain,
            "reasonEdited": vital.reasonEdited,
            "dateTaken": vital.dateTaken.strftime("%Y-%m-%d")
                if isinstance(vital.dateTaken, datetime) else vital.dateTaken,
            "createdAt": vital.createdAt.strftime("%Y-%m-%d %H:%M:%S"),
            "modifiedAt": vital.modifiedAt.strftime("%Y-%m-%d %H:%M:%S"),
        }
