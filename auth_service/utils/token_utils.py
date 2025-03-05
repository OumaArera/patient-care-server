import jwt # type: ignore
from django.utils import timezone # type: ignore

from patient_project.settings import *
from auth_service.exceptions.auth_exceptions import *

def generate_jwt_token(user):
	"""
	Generate a JWT access token for the given user.
	"""
	payload = {
		"user_id": user.id,
		"username": user.username,
		"branch": user.branch.branchId if user.branch else None,
		"fullName": f"{user.firstName} {user.lastName}",
		"role": user.role,
		"iss": JWT_ISSUER,
		"aud": JWT_AUDIENCE,
		"exp": timezone.now() + timedelta(minutes=int(JWT_EXPIRATION_MINUTES)),
		"iat": timezone.now(),
	}
	token = jwt.encode(
		payload=payload,
		key=SECRET_KEY,
		algorithm=JWT_ALGORITHM
	)
	return token

def decode_jwt_token(token: str):
	"""
	Decodes a JWT token and returns the payload.
	"""
	try:
		payload = jwt.decode(
			jwt=token,
			key=SECRET_KEY,
			algorithms=JWT_ALGORITHM,
			audience=JWT_AUDIENCE,
			issuer=JWT_ISSUER
		)
		return payload
	except jwt.ExpiredSignatureError:
		raise CustomNotAuthenticated("Token has expired")
	except jwt.InvalidTokenError:
		raise CustomNotAuthenticated("Invalid token")