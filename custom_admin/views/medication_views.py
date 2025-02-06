from core.permissions import *
from core.utils.validate_query_params import validate_query_params
from custom_admin.serializers.medication_serializers import *
from rest_framework.views import APIView  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework import status  # type: ignore
from core.utils.responses import APIResponse
from core.utils.query_params import valid_query_params
from custom_admin.services.medication_service import MedicationService
from core.utils.format_errors import format_validation_errors as fve

class MedicationView(APIView):

    permission_classes = [IsManager]

    def post(self, request):
        """Handles creating a new medication."""
        try:
            deserializer = MedicationSerializer(data=request.data)
            if deserializer.is_valid():
                medication = MedicationService.create_medication(data=deserializer.validated_data)
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Medication created successfully",
                        data=medication
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
                    message="An error occurred while creating medication",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def get(self, request):
        """Handles fetching medications."""
        try:
            query_params = validate_query_params(
                query_params=request.query_params,
                valid_query_params=valid_query_params
            )
            medications = MedicationService.get_all_medications(
                query_params=query_params
            )
            return Response(
                APIResponse.success(
                    code="00",
                    message="Medications fetched successfully",
                    data=medications
                ),
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error fetching medications",
                    error=str(ex)
                ),
                status=ex.status_code
            )


class MedicationQueryByIDView(APIView):

    permission_classes = [IsManager]

    def get(self, request, medicationId):
        """Handles fetching a medication by ID."""
        try:
            medication = MedicationService.get_medication_by_id(medication_id=medicationId)
            return Response(
                APIResponse.success(
                    code="00",
                    message="Medication fetched successfully",
                    data=medication
                ),
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error fetching medication",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def put(self, request, medicationId):
        """Handles updating a medication."""
        try:
            deserializer = MedicationUpdateSerializer(data=request.data)
            if deserializer.is_valid():
                updated_medication = MedicationService.update_medication(
                    medication_id=medicationId,
                    medication_data=deserializer.validated_data
                )
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Medication updated successfully",
                        data=updated_medication
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
                    message="Error updating medication",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def delete(self, request, medicationId):
        """Handles deleting a medication."""
        try:
            if MedicationService.delete_medication(medication_id=medicationId):
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Medication deleted successfully",
                        data={"medication_id": medicationId}
                    ),
                    status=status.HTTP_200_OK
                )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error deleting medication",
                    error=str(ex)
                ),
                status=ex.status_code
            )
