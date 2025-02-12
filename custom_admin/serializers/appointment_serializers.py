from core.utils.non_empty_validator import NonEmptyListValidator
from custom_admin.models.appointment import Appointment
from custom_admin.models.chart import Chart
from custom_admin.models.patient import Patient
from rest_framework import serializers # type: ignore

class AppointmentSerializer(serializers.ModelSerializer):
    """Serializer for creating appointments entries."""
    
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), required=True)
    weeeklyAppointments = serializers.JSONField(validators=[NonEmptyListValidator()], required=True)
    fortnightAppoints = serializers.JSONField(validators=[NonEmptyListValidator()], required=True)
    monthlyAppoints = serializers.JSONField(validators=[NonEmptyListValidator()], required=True)

    class Meta:
        model = Chart
        fields = ["patient", "weeeklyAppointments", "fortnightAppoints", "monthlyAppoints"]

    def validate(self, data):
        patient = data.get("patient")

        if Appointment.objects.filter(patient=patient).exists():
            raise serializers.ValidationError(
                "An appointment entry for this resident already exists on this date."
            )
        return data



class AppointmentUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating Appointment entries, all fields are optional."""
    weeeklyAppointments = serializers.JSONField(validators=[NonEmptyListValidator()], required=False)
    fortnightAppoints = serializers.JSONField(validators=[NonEmptyListValidator()], required=False)
    monthlyAppoints = serializers.JSONField(validators=[NonEmptyListValidator()], required=False)

    class Meta:
        model = Chart
        fields = ["weeeklyAppointments", "fortnightAppoints", "monthlyAppoints",]



