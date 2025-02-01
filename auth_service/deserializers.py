from rest_framework import serializers # type: ignore
import re

class LoginSerializer(serializers.Serializer):
	"""Validates user input for login"""
	username = serializers.CharField(required=True)
	password = serializers.CharField(required=True, write_only=True, min_length=8)


class ChangePasswordSerializer(serializers.Serializer):
	"""Validates user inputs for password change"""
	currentPassword = serializers.CharField(required=True)
	newPassword = serializers.CharField(required=True, min_length=8, write_only=True)

	def validate_newPassword(self, value):
		"""Validates the new password meets security requirements"""
		if len(value) < 8:
			raise serializers.ValidationError("Password must be at least 8 characters long.")
		if not any(char.isupper() for char in value):
			raise serializers.ValidationError("Password must contain at least one uppercase letter.")
		if not any(char.islower() for char in value):
			raise serializers.ValidationError("Password must contain at least one lowercase letter.")
		if not re.search(r"[@#$%^&+=!]", value): 
			raise serializers.ValidationError("Password must contain at least one special character (@#$%^&+=!).")
		return value
	