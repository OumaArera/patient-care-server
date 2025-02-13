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
    vitals = serializers.JSONField(validators=[NonEmptyListValidator()], required=True)
    dateTaken = serializers.DateTimeField(required=True)
    reasonNotFiled = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = Chart
        fields = ["patient", "vitals", "behaviors", "reasonNotFiled", "behaviorsDescription", "dateTaken"]

    def validate(self, data):
        patient = data.get("patient")
        date_taken = localtime(data.get("dateTaken")).date() 

        if Chart.objects.filter(
            Q(patient=patient) & 
            Q(dateTaken__date=date_taken)
        ).exists():
            raise serializers.ValidationError(
                "A chart entry for this resident already exists on this date."
            )
        return data



class ChartUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating Chart entries, all fields are optional."""
    behaviors = serializers.JSONField(validators=[NonEmptyListValidator()], required=False)
    behaviorsDescription = serializers.JSONField(validators=[NonEmptyListValidator()], required=False)
    vitals = serializers.JSONField(validators=[NonEmptyListValidator()], required=False)
    status = serializers.ChoiceField(required=False, choices=['pending', 'declined', 'approved'])
    reasonNotFiled = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = Chart
        fields = ["status", "behaviors", "vitals", "behaviorsDescription", "reasonNotFiled"]



