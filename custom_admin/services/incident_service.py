from custom_admin.repositories.incident_repo import IncidentRepository
from core.dtos.incident_dto import IncidentResponseDTO

class IncidentService:
    """Handles the business logic for incidents."""

    @staticmethod
    def create_incident(data):
        """Creates a new incident entry in the database."""
        try:
            new_incident = IncidentRepository.create_incident(incident_data=data)
            return IncidentResponseDTO.transform_incident(incident=new_incident)
        except Exception as ex:
            raise ex

    @staticmethod
    def get_incident_by_id(incident_id):
        """Fetches details of an incident by ID."""
        try:
            incident = IncidentRepository.get_incident_by_id(incident_id=incident_id)
            return IncidentResponseDTO.transform_incident(incident=incident)
        except Exception as ex:
            raise ex

    @staticmethod
    def get_all_incidents(query_params):
        """Fetches and returns all incidents with optional filtering."""
        try:
            query_params.pop("pageSize", None)
            query_params.pop("pageNumber", None)
            incidents = IncidentRepository.get_all_incidents(query_params=query_params)
            return incidents
        except Exception as ex:
            raise ex

    @staticmethod
    def update_incident(incident_id, incident_data):
        """Updates an existing incident entry."""
        try:
            updated_incident = IncidentRepository.update_incident(
                incident_id=incident_id,
                incident_data=incident_data
            )
            return IncidentResponseDTO.transform_incident(incident=updated_incident)
        except Exception as ex:
            raise ex

    @staticmethod
    def delete_incident(incident_id):
        """Deletes an incident entry by ID."""
        try:
            return IncidentRepository.delete_incident(incident_id=incident_id)
        except Exception as ex:
            raise ex
