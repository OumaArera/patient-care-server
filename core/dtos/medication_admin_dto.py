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
                "medicationId": data.get("medication__medicationId"),
                "careGiverId": data.get("careGiver"),
                "timeAdministered": data.get("timeAdministered"),
            }
        else:  
            return {
                "medicationAdministrationId": data.medicationAdministrationId,
                "patientId": data.patient.patientId,
                "medicationId": data.medication.medicationId,
                "careGiverId": data.careGiver.id if data.careGiver else None,
                "timeAdministered": data.timeAdministered,
            }
