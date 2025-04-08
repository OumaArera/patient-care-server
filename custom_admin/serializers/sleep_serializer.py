from rest_framework import serializers
from custom_admin.models.sleep import Sleep
from custom_admin.models import Patient

class SleepSerializer(serializers.ModelSerializer):
    """Serializer for creating a Sleep instance."""

    resident = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), required=True)

    class Meta:
        model = Sleep
        fields = [
            "sleepId", "resident", "markAs", "dateTaken", "markedFor",
            "createdAt", "modifiedAt", "reasonFilledLate"
        ]
        read_only_fields = ["sleepId", "createdAt", "modifiedAt"]

    def validate_markAs(self, value):
        """Validate that the markAs choice is valid."""
        valid_choices = dict(Sleep.SLEEP_CHOICES).keys()
        if value not in valid_choices:
            raise serializers.ValidationError(f"markAs must be one of {list(valid_choices)}")
        return value

    def validate_markedFor(self, value):
        """Validate that the markedFor choice is valid."""
        valid_times = dict(Sleep.TIME_CHOICES).keys()
        if value not in valid_times:
            raise serializers.ValidationError(f"markedFor must be one of {list(valid_times)}")
        return value

    def validate(self, data):
        # Place for any cross-field validation
        return data

class SleepUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating a Sleep instance."""

    resident = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), required=False, allow_null=True)
    markAs = serializers.ChoiceField(choices=Sleep.SLEEP_CHOICES, required=False)
    markedFor = serializers.ChoiceField(choices=Sleep.TIME_CHOICES, required=False)
    dateTaken = serializers.DateField(required=False)

    class Meta:
        model = Sleep
        fields = ["resident", "markAs", "markedFor", "dateTaken"]
