from rest_framework import serializers  # type: ignore
from custom_admin.models.update import Update
from custom_admin.models.patient import Patient

class UpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating an Update instance."""
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    notes = serializers.CharField()
    dateTaken = serializers.DateField()

    class Meta:
        model = Update
        fields = [
            "updateId", "patient", "notes", "dateTaken",
            "createdAt", "modifiedAt"
        ]
        read_only_fields = ["updateId", "createdAt", "modifiedAt"]


class UpdateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating an Update instance."""
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), required=False)
    notes = serializers.CharField(required=False)
    dateTaken = serializers.DateField(required=False)
    status = serializers.ChoiceField(required=False, choices=['pending', 'declined', 'approved'])

    class Meta:
        model = Update
        fields = [
            "patient", "notes", "dateTaken", "status"
        ]
