class PatientManagerResponseDTO:
    """DTO for transforming PatientManager model responses."""

    @staticmethod
    def transform_patient_manager(manager):
        """Converts a PatientManager instance or dictionary into a structured response."""
        print(f"Data: {manager}")
        if isinstance(manager, dict):
            return {
                "patientManagerId": manager.get("patientManagerId"),
                "patient": {
                    "patientId": manager.get("patient__patientId"),
                    "firstName": manager.get("patient__firstName"),
                    "lastName": manager.get("patient__lastName"),
                    "dateOfBirth": manager.get("patient__dateOfBirth"),
                    "diagnosis": manager.get("patient__diagnosis"),
                    "allergies": manager.get("patient__allergies"),
                    "physicianName": manager.get("patient__physicianName"),
                    "branchName": manager.get("patient__branch__branchName"),
                    "facilityName": manager.get("patient__branch__facility__facilityName"),
                    "room": manager.get("patient__room"),
                    "cart": manager.get("patient__cart"),
                },
                "careGiver": {
                    "user_id": manager.get("careGiver__id"),
                    "firstName": manager.get("careGiver__firstName"),
                    "lastName": manager.get("careGiver__lastName"),
                }
            }
        else:
            return {
                "patientManagerId": manager.patientManagerId,
                "patient": {
                    "patientId": manager.patient.patientId,
                    "firstName": manager.patient.firstName,
                    "lastName": manager.patient.lastName,
                    "dateOfBirth": manager.patient.dateOfBirth,
                    "diagnosis": manager.patient.diagnosis,
                    "allergies": manager.patient.allergies,
                    "physicianName": manager.patient.physicianName\
                        if manager.patient else None,
                    "branchName": manager.patient.branch.branchName\
                        if manager.patient and manager.patient.branch else None,
                    "facilityName": manager.patient.branch.facility.facilityName\
                        if manager.patient and manager.patient.branch and\
                        manager.patient.branch.facility else None,
                    "room": manager.patient.room,
                    "cart": manager.patient.cart,
                },
                "careGiver": {
                    "user_id": manager.careGiver.id if manager.careGiver else None,
                    "firstName": manager.careGiver.firstName if manager.careGiver else None,
                    "lastName": manager.careGiver.lastName if manager.careGiver else None,
                }
            }