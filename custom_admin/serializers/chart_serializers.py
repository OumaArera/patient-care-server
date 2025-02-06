from core.utils.non_empty_validator import NonEmptyListValidator
from custom_admin.models.chart import Chart
from custom_admin.models.patient import Patient
from rest_framework import serializers # type: ignore
from users.models import User  # type: ignore
from django.utils.timezone import localtime # type: ignore
from django.db.models import Q # type: ignore

class ChartSerializer(serializers.ModelSerializer):
    """Serializer for creating Chart entries."""
    
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), required=True)
    behaviors = serializers.JSONField(validators=[NonEmptyListValidator()], required=True)
    behaviorsDescription = serializers.JSONField(validators=[NonEmptyListValidator()], required=True)
    dateTaken = serializers.DateTimeField(required=True)
    reasonNotFiled = serializers.CharField(required=False)

    class Meta:
        model = Chart
        fields = ["patient", "behaviors", "reasonNotFiled", "behaviorsDescription", "dateTaken"]

    def validate(self, data):
        patient = data.get("patient")
        date_taken = localtime(data.get("dateTaken")).date() 

        if Chart.objects.filter(
            Q(patient=patient) & 
            Q(dateTaken__date=date_taken)
        ).exists():
            raise serializers.ValidationError(
                "A chart entry for this patient already exists on this date."
            )

        return data



class ChartUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating Chart entries, all fields are optional."""
    
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), required=False)
    behaviors = serializers.JSONField(validators=[NonEmptyListValidator()], required=False)
    behaviorsDescription = serializers.JSONField(validators=[NonEmptyListValidator()], required=False)
    dateTaken = serializers.DateTimeField(required=False)
    status = serializers.ChoiceField(required=False, choices=['pending', 'declined', 'approved'])

    class Meta:
        model = Chart
        fields = ["patient", "status", "behaviors", "behaviorsDescription", "dateTaken"]



