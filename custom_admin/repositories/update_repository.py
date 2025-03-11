import logging
from django.db import IntegrityError, DatabaseError  # type: ignore
from django.core.exceptions import ValidationError  # type: ignore
from core.db_exceptions import *
from core.paginator import paginator
from core.dtos.update_dto import UpdateResponseDTO  # Import the DTO
from core.utils.email_html import EmailHtmlContent
from core.utils.send_email import send_email
from custom_admin.models.update import Update

logger = logging.getLogger(__name__)

class UpdateRepository:
    """Handles CRUD operations on the Update model."""

    @staticmethod
    def create_update(update_data):
        """Creates a new update entry in the database."""
        try:
            new_update = Update.create_update(validated_data=update_data)
            new_update.full_clean()
            new_update.save()
            return new_update
        except ValidationError as ex:
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while creating a new update: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to create update.")
        except Exception as ex:
            logger.error(f"Unexpected error while creating a new update: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while creating update.")

    @staticmethod
    def get_update_by_id(update_id):
        """Fetches details of an update by ID."""
        try:
            update = Update.objects.get(pk=update_id)
            return update
        except Update.DoesNotExist:
            raise NotFoundException(entity_name=f"Update with ID: {update_id}")
        except DatabaseError as ex:
            logger.error(f"Database error while fetching update by ID: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch update by ID.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching update by ID: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching update by ID.")

    @staticmethod
    def get_all_updates(request, query_params):
        """Fetches and returns all updates with optional filtering."""
        try:
            field_mapping = {
                "patient": "patient_id",
                "careGiver": "careGiver_id",
                "dateTaken": "dateTaken",
                "status": "status__icontains",
                "type": "type__icontains"
            }

            adjusted_filters = {
                field_mapping.get(key, key): value
                for key, value in query_params.items()
                if value
            }

            updates = Update.objects.select_related(
                "patient", 
                "careGiver"
            ).filter(
                **adjusted_filters
            ).values(
                "updateId", 
                "notes", 
                "dateTaken", 
                "createdAt", 
                "modifiedAt",
                "type",
                "weight",
                "weightDeviation",
                "patient__patientId", 
                "patient__firstName",
                "patient__lastName",
                "patient__branch__facility__facilityName",
                "patient__branch__branchName",
                "careGiver",
                "careGiver__firstName",
                "careGiver__lastName",
                "reasonEdited",
                "reasonFilledLate",
                "declineReason",
                "status"
            ).order_by(
                "dateTaken"
            )

            updates = paginator.paginate_queryset(queryset=updates, request=request)
            return [UpdateResponseDTO.transform_update(update) for update in updates]
        except DatabaseError as ex:
            logger.error(f"Database error while fetching updates: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch updates.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching updates: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching updates.")

    @staticmethod
    def update_update(update_id, update_data):
        """Updates the details of an existing update."""
        try:
            update = UpdateRepository.get_update_by_id(update_id=update_id)
            status_updated = True
            for field, value in update_data.items():
                if hasattr(update, field):
                    if field == "status" and getattr(update, field) != value:
                        status_updated = True
                    setattr(update, field, value)
            update.full_clean()
            update.save()

            if status_updated:
                patientName = f"{update.patient.firstName} {update.patient.lastName}"
                html_body = EmailHtmlContent.chart_update_html(
                    update.careGiver.firstName,
                    patientName,
                    update.status
                )

                send_email(
                    recipient_email=update.careGiver.username,
                    recipient_name=update.careGiver.firstName,
                    subject=f"Update for {update.patient.firstName} {update.patient.lastName}",
                    html_content=html_body
                )

            return update
        except ValidationError as ex:
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while updating update: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to update update.")
        except Exception as ex:
            logger.error(f"Unexpected error while updating update: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while updating update.")

    @staticmethod
    def delete_update(update_id):
        """Deletes an update record by ID."""
        try:
            update = UpdateRepository.get_update_by_id(update_id=update_id)
            update.delete()
            return True
        except NotFoundException as ex:
            raise ex
        except IntegrityError as ex:
            logger.error(f"Integrity error while deleting update: {ex}", exc_info=True)
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while deleting update: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to delete update.")
        except Exception as ex:
            logger.error(f"Unexpected error while deleting update: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while deleting update.")
