from core.permissions import *
from core.utils.validate_query_params import validate_query_params
from custom_admin.serializers.leave_serializer import *
from rest_framework.views import APIView 
from rest_framework.response import Response  
from rest_framework import status
from core.utils.responses import APIResponse
from core.utils.query_params import valid_query_params
from custom_admin.services.leave_service import *
from core.utils.format_errors import format_validation_errors as fve


class LeaveView(APIView):
    
    permission_classes = [IsAllUsers]

    def post(self, request):
        """Handles creating a new leave request."""
        try:
            deserializer = LeaveSerializer(data=request.data)
            if deserializer.is_valid():
                validated_data = deserializer.validated_data
                validated_data['staff'] = request.user
                new_leave = LeaveService.create_leave(data=validated_data)
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Leave request created successfully",
                        data=new_leave
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
                    message="An error occurred while creating the leave request",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def get(self, request):
        """Handles fetching all leave requests."""
        try:
            query_params = validate_query_params(
                query_params=request.query_params,
                valid_query_params=valid_query_params
            )
            leaves = LeaveService.get_all_leaves(query_params=query_params)
            return Response(
                APIResponse.success(
                    code="00",
                    message="Leave requests fetched successfully",
                    data=leaves
                ),
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error fetching leave requests",
                    error=str(ex)
                ),
                status=ex.status_code
            )


class LeaveQueryByIDView(APIView):

    permission_classes = [IsAllUsers]

    def get(self, request, leaveId):
        """Handles fetching a leave request by ID."""
        try:
            leave = LeaveService.get_leave_by_id(leave_id=leaveId)
            return Response(
                APIResponse.success(
                    code="00",
                    message="Leave request fetched successfully",
                    data=leave
                ),
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error fetching leave request",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def put(self, request, leaveId):
        """Handles updating a leave request."""
        try:
            deserializer = LeaveUpdateSerializer(data=request.data)
            if deserializer.is_valid():
                updated_leave = LeaveService.update_leave(
                    leave_id=leaveId,
                    leave_data=deserializer.validated_data
                )
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Leave request updated successfully",
                        data=updated_leave
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
                    message="Error updating leave request",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def delete(self, request, leaveId):
        """Handles deleting a leave request."""
        try:
            if LeaveService.delete_leave(leave_id=leaveId):
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Leave request deleted successfully",
                        data={"leave_id": leaveId}
                    ),
                    status=status.HTTP_200_OK
                )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error deleting leave request",
                    error=str(ex)
                ),
                status=ex.status_code
            )
