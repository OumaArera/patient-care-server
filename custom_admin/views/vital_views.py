from core.permissions import *
from core.utils.validate_query_params import validate_query_params
from custom_admin.serializers.vitals_serializers import *
from rest_framework.views import APIView  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework import status  # type: ignore
from core.utils.responses import APIResponse
from core.utils.query_params import valid_query_params
from custom_admin.services.vitals_service import *
from core.utils.format_errors import format_validation_errors as fve


class VitalView(APIView):

    def get_permissions(self):
        """Dynamically assigns permissions based on request method."""
        if self.request.method == "POST":
            self.permission_classes = [IsCareGiver]
        elif self.request.method == "GET":
            self.permission_classes = [IsAllUsers]
        return [permission() for permission in self.permission_classes]

    def post(self, request):
        """Handles creating a new vital entry."""
        try:
            deserializer = VitalSerializer(data=request.data)
            if deserializer.is_valid():
                validated_data = deserializer.validated_data
                validated_data['careGiver'] = request.user
                new_vital = VitalService.create_vital(data=validated_data)
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Vital created successfully",
                        data=new_vital
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
                    message="An error occurred while creating the vital",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def get(self, request):
        """Handles fetching all vitals."""
        try:
            query_params = validate_query_params(
                query_params=request.query_params,
                valid_query_params=valid_query_params
            )
            vitals = VitalService.get_all_vitals(
                request=request, 
                query_params=query_params
            )
            return Response(
                APIResponse.success(
                    code="00",
                    message="Vitals fetched successfully",
                    data=vitals
                ),
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error fetching vitals",
                    error=str(ex)
                ),
                status=ex.status_code
            )


class VitalQueryByIDView(APIView):

    def get_permissions(self):
        """Dynamically assigns permissions based on request method."""
        if self.request.method == "PUT":
            self.permission_classes = [IsCareGiver]
        elif self.request.method == "GET":
            self.permission_classes = [IsAllUsers]
        elif self.request.method == "DELETE":
            self.permission_classes = [IsSuperUser]
        return [permission() for permission in self.permission_classes]

    def get(self, request, vitalId):
        """Handles fetching a vital by ID."""
        try:
            vital = VitalService.get_vital_by_id(vital_id=vitalId)
            return Response(
                APIResponse.success(
                    code="00",
                    message="Vital fetched successfully",
                    data=vital
                ),
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error fetching vital",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def put(self, request, vitalId):
        """Handles updating a vital."""
        try:
            deserializer = VitalUpdateSerializer(data=request.data)
            if deserializer.is_valid():
                updated_vital = VitalService.update_vital(
                    vital_id=vitalId,
                    vital_data=deserializer.validated_data
                )
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Vital updated successfully",
                        data=updated_vital
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
                    message="Error updating vital",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def delete(self, request, vitalId):
        """Handles deleting a vital."""
        try:
            if VitalService.delete_vital(vital_id=vitalId):
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Vital deleted successfully",
                        data={"vital_id": vitalId}
                    ),
                    status=status.HTTP_200_OK
                )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error deleting vital",
                    error=str(ex)
                ),
                status=ex.status_code
            )