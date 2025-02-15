from core.utils.non_empty_validator import *
from custom_admin.models.appointment import Appointment
from custom_admin.models.chart import Chart
from custom_admin.models.patient import Patient
from rest_framework import serializers # type: ignore

class AppointmentSerializer(serializers.ModelSerializer):
    """Serializer for creating appointments entries."""
    
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), required=True)
    weeklyAppointments = serializers.JSONField(validators=[NonEmptyListValidator()], required=True)
    fortnightAppointments = serializers.JSONField(validators=[NonEmptyListValidator()], required=True)
    monthlyAppointments = serializers.JSONField(validators=[NonEmptyListValidator()], required=True)
    attendedTo = serializers.ListField(validators=[MedicationTimeValidator], required=True)

    class Meta:
        model = Chart
        fields = ["patient", "weeklyAppointments", "fortnightAppointments", "monthlyAppointments", "attendedTo"]

    def validate(self, data):
        patient = data.get("patient")

        if Appointment.objects.filter(patient=patient).exists():
            raise serializers.ValidationError(
                "An appointment entry for this resident already exists on this date."
            )
        return data



class AppointmentUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating Appointment entries, all fields are optional."""
    weeklyAppointments = serializers.JSONField(validators=[NonEmptyListValidator()], required=False)
    fortnightAppointments = serializers.JSONField(validators=[NonEmptyListValidator()], required=False)
    monthlyAppointments = serializers.JSONField(validators=[NonEmptyListValidator()], required=False)
    attendedTo = serializers.ListField(validators=[MedicationTimeValidator], required=True)

    class Meta:
        model = Chart
        fields = ["weeklyAppointments", "fortnightAppointments", "monthlyAppointments", "attendedTo"]



