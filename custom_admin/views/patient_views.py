from core.permissions import *
from core.utils.file_handler import handle_file
from core.utils.validate_query_params import validate_query_params
from custom_admin.serializers.patient_serializers import *
from rest_framework.views import APIView  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework import status  # type: ignore
from core.utils.responses import APIResponse
from core.utils.query_params import valid_query_params
from custom_admin.services.patient_service import PatientService
from core.utils.format_errors import format_validation_errors as fve


class PatientView(APIView):
    def get_permissions(self):
        """Dynamically assigns permissions based on request method."""
        if self.request.method == "POST":
            self.permission_classes = [IsManager]
        elif self.request.method == "GET":
            self.permission_classes = [IsAllUsers]
        return [permission() for permission in self.permission_classes]

    def post(self, request):
        """Handles creating a new patient."""
        try:
            deserializer = PatientSerializer(data=request.data)
            if deserializer.is_valid():
                validated_data = deserializer.validated_data
                file = request.FILES.get("file", None)
                if file:
                    validated_data['avatar'] = handle_file(file=file, directory='patients')
                patient = PatientService.create_patient(data=validated_data)
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Patient created successfully",
                        data=patient
                    ),
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    APIResponse.error(
                        code="99",
                        message="Validation failed",
                        error=fve(deserializer.errors)
                    ),
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="An error occurred while creating patient",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def get(self, request):
        """Handles fetching patients."""
        try:
            query_params = validate_query_params(
                query_params=request.query_params,
                valid_query_params=valid_query_params
            )
            patients = PatientService.get_all_patients(
                query_params=query_params
            )
            return Response(
                APIResponse.success(
                    code="00",
                    message="Patients fetched successfully",
                    data=patients
                ),
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error fetching patients",
                    error=str(ex)
                ),
                status=ex.status_code
            )


class PatientQueryByIDView(APIView):
    
    def get_permissions(self):
        """Dynamically assigns permissions based on request method."""
        if self.request.method in ["DELETE"]:
            self.permission_classes = [IsManager]
        elif self.request.method in ["GET", "PUT"]:
            self.permission_classes = [IsAllUsers]
        return [permission() for permission in self.permission_classes]

    def get(self, request, patientId):
        """Handles fetching a patient by ID."""
        try:
            patient = PatientService.get_patient_by_id(patient_id=patientId)
            return Response(
                APIResponse.success(
                    code="00",
                    message="Patient fetched successfully",
                    data=patient
                ),
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error fetching patient",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def put(self, request, patientId):
        """Handles updating a patient."""
        try:
            deserializer = PatientUpdateSerializer(data=request.data)
            if deserializer.is_valid():
                validated_data = deserializer.validated_data
                file = request.FILES.get("file", None)
                if file:
                    validated_data['avatar'] = handle_file(file=file, directory='patients')
                updated_patient = PatientService.update_patient(
                    patient_id=patientId,
                    patient_data=validated_data
                )
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Patient updated successfully",
                        data=updated_patient
                    ),
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    APIResponse.error(
                        code="99",
                        message="Validation failed",
                        error=fve(deserializer.errors)
                    ),
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error updating patient",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def delete(self, request, patientId):
        """Handles deleting a patient."""
        try:
            if PatientService.delete_patient(patient_id=patientId):
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Patient deleted successfully",
                        data={"patient_id": patientId}
                    ),
                    status=status.HTTP_200_OK
                )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error deleting patient",
                    error=str(ex)
                ),
                status=ex.status_code
            )
