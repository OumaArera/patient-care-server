from core.permissions import *
from rest_framework.views import APIView  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework import status  # type: ignore
from core.utils.responses import APIResponse
from core.utils.validate_query_params import validate_query_params
from core.utils.query_params import valid_query_params
from custom_admin.services.patient_manager_service import *
from core.utils.format_errors import format_validation_errors as fve


class PatientManagerView(APIView):

    def get_permissions(self):
        """Dynamically assigns permissions based on request method."""
        if self.request.method == "POST":
            self.permission_classes = [IsSuperUser]
        elif self.request.method == "GET":
            self.permission_classes = [IsAllUsers]
        return [permission() for permission in self.permission_classes]

    def post(self, request):
        """Handles creating or updating a patient manager."""
        try:
            patient = request.data.get("patient")
            care_giver = request.data.get("careGiver")

            if not patient or not care_giver:
                return Response(
                    APIResponse.error(
                        code="99",
                        message="Validation failed",
                        error="Both 'patient' and 'careGiver' are required."
                    ),
                    status=status.HTTP_400_BAD_REQUEST
                )

            patient_manager = PatientManagerService.create_or_update_patient_manager(
                data={"patient": patient, "careGiver": care_giver}
            )

            return Response(
                APIResponse.success(
                    code="00",
                    message="Patient manager created/updated successfully",
                    data=patient_manager
                ),
                status=status.HTTP_201_CREATED
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="An error occurred while creating/updating patient manager",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def get(self, request):
        """Handles fetching all patient managers."""
        try:
            query_params = validate_query_params(
                query_params=request.query_params,
                valid_query_params=valid_query_params
            )

            patient_managers = PatientManagerService.get_all_patient_managers(
                request=request,
                query_params=query_params
            )

            return Response(
                APIResponse.success(
                    code="00",
                    message="Patient managers fetched successfully",
                    data=patient_managers
                ),
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error fetching patient managers",
                    error=str(ex)
                ),
                status=ex.status_code
            )


class PatientManagerQueryByIDView(APIView):

    def get_permissions(self):
        """Dynamically assigns permissions based on request method."""
        if self.request.method == "DELETE":
            self.permission_classes = [IsSuperUser]
        elif self.request.method == "GET":
            self.permission_classes = [IsAllUsers]
        return [permission() for permission in self.permission_classes]

    def get(self, request, managerId):
        """Handles fetching a patient manager by ID."""
        try:
            patient_manager = PatientManagerService.get_patient_manager_by_id(
                manager_id=managerId
            )

            return Response(
                APIResponse.success(
                    code="00",
                    message="Patient manager fetched successfully",
                    data=patient_manager
                ),
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error fetching patient manager",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def delete(self, request, managerId):
        """Handles deleting a patient manager by ID."""
        try:
            if PatientManagerService.delete_patient_manager(manager_id=managerId):
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Patient manager deleted successfully",
                        data={"manager_id": managerId}
                    ),
                    status=status.HTTP_200_OK
                )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error deleting patient manager",
                    error=str(ex)
                ),
                status=ex.status_code
            )
