from core.permissions import *
from core.utils.validate_query_params import validate_query_params
from custom_admin.serializers.appointment_serializers import *
from rest_framework.views import APIView  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework import status  # type: ignore
from core.utils.responses import APIResponse
from core.utils.query_params import valid_query_params
from custom_admin.services.appointment_services import AppointmentService
from core.utils.format_errors import format_validation_errors as fve


class AppointmentView(APIView):

    def get_permissions(self):
        """Dynamically assigns permissions based on request method."""
        if self.request.method == "POST":
            self.permission_classes = [IsManager]
        elif self.request.method == "GET":
            self.permission_classes = [IsAllUsers]
        return [permission() for permission in self.permission_classes]

    def post(self, request):
        """Handles creating a new appointment entry."""
        try:
            deserializer = AppointmentSerializer(data=request.data)
            if deserializer.is_valid():
                appointment = AppointmentService.create_appointment(
                    data=deserializer.validated_data
                )
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Appointment created successfully",
                        data=appointment
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
                    message="An error occurred while creating appointment",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def get(self, request):
        """Handles fetching all appointments."""
        try:
            query_params = validate_query_params(
                query_params=request.query_params,
                valid_query_params=valid_query_params
            )
            appointment_list = AppointmentService.get_all_appointments(
                query_params=query_params
            )
            return Response(
                APIResponse.success(
                    code="00",
                    message="Appointments fetched successfully",
                    data=appointment_list
                ),
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error fetching appointments",
                    error=str(ex)
                ),
                status=ex.status_code
            )


class AppointmentQueryByIDView(APIView):

    def get_permissions(self):
        """Dynamically assigns permissions based on request method."""
        if self.request.method in ["GET", "DELETE"]:
            self.permission_classes = [IsManager]
        elif self.request.method == "PUT":
            self.permission_classes = [IsAllUsers]
        return [permission() for permission in self.permission_classes]

    def get(self, request, appointmentId):
        """Handles fetching an appointment entry by ID."""
        try:
            appointment = AppointmentService.get_appointment_by_id(appointment_id=appointmentId)
            return Response(
                APIResponse.success(
                    code="00",
                    message="Appointment fetched successfully",
                    data=appointment
                ),
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error fetching appointment",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def put(self, request, appointmentId):
        """Handles updating an appointment entry."""
        try:
            deserializer = AppointmentUpdateSerializer(data=request.data)
            if deserializer.is_valid():
                updated_appointment = AppointmentService.update_appointment(
                    appointment_id=appointmentId,
                    appointment_data=deserializer.validated_data
                )
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Appointment updated successfully",
                        data=updated_appointment
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
                    message="Error updating appointment",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def delete(self, request, appointmentId):
        """Handles deleting an appointment entry."""
        try:
            if AppointmentService.delete_appointment(appointment_id=appointmentId):
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Appointment deleted successfully",
                        data={"appointment_id": appointmentId}
                    ),
                    status=status.HTTP_200_OK
                )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error deleting appointment",
                    error=str(ex)
                ),
                status=ex.status_code
            )