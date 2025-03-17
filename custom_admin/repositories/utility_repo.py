import logging
from django.db import IntegrityError, DatabaseError
from django.core.exceptions import ValidationError
from core.db_exceptions import *
from core.dtos.utility_dto import UtilityResponseDTO
from core.utils.email_html import EmailHtmlContent
from core.utils.send_email import send_email
from custom_admin.models.utility import Utility

logger = logging.getLogger(__name__)

class UtilityRepository:
    """Handles CRUD operations on the Utility model."""
    
    @staticmethod
    def create_utility(utility_data):
        """Creates a new utility entry in the database and sends notification emails."""
        try:
            new_utility = Utility.create_utility(validated_data=utility_data)
            new_utility.full_clean()
            new_utility.save()

            # Send notification emails
            recipients = [
                {"name": "Ouma Arera", "email": "johnouma999@gmail.com"},
                {"name": "Agnes Atieno", "email": "aluoch.kalal@gmail.com"}
            ]
            staff = f"{new_utility.staff.firstName} {new_utility.staff.lastName}"
            for recipient in recipients:
                html_body = EmailHtmlContent.utility_notification_html(
                    item=new_utility.item,
                    details=new_utility.details,
                    staff=staff,
                    recipient = recipient["name"]
                )
                send_email(
                    recipient_email=recipient["email"],
                    recipient_name=recipient["name"],
                    subject="Utilities Reporting",
                    html_content=html_body
                )
            
            return new_utility
        except ValidationError as ex:
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while creating a new utility: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to create utility.")
        except Exception as ex:
            logger.error(f"Unexpected error while creating a new utility: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while creating utility.")


    @staticmethod
    def get_utility_by_id(utility_id):
        """Fetches details of a utility by ID."""
        try:
            utility = Utility.objects.get(pk=utility_id)
            return utility
        except Utility.DoesNotExist:
            raise NotFoundException(entity_name=f"Utility with ID: {utility_id}")
        except DatabaseError as ex:
            logger.error(f"Database error while fetching utility by ID: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch utility by ID.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching utility by ID: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching utility by ID.")


    @staticmethod
    def get_all_utilities(query_params):
        """Fetches and returns all utilities with optional filtering."""
        try:
            field_mapping = {
                "staff": "staff_id",
                "status": "status__icontains"
            }
            adjusted_filters = {
                field_mapping.get(key, key): value
                for key, value in query_params.items()
                if value
            }

            utilities = Utility.objects.select_related(
                "staff"
            ).filter(
                **adjusted_filters
            ).values(
                "utilityId", "item", "details", "status", "createdAt", "modifiedAt",
                "staff__id", "staff__firstName", "staff__lastName"
            ).order_by("createdAt")

            return [UtilityResponseDTO.transform_utility(utility) for utility in utilities]
        except DatabaseError as ex:
            logger.error(f"Database error while fetching utilities: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch utilities.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching utilities: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching utilities.")


    @staticmethod
    def update_utility(utility_id, utility_data):
        """Updates the details of an existing utility."""
        try:
            utility = UtilityRepository.get_utility_by_id(utility_id=utility_id)
            for field, value in utility_data.items():
                if hasattr(utility, field):
                    setattr(utility, field, value)
            utility.full_clean()
            utility.save()
            return utility
        except NotFoundException as ex:
            raise ex
        except ValidationError as ex:
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while updating utility: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to update utility.")
        except Exception as ex:
            logger.error(f"Unexpected error while updating utility: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while updating utility.")


    @staticmethod
    def delete_utility(utility_id):
        """Deletes a utility record by ID."""
        try:
            utility = UtilityRepository.get_utility_by_id(utility_id=utility_id)
            utility.delete()
            return True
        except NotFoundException as ex:
            raise ex
        except IntegrityError as ex:
            logger.error(f"Integrity error while deleting utility: {ex}", exc_info=True)
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while deleting utility: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to delete utility.")
        except Exception as ex:
            logger.error(f"Unexpected error while deleting utility: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while deleting utility.")


