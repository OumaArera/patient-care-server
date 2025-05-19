from rest_framework import serializers
from users.models import User
from custom_admin.models.incident import Incident


class IncidentSerializer(serializers.ModelSerializer):
    """Serializer for creating and retrieving an Incident instance."""

    raisedBy = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    assignedTo = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    comments = serializers.JSONField()
    resolvedAt = serializers.DateTimeField(required=False, allow_null=True)

    class Meta:
        model = Incident
        fields = [
            "incidentId", "raisedBy", "assignedTo", "incident", "type", "comments", "status",
            "priority", "resolvedAt", "createdAt", "modifiedAt"
        ]
        read_only_fields = ["incidentId", "createdAt", "modifiedAt", "status", "resolvedAt"]

    def validate_comments(self, value):
        """Ensure comments field contains valid data."""
        if not isinstance(value, list):
            raise serializers.ValidationError("Comments must be a list.")
        return value

    def validate_incident(self, value):
        """Ensure incident field is not empty."""
        if not value or not value.strip():
            raise serializers.ValidationError("Incident field cannot be empty.")
        return value

    def validate(self, data):
        """Optional global validation logic."""
        return data



class IncidentUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating an Incident instance."""

    assignedTo = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    incident = serializers.CharField(required=False)
    type = serializers.CharField(required=False)
    comments = serializers.JSONField(required=False)
    status = serializers.ChoiceField(required=False, choices=[c[0] for c in Incident.STATUS_CHOICES])
    priority = serializers.ChoiceField(required=False, choices=[c[0] for c in Incident.PRIORITY_CHOICES])
    resolvedAt = serializers.DateTimeField(required=False, allow_null=True)

    class Meta:
        model = Incident
        fields = ["assignedTo", "incident", "type", "comments", "status", "priority", "resolvedAt"]

    def validate_comments(self, value):
        """Ensure updated comments are valid if provided."""
        if not isinstance(value, list):
            raise serializers.ValidationError("Comments must be a list.")
        return value
