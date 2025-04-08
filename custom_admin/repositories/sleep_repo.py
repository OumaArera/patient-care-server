import logging
from django.db import IntegrityError, DatabaseError
from django.core.exceptions import ValidationError
from core.db_exceptions import *
from custom_admin.models.sleep import Sleep 

logger = logging.getLogger(__name__)

class SleepRepository:
    """Handles CRUD operations on the Sleep model."""

    @staticmethod
    def create_sleep(sleep_data):
        """Creates a new sleep entry in the database."""
        try:
            new_sleep = Sleep.create_sleep_entry(validated_data=sleep_data)
            new_sleep.full_clean()
            new_sleep.save()
            return new_sleep
        except ValidationError as ex:
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while creating a new sleep entry: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to create sleep entry.")
        except Exception as ex:
            logger.error(f"Unexpected error while creating a new sleep entry: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while creating sleep entry.")

    @staticmethod
    def get_sleep_by_id(sleep_id):
        """Fetches a sleep entry by ID."""
        try:
            sleep = Sleep.objects.select_related("resident").get(pk=sleep_id)
            return sleep
        except Sleep.DoesNotExist:
            raise NotFoundException(entity_name=f"Sleep with ID: {sleep_id}")
        except DatabaseError as ex:
            logger.error(f"Database error while fetching sleep entry by ID: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch sleep entry.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching sleep entry by ID: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching sleep entry.")

    @staticmethod
    def get_all_sleeps(query_params):
        """Fetches and returns all sleep entries with optional filtering."""
        try:
            field_mapping = {
                "resident": "resident_id",
                "markAs": "markAs",
                "dateTaken": "dateTaken",
            }

            filters = {
                field_mapping.get(key, key): value
                for key, value in query_params.items()
                if value
            }

            sleeps = Sleep.objects.select_related("resident").filter(
                **filters
            ).values(
                "sleepId", "markAs", "dateTaken", "markedFor",
                "createdAt", "modifiedAt", "reasonFilledLate",
                "resident__patientId", "resident__firstName", "resident__lastName"
            ).order_by("-createdAt")

            return list(sleeps)
        except DatabaseError as ex:
            logger.error(f"Database error while fetching sleep entries: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch sleep entries.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching sleep entries: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching sleep entries.")

    @staticmethod
    def update_sleep(sleep_id, sleep_data):
        """Updates the details of an existing sleep entry."""
        try:
            sleep = SleepRepository.get_sleep_by_id(sleep_id=sleep_id)
            for field, value in sleep_data.items():
                if hasattr(sleep, field):
                    setattr(sleep, field, value)
            sleep.full_clean()
            sleep.save()
            return sleep
        except NotFoundException as ex:
            raise ex
        except ValidationError as ex:
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while updating sleep entry: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to update sleep entry.")
        except Exception as ex:
            logger.error(f"Unexpected error while updating sleep entry: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while updating sleep entry.")

    @staticmethod
    def delete_sleep(sleep_id):
        """Deletes a sleep entry by ID."""
        try:
            sleep = SleepRepository.get_sleep_by_id(sleep_id=sleep_id)
            sleep.delete()
            return True
        except NotFoundException as ex:
            raise ex
        except IntegrityError as ex:
            logger.error(f"Integrity error while deleting sleep entry: {ex}", exc_info=True)
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while deleting sleep entry: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to delete sleep entry.")
        except Exception as ex:
            logger.error(f"Unexpected error while deleting sleep entry: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while deleting sleep entry.")
