from core.db_exceptions import ValidationException
from core.utils.send_email import send_email
from core.utils.generate_random_password import generate_random_password
from rest_framework.response import Response # type: ignore
from rest_framework.views import APIView # type: ignore
from rest_framework.exceptions import * # type: ignore
from rest_framework.permissions import AllowAny # type: ignore
from rest_framework import status # type: ignore
from auth_service.utils.password_utils import *
from users.repository import UserRepository
from core.utils.responses import APIResponse


class ResetPasswordView(APIView):
	"""
	View to handle reset password functionality
	"""
	authentication_classes = []
	permission_classes = [AllowAny]
	def post(self, request):
		try:
			username = request.data.get("username", None)
			
			if not username:
				raise ValidationException(
					message="'username' field and value are required. Please check and try again")
			
			new_password = generate_random_password()
			new_password = "Password2025!"
			updated_user = UserRepository.update_user_password(
				username=username,
				password=new_password
			)
			html_content = EmailHtmlContent.reset_password_html(
                password=new_password,
                username=updated_user.username,
                recipient=updated_user.firstName
            )
			send_email(
				recipient_email=updated_user.username, 
				recipient_name=updated_user.firstName, 
				subject="Password Reset", 
				html_content=html_content
			)
			
			data = {
				'target_user': {
					'username': updated_user.username,
					'email': updated_user.email,
					'name': f"{updated_user.firstName} {updated_user.lastName}",
					'role': updated_user.role
				}
			}
	
			return Response(
				data=APIResponse.success(
					code='00', 
					message='Check your email/sms for your new password', 
					data=data
				),
				status=status.HTTP_200_OK
			)
			
		except Exception as ex:
			return Response(
				data=APIResponse.error(
					code='06', 
					message='Error occurred while resetting your password', 
					error=ex
				),
				status=ex.status_code
			)
		
