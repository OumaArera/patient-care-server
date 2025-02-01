from drf_yasg.utils import swagger_auto_schema # type: ignore
from rest_framework import status # type: ignore
from rest_framework.exceptions import AuthenticationFailed, UnsupportedMediaType  # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.views import APIView # type: ignore
from django.contrib.auth import authenticate # type: ignore
from rest_framework.permissions import AllowAny # type: ignore
from django.utils.timezone import now # type: ignore

from auth_service.utils.token_utils import generate_jwt_token
from auth_service.deserializers import LoginSerializer
from core.utils.responses import APIResponse
from core.utils.format_errors import format_validation_errors as fve

class LoginView(APIView):
	"""
	View to authenticate users using their username and password.
	- Generates a JWT access token for authenticated users.
	- Ensures the user's status is active.
	"""
	authentication_classes = []
	permission_classes = [AllowAny]
	
	@swagger_auto_schema(request_body=LoginSerializer, examples={
		"application/json": {
			"username": "TSC789012",
			"password": "Istiwai2025#",
		}
	})
	def post(self, request):
		"""
		Handles user login.
		"""
		try:
			
			if request.content_type != 'application/json':
				raise UnsupportedMediaType(media_type=request.content_type)
				
			serializer = LoginSerializer(data=request.data)
			
			if serializer.is_valid():
				
				username = serializer.validated_data['username']
				password = serializer.validated_data['password']
				
				# Authenticate user using Django's authenticate method
				user = authenticate(username=username, password=password)
				
				if not user:
					raise AuthenticationFailed("Invalid username or password")
				
				if user and not user.is_active:
					raise AuthenticationFailed("User account is inactive. Contact System administrator.")
				
				# Update last login column
				if user:
					user.last_login = now()
					user.save(update_fields=['last_login'])
				
				# Generate JWT token
				token = generate_jwt_token(user)
				return Response(
					data=APIResponse.success('00', 'User successfully logged in', data={'token':token, 'last_login': user.last_login}),
					status=status.HTTP_200_OK,
					content_type='application/json'
				)
			else:
				return Response(
					data=APIResponse.error('99', "Validation failed", error=fve(serializer.errors)),
					status=status.HTTP_400_BAD_REQUEST,
					content_type='application/json'
					
				)
		except Exception as ex:
			return Response(
				data=APIResponse.error('99', "An error occurred while logging in the user", error=ex),
				status=ex.status_code,
				content_type='application/json'
			)