from core.permissions import *
from core.utils.validate_query_params import validate_query_params
from custom_admin.serializers.chart_serializers import *
from rest_framework.views import APIView  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework import status  # type: ignore
from core.utils.responses import APIResponse
from core.utils.query_params import valid_query_params
from custom_admin.services.chart_service import ChartService
from core.utils.format_errors import format_validation_errors as fve


class ChartView(APIView):

    def get_permissions(self):
        """Dynamically assigns permissions based on request method."""
        if self.request.method == "POST":
            self.permission_classes = [IsCareGiver]
        elif self.request.method == "GET":
            self.permission_classes = [IsAllUsers]
        return [permission() for permission in self.permission_classes]

    

    def post(self, request):
        """Handles creating a new chart entry."""
        try:
            deserializer = ChartSerializer(data=request.data)
            if deserializer.is_valid():
                validated_data = deserializer.validated_data
                validated_data["careGiver"] = request.user
                chart = ChartService.create_chart(data=validated_data)
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Chart created successfully",
                        data=chart
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
                    message="An error occurred while creating chart",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def get(self, request):
        """Handles fetching all charts."""
        try:
            query_params = validate_query_params(
                query_params=request.query_params,
                valid_query_params=valid_query_params
            )
            chart_list = ChartService.get_all_charts(
                request=request,
                query_params=query_params
            )
            return Response(
                APIResponse.success(
                    code="00",
                    message="Charts fetched successfully",
                    data=chart_list
                ),
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error fetching charts",
                    error=str(ex)
                ),
                status=ex.status_code
            )


class ChartQueryByIDView(APIView):

    def get_permissions(self):
        """Dynamically assigns permissions based on request method."""
        if self.request.method == "PUT":
            self.permission_classes = [IsCareGiver]
        elif self.request.method == "GET":
            self.permission_classes = [IsAllUsers]
        elif self.request.method == "DELETE":
            self.permission_classes = [IsSuperUser]
        return [permission() for permission in self.permission_classes]

    def get(self, request, chartId):
        """Handles fetching a chart entry by ID."""
        try:
            chart = ChartService.get_chart_by_id(chart_id=chartId)
            return Response(
                APIResponse.success(
                    code="00",
                    message="Chart fetched successfully",
                    data=chart
                ),
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error fetching chart",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def put(self, request, chartId):
        """Handles updating a chart entry."""
        try:
            deserializer = ChartUpdateSerializer(data=request.data)
            if deserializer.is_valid():
                updated_chart = ChartService.update_chart(
                    chart_id=chartId,
                    chart_data=deserializer.validated_data
                )
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Chart updated successfully",
                        data=updated_chart
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
                    message="Error updating chart",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def delete(self, request, chartId):
        """Handles deleting a chart entry."""
        try:
            if ChartService.delete_chart(chart_id=chartId):
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Chart deleted successfully",
                        data={"chart_id": chartId}
                    ),
                    status=status.HTTP_200_OK
                )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error deleting chart",
                    error=str(ex)
                ),
                status=ex.status_code
            )
