from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.permissions import IsAllUsers
from core.utils.responses import APIResponse
from core.utils.validate_query_params import validate_query_params
from core.utils.format_errors import format_validation_errors as fve
from core.utils.query_params import valid_query_params
from custom_admin.serializers.sleep_serializer import *
from custom_admin.services.sleep_service import SleepService


class SleepView(APIView):
    """Handles creation and retrieval of sleep entries."""

    permission_classes = [IsAllUsers]

    def post(self, request):
        """Handles creation of a new sleep entry."""
        try:
            serializer = SleepSerializer(data=request.data)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                new_sleep = SleepService.create_sleep(data=validated_data)
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Sleep entry created successfully",
                        data=new_sleep
                    ),
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    APIResponse.error(
                        code="99",
                        message="Validation failed",
                        error=fve(serializer.errors)
                    ),
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="An error occurred while creating the sleep entry",
                    error=str(ex)
                ),
                status=getattr(ex, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
            )

    def get(self, request):
        """Handles retrieval of all sleep entries."""
        try:
            query_params = validate_query_params(
                query_params=request.query_params,
                valid_query_params=valid_query_params
            )
            sleeps = SleepService.get_all_sleeps(query_params=query_params)
            return Response(
                APIResponse.success(
                    code="00",
                    message="Sleep entries fetched successfully",
                    data=sleeps
                ),
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error fetching sleep entries",
                    error=str(ex)
                ),
                status=getattr(ex, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
            )


class SleepQueryByIDView(APIView):
    """Handles retrieval, updating, and deletion of a specific sleep entry."""

    permission_classes = [IsAllUsers]

    def get(self, request, sleepId):
        """Fetch a single sleep entry by ID."""
        try:
            sleep = SleepService.get_sleep_by_id(sleep_id=sleepId)
            return Response(
                APIResponse.success(
                    code="00",
                    message="Sleep entry fetched successfully",
                    data=sleep
                ),
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error fetching sleep entry",
                    error=str(ex)
                ),
                status=getattr(ex, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
            )

    def put(self, request, sleepId):
        """Update a specific sleep entry."""
        try:
            serializer = SleepUpdateSerializer(data=request.data)
            if serializer.is_valid():
                updated_sleep = SleepService.update_sleep(
                    sleep_id=sleepId,
                    sleep_data=serializer.validated_data
                )
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Sleep entry updated successfully",
                        data=updated_sleep
                    ),
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    APIResponse.error(
                        code="99",
                        message="Validation failed",
                        error=fve(serializer.errors)
                    ),
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error updating sleep entry",
                    error=str(ex)
                ),
                status=getattr(ex, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
            )

    def delete(self, request, sleepId):
        """Delete a specific sleep entry."""
        try:
            if SleepService.delete_sleep(sleep_id=sleepId):
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Sleep entry deleted successfully",
                        data={"sleep_id": sleepId}
                    ),
                    status=status.HTTP_200_OK
                )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error deleting sleep entry",
                    error=str(ex)
                ),
                status=getattr(ex, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
            )
