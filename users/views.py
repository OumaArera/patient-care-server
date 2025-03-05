from core.permissions import *
from core.utils.file_handler import handle_file
from core.utils.validate_query_params import validate_query_params
from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from core.utils.responses import APIResponse
from core.utils.format_errors import format_validation_errors as fve
from core.utils.query_params import valid_query_params
from users.serializers import *
from users.service import UserService

class UserView(APIView):

	def get_permissions(self):
		"""Dynamically assigns permissions based on request method."""
		if self.request.method == "POST":
			self.permission_classes = [IsSuperUser]
		elif self.request.method == "GET":
			self.permission_classes = [IsManager]
		return [permission() for permission in self.permission_classes]


	def post(self, request):
		"""Handles creating a new assignments user."""
		try:
			deserializer = UserDeserializer(data=request.data)
			if deserializer.is_valid():
				validated_data = deserializer.validated_data
				validated_data['username'] = validated_data['email']
				file = validated_data.pop('file', None)
				
				if file:
					validated_data['avatar'] = handle_file(file=file, directory='resources')
				
				if validated_data.get('role') == "superuser":
					user = UserService.create_super_user(
						superuser_data=validated_data
                    )
				else:
					user = UserService.create_user(
						data=validated_data
                    )
				serialized_user = UserSerializer(instance=user)
				return Response(
					APIResponse.success(
						code="00",
						message="User created successfully",
						data=serialized_user.data
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
					message="An error occurred while creating user",
					error=ex),
				status=ex.status_code
			)
	
	def get(self, request):
		"""Handles fetching users."""
		try:
			query_params = validate_query_params(
				query_params=request.query_params,
				valid_query_params=valid_query_params
			)
			users = UserService.get_all_users(
				query_params=query_params,
				)
			return Response(
				APIResponse.success(
					code="00",
					message="Users fetched successfully",
					data=users
				),
				status=status.HTTP_200_OK
			)
		except Exception as ex:
			return Response(
				APIResponse.error(
					code="99",
					message="Error fetching Users",
					error=ex
				),
				status=ex.status_code
			)
		
class UserQueryByIDView(APIView):

    def get_permissions(self):
        """Dynamically assigns permissions based on request method."""
        if self.request.method == "DELETE" or self.request.method == "GET":
            self.permission_classes = [IsSuperUser]
        elif self.request.method == "PUT":
            self.permission_classes = [IsAllUsers]
        return [permission() for permission in self.permission_classes]
	

    def get(self, request, userId):
        """Handles fetching User."""
        try:
            user = UserService.get_user_by_id(
                user_id=userId
            )
            return Response(
                APIResponse.success(
                    code="00",
                    message="User fetched successfully",
                    data=user
                ),
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error fetching user",
                    error=ex),
                status=ex.status_code
            )

    def put(self, request, userId):
        """Handles updating an user."""
        try:
            deserializer = UpdateUserDeserializer(data=request.data)
            if deserializer.is_valid():
                validated_data = deserializer.validated_data
                file = validated_data.pop('file', None)
                if file:
                    validated_data['avatar'] = handle_file(file=file, directory='resources')
                updated_user = UserService.update_user(
                    user_id=userId,
                    user_data=validated_data
                )
                return Response(
                    APIResponse.success(
                        code="00",
                        message="User updated successfully",
                        data=updated_user
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
                    message="Error updating user",
                    error=str(ex)),
                status=ex.status_code
            )

    def delete(self, request, userId):
        """Handles deleting a user."""
        try:
            if UserService.delete_user(
                user_id=userId
            ):
                return Response(
                    APIResponse.success(
                        code="00",
                        message="User deleted successfully",
                        data={"catalogue_id": userId}
                    ),
                    status=status.HTTP_200_OK
                )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99", 
                    message="Error deleting user", 
                    error=str(ex)
                ),
                status=ex.status_code
            )