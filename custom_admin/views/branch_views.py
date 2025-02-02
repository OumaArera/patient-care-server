from core.permissions import *
from core.utils.validate_query_params import validate_query_params
from custom_admin.serializers.branch_serializers import *
from rest_framework.views import APIView  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework import status  # type: ignore
from core.utils.responses import APIResponse
from core.utils.query_params import valid_query_params
from custom_admin.services.branch_service import BranchService
from core.utils.format_errors import format_validation_errors as fve


class BranchView(APIView):

    def get_permissions(self):
        """Dynamically assigns permissions based on request method."""
        if self.request.method == "POST":
            self.permission_classes = [IsManager]
        elif self.request.method == "GET":
            self.permission_classes = [IsManager]
        return [permission() for permission in self.permission_classes]

    def post(self, request):
        """Handles creating a new branch."""
        try:
            deserializer = BranchSerializer(data=request.data)
            if deserializer.is_valid():
                branch = BranchService.create_branch(data=deserializer.validated_data)
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Branch created successfully",
                        data=branch
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
                    message="An error occurred while creating branch",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def get(self, request):
        """Handles fetching branches."""
        try:
            query_params = validate_query_params(
                query_params=request.query_params,
                valid_query_params=valid_query_params
            )
            branches = BranchService.get_all_branches(
                request=request,
                query_params=query_params
            )
            return Response(
                APIResponse.success(
                    code="00",
                    message="Branches fetched successfully",
                    data=branches
                ),
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error fetching branches",
                    error=str(ex)
                ),
                status=ex.status_code
            )


class BranchQueryByIDView(APIView):
    
    def get_permissions(self):
        """Dynamically assigns permissions based on request method."""
        if self.request.method in ["GET", "DELETE"]:
            self.permission_classes = [IsManager]
        elif self.request.method == "PUT":
            self.permission_classes = [IsAllUsers]
        return [permission() for permission in self.permission_classes]

    def get(self, request, branchId):
        """Handles fetching a branch by ID."""
        try:
            branch = BranchService.get_branch_by_id(branch_id=branchId)
            return Response(
                APIResponse.success(
                    code="00",
                    message="Branch fetched successfully",
                    data=branch
                ),
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error fetching branch",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def put(self, request, branchId):
        """Handles updating a branch."""
        try:
            deserializer = BranchUpdateSerializer(data=request.data)
            if deserializer.is_valid():
                updated_branch = BranchService.update_branch(
                    branch_id=branchId,
                    branch_data=deserializer.validated_data
                )
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Branch updated successfully",
                        data=updated_branch
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
                    message="Error updating branch",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def delete(self, request, branchId):
        """Handles deleting a branch."""
        try:
            if BranchService.delete_branch(branch_id=branchId):
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Branch deleted successfully",
                        data={"branch_id": branchId}
                    ),
                    status=status.HTTP_200_OK
                )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error deleting branch",
                    error=str(ex)
                ),
                status=ex.status_code
            )
