import phonenumbers  # type: ignore
from rest_framework import serializers  # type: ignore
from users.models import User
import re

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'avatar',
            'firstName',
            'lastName',
            'email',
            'phoneNumber',
            'sex',
            'role',
            'status'
        ]

class UserDeserializer(serializers.Serializer):
    file = serializers.FileField(required=False)
    firstName = serializers.CharField(required=True)
    middleNames = serializers.CharField(required=False, allow_blank=True)
    lastName = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    phoneNumber = serializers.CharField(required=True)
    sex = serializers.ChoiceField(choices=["male", "female", "other"], required=True)
    role = serializers.ChoiceField(choices=["care giver", "manager", "superuser"], required=True)

    def validate_phoneNumber(self, value):
        """Validates that the phone number is a valid international number """
        try:
            parsed_number = phonenumbers.parse(value, None)
            if not phonenumbers.is_valid_number(parsed_number):
                raise serializers.ValidationError("Invalid phone number.")
        except phonenumbers.NumberParseException:
            raise serializers.ValidationError("Invalid phone number format.")
        return value


class UpdateUserDeserializer(serializers.Serializer):
    file = serializers.FileField(required=False)
    firstName = serializers.CharField(required=False)
    middleNames = serializers.CharField(required=False, allow_blank=True)
    lastName = serializers.CharField(required=False)
    password = serializers.CharField(required=False, write_only=True)  # 👈 `write_only=True` so it won’t be returned
    phoneNumber = serializers.CharField(required=False)
    sex = serializers.ChoiceField(choices=["male", "female", "other"], required=False)
    role = serializers.ChoiceField(choices=["care giver", "manager", "superuser"], required=False)

    def validate_phoneNumber(self, value):
        """Validates that the phone number is a valid international number"""
        try:
            parsed_number = phonenumbers.parse(value, None)
            if not phonenumbers.is_valid_number(parsed_number):
                raise serializers.ValidationError("Invalid phone number.")
        except phonenumbers.NumberParseException:
            raise serializers.ValidationError("Invalid phone number format.")
        return value

    def validate_password(self, value):
        """Validates the password meets security requirements"""
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not any(char.islower() for char in value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r"[@#$%^&+=!]", value): 
            raise serializers.ValidationError("Password must contain at least one special character (@#$%^&+=!).")
        return value

