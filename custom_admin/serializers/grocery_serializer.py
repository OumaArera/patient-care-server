from rest_framework import serializers
from custom_admin.models.branch import Branch
from custom_admin.models.grocery import Grocery
from users.models import User


class GrocerySerializer(serializers.ModelSerializer):
    """Serializer for creating a Grocery instance."""

    details = serializers.JSONField()
    branch = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all(), required=True)

    class Meta:
        model = Grocery
        fields = [
            "groceryId", "staff", "details", "status", "feedback", "feedback", "createdAt", "modifiedAt",
            "branch"
        ]
        read_only_fields = ["groceryId", "createdAt", "feedback", "status", "staff", "modifiedAt"]

    def validate_details(self, value):
        """Ensure details field contains valid data."""
        if not isinstance(value, list):
            raise serializers.ValidationError("Details must be a list.")
        if not value:
            raise serializers.ValidationError("Details cannot be empty.")
        return value

    def validate(self, data):
        """Additional validation if needed."""
        return data


class GroceryUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating a Grocery instance."""

    staff = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    details = serializers.JSONField(required=False)
    feedback = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    status = serializers.ChoiceField(required=False, choices=['pending', 'updated', 'approved', 'updated'])

    class Meta:
        model = Grocery
        fields = ["staff", "details", "status", "feedback"]
