from django.utils import timezone # type: ignore
from rest_framework import status # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.views import APIView # type: ignore
from django.contrib.auth import authenticate # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore
from rest_framework.exceptions import ValidationError # type: ignore
from rest_framework.exceptions import AuthenticationFailed # type: ignore

from auth_service.deserializers import ChangePasswordSerializer
from core.utils.responses import APIResponse
from core.utils.format_errors import format_validation_errors as fve

class ChangePasswordView(APIView):
	"""
	View to change the user's password.
	The user must be logged in and provide the current password for validation.
	A new password should be provided and will replace the current password.
	"""
	permission_classes = [IsAuthenticated]
	
	def post(self, request):
		try:
			# 1. Get the current logged-in user
			logged_in_user = request.user
			
			# 2. Validate the user input
			serializer = ChangePasswordSerializer(data=request.data)
			
			# 3. If the validation is successful
			if serializer.is_valid():
				# 4. Get validated data from the serializer
				current_password = serializer.validated_data['currentPassword']
				new_password = serializer.validated_data['newPassword']
				
				# 5. Check if current and new passwords are matching
				if current_password == new_password:
					raise ValidationError("Your old password and new password cannot be the same")
					
				# 6. Authenticate the user with the current password
				user = authenticate(username=logged_in_user.username, password=current_password)
				if user is None:
					raise ValidationError("Current password is incorrect")
				
				if user and not user.is_active:
					raise AuthenticationFailed("User account is inactive. Contact System administrator.")
					
				# 7. Update the password
				user.set_password(new_password)
				user.modified_at = timezone.now()
				user.save()
				
				data = {
					'user':{
						'username': user.username,
						'role': user.role
					}
				}
				# 8. Return success response to the client
				return Response(
					data=APIResponse.success('00', "Password changed successfully", data=data),
					status=status.HTTP_200_OK
				)
			# 9. Return error response to the client is validation has failed
			else:
				return Response(
					data=APIResponse.error('99', "Validation failed", error=fve(serializer.errors)),
					status=status.HTTP_400_BAD_REQUEST
				)
		# 10. Return error response to the client in case any other error has occurred
		except Exception as ex:
			return Response(
				data=APIResponse.error('99','Error occurred while changing the user password', error=ex),
				status=ex.status_code
			)