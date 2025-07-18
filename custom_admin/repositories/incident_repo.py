import logging
from django.db import IntegrityError, DatabaseError
from django.core.exceptions import ValidationError
from core.db_exceptions import *
from core.dtos.incident_dto import IncidentResponseDTO
from core.utils.email_html import EmailHtmlContent
from core.utils.send_email import send_email
from custom_admin.models.incident import Incident

logger = logging.getLogger(__name__)

class IncidentRepository:
    """Handles CRUD operations on the Incident model."""

    @staticmethod
    def create_incident(incident_data):
        """Creates a new incident entry in the database and sends notification emails."""
        try:
            new_incident = Incident.create_incident(validated_data=incident_data)
            new_incident.full_clean()
            new_incident.save() 
            return new_incident
        except ValidationError as ex:
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while creating a new incident: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to create incident.")
        except Exception as ex:
            logger.error(f"Unexpected error while creating a new incident: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while creating incident.")

    @staticmethod
    def get_incident_by_id(incident_id):
        """Fetches details of an incident by ID."""
        try:
            incident = Incident.objects.get(pk=incident_id)
            return incident
        except Incident.DoesNotExist:
            raise NotFoundException(entity_name=f"Incident with ID: {incident_id}")
        except DatabaseError as ex:
            logger.error(f"Database error while fetching incident by ID: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch incident by ID.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching incident by ID: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching incident by ID.")

    @staticmethod
    def get_all_incidents(query_params):
        """Fetches and returns all incidents with optional filtering."""
        try:
            field_mapping = {
                "raisedBy": "raisedBy__id",
                "assignedTo": "assignedTo__id",
                "type": "type__icontains",
                "status": "status__icontains",
                "priority": "priority__icontains",
                "resolvedAt": "resolvedAt__gte",
                "createdAt": "createdAt__gte"
            }
            adjusted_filters = {
                field_mapping.get(key, key): value
                for key, value in query_params.items()
                if value
            }

            incidents = Incident.objects.select_related("raisedBy", "assignedTo").filter(
                **adjusted_filters
            ).values(
                "incidentId", 
                "raisedBy__id",
                "raisedBy__firstName", 
                "raisedBy__lastName",
                "assignedTo__id",
                "assignedTo__firstName", 
                "assignedTo__lastName",
                "incident", "type",
                "comments", "status", 
                "priority", "resolvedAt", 
                "createdAt",
                "modifiedAt"
            ).order_by("createdAt")

            return [IncidentResponseDTO.transform_incident(incident) for incident in incidents]
        except DatabaseError as ex:
            logger.error(f"Database error while fetching incidents: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch incidents.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching incidents: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching incidents.")

    @staticmethod
    def update_incident(incident_id, incident_data):
        """Updates the details of an existing incident."""
        try:
            incident = IncidentRepository.get_incident_by_id(incident_id=incident_id)
            for field, value in incident_data.items():
                if hasattr(incident, field):
                    setattr(incident, field, value)
            incident.full_clean()
            incident.save()
            return incident
        except NotFoundException as ex:
            raise ex
        except ValidationError as ex:
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while updating incident: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to update incident.")
        except Exception as ex:
            logger.error(f"Unexpected error while updating incident: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while updating incident.")

    @staticmethod
    def delete_incident(incident_id):
        """Deletes an incident record by ID."""
        try:
            incident = IncidentRepository.get_incident_by_id(incident_id=incident_id)
            incident.delete()
            return True
        except NotFoundException as ex:
            raise ex
        except IntegrityError as ex:
            logger.error(f"Integrity error while deleting incident: {ex}", exc_info=True)
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while deleting incident: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to delete incident.")
        except Exception as ex:
            logger.error(f"Unexpected error while deleting incident: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while deleting incident.")
