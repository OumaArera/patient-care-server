from core.utils.non_empty_validator import *
from custom_admin.models.chart import Chart
from custom_admin.models.patient import Patient
from rest_framework import serializers # type: ignore
from django.utils.timezone import localtime # type: ignore
from django.db.models import Q # type: ignore

class ChartSerializer(serializers.ModelSerializer):
    """Serializer for creating Chart entries."""
    
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), required=True)
    behaviors = serializers.JSONField(validators=[NonEmptyListValidator()], required=True)
    behaviorsDescription = serializers.JSONField(validators=[MedicationTimeValidator()], required=True)
    vitals = serializers.JSONField(validators=[NonEmptyListValidator()], required=False)
    dateTaken = serializers.DateTimeField(required=True)
    reasonFilledLate = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = Chart
        fields = ["patient", "vitals", "behaviors", "behaviorsDescription", "dateTaken", "reasonFilledLate"]

    def validate(self, data):
        patient = data.get("patient")
        date_taken = localtime(data.get("dateTaken"))

        # Extract time portion
        hour = date_taken.hour

        # Ensure time is T04 or T03
        if hour not in [3, 4]:
            date_taken = date_taken.replace(hour=20, minute=0, second=0, microsecond=0)

        # Convert to date for comparison
        date_only = date_taken.date()

        if Chart.objects.filter(
            Q(patient=patient) & 
            Q(dateTaken__date=date_only)
        ).exists():
            raise serializers.ValidationError(
                "A chart entry for this resident already exists on this date."
            )
        
        data["dateTaken"] = date_taken  # Update the dateTaken with modified time
        return data



class ChartUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating Chart entries, all fields are optional."""
    behaviors = serializers.JSONField(validators=[NonEmptyListValidator()], required=False)
    behaviorsDescription = serializers.JSONField(validators=[NonEmptyListValidator()], required=False)
    vitals = serializers.JSONField(validators=[NonEmptyListValidator()], required=False)
    dateTaken = serializers.DateTimeField(required=False)
    reasonEdited = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    status = serializers.ChoiceField(required=False, choices=['pending', 'approved', 'declined', 'updated'])
    declineReason = serializers.CharField(required=False)

    class Meta:
        model = Chart
        fields = ["behaviors", "vitals", "dateTaken", "behaviorsDescription", "reasonEdited",
                  "declineReason","status"
                ]



