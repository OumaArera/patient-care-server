from core.permissions import *
from core.utils.validate_query_params import validate_query_params
from custom_admin.serializers.chart_data_serializers import *
from rest_framework.views import APIView  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework import status  # type: ignore
from core.utils.responses import APIResponse
from core.utils.query_params import valid_query_params
from custom_admin.services.chart_data_service import ChartDataService
from core.utils.format_errors import format_validation_errors as fve


class ChartDataView(APIView):

    def get_permissions(self):
        """Dynamically assigns permissions based on request method."""
        if self.request.method == "POST":
            self.permission_classes = [IsManager]
        elif self.request.method == "GET":
            self.permission_classes = [IsManager]
        return [permission() for permission in self.permission_classes]

    def post(self, request):
        """Handles creating a new chart data entry."""
        try:
            deserializer = ChartDataSerializer(data=request.data)
            if deserializer.is_valid():
                chart_data = ChartDataService.create_chart_data(
                    data=deserializer.validated_data
                )
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Chart data created successfully",
                        data=chart_data
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
                    message="An error occurred while creating chart data",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def get(self, request):
        """Handles fetching all chart data."""
        try:
            query_params = validate_query_params(
                query_params=request.query_params,
                valid_query_params=valid_query_params
            )
            chart_data_list = ChartDataService.get_all_chart_data(
                query_params=query_params
            )
            return Response(
                APIResponse.success(
                    code="00",
                    message="Chart data fetched successfully",
                    data=chart_data_list
                ),
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error fetching chart data",
                    error=str(ex)
                ),
                status=ex.status_code
            )


class ChartDataQueryByIDView(APIView):

    def get_permissions(self):
        """Dynamically assigns permissions based on request method."""
        if self.request.method in ["GET", "DELETE"]:
            self.permission_classes = [IsManager]
        elif self.request.method == "PUT":
            self.permission_classes = [IsAllUsers]
        return [permission() for permission in self.permission_classes]

    def get(self, request, chartDataId):
        """Handles fetching a chart data entry by ID."""
        try:
            chart_data = ChartDataService.get_chart_data_by_id(chart_data_id=chartDataId)
            return Response(
                APIResponse.success(
                    code="00",
                    message="Chart data fetched successfully",
                    data=chart_data
                ),
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error fetching chart data",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def put(self, request, chartDataId):
        """Handles updating a chart data entry."""
        try:
            deserializer = ChartDataUpdateSerializer(data=request.data)
            if deserializer.is_valid():
                updated_chart_data = ChartDataService.update_chart_data(
                    chart_data_id=chartDataId,
                    chart_data=deserializer.validated_data
                )
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Chart data updated successfully",
                        data=updated_chart_data
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
                    message="Error updating chart data",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def delete(self, request, chartDataId):
        """Handles deleting a chart data entry."""
        try:
            if ChartDataService.delete_chart_data(chart_data_id=chartDataId):
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Chart data deleted successfully",
                        data={"chart_data_id": chartDataId}
                    ),
                    status=status.HTTP_200_OK
                )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error deleting chart data",
                    error=str(ex)
                ),
                status=ex.status_code
            )
