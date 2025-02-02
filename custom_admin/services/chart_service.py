from core.db_exceptions import *
from custom_admin.repositories.chart_repo import ChartRepository
from core.dtos.chart_dto import ChartResponseDTO
from users.models import User


class ChartService:
    """Handles the business logic for charts."""

    @staticmethod
    def create_chart(data):
        """Creates a chart entry in the database."""
        try:
            new_chart = ChartRepository.create_chart(chart_data=data)
            return ChartResponseDTO.transform_chart(chart=new_chart)

        except (NotFoundException, IntegrityException) as ex:
            raise ex
        except Exception as ex:
            raise ex

    @staticmethod
    def get_chart_by_id(chart_id):
        """Fetches details of a chart entry by ID."""
        try:
            chart = ChartRepository.get_chart_by_id(chart_id=chart_id)
            return ChartResponseDTO.transform_chart(chart=chart)
        except Exception as ex:
            raise ex

    @staticmethod
    def get_all_charts(request, query_params):
        """Fetches and returns all charts with optional filters."""
        try:
            query_params.pop("pageSize", None)
            query_params.pop("pageNumber", None)
            chart_list = ChartRepository.get_all_charts(
                request=request, 
                query_params=query_params
            )
            return chart_list
        except Exception as ex:
            raise ex

    @staticmethod
    def update_chart(chart_id, chart_data):
        """Updates an existing chart entry."""
        try:
            updated_chart = ChartRepository.update_chart(
                chart_id=chart_id, 
                chart_data=chart_data
            )
            return ChartResponseDTO.transform_chart(chart=updated_chart)
        except Exception as ex:
            raise ex

    @staticmethod
    def delete_chart(chart_id):
        """Deletes a chart entry by ID."""
        try:
            return ChartRepository.delete_chart(chart_id=chart_id)
        except Exception as ex:
            raise ex
