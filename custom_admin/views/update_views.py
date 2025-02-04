from core.permissions import *
from core.utils.validate_query_params import validate_query_params
from custom_admin.serializers.update_serializers import *
from rest_framework.views import APIView  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework import status  # type: ignore
from core.utils.responses import APIResponse
from core.utils.query_params import valid_query_params
from custom_admin.services.update_service import *
from core.utils.format_errors import format_validation_errors as fve


class UpdateView(APIView):

    def get_permissions(self):
        """Dynamically assigns permissions based on request method."""
        if self.request.method == "POST":
            self.permission_classes = [IsCareGiver]
        elif self.request.method == "GET":
            self.permission_classes = [IsAllUsers]
        return [permission() for permission in self.permission_classes]

    def post(self, request):
        """Handles creating a new update."""
        try:
            deserializer = UpdateSerializer(data=request.data)
            if deserializer.is_valid():
                validated_data = deserializer.validated_data
                validated_data['careGiver'] = request.user
                new_update = UpdateService.create_update(data=validated_data)
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Update created successfully",
                        data=new_update
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
                    message="An error occurred while creating the update",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def get(self, request):
        """Handles fetching all updates."""
        try:
            query_params = validate_query_params(
                query_params=request.query_params,
                valid_query_params=valid_query_params
            )
            updates = UpdateService.get_all_updates(
                request=request, 
                query_params=query_params
            )
            return Response(
                APIResponse.success(
                    code="00",
                    message="Updates fetched successfully",
                    data=updates
                ),
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error fetching updates",
                    error=str(ex)
                ),
                status=ex.status_code
            )


class UpdateQueryByIDView(APIView):

    def get_permissions(self):
        """Dynamically assigns permissions based on request method."""
        if self.request.method == "PUT":
            self.permission_classes = [IsCareGiver]
        elif self.request.method == "GET":
            self.permission_classes = [IsAllUsers]
        elif self.request.method == "DELETE":
            self.permission_classes = [IsSuperUser]
        return [permission() for permission in self.permission_classes]

    def get(self, request, updateId):
        """Handles fetching an update by ID."""
        try:
            update = UpdateService.get_update_by_id(update_id=updateId)
            return Response(
                APIResponse.success(
                    code="00",
                    message="Update fetched successfully",
                    data=update
                ),
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error fetching update",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def put(self, request, updateId):
        """Handles updating an update."""
        try:
            deserializer = UpdateUpdateSerializer(data=request.data)
            if deserializer.is_valid():
                updated_update = UpdateService.update_update(
                    update_id=updateId,
                    update_data=deserializer.validated_data
                )
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Update updated successfully",
                        data=updated_update
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
                    message="Error updating update",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def delete(self, request, updateId):
        """Handles deleting an update."""
        try:
            if UpdateService.delete_update(update_id=updateId):
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Update deleted successfully",
                        data={"update_id": updateId}
                    ),
                    status=status.HTTP_200_OK
                )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error deleting update",
                    error=str(ex)
                ),
                status=ex.status_code
            )
