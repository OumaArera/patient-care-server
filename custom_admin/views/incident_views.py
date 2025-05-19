from core.permissions import IsAllUsers
from core.utils.validate_query_params import validate_query_params
from custom_admin.serializers.incident_serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.utils.responses import APIResponse
from core.utils.query_params import valid_query_params
from custom_admin.services.incident_service import IncidentService
from core.utils.format_errors import format_validation_errors as fve


class IncidentView(APIView):
    """Handles creating and fetching incident reports."""
    
    permission_classes = [IsAllUsers]

    def post(self, request):
        """Handles creating a new incident report."""
        try:
            deserializer = IncidentSerializer(data=request.data)
            if deserializer.is_valid():
                validated_data = deserializer.validated_data
                validated_data["raisedBy"] = request.user 
                new_incident = IncidentService.create_incident(data=validated_data)
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Incident report created successfully",
                        data=new_incident
                    ),
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    APIResponse.error(
                        code="99",
                        message="Validation failed",
                        error=fve(deserializer.errors)
                    ),
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="An error occurred while creating the incident report",
                    error=str(ex)
                ),
                status=getattr(ex, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
            )

    def get(self, request):
        """Handles fetching all incident reports."""
        try:
            query_params = validate_query_params(
                query_params=request.query_params,
                valid_query_params=valid_query_params
            )
            incidents = IncidentService.get_all_incidents(query_params=query_params)
            return Response(
                APIResponse.success(
                    code="00",
                    message="Incident reports fetched successfully",
                    data=incidents
                ),
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error fetching incident reports",
                    error=str(ex)
                ),
                status=getattr(ex, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
            )


class IncidentQueryByIDView(APIView):
    """Handles fetching, updating, and deleting an incident report by ID."""

    permission_classes = [IsAllUsers]

    def get(self, request, incidentId):
        """Handles fetching an incident report by ID."""
        try:
            incident = IncidentService.get_incident_by_id(incident_id=incidentId)
            return Response(
                APIResponse.success(
                    code="00",
                    message="Incident report fetched successfully",
                    data=incident
                ),
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error fetching incident report",
                    error=str(ex)
                ),
                status=getattr(ex, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
            )

    def put(self, request, incidentId):
        """Handles updating an incident report."""
        try:
            deserializer = IncidentUpdateSerializer(data=request.data)
            if deserializer.is_valid():
                updated_incident = IncidentService.update_incident(
                    incident_id=incidentId,
                    incident_data=deserializer.validated_data
                )
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Incident report updated successfully",
                        data=updated_incident
                    ),
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    APIResponse.error(
                        code="99",
                        message="Validation failed",
                        error=fve(deserializer.errors)
                    ),
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error updating incident report",
                    error=str(ex)
                ),
                status=getattr(ex, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
            )

    def delete(self, request, incidentId):
        """Handles deleting an incident report."""
        try:
            if IncidentService.delete_incident(incident_id=incidentId):
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Incident report deleted successfully",
                        data={"incident_id": incidentId}
                    ),
                    status=status.HTTP_200_OK
                )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error deleting incident report",
                    error=str(ex)
                ),
                status=getattr(ex, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
            )
