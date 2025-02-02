from core.utils.format_file_path import build_absolute_url

class PatientResponseDTO:
    """Transforms Patient model instances into structured response data."""
    
    @staticmethod
    def transform_patient(patient):
        """Transforms a single Patient instance into a dictionary."""
        if isinstance(patient, dict):
            return {
                "patientId": patient.get('patientId'),
                "avatar": build_absolute_url(patient.get("avatar")) if patient.get("avatar") else None,
                "firstName": patient.get('firstName'),
                "middleNames": patient.get("middleNames"),
                "lastName": patient.get("lastName"),
                "dateOfBirth": str(patient.get("dateOfBirth")),
                "diagnosis": patient.get("diagnosis"),
                "allergies": patient.get("allergies"),
                "physicianName": patient.get("physicianName"),
                "pcpOrDoctor": patient.get("pcpOrDoctor"),
                "branchId": patient.get("branch__branchId"),
                "branchName": patient.get("branch__branchName"),
                "room": patient.get("room"),
                "cart": patient.get("cart"),
            }
        else:
            return {
                "patientId": patient.patientId,
                "avatar": build_absolute_url(patient.avatar) if patient.avatar else None,
                "firstName": patient.firstName,
                "middleNames": patient.middleNames,
                "lastName": patient.lastName,
                "dateOfBirth": str(patient.dateOfBirth),
                "diagnosis": patient.diagnosis,
                "allergies": patient.allergies,
                "physicianName": patient.physicianName,
                "pcpOrDoctor": patient.pcpOrDoctor,
                "branchId": patient.branch.branchId if patient.branch else None,
                "branchName": patient.branch.branchName if patient.branch else None,
                "room": patient.room,
                "cart": patient.cart,
            }
    
    @staticmethod
    def transform_patients(patients):
        """Transforms a list of Patient instances into a list of dictionaries."""
        return [PatientResponseDTO.transform_patient(patient) for patient in patients]