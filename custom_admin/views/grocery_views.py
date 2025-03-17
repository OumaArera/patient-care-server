from core.permissions import IsAllUsers
from core.utils.validate_query_params import validate_query_params
from custom_admin.serializers.grocery_serializer import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.utils.responses import APIResponse
from core.utils.query_params import valid_query_params
from custom_admin.services.grocery_service import GroceryService
from core.utils.format_errors import format_validation_errors as fve


class GroceryView(APIView):
    """Handles creating and fetching grocery requests."""
    
    permission_classes = [IsAllUsers]

    def post(self, request):
        """Handles creating a new grocery request."""
        try:
            deserializer = GrocerySerializer(data=request.data)
            if deserializer.is_valid():
                validated_data = deserializer.validated_data
                validated_data["staff"] = request.user
                new_grocery = GroceryService.create_grocery(data=validated_data)
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Grocery request created successfully",
                        data=new_grocery
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
                    message="An error occurred while creating the grocery request",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def get(self, request):
        """Handles fetching all grocery requests."""
        try:
            query_params = validate_query_params(
                query_params=request.query_params,
                valid_query_params=valid_query_params
            )
            groceries = GroceryService.get_all_groceries(query_params=query_params)
            return Response(
                APIResponse.success(
                    code="00",
                    message="Grocery requests fetched successfully",
                    data=groceries
                ),
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error fetching grocery requests",
                    error=str(ex)
                ),
                status=ex.status_code
            )


class GroceryQueryByIDView(APIView):
    """Handles fetching, updating, and deleting a grocery request by ID."""

    permission_classes = [IsAllUsers]

    def get(self, request, groceryId):
        """Handles fetching a grocery request by ID."""
        try:
            grocery = GroceryService.get_grocery_by_id(grocery_id=groceryId)
            return Response(
                APIResponse.success(
                    code="00",
                    message="Grocery request fetched successfully",
                    data=grocery
                ),
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error fetching grocery request",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def put(self, request, groceryId):
        """Handles updating a grocery request."""
        try:
            deserializer = GroceryUpdateSerializer(data=request.data)
            if deserializer.is_valid():
                updated_grocery = GroceryService.update_grocery(
                    grocery_id=groceryId,
                    grocery_data=deserializer.validated_data
                )
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Grocery request updated successfully",
                        data=updated_grocery
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
                    message="Error updating grocery request",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def delete(self, request, groceryId):
        """Handles deleting a grocery request."""
        try:
            if GroceryService.delete_grocery(grocery_id=groceryId):
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Grocery request deleted successfully",
                        data={"grocery_id": groceryId}
                    ),
                    status=status.HTTP_200_OK
                )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error deleting grocery request",
                    error=str(ex)
                ),
                status=ex.status_code
            )
