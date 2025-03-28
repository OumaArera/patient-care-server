from core.permissions import IsAllUsers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.utils.responses import APIResponse
from custom_admin.services.assessment_service import AssessmentService
from core.utils.format_errors import format_validation_errors as fve
from custom_admin.serializers.assessment_serializer import *


class AssessmentView(APIView):
    """Handles creating and fetching assessment records."""
    
    permission_classes = [IsAllUsers]

    def post(self, request):
        """Handles creating a new assessment record."""
        try:
            deserializer = AssessmentSerializer(data=request.data)
            if deserializer.is_valid():
                validated_data = deserializer.validated_data
                new_assessment = AssessmentService.create_assessment(data=validated_data)
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Assessment record created successfully",
                        data=new_assessment
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
                    message="An error occurred while creating the assessment record",
                    error=str(ex)
                ),
                status=getattr(ex, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
            )

    def get(self, request):
        """Handles fetching all due assessments."""
        try:
            assessments = AssessmentService.get_due_assessments()
            return Response(
                APIResponse.success(
                    code="00",
                    message="Due assessments fetched successfully",
                    data=assessments
                ),
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error fetching due assessments",
                    error=str(ex)
                ),
                status=getattr(ex, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
            )


class AssessmentQueryByIDView(APIView):
    """Handles fetching, updating, and deleting an assessment record by ID."""

    permission_classes = [IsAllUsers]

    def get(self, request, assessmentId):
        """Handles fetching an assessment record by ID."""
        try:
            assessment = AssessmentService.get_assessment_by_id(assessment_id=assessmentId)
            return Response(
                APIResponse.success(
                    code="00",
                    message="Assessment record fetched successfully",
                    data=assessment
                ),
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error fetching assessment record",
                    error=str(ex)
                ),
                status=getattr(ex, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
            )

    def put(self, request, assessmentId):
        """Handles updating an assessment record."""
        try:
            deserializer = AssessmentUpdateSerializer(data=request.data)
            if deserializer.is_valid():
                updated_assessment = AssessmentService.update_assessment(
                    assessment_id=assessmentId,
                    assessment_data=deserializer.validated_data
                )
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Assessment record updated successfully",
                        data=updated_assessment
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
                    message="Error updating assessment record",
                    error=str(ex)
                ),
                status=getattr(ex, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
            )

    def delete(self, request, assessmentId):
        """Handles deleting an assessment record."""
        try:
            if AssessmentService.delete_assessment(assessment_id=assessmentId):
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Assessment record deleted successfully",
                        data={"assessment_id": assessmentId}
                    ),
                    status=status.HTTP_200_OK
                )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error deleting assessment record",
                    error=str(ex)
                ),
                status=getattr(ex, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
            )


class AssessmentNotificationSchedulerView(APIView):
    """Handles scheduling notifications for assessments."""
    
    permission_classes = [IsAllUsers]

    def get(self, request):
        """Triggers scheduled email notifications for assessments."""
        try:
            AssessmentService.schedule_assessment_notifications()
            return Response(
                APIResponse.success(
                    code="00",
                    message="Assessment notifications scheduled successfully",
                    data={"assessment": "Success"}
                ),
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error scheduling assessment notifications",
                    error=str(ex)
                ),
                status=getattr(ex, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
            )
