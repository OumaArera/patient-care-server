from core.permissions import *
from core.utils.validate_query_params import validate_query_params
from custom_admin.serializers.medication_admin_serializers import *
from rest_framework.views import APIView  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework import status  # type: ignore
from core.utils.responses import APIResponse
from core.utils.query_params import valid_query_params
from custom_admin.services.medication_admin_service import *
from core.utils.format_errors import format_validation_errors as fve


class MedicationAdministrationView(APIView):

    permission_classes = [IsAllUsers]

    def post(self, request):
        """Handles creating a new medication administration."""
        try:
            deserializer = MedicationAdministrationSerializer(data=request.data)
            if deserializer.is_valid():
                validated_data = deserializer.validated_data
                validated_data['careGiver'] = request.user
                administration = MedicationAdministrationService.\
                    create_medication_administration(
                        data=validated_data
                    )
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Medication administration created successfully",
                        data=administration
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
                    message="An error occurred while creating medication administration",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def get(self, request):
        """Handles fetching medication administrations."""
        try:
            query_params = validate_query_params(
                query_params=request.query_params,
                valid_query_params=valid_query_params
            )
            administrations = MedicationAdministrationService.\
                get_all_medications_administrations(
                    request=request,
                    query_params=query_params
                )
            return Response(
                APIResponse.success(
                    code="00",
                    message="Medication administrations fetched successfully",
                    data=administrations
                ),
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error fetching medication administrations",
                    error=str(ex)
                ),
                status=ex.status_code
            )


class MedicationAdministrationQueryByIDView(APIView):

    permission_classes = [IsAllUsers]

    def get(self, request, administrationId):
        """Handles fetching a medication administration by ID."""
        try:
            administration = MedicationAdministrationService.\
                get_medication_administration_by_id(
                    administration_id=administrationId
                )
            return Response(
                APIResponse.success(
                    code="00",
                    message="Medication administration fetched successfully",
                    data=administration
                ),
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error fetching medication administration",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def put(self, request, administrationId):
        """Handles updating a medication administration."""
        try:
            deserializer = MedicationAdministrationUpdateSerializer(data=request.data)
            if deserializer.is_valid():
                updated_administration = MedicationAdministrationService.\
                    update_medication_administration(
                        administration_id=administrationId,
                        administration_data=deserializer.validated_data
                    )
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Medication administration updated successfully",
                        data=updated_administration
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
                    message="Error updating medication administration",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def delete(self, request, administrationId):
        """Handles deleting a medication administration."""
        try:
            if MedicationAdministrationService.\
                    delete_medication_administration(
                        administration_id=administrationId
                    ):
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Medication administration deleted successfully",
                        data={"administration_id": administrationId}
                    ),
                    status=status.HTTP_200_OK
                )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error deleting medication administration",
                    error=str(ex)
                ),
                status=ex.status_code
            )
