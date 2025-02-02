from custom_admin.repositories.chart_data_repo import ChartDataRepository
from core.dtos.chart_data_dto import ChartDataResponseDTO


class ChartDataService:
    """Handles the business logic for chart data."""

    @staticmethod
    def create_chart_data(data):
        """Creates a chart data entry in the database."""
        try:
            new_chart_data = ChartDataRepository.create_chart_data(chart_data=data)
            return ChartDataResponseDTO.transform_chart_data(chart_data=new_chart_data)
        except Exception as ex:
            raise ex

    @staticmethod
    def get_chart_data_by_id(chart_data_id):
        """Fetches details of a chart data entry by ID."""
        try:
            chart_data = ChartDataRepository.get_chart_data_by_id(chart_data_id=chart_data_id)
            return ChartDataResponseDTO.transform_chart_data(chart_data=chart_data)
        except Exception as ex:
            raise ex

    @staticmethod
    def get_all_chart_data(request, query_params):
        """Fetches and returns all chart data with optional filters."""
        try:
            query_params.pop("pageSize", None)
            query_params.pop("pageNumber", None)
            chart_data_list = ChartDataRepository.get_all_chart_data(
                request=request, 
                query_params=query_params
            )
            return chart_data_list
        except Exception as ex:
            raise ex

    @staticmethod
    def update_chart_data(chart_data_id, chart_data):
        """Updates an existing chart data entry."""
        try:
            updated_chart_data = ChartDataRepository.update_chart_data(
                chart_data_id=chart_data_id, 
                chart_data=chart_data
            )
            return ChartDataResponseDTO.transform_chart_data(chart_data=updated_chart_data)
        except Exception as ex:
            raise ex

    @staticmethod
    def delete_chart_data(chart_data_id):
        """Deletes a chart data entry by ID."""
        try:
            return ChartDataRepository.delete_chart_data(chart_data_id=chart_data_id)
        except Exception as ex:
            raise ex
