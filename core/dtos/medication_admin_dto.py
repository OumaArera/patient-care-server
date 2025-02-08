

from core.utils.format_null_values import format_value


class MedicationAdministrationResponseDTO:
    """Transforms MedicationAdministration model instances or dictionaries into response format."""

    @staticmethod
    def transform_medication_administration(data):
        """
        Transforms a MedicationAdministration instance or dictionary into a structured response format.
        """
        if isinstance(data, dict):
            return {
                "medicationAdministrationId": data.get("medicationAdministrationId"),
                "patientId": data.get("patient__patientId"),
                "patientName": format_value(
                    data.get("patient__firstName"),
                    data.get("patient__lastName")
                ),
                "medicationId": data.get("medication__medicationId"),
                "careGiverId": data.get("careGiver"),
                "careGiverName": format_value(
                    data.get("careGiver__firstName"),
                    data.get("careGiver__lastName")
                ),
                "timeAdministered": data.get("timeAdministered"),
                "status": data.get("status"),
                "reasonNotFiled": data.get("reasonNotFiled"),
                "createdAt": data.get("createdAt"),
                "modifiedAt": data.get("modifiedAt"),
            }
        else:  
            return {
                "medicationAdministrationId": data.medicationAdministrationId,
                "patientId": data.patient.patientId,
                "patientName": format_value(
                    data.patient.firstName if data.patient else None,
                    data.patient.lastName if data.patient else None
                ),
                "medicationId": data.medication.medicationId,
                "careGiverName": format_value(
                    data.careGiver.firstName if data.careGiver else None,
                    data.careGiver.lastName if data.careGiver else None
                ),
                "careGiverId": data.careGiver.id if data.careGiver else None,
                "timeAdministered": data.timeAdministered,
                "status": data.status,
                "reasonNotFiled": data.reasonNotFiled,
                "createdAt": data.createdAt.strftime("%Y-%m-%d %H:%M:%S"),
                "modifiedAt": data.modifiedAt.strftime("%Y-%m-%d %H:%M:%S"),
            }
