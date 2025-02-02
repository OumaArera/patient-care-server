from core.permissions import *
from core.utils.validate_query_params import validate_query_params
from custom_admin.serializers.facility_serializers import *
from rest_framework.views import APIView  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework import status  # type: ignore
from core.utils.responses import APIResponse
from core.utils.query_params import valid_query_params
from custom_admin.services.facility_service import FacilityService
from core.utils.format_errors import format_validation_errors as fve

class FacilityView(APIView):

    def get_permissions(self):
        """Dynamically assigns permissions based on request method."""
        if self.request.method == "POST":
            self.permission_classes = [IsManager]
        elif self.request.method == "GET":
            self.permission_classes = [IsManager]
        return [permission() for permission in self.permission_classes]

    def post(self, request):
        """Handles creating a new facility."""
        try:
            deserializer = FacilitySerializer(data= request.data)
            if deserializer.is_valid():
                facility = FacilityService.create_facility(data=deserializer.validated_data)
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Facility created successfully",
                        data=facility
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
                    message="An error occurred while creating facility",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def get(self, request):
        """Handles fetching facilities."""
        try:
            query_params = validate_query_params(
                query_params=request.query_params,
                valid_query_params=valid_query_params
            )
            facilities = FacilityService.get_all_facilities(
                request=request,
                query_params=query_params
            )
            return Response(
                APIResponse.success(
                    code="00",
                    message="Facilities fetched successfully",
                    data=facilities
                ),
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error fetching facilities",
                    error=str(ex)
                ),
                status=ex.status_code
            )


class FacilityQueryByIDView(APIView):

    def get_permissions(self):
        """Dynamically assigns permissions based on request method."""
        if self.request.method in ["GET", "DELETE"]:
            self.permission_classes = [IsManager]
        elif self.request.method == "PUT":
            self.permission_classes = [IsAllUsers]
        return [permission() for permission in self.permission_classes]

    def get(self, request, facilityId):
        """Handles fetching a facility by ID."""
        try:
            facility = FacilityService.get_facility_by_id(facility_id=facilityId)
            return Response(
                APIResponse.success(
                    code="00",
                    message="Facility fetched successfully",
                    data=facility
                ),
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error fetching facility",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def put(self, request, facilityId):
        """Handles updating a facility."""
        try:
            deserializer = FacilityUpdateSerializer(data = request.data)
            if deserializer.is_valid():
                updated_facility = FacilityService.update_facility(
                    facility_id=facilityId,
                    facility_data=deserializer.validated_data
                )
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Facility updated successfully",
                        data=updated_facility
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
                    message="Error updating facility",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def delete(self, request, facilityId):
        """Handles deleting a facility."""
        try:
            if FacilityService.delete_facility(facility_id=facilityId):
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Facility deleted successfully",
                        data={"facility_id": facilityId}
                    ),
                    status=status.HTTP_200_OK
                )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error deleting facility",
                    error=str(ex)
                ),
                status=ex.status_code
            )
