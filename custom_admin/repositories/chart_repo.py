import logging
from core.db_exceptions import *
from django.db import IntegrityError, DatabaseError  # type: ignore
from django.core.exceptions import ValidationError  # type: ignore
from core.dtos.chart_dto import ChartResponseDTO
from core.paginator import paginator
from custom_admin.models.chart import Chart

logger = logging.getLogger(__name__)

class ChartRepository:
    """Handles the CRUD operations on the Chart model."""

    @staticmethod
    def create_chart(chart_data):
        """Creates chart in the database."""
        try:
            new_chart = Chart.create_chart(validated_data=chart_data)
            new_chart.full_clean()
            new_chart.save()
            return new_chart
        except ValidationError as ex:
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while creating new chart: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to create chart.")
        except Exception as ex:
            logger.error(f"Unexpected error while creating new chart: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while creating chart.")

    @staticmethod
    def get_chart_by_id(chart_id):
        """Fetches details of a chart by ID."""
        try:
            chart = Chart.objects.get(pk=chart_id)
            return chart
        except Chart.DoesNotExist:
            raise NotFoundException(entity_name=f"Chart with ID: {chart_id}")
        except DatabaseError as ex:
            logger.error(f"Database error while fetching chart by ID: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch chart by ID.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching chart by ID: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching chart by ID.")

    @staticmethod
    def get_all_charts(request, query_params):
        """Fetches and returns all charts with optional filtering."""
        try:
            field_mapping = {
                "patient": "patient__patientId",
                "dateTaken": "dateTaken",
                "status": "status__icontains"
            }

            adjusted_filters = {
                field_mapping.get(key, key): value
                for key, value in query_params.items()
                if value
            }


            charts = Chart.objects.select_related(
                "patient", "careGiver"
            ).filter(
                **adjusted_filters
            ).values(
                "chartId", "behaviors", 
                "behaviorsDescription", 
                "dateTaken", "vitals",
                "patient__firstName", 
                "patient__lastName", 
                "patient__patientId",
                "patient__branch__branchName",
                "patient__branch__facility__facilityName",
                "careGiver__firstName", 
                "careGiver__lastName",
                "reasonEdited", 
                "createdAt", 
                "modifiedAt"
            ).order_by("createdAt")
            
            charts = paginator.paginate_queryset(queryset=charts, request=request)
            return [ChartResponseDTO.transform_chart(chart) for chart in charts]
        except DatabaseError as ex:
            logger.error(f"Database error while fetching charts: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch charts.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching charts: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching charts.")

    @staticmethod
    def update_chart(chart_id, chart_data):
        """Updates the details of an existing chart entry."""
        try:
            chart = ChartRepository.get_chart_by_id(chart_id=chart_id)
            for field, value in chart_data.items():
                if hasattr(chart, field):  
                    setattr(chart, field, value)
            chart.full_clean()
            chart.save()
            return chart
        except NotFoundException as ex:
            raise ex
        except ValidationError as ex:
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while updating chart: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to update chart.")
        except Exception as ex:
            logger.error(f"Unexpected error while updating chart: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while updating chart.")

    @staticmethod
    def delete_chart(chart_id):
        """Deletes chart record by ID."""
        try:
            chart = ChartRepository.get_chart_by_id(chart_id=chart_id)
            chart.delete()
            return True
        except NotFoundException as ex:
            raise ex
        except IntegrityError as ex:
            logger.error(f"Integrity error while deleting chart: {ex}", exc_info=True)
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while deleting chart: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to delete chart.")
        except Exception as ex:
            logger.error(f"Unexpected error while deleting chart: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while deleting chart.")


