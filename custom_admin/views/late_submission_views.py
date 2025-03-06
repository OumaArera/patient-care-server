from core.permissions import *
from core.utils.validate_query_params import validate_query_params
from custom_admin.serializers.late_submission_serializer import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.utils.responses import APIResponse
from core.utils.query_params import valid_query_params
from custom_admin.services.late_submission_service import *
from core.utils.format_errors import format_validation_errors as fve


class LateSubmissionView(APIView):

    def get_permissions(self):
        """Dynamically assigns permissions based on request method."""
        if self.request.method == "POST":
            self.permission_classes = [IsManager]
        elif self.request.method == "GET":
            self.permission_classes = [IsAllUsers]
        return [permission() for permission in self.permission_classes]

    def post(self, request):
        """Handles creating a new late submission entry."""
        try:
            deserializer = LateSubmissionSerializer(data=request.data)
            if deserializer.is_valid():
                validated_data = deserializer.validated_data
                validated_data['manager'] = request.user
                new_submission = LateSubmissionService.create_late_submission(data=validated_data)
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Late submission created successfully",
                        data=new_submission
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
                    message="An error occurred while creating the late submission",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def get(self, request):
        """Handles fetching all late submissions."""
        try:
            query_params = validate_query_params(
                query_params=request.query_params,
                valid_query_params=valid_query_params
            )
            submissions = LateSubmissionService.get_all_late_submissions(
                request=request,
                query_params=query_params
            )
            return Response(
                APIResponse.success(
                    code="00",
                    message="Late submissions fetched successfully",
                    data=submissions
                ),
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error fetching late submissions",
                    error=str(ex)
                ),
                status=ex.status_code
            )


class LateSubmissionQueryByIDView(APIView):

    def get_permissions(self):
        """Dynamically assigns permissions based on request method."""
        if self.request.method == "PUT":
            self.permission_classes = [IsManager]
        elif self.request.method == "GET":
            self.permission_classes = [IsAllUsers]
        elif self.request.method == "DELETE":
            self.permission_classes = [IsSuperUser]
        return [permission() for permission in self.permission_classes]

    def get(self, request, submissionId):
        """Handles fetching a late submission by ID."""
        try:
            submission = LateSubmissionService.get_late_submission_by_id(submission_id=submissionId)
            return Response(
                APIResponse.success(
                    code="00",
                    message="Late submission fetched successfully",
                    data=submission
                ),
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error fetching late submission",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def put(self, request, submissionId):
        """Handles updating a late submission."""
        try:
            deserializer = LateSubmissionUpdateSerializer(data=request.data)
            if deserializer.is_valid():
                updated_submission = LateSubmissionService.update_late_submission(
                    submission_id=submissionId,
                    submission_data=deserializer.validated_data
                )
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Late submission updated successfully",
                        data=updated_submission
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
                    message="Error updating late submission",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def delete(self, request, submissionId):
        """Handles deleting a late submission."""
        try:
            if LateSubmissionService.delete_late_submission(submission_id=submissionId):
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Late submission deleted successfully",
                        data={"submission_id": submissionId}
                    ),
                    status=status.HTTP_200_OK
                )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error deleting late submission",
                    error=str(ex)
                ),
                status=ex.status_code
            )