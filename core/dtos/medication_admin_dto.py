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
                "facilityName": data.get('patient__branch__facility__facilityName'),
                "branchName": data.get('patient__branch__branchName'),
                "medication": {
                    "medicationId": data.get("medication__medicationId"),
                    "medicationName": data.get("medication__medicationName"),
                    "medicationCode": data.get("medication__medicationCode"),
                    "equivalentTo": data.get("medication__equivalentTo"),
                    "instructions": data.get("medication__instructions"),
                    "quantity": data.get("medication__quantity"),
                    "diagnosis": data.get("medication__diagnosis"),
                    "medicationTimes": data.get("medication__medicationTime")
                },
                "careGiverId": data.get("careGiver"),
                "careGiverName": format_value(
                    data.get("careGiver__firstName"),
                    data.get("careGiver__lastName")
                ),
                "timeAdministered": data.get("timeAdministered"),
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
                "facilityName": data.patient.branch.facility.facilityName\
                    if data.patient and data.patient.branch and\
                    data.patient.branch.facility else None,
                "branchName": data.patient.branch.branchName\
                    if data.patient and data.patient.branch else None,
                "medication": {
                    "medicationId": data.medication.medicationId if data.medication else None,
                    "medicationName": data.medication.medicationName if data.medication else None,
                    "medicationCode": data.medication.medicationCode if data.medication else None,
                    "equivalentTo": data.medication.equivalentTo if data.medication else None,
                    "instructions": data.medication.instructions if data.medication else None,
                    "quantity": data.medication.quantity if data.medication else None,
                    "diagnosis": data.medication.diagnosis if data.medication else None,
                    "medicationTimes": data.medication.medicationTime if data.medication else None
                },
                "careGiverName": format_value(
                    data.careGiver.firstName if data.careGiver else None,
                    data.careGiver.lastName if data.careGiver else None
                ),
                "careGiverId": data.careGiver.id if data.careGiver else None,
                "timeAdministered": data.timeAdministered,
                # "status": data.status,
                "createdAt": data.createdAt.strftime("%Y-%m-%d %H:%M:%S"),
                "modifiedAt": data.modifiedAt.strftime("%Y-%m-%d %H:%M:%S"),
            }
