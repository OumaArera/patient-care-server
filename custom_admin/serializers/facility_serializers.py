from custom_admin.models.facility import Facility
from rest_framework import serializers # type: ignore
from django.core.validators import RegexValidator  # type: ignore


class FacilitySerializer(serializers.ModelSerializer):
    """Serializer for Facility model with validation on address format."""

    facilityAddress = serializers.CharField(
        required=True,
        validators=[
            RegexValidator(
                regex=r"^\d+\s[A-Za-z\s]+,\s[A-Za-z\s]+,\s[A-Z]{2}\s\d{5}(-\d{4})?$",
                message="Invalid address format. Expected format: '123 Main St, Springfield, IL 62704' "
                        "or '456 Elm Ave, New York, NY 10001-2345'"
            )
        ]
    )

    class Meta:
        model = Facility
        fields = ["facilityName", "facilityAddress"]


class FacilityUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating Facility with optional fields and validation on address if provided."""

    facilityAddress = serializers.CharField(
        required=False,
        validators=[
            RegexValidator(
                regex=r"^\d+\s[A-Za-z\s]+,\s[A-Za-z\s]+,\s[A-Z]{2}\s\d{5}(-\d{4})?$",
                message="Invalid address format. Expected format: '123 Main St, Springfield, IL 62704' "
                        "or '456 Elm Ave, New York, NY 10001-2345'"
            )
        ]
    )
    facilityName = serializers.CharField(required=False)

    class Meta:
        model = Facility
        fields = ["facilityName", "facilityAddress"]