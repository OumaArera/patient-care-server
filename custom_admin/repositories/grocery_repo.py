import logging
from django.db import IntegrityError, DatabaseError
from django.core.exceptions import ValidationError
from core.db_exceptions import *
from core.dtos.grocery_dto import GroceryResponseDTO
from core.utils.email_html import EmailHtmlContent
from core.utils.send_email import send_email
from custom_admin.models.grocery import Grocery

logger = logging.getLogger(__name__)

class GroceryRepository:
    """Handles CRUD operations on the Grocery model."""

    @staticmethod
    def create_grocery(grocery_data):
        """Creates a new grocery entry in the database and sends notification emails."""
        try:
            new_grocery = Grocery.create_grocery(validated_data=grocery_data)
            new_grocery.full_clean()
            new_grocery.save()

            # Send notification emails
            recipients = [
                {"name": "Ouma Arera", "email": "johnouma999@gmail.com"},
                {"name": "Agnes Atieno", "email": "aluoch.kalal@gmail.com"}
            ]
            staff = f"{new_grocery.staff.firstName} {new_grocery.staff.lastName}" if new_grocery.staff else "Unknown Staff"
            for recipient in recipients:
                html_body = EmailHtmlContent.grocery_notification_html(
                    details=new_grocery.details,
                    branch = new_grocery.branch.branchName,
                    staff=staff,
                    recipient=recipient["name"]
                )
                send_email(
                    recipient_email=recipient["email"],
                    recipient_name=recipient["name"],
                    subject="Grocery Reporting",
                    html_content=html_body
                )
            
            return new_grocery
        except ValidationError as ex:
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while creating a new grocery: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to create grocery.")
        except Exception as ex:
            logger.error(f"Unexpected error while creating a new grocery: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while creating grocery.")

    @staticmethod
    def get_grocery_by_id(grocery_id):
        """Fetches details of a grocery by ID."""
        try:
            grocery = Grocery.objects.get(pk=grocery_id)
            return grocery
        except Grocery.DoesNotExist:
            raise NotFoundException(entity_name=f"Grocery with ID: {grocery_id}")
        except DatabaseError as ex:
            logger.error(f"Database error while fetching grocery by ID: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch grocery by ID.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching grocery by ID: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching grocery by ID.")

    @staticmethod
    def get_all_groceries(query_params):
        """Fetches and returns all groceries with optional filtering."""
        try:
            field_mapping = {
                "staff": "staff_id",
                "feedback": "feedback__icontains"
            }
            adjusted_filters = {
                field_mapping.get(key, key): value
                for key, value in query_params.items()
                if value
            }

            groceries = Grocery.objects.select_related(
                "staff", "branch"
            ).filter(
                **adjusted_filters
            ).values(
                "groceryId", "details", "feedback", "createdAt", "modifiedAt",
                "staff__id", "staff__firstName", "staff__lastName", "status", "branch__branchName"
            ).order_by("createdAt")

            return [GroceryResponseDTO.transform_grocery(grocery) for grocery in groceries]
        except DatabaseError as ex:
            logger.error(f"Database error while fetching groceries: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch groceries.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching groceries: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching groceries.")

    @staticmethod
    def update_grocery(grocery_id, grocery_data):
        """Updates the details of an existing grocery."""
        try:
            grocery = GroceryRepository.get_grocery_by_id(grocery_id=grocery_id)
            for field, value in grocery_data.items():
                if hasattr(grocery, field):
                    setattr(grocery, field, value)
            grocery.full_clean()
            grocery.save()
            return grocery
        except NotFoundException as ex:
            raise ex
        except ValidationError as ex:
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while updating grocery: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to update grocery.")
        except Exception as ex:
            logger.error(f"Unexpected error while updating grocery: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while updating grocery.")

    @staticmethod
    def delete_grocery(grocery_id):
        """Deletes a grocery record by ID."""
        try:
            grocery = GroceryRepository.get_grocery_by_id(grocery_id=grocery_id)
            grocery.delete()
            return True
        except NotFoundException as ex:
            raise ex
        except IntegrityError as ex:
            logger.error(f"Integrity error while deleting grocery: {ex}", exc_info=True)
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while deleting grocery: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to delete grocery.")
        except Exception as ex:
            logger.error(f"Unexpected error while deleting grocery: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while deleting grocery.")