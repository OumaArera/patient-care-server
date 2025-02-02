import logging
from core.db_exceptions import *
from django.db import IntegrityError, DatabaseError  # type: ignore
from django.core.exceptions import ValidationError  # type: ignore
from core.dtos.chart_data_dto import ChartDataResponseDTO
from core.paginator import paginator
from custom_admin.models.chart_data import ChartData

logger = logging.getLogger(__name__)

class ChartDataRepository:
    """Handles the CRUD operations on the ChartData model."""

    @staticmethod
    def create_chart_data(chart_data):
        """Creates chart data in the database."""
        try:
            new_chart_data = ChartData.create_chart_data(validated_data=chart_data)
            new_chart_data.full_clean()
            new_chart_data.save()
            return new_chart_data
        except ValidationError as ex:
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while creating new chart data: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to create chart data.")
        except Exception as ex:
            logger.error(f"Unexpected error while creating new chart data: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while creating chart data.")

    @staticmethod
    def get_chart_data_by_id(chart_data_id):
        """Fetches details of chart data by ID."""
        try:
            chart_data = ChartData.objects.get(pk=chart_data_id)
            return chart_data
        except ChartData.DoesNotExist:
            raise NotFoundException(entity_name=f"ChartData with ID: {chart_data_id}")
        except DatabaseError as ex:
            logger.error(f"Database error while fetching chart data by ID: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch chart data by ID.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching chart data by ID: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching chart data by ID.")

    @staticmethod
    def get_all_chart_data(request, query_params):
        """Fetches and returns all the chart data with optional filtering."""
        try:
            field_mapping = {
                "patient": "patient__patientId",
                "timeToBeTaken": "timeToBeTaken__lte",
            }

            adjusted_filters = {
                field_mapping.get(key, key): value
                for key, value in query_params.items()
                if value
            }

            chart_data = ChartData.objects.select_related(
                "patient"
            ).filter(**adjusted_filters).values(
                "chartDataId", "behaviors", "behaviorsDescription", "timeToBeTaken",
                  "patient__firstName", "patient__lastName"
            ).order_by("createdAt")
            
            chart_data = paginator.paginate_queryset(queryset=chart_data, request=request)
            return [ChartDataResponseDTO.transform_chart_data(data) for data in chart_data]
        except DatabaseError as ex:
            logger.error(f"Database error while fetching chart data: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch chart data.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching chart data: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching chart data.")

    @staticmethod
    def update_chart_data(chart_data_id, chart_data):
        """Updates the details of an existing chart data entry."""
        try:
            data = ChartDataRepository.get_chart_data_by_id(chart_data_id=chart_data_id)
            for field, value in chart_data.items():
                if hasattr(data, field):  
                    setattr(data, field, value)
            data.full_clean()
            data.save()
            return data
        except ValidationError as ex:
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while updating chart data: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to update chart data.")
        except Exception as ex:
            logger.error(f"Unexpected error while updating chart data: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while updating chart data.")

    @staticmethod
    def delete_chart_data(chart_data_id):
        """Deletes chart data record by ID."""
        try:
            data = ChartDataRepository.get_chart_data_by_id(chart_data_id=chart_data_id)
            data.delete()
            return True
        except NotFoundException as ex:
            raise ex
        except IntegrityError as ex:
            logger.error(f"Integrity error while deleting chart data: {ex}", exc_info=True)
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while deleting chart data: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to delete chart data.")
        except Exception as ex:
            logger.error(f"Unexpected error while deleting chart data: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while deleting chart data.")
