from rest_framework import serializers
from custom_admin.models.utility import Utility

class UtilitySerializer(serializers.ModelSerializer):
    """Serializer for creating a Utility instance."""

    item = serializers.CharField(required=True)
    details = serializers.CharField(required=True, allow_null=True, allow_blank=True)
    status = serializers.ChoiceField(choices=['addressed', 'review', 'pending'], default='pending', read_only=True)

    class Meta:
        model = Utility
        fields = [
            "utilityId", "staff", "item", "details", "status", "createdAt", "modifiedAt"
        ]
        read_only_fields = ["utilityId", "createdAt", "modifiedAt", "status", "staff"]


class UtilityUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating a Utility instance."""

    item = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    details = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    status = serializers.ChoiceField(required=False, choices=['addressed', 'review', 'pending'])

    class Meta:
        model = Utility
        fields = ["item", "details", "status"]
