from rest_framework import status  # type: ignore
from rest_framework.exceptions import AuthenticationFailed, UnsupportedMediaType  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework.views import APIView  # type: ignore
from django.contrib.auth import authenticate, get_user_model  # type: ignore
from rest_framework.permissions import AllowAny  # type: ignore
from django.utils.timezone import now  # type: ignore

from auth_service.utils.token_utils import generate_jwt_token
from auth_service.deserializers import LoginSerializer
from core.utils.responses import APIResponse
from core.utils.format_errors import format_validation_errors as fve

User = get_user_model()

class LoginView(APIView):
    """
    View to authenticate users using their username and password.
    - Generates a JWT access token for authenticated users.
    - Ensures the user's status is active.
    """
    authentication_classes = []
    permission_classes = [AllowAny]

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

                # Retrieve user first
                user = User.objects.filter(username=username).first()

                if user:
                    # Check if user is inactive before authentication
                    if not user.is_active:
                        raise AuthenticationFailed("User account is inactive. Contact system administrator.")

                    # Authenticate user
                    authenticated_user = authenticate(username=username, password=password)
                    if not authenticated_user:
                        raise AuthenticationFailed("Invalid username or password")
                    
                    # Update last login column
                    user.last_login = now()
                    user.save(update_fields=['last_login'])

                    # Generate JWT token
                    token = generate_jwt_token(user)
                    return Response(
                        data=APIResponse.success(
                            '00', 'User successfully logged in', 
                            data={'token': token, 'last_login': user.last_login}
                        ),
                        status=status.HTTP_200_OK,
                        content_type='application/json'
                    )
                else:
                    raise AuthenticationFailed("Invalid username or password")

            return Response(
                data=APIResponse.error('99', "Validation failed", error=fve(serializer.errors)),
                status=status.HTTP_400_BAD_REQUEST,
                content_type='application/json'
            )

        except AuthenticationFailed as auth_ex:
            return Response(
                data=APIResponse.error(code='99', message="Authentication Failure", error=str(auth_ex)),
                status=status.HTTP_401_UNAUTHORIZED,
                content_type='application/json'
            )

        except Exception as ex:
            return Response(
                data=APIResponse.error(code='99', message="An error occurred while logging in the user", error=str(ex)),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type='application/json'
            )
