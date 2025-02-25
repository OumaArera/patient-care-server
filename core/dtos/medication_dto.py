class MedicationResponseDTO:
    """Data Transfer Object for Medication responses."""

    @staticmethod
    def transform_medication(medication):
        """Transforms a medication instance or dictionary into a structured response."""
        if isinstance(medication, dict):
            return {
                "medicationId": medication.get("medicationId"),
                "medicationName": medication.get("medicationName"),
                "medicationCode": medication.get("medicationCode"),
                "equivalentTo": medication.get("equivalentTo"),
                "instructions": medication.get("instructions"),
                "quantity": medication.get("quantity"),
                "diagnosis": medication.get("diagnosis"),
                "medicationTime": medication.get("medicationTime"),
                "status": medication.get("status"),
                "patientId": medication.get("patient__patientId"),
                "patientFirstName": medication.get("patient__firstName"),
                "patientLastName": medication.get("patient__lastName"),
            }
        return {
            "medicationId": medication.medicationId,
            "medicationName": medication.medicationName,
            "medicationCode": medication.medicationCode,
            "equivalentTo": medication.equivalentTo,
            "instructions": medication.instructions,
            "quantity": medication.quantity,
            "diagnosis": medication.diagnosis,
            "medicationTime": medication.medicationTime,
            "status": medication.status,
            "patientId": medication.patient.patientId,
            "patientFirstName": medication.patient.firstName,
            "patientLastName": medication.patient.lastName,
        }