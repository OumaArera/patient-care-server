from core.permissions import *
from core.utils.validate_query_params import validate_query_params
from custom_admin.serializers.utility_serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.utils.responses import APIResponse
from core.utils.query_params import valid_query_params
from custom_admin.services.utility_services import UtilityService
from core.utils.format_errors import format_validation_errors as fve


class UtilityView(APIView):
    
    permission_classes = [IsAllUsers]

    def post(self, request):
        """Handles creating a new utility request."""
        try:
            deserializer = UtilitySerializer(data=request.data)
            if deserializer.is_valid():
                validated_data = deserializer.validated_data
                validated_data['staff'] = request.user
                new_utility = UtilityService.create_utility(data=validated_data)
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Utility created successfully",
                        data=new_utility
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
                    message="An error occurred while creating the utility",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def get(self, request):
        """Handles fetching all utility records."""
        try:
            query_params = validate_query_params(
                query_params=request.query_params,
                valid_query_params=valid_query_params
            )
            utilities = UtilityService.get_all_utilities(query_params=query_params)
            return Response(
                APIResponse.success(
                    code="00",
                    message="Utilities fetched successfully",
                    data=utilities
                ),
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error fetching utilities",
                    error=str(ex)
                ),
                status=ex.status_code
            )


class UtilityQueryByIDView(APIView):

    permission_classes = [IsAllUsers]

    def get(self, request, utilityId):
        """Handles fetching a utility record by ID."""
        try:
            utility = UtilityService.get_utility_by_id(utility_id=utilityId)
            return Response(
                APIResponse.success(
                    code="00",
                    message="Utility fetched successfully",
                    data=utility
                ),
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error fetching utility",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def put(self, request, utilityId):
        """Handles updating a utility record."""
        try:
            deserializer = UtilityUpdateSerializer(data=request.data)
            if deserializer.is_valid():
                updated_utility = UtilityService.update_utility(
                    utility_id=utilityId,
                    utility_data=deserializer.validated_data
                )
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Utility updated successfully",
                        data=updated_utility
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
                    message="Error updating utility",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def delete(self, request, utilityId):
        """Handles deleting a utility record."""
        try:
            if UtilityService.delete_utility(utility_id=utilityId):
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Utility deleted successfully",
                        data={"utility_id": utilityId}
                    ),
                    status=status.HTTP_200_OK
                )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error deleting utility",
                    error=str(ex)
                ),
                status=ex.status_code
            )
