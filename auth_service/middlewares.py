from rest_framework.authentication import BaseAuthentication # type: ignore
from rest_framework.exceptions import AuthenticationFailed # type: ignore
from auth_service.exceptions.auth_exceptions import * # type: ignore
from auth_service.utils.token_utils import decode_jwt_token # type: ignore
from users.models import User

class JWTAuthentication(BaseAuthentication):
	def authenticate(self, request):
		"""
		Authenticate the request by validating the JWT token provided in the 'Authorization' header.
		"""
		# Retrieve the token from the Authorization header
		
		auth_header = request.headers.get('Authorization')
		
		if not auth_header:
			raise CustomNotAuthenticated(detail="You are not authenticated. Please login and try again!")

		token = auth_header.split(" ")[1] if auth_header.startswith('Bearer') else None
		
		if not token:
			raise CustomNotAuthenticated(detail="You are not authenticated. Please login and try again!")
		
		payload = decode_jwt_token(token=token)
		
		# Retrieve the user from the payload
		user = self.get_user(user_id=payload.get('user_id'))
		return user, None
	
	@staticmethod
	def get_user(user_id):
		"""
		Fetch the user from the database using the user_id from the decoded payload.
		"""
		try:
			return User.objects.get(id=user_id)
		except User.DoesNotExist:
			raise AuthenticationFailed('User not found')